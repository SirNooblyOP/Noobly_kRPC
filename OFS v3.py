# ORBITAL FLIGHT SCRIPT
# Version: 3.0
# Creator: Noobly
# Date: 08/06/2024

import krpc
import time
import math

# Launch Parameters:
turn_start_altitude = 1500
turn_end_altitude = 47000
target_altitude = 85000
target_roll = 90 # 90º respect to heading (for flaps)
target_heading = 90

# Getting target_ship Connected:
conn = krpc.connect("OFS v3")
vessels = conn.space_center.vessels
ship = "Starship"
booster = "Booster"
target_ship = None
target_booster = None
booster_separated = False
mode = None

for vessel in vessels:
    if vessel.name == ship:
        target_ship = vessel
        break
if target_ship is None:
    print(f'Vessel "{ship}" not found')
else:
    print(f'Controlling vessel: {ship}')

# Telemetry Streams:
ut = conn.add_stream(getattr, conn.space_center, "ut")
altitude = conn.add_stream(getattr, target_ship.flight(), "mean_altitude")
apoapsis = conn.add_stream(getattr, target_ship.orbit, "apoapsis_altitude")
booster_resources = target_ship.resources_in_decouple_stage(stage=1, cumulative=True)
booster_fuel = conn.add_stream(booster_resources.amount, "LiquidFuel")

# All Booster Engines Ignition:
def booster_all_engine_ignition():
    for i in range(1, 20):
        tag = f"E{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = True
            engine.engine.gimbal_locked = False

# Outer1 Half Booster Engines Shutdown:
def outer1_engine_shutdown():
    for i in [8, 10, 12, 14, 16, 18]:
        tag = f"E{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = False
            engine.engine.gimbal_locked = True

# Outer2 Half Booster Engines Shutdown:
def outer2_engine_shutdown():
    for i in [9, 11, 13, 15, 17, 19]:
        tag = f"E{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = False
            engine.engine.gimbal_locked = True

# Booster Gimbal Engines Shutdown:
def booster_gimbal_shutdown():
    for i in range(2, 8):
        tag = f"E{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = False
            engine.engine.gimbal_locked = True

# Booster Gimbal Engines Shutdown:
def booster_gimbal_ignition():
    for i in range(2, 8):
        tag = f"E{i}"
        engines = target_booster.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = True
            engine.engine.gimbal_locked = False

# Launch Clamps:
def launch_clamps():
    for i in range(1, 10):
        tag = f"LC{i}"
        target_ship.parts.with_tag(tag)[0].launch_clamp.release()

# Vac Engines Ignition:
def vac_engine_ignition():
    for i in range(1, 4):
        tag = f"VAC{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = True

# Vac Engines Shutdown:
def vac_engine_shutdown():
    for i in range(1, 4):
        tag = f"VAC{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = False

# SL Engines Ignition:
def sl_engine_ignition():
    for i in range(1, 4):
        tag = f"SL{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = True
            engine.engine.gimbal_locked = False

# SL Engines Shutdown:
def sl_engine_shutdown():
    for i in range(1, 4):
        tag = f"SL{i}"
        engines = target_ship.parts.with_tag(tag)
        for engine in engines:
            engine.engine.active = False
            engine.engine.gimbal_locked = True

# Lift Off:
def lift_off():
    global mode
    print(f'Actual Mode: {mode}')
    print("Vehicle in Control")
    target_ship.control.sas = False
    target_ship.control.rcs = False
    time.sleep(2)
    for countDown in range(10,2,-1):
        print(countDown)
        time.sleep(1)
    print("Booster Engines Ignition")
    booster_all_engine_ignition()
    target_ship.control.throttle = 1
    target_ship.auto_pilot.engage()
    print("Lift Off!")
    launch_clamps()
    target_ship.auto_pilot.target_pitch_and_heading(89, target_heading)
    while True:
        if altitude() > 200:
            print("Commencing Roll Program")
            target_ship.auto_pilot.target_roll = target_roll
            target_ship.auto_pilot.wait
            mode = 1
            break

# MaxQ:
def max_q():
    if target_ship.flight().dynamic_pressure > 20000:
        target_ship.control.throttle = 0.85
    else:
        target_ship.control.throttle = 1

# MaxG:
max_g = 3.5
def get_g_force():
    return target_ship.flight().g_force
def g_limiter():
    while True:
        actual_g_force = get_g_force()
        g_force_error = max_g - actual_g_force
        if g_force_error > 0:
            target_ship.control.throttle += 0.01
        elif g_force_error < 0:
            target_ship.control.throttle -= 0.01
        target_ship.control.throttle = max(0, min(1, target_ship.control.throttle))


# Main Ascent Loop:
def main_ascent():
    global mode
    print(f'Actual Mode: {mode}')
    turn_angle = 0
    global booster_separated
    print("Pitch Program Start")
    target_ship.auto_pilot.engage()
    while mode == 1:
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > .5:
                turn_angle = new_turn_angle
                target_ship.auto_pilot.target_pitch_and_heading(88 - turn_angle, target_heading)
        if not booster_separated:
            if booster_fuel() < 5000:
                print("Booster Engines Shutdown")
                outer1_engine_shutdown()
                time.sleep(1)
                outer2_engine_shutdown()
                time.sleep(1)
                booster_gimbal_shutdown()
                target_ship.control.throttle = 0.3
                target_ship.control.toggle_action_group(0)
                target_ship.control.rcs = True
                print("Starship Sea Level Engines Ignition")
                sl_engine_ignition()
                time.sleep(2)
                print("Stage Separation")
                target_ship.parts.with_tag("BD1")[0].decoupler.decouple()
                time.sleep(2)
                target_ship.control.throttle = 0.75
                print("Starship Vaccum Engines Ignition")
                vac_engine_ignition()
                target_ship.control.throttle = 1
                print("Good Light On All Engines")
                booster_separated = True
        if altitude() > 47000:
            mode = 2
        else:
            mode = 1

# Orbital Insertion:
def orbital_insertion():
    print(f'Actual Mode: {mode}')
    while mode == 2:
        if apoapsis() >= target_altitude * 0.98:
            print("Approaching Target Apoapsis")
            target_ship.control.throttle = 0.5
            target_ship.control.throttle = 0
            print("Engines Shutdown")
            sl_engine_shutdown()
            time.sleep(0.5)
            # Plan circularization burn using vis-viva equation
            print("Planning Orbital Insertion Burn")
            mu = target_ship.orbit.body.gravitational_parameter
            r = target_ship.orbit.apoapsis
            a1 = target_ship.orbit.semi_major_axis
            a2 = r
            v1 = math.sqrt(mu * ((2. / r) - (1. / a1)))
            v2 = math.sqrt(mu * ((2. / r) - (1. / a2)))
            delta_v = v2 - v1
            node = target_ship.control.add_node(
                ut() + target_ship.orbit.time_to_apoapsis, prograde=delta_v)
            # Calculate burn time (rocket equation)
            F = target_ship.available_thrust
            Isp = target_ship.specific_impulse * 9.82
            m0 = target_ship.mass
            m1 = m0 / math.exp(delta_v / Isp)
            flow_rate = F / Isp
            burn_time = (m0 - m1) / flow_rate
            while altitude() < 70000:
                pass
            #Ship reorientation
            print("Ship Reorientation")
            # Check if autopilot is engaged
            if target_ship.auto_pilot.engage:
                print("Autopilot is engaged")
            else:
                print("Autopilot is not engaged")
            target_ship.auto_pilot.reference_frame = node.reference_frame
            target_ship.auto_pilot.target_direction = (0, 1, 0)
            target_ship.auto_pilot.wait()
            time.sleep(1)
            # Wait until orbital insertion burn
            print("Time Warping")
            burn_ut = ut() + target_ship.orbit.time_to_apoapsis - (burn_time / 2)
            lead_time = 10
            conn.space_center.warp_to(burn_ut - lead_time)
            print("Warp Complete")
            # Orbital insertion burn
            print("VAC Engines Chill")
            time_to_apoapsis = conn.add_stream(getattr, target_ship.orbit, "time_to_apoapsis")
            while time_to_apoapsis() - (burn_time/2) > 0:
                pass
                print("Orbital Insertion Burn")
            target_ship.control.throttle = 1
            while node.remaining_delta_v > 150:
                pass
            print("VAC Engines Throttle Down to 25%")
            target_ship.control.throttle = 0.25
            while node.remaining_delta_v > 2:
                pass
            target_ship.control.throttle = 0
            print("VAC Engines Shutdown")
            vac_engine_shutdown()
            node.remove()
            target_ship.control.sas = True
            target_ship.control.sas_mode = target_ship.control.sas_mode.prograde
            time.sleep(10)
            print("Nominal Orbit Insertion!")


# Booster Connection:
def booster_conn():
    global target_booster
    for vessel in vessels:
        if vessel.name == booster:
            target_booster = vessel
    if target_booster is None:
        print(f'Vessel "{booster}" not found')
    else:
        print(f'Controlling vessel: {booster}')

# Booster Flip and Boost Back:
def booster_boostback():
    global mode
    time.sleep(1)
    target_booster.control.throttle = 1


# Main Loop:
def launch():
    global mode
    global booster_separated
    if mode == None:
        lift_off()
    if mode == 1:
        main_ascent()
    if mode == 2:
        orbital_insertion()

# Launch!
launch()