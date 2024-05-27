# STARSHIP LIBRARY
# Version: 1.0
# Date: 19/05/2024
# Creator: Noobly

import time
import krpc


#BOOSTER ENGINES STATIC FIRE SCRIPT
conn = krpc.connect("Booster Static Fire v1")
vessel = conn.space_center.active_vessel

def CENTER_ENGINE_IGNITION():
    vessel.parts.with_tag("E1")[0].engine.active = True
    vessel.parts.with_tag("E1")[0].engine.gimbal_locked = False

def GIMBAL_ENGINES_IGNITION():
    vessel.parts.with_tag("E2")[0].engine.active = True
    vessel.parts.with_tag("E2")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E3")[0].engine.active = True
    vessel.parts.with_tag("E3")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E4")[0].engine.active = True
    vessel.parts.with_tag("E4")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E5")[0].engine.active = True
    vessel.parts.with_tag("E5")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E6")[0].engine.active = True
    vessel.parts.with_tag("E6")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E7")[0].engine.active = True
    vessel.parts.with_tag("E7")[0].engine.gimbal_locked = False

def OUTER_ENGINES_1_IGNITION():
    vessel.parts.with_tag("E8")[0].engine.active = True
    vessel.parts.with_tag("E8")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E10")[0].engine.active = True
    vessel.parts.with_tag("E10")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E12")[0].engine.active = True
    vessel.parts.with_tag("E12")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E14")[0].engine.active = True
    vessel.parts.with_tag("E14")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E16")[0].engine.active = True
    vessel.parts.with_tag("E16")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E18")[0].engine.active = True
    vessel.parts.with_tag("E18")[0].engine.gimbal_locked = False

def OUTER_ENGINES_2_IGNITION():
    vessel.parts.with_tag("E9")[0].engine.active = True
    vessel.parts.with_tag("E9")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E11")[0].engine.active = True
    vessel.parts.with_tag("E11")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E13")[0].engine.active = True
    vessel.parts.with_tag("E13")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E15")[0].engine.active = True
    vessel.parts.with_tag("E15")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E17")[0].engine.active = True
    vessel.parts.with_tag("E17")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("E19")[0].engine.active = True
    vessel.parts.with_tag("E19")[0].engine.gimbal_locked = False

def ENGINES_IGNITION():
    print("Engines Chill")
    vessel.control.throttle = 0
    time.sleep(0.5)
    CENTER_ENGINE_IGNITION()
    vessel.control.throttle = 0.1
    time.sleep(0.5)
    print("3")
    GIMBAL_ENGINES_IGNITION()
    vessel.control.throttle = 0.2
    time.sleep(0.5)
    OUTER_ENGINES_1_IGNITION()
    vessel.control.throttle = 0.3
    time.sleep(0.5)
    print("2")
    OUTER_ENGINES_2_IGNITION()
    vessel.control.throttle = 0.4
    print("Engines Throttle Up")
    vessel.control.throttle = 0.5
    time.sleep(1)
    print("1")
    vessel.control.throttle = 1
    print("Engines Throttle at Max.")
#--------------------------------------------------------------------------------
def CENTER_ENGINE_SHUTDOWN():
    vessel.parts.with_tag("E1")[0].engine.active = False
    vessel.parts.with_tag("E1")[0].engine.gimbal_locked = True

def GIMBAL_ENGINES_SHUTDOWN():
    vessel.parts.with_tag("E2")[0].engine.active = False
    vessel.parts.with_tag("E2")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E3")[0].engine.active = False
    vessel.parts.with_tag("E3")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E4")[0].engine.active = False
    vessel.parts.with_tag("E4")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E5")[0].engine.active = False
    vessel.parts.with_tag("E5")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E6")[0].engine.active = False
    vessel.parts.with_tag("E6")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E7")[0].engine.active = False
    vessel.parts.with_tag("E7")[0].engine.gimbal_locked = True

def OUTER_ENGINES_1_SHUTDOWN():
    vessel.parts.with_tag("E8")[0].engine.active = False
    vessel.parts.with_tag("E8")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E10")[0].engine.active = False
    vessel.parts.with_tag("E10")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E12")[0].engine.active = False
    vessel.parts.with_tag("E12")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E14")[0].engine.active = False
    vessel.parts.with_tag("E14")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E16")[0].engine.active = False
    vessel.parts.with_tag("E16")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E18")[0].engine.active = False
    vessel.parts.with_tag("E18")[0].engine.gimbal_locked = True

def OUTER_ENGINES_2_SHUTDOWN():
    vessel.parts.with_tag("E9")[0].engine.active = False
    vessel.parts.with_tag("E9")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E11")[0].engine.active = False
    vessel.parts.with_tag("E11")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E13")[0].engine.active = False
    vessel.parts.with_tag("E13")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E15")[0].engine.active = False
    vessel.parts.with_tag("E15")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E17")[0].engine.active = False
    vessel.parts.with_tag("E17")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("E19")[0].engine.active = False
    vessel.parts.with_tag("E19")[0].engine.gimbal_locked = True

def ENGINES_SHUTDOWN():
    print("Beginning Engines Shutdown")
    vessel.control.throttle = 0.75
    time.sleep(0.5)
    OUTER_ENGINES_2_SHUTDOWN()
    time.sleep(0.5)
    OUTER_ENGINES_1_SHUTDOWN()
    time.sleep(0.5)
    GIMBAL_ENGINES_SHUTDOWN()
    time.sleep(0.5)
    CENTER_ENGINE_SHUTDOWN()
    vessel.control.throttle = 0
    print("Engines Shutdown")

#--------------------------------------------------------------------------------

def SL_ENGINES_IGNITION():
    vessel.parts.with_tag("SL1")[0].engine.active = True
    vessel.parts.with_tag("SL1")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("SL2")[0].engine.active = True
    vessel.parts.with_tag("SL2")[0].engine.gimbal_locked = False
    vessel.parts.with_tag("SL3")[0].engine.active = True
    vessel.parts.with_tag("SL3")[0].engine.gimbal_locked = False


def SL_ENGINES_SHUTDOWN():
    vessel.parts.with_tag("SL1")[0].engine.active = False
    vessel.parts.with_tag("SL1")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("SL2")[0].engine.active = False
    vessel.parts.with_tag("SL2")[0].engine.gimbal_locked = True
    vessel.parts.with_tag("SL3")[0].engine.active = False
    vessel.parts.with_tag("SL3")[0].engine.gimbal_locked = True

def VAC_ENGINES_IGNITION():
    vessel.parts.with_tag("VAC1")[0].engine.active = True
    vessel.parts.with_tag("VAC2")[0].engine.active = True
    vessel.parts.with_tag("VAC3")[0].engine.active = True

def VAC_ENGINES_SHUTDOWN():
    vessel.parts.with_tag("VAC1")[0].engine.active = False
    vessel.parts.with_tag("VAC2")[0].engine.active = False
    vessel.parts.with_tag("VAC3")[0].engine.active = False

#--------------------------------------------------------------------------------