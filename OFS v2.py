# STARSHIP ORBITAL FLIGHT SCRIPT
# Version: 2.0
# Date: 02/06/2024
# Creator: Noobly

import math
import time
import krpc
import Starship_Library

conn = krpc.connect("Starship Launch Program v1")
# Getting Starship Connected
vessels = conn.space_center.vessels
target1 = "Starship"
target_vessel = None

for vessel in vessels:
    if vessel.name == target1:
        target_vessel = vessel
        break

if target_vessel is None:
    print(f'Vessel f"{target1}" not found')
else:
    print(f'Controlling vessel: {target1}')

starship = target_vessel

#Launch Parameters:
turn_start_altitude = 1500
turn_end_altitude = 47000
target_altitude = 85000
target_roll = 90 # 90º respect to heading for the flaps
target_heading = 90

# Program Start
print("Program Start")
starship.control.sas = False
starship.control.rcs = False
# Telemetry Streams
ut = conn.add_stream(getattr, conn.space_center, "ut")
altitude = conn.add_stream(getattr, starship.flight(), "mean_altitude")
apoapsis = conn.add_stream(getattr, starship.orbit, "apoapsis_altitude")
booster_resources = starship.resources_in_decouple_stage(stage=1, cumulative=True)
booster_fuel = conn.add_stream(booster_resources.amount, "LiquidFuel")
# Launch!
time.sleep(10)
for countDown in range(10,3,-1):
    print(countDown)
    time.sleep(1)
Starship_Library.ENGINES_IGNITION()
time.sleep(0.5)
print("LAUNCH!")
Starship_Library.LAUNCH_CLAMPS()
starship.auto_pilot.engage()
starship.auto_pilot.target_pitch_and_heading(88, target_heading)
time.sleep(15)
print("Commencing Roll Program")
starship.auto_pilot.target_roll = target_roll
time.sleep(5)
# Main ascent loop
booster_separated = False
turn_angle = 0
print("Commencing Pitch Program")
while True:
    while starship.flight().dynamic_pressure > 20000:
        starship.control.throttle = 0.85
    else:
        starship.control.throttle = 1
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = ((altitude() - turn_start_altitude) /
                (turn_end_altitude - turn_start_altitude))
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > .5:
            turn_angle = new_turn_angle
            starship.auto_pilot.target_pitch_and_heading(88 - turn_angle, target_heading)
    if not booster_separated:
        if booster_fuel() < 5000:
            Starship_Library.OUTER_ENGINES_2_SHUTDOWN()
            time.sleep(0.5)
            Starship_Library.OUTER_ENGINES_1_SHUTDOWN()
            time.sleep(0.75)
            Starship_Library.GIMBAL_ENGINES_SHUTDOWN()
            print("Booster Engines Shutdown")
            starship.control.throttle = 0.25
            starship.control.toggle_action_group(0)
            starship.control.rcs = True
            print("Starship Sea Level Engines Ignition")
            Starship_Library.SL_ENGINES_IGNITION()
            starship.control.throttle =0.5
            time.sleep(2)
            print("Stage Separation")
            starship.parts.with_tag("BD1")[0].decoupler.decouple()
            time.sleep(2)
            starship.control.throttle = 0.75
            print("Starship VAC ignition")
            Starship_Library.VAC_ENGINES_IGNITION()
            starship.control.throttle = 1
            print("Good light on all engines")
            booster_separated = True
    if apoapsis() >= target_altitude * 0.98:
        print("Approaching Target Apoapsis")
        starship.control.throttle = 0.5
        starship.control.throttle = 0
        print("Engines Shutdown")
        Starship_Library.SL_ENGINES_SHUTDOWN()
        time.sleep(0.5)
        # Plan circularization burn using vis-viva equation
        print("Planning Orbital Insertion Burn")
        mu = starship.orbit.body.gravitational_parameter
        r = starship.orbit.apoapsis
        a1 = starship.orbit.semi_major_axis
        a2 = r
        v1 = math.sqrt(mu * ((2. / r) - (1. / a1)))
        v2 = math.sqrt(mu * ((2. / r) - (1. / a2)))
        delta_v = v2 - v1
        node = starship.control.add_node(
            ut() + starship.orbit.time_to_apoapsis, prograde=delta_v)
        # Calculate burn time (rocket equation)
        F = starship.available_thrust
        Isp = starship.specific_impulse * 9.82
        m0 = starship.mass
        m1 = m0 / math.exp(delta_v / Isp)
        flow_rate = F / Isp
        burn_time = (m0 - m1) / flow_rate
        while altitude() < 70000:
            pass
        #Ship reorientation
        print("Ship Reorientation")
        # Check if autopilot is engaged
        if starship.auto_pilot.engage:
            print("Autopilot is engaged")
        else:
            print("Autopilot is not engaged")
        starship.auto_pilot.reference_frame = node.reference_frame
        starship.auto_pilot.target_direction = (0, 1, 0)
        starship.auto_pilot.wait()
        time.sleep(1)
        # Wait until orbital insertion burn
        print("Time Warping")
        burn_ut = ut() + starship.orbit.time_to_apoapsis - (burn_time / 2)
        lead_time = 10
        conn.space_center.warp_to(burn_ut - lead_time)
        print("Warp Complete")
        # Orbital insertion burn
        print("VAC Engines Chill")
        time_to_apoapsis = conn.add_stream(getattr, starship.orbit, "time_to_apoapsis")
        while time_to_apoapsis() - (burn_time/2) > 0:
            pass
        print("Orbital Insertion Burn")
        starship.control.throttle = 1
        while node.remaining_delta_v > 150:
            pass
        print("VAC Engines Throttle Down to 25%")
        starship.control.throttle = 0.25
        while node.remaining_delta_v > 2:
            pass
        starship.control.throttle = 0
        print("VAC Engines Shutdown")
        Starship_Library.VAC_ENGINES_SHUTDOWN()
        node.remove()
        starship.control.sas = True
        starship.control.sas_mode = starship.control.sas_mode.prograde
        time.sleep(10)
        print("Nominal Orbit Insertion!")
        break