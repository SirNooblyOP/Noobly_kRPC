# STARSHIP ORBITAL FLIGHT SCRIPT
# Version: 1.25
# Date: 27/05/2024
# Creator: Noobly

import math
import time
import krpc
import Starship_Library

conn = krpc.connect("Starship Launch Program v1")
vessel = conn.space_center.active_vessel

#Launch Parameters:
turn_start_altitude = 1500
turn_end_altitude = 47000
target_altitude = 85000
target_roll = 90 # 90º respect to heading for the flaps
target_heading = 90

# Program Start
print("Program Start")
vessel.control.sas = False
vessel.control.rcs = False
# Telemetry Streams
ut = conn.add_stream(getattr, conn.space_center, "ut")
altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
booster_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=True)
booster_fuel = conn.add_stream(booster_resources.amount, "LiquidFuel")
# Launch!
time.sleep(10)
for countDown in range(10,3,-1):
    print(countDown)
    time.sleep(1)
Starship_Library.ENGINES_IGNITION()
time.sleep(0.5)
print("LAUNCH!")
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(88, target_heading)
time.sleep(15)
print("Commencing Roll Program")
vessel.auto_pilot.target_roll = target_roll
time.sleep(5)
# Main ascent loop
booster_separated = False
turn_angle = 0
print("Commencing Pitch Program")
while True:
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = ((altitude() - turn_start_altitude) /
                (turn_end_altitude - turn_start_altitude))
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > .5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(88 - turn_angle, target_heading)
    if not booster_separated:
        if booster_fuel() < 5000:
            Starship_Library.OUTER_ENGINES_2_SHUTDOWN()
            time.sleep(0.5)
            Starship_Library.OUTER_ENGINES_1_SHUTDOWN()
            time.sleep(0.75)
            Starship_Library.GIMBAL_ENGINES_SHUTDOWN()
            print("Booster Engines Shutdown")
            vessel.control.throttle = 0.25
            print("Starship Sea Level Engines Ignition")
            Starship_Library.SL_ENGINES_IGNITION()
            vessel.control.throttle =0.5
            time.sleep(2)
            print("Stage Separation")
            vessel.control.activate_next_stage()
            time.sleep(2)
            vessel.control.throttle = 0.75
            print("Starship VAC ignition")
            Starship_Library.VAC_ENGINES_IGNITION()
            vessel.control.throttle = 1
            print("Good light on all engines")
            booster_separated = True
    if apoapsis() >= target_altitude * 0.98:
        print("Approaching Target Apoapsis")
        vessel.control.throttle = 0.5
        vessel.control.throttle = 0
        print("Engines Shutdown")
        Starship_Library.SL_ENGINES_SHUTDOWN()
        time.sleep(0.5)
        # Plan circularization burn using vis-viva equation
        print("Planning Orbital Insertion Burn")
        mu = vessel.orbit.body.gravitational_parameter
        r = vessel.orbit.apoapsis
        a1 = vessel.orbit.semi_major_axis
        a2 = r
        v1 = math.sqrt(mu * ((2. / r) - (1. / a1)))
        v2 = math.sqrt(mu * ((2. / r) - (1. / a2)))
        delta_v = v2 - v1
        node = vessel.control.add_node(
            ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)
        # Calculate burn time (rocket equation)
        F = vessel.available_thrust
        Isp = vessel.specific_impulse * 9.82
        m0 = vessel.mass
        m1 = m0 / math.exp(delta_v / Isp)
        flow_rate = F / Isp
        burn_time = (m0 - m1) / flow_rate
        while altitude() < 70000:
            pass
        #Ship reorientation
        print("Ship Reorientation")
        # Check if autopilot is engaged
        if vessel.auto_pilot.engage:
            print("Autopilot is engaged")
        else:
            print("Autopilot is not engaged")
        vessel.auto_pilot.reference_frame = node.reference_frame
        vessel.auto_pilot.target_direction = (0, 1, 0)
        vessel.auto_pilot.wait()
        time.sleep(1)
        # Wait until orbital insertion burn
        print("Time Warping")
        burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time / 2)
        lead_time = 10
        conn.space_center.warp_to(burn_ut - lead_time)
        print("Warp Complete")
        # Orbital insertion burn
        print("VAC Engines Chill")
        time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, "time_to_apoapsis")
        while time_to_apoapsis() - (burn_time/2) > 0:
            pass
        print("Orbital Insertion Burn")
        vessel.control.throttle = 1
        while node.remaining_delta_v > 150:
            pass
        print("VAC Engines Throttle Down to 25%")
        vessel.control.throttle = 0.25
        while node.remaining_delta_v > 2:
            pass
        vessel.control.throttle = 0
        print("VAC Engines Shutdown")
        Starship_Library.VAC_ENGINES_SHUTDOWN()
        node.remove()
        vessel.auto_pilot.reference_frame = vessel.surface_reference_frame
        vessel.auto_pilot.target_pitch_and_heading(0, 90)
        vessel.auto_pilot.target_roll = 0
        vessel.auto_pilot.wait()
        time.sleep(25)
        vessel.control.sas = True
        print("Nominal Orbit Insertion!")
        break