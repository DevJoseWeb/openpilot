#!/usr/bin/env python
from cereal import car
from common.realtime import sec_since_boot
from selfdrive.config import Conversions as CV
from selfdrive.controls.lib.drive_helpers import EventTypes as ET, create_event
from selfdrive.controls.lib.vehicle_model import VehicleModel
from selfdrive.car.hyundai.carstate import CarState, get_can_parser, get_camera_parser
from selfdrive.car.hyundai.values import CAMERA_MSGS, CAR, get_hud_alerts, FEATURES

try:
  from selfdrive.car.hyundai.carcontroller import CarController
except ImportError:
  CarController = None


class CarInterface(object):
  def __init__(self, CP, sendcan=None):
    self.CP = CP
    self.VM = VehicleModel(CP)
    self.idx = 0
    self.lanes = 0
    self.lkas_request = 0

    self.gas_pressed_prev = False
    self.brake_pressed_prev = False
    self.can_invalid_count = 0
    self.cruise_enabled_prev = False
    self.low_speed_alert = False

    # *** init the major players ***
    self.CS = CarState(CP)
    self.cp = get_can_parser(CP)
    self.cp_cam, self.cp_cam2 = get_camera_parser(CP)

    # sending if read only is False
    if sendcan is not None:
      self.sendcan = sendcan
      self.CC = CarController(self.cp.dbc_name, CP.carFingerprint, CP.enableCamera)

  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 3.0

  @staticmethod
  def calc_accel_override(a_ego, a_target, v_ego, v_target):
    return 1.0

  @staticmethod
  def get_params(candidate, fingerprint):

    # kg of standard extra cargo to count for drive, gas, etc...
    std_cargo = 200 # Comma use 136kg  ..  Fuel = 60kg, Driver = 80kg (assuming 70kg and not naked), Cargo = 20kg .. This is the minimum.. assume 50% of the time there is a passenger also 70kg and not naked, so 40kg.
    weight_dist_rear = 0.45

    ret = car.CarParams.new_message()

    ret.carName = "hyundai"
    ret.carFingerprint = candidate
    ret.radarOffCan = True
    ret.safetyModel = car.CarParams.SafetyModels.hyundai
    ret.enableCruise = True  # stock acc

    # FIXME: hardcoding honda civic 2016 touring params so they can be used to
    # scale unknown params for other cars
    mass_civic = 2923 * CV.LB_TO_KG + std_cargo
    wheelbase_civic = 2.70
    centerToFront_civic = wheelbase_civic * weight_dist_rear
    centerToRear_civic = wheelbase_civic - centerToFront_civic
    rotationalInertia_civic = 2500
    tireStiffnessFront_civic = 192150
    tireStiffnessRear_civic = 202500

    ret.steerActuatorDelay = 0.10
    ret.steerKf = 0.00006
    ret.steerRateCost = 0.50
    tire_stiffness_factor = 0.60
    ret.steerKiBP, ret.steerKpBP = [[0.], [0.]]
    ret.steerKpV, ret.steerKiV = [[0.12], [0.06]]
    ret.minSteerSpeed = 0.

    if candidate == CAR.ELANTRA:
      ret.mass = 1275
      ret.wheelbase = 2.7
      ret.steerRatio = 13.447
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.GENESIS:
      ret.mass = 2060
      ret.wheelbase = 3.01
      ret.steerRatio = 12.069
    elif candidate == CAR.KIA_OPTIMA:
      ret.mass = 3558 * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
    elif candidate == CAR.KIA_SORENTO:
      ret.mass = 1985
      ret.wheelbase = 2.78
      ret.steerRatio = 13.76
    elif candidate == CAR.KIA_STINGER:  #AWD
      ret.mass = 1814
      ret.wheelbase = 2.906
      ret.steerRatio = 11.451
    elif candidate == CAR.SANTA_FE:  #AWD
      ret.mass = 3982 * CV.LB_TO_KG
      ret.wheelbase = 2.766
      ret.steerRatio = 13.321
    elif candidate == CAR.UNKNOWN:
      ret.mass = 1800
      ret.wheelbase = 2.8
      ret.steerRatio = 13.0

    ret.mass += std_cargo
    ret.minEnableSpeed = -1.   # enable is done by stock ACC, so ignore this
    ret.longitudinalKpBP = [0.]
    ret.longitudinalKpV = [0.]
    ret.longitudinalKiBP = [0.]
    ret.longitudinalKiV = [0.]

    ret.centerToFront = ret.wheelbase * weight_dist_rear

    centerToRear = ret.wheelbase - ret.centerToFront

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = rotationalInertia_civic * \
                            ret.mass * ret.wheelbase**2 / (mass_civic * wheelbase_civic**2)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront = (tireStiffnessFront_civic * tire_stiffness_factor) * \
                             ret.mass / mass_civic * \
                             (centerToRear / ret.wheelbase) / (centerToRear_civic / wheelbase_civic)
    ret.tireStiffnessRear = (tireStiffnessRear_civic * tire_stiffness_factor) * \
                            ret.mass / mass_civic * \
                            (ret.centerToFront / ret.wheelbase) / (centerToFront_civic / wheelbase_civic)


    # no rear steering, at least on the listed cars above
    ret.steerRatioRear = 0.
    ret.steerControlType = car.CarParams.SteerControlType.torque

    # steer, gas, brake limitations VS speed
    ret.steerMaxBP = [0.]
    ret.steerMaxV = [1.0]
    ret.gasMaxBP = [0.]
    ret.gasMaxV = [1.]
    ret.brakeMaxBP = [0.]
    ret.brakeMaxV = [1.]
    ret.longPidDeadzoneBP = [0.]
    ret.longPidDeadzoneV = [0.]

    ret.enableCamera = not any(x for x in CAMERA_MSGS if x in fingerprint)
    ret.openpilotLongitudinalControl = True

    ret.steerLimitAlert = True
    ret.stoppingControl = False
    ret.startAccel = 0.0

    return ret

  # returns a car.CarState
  def update(self, c):
    # ******************* do can recv *******************
    canMonoTimes = []
    self.cp.update(int(sec_since_boot() * 1e9), False)
    self.cp_cam.update(int(sec_since_boot() * 1e9), False)
    self.cp_cam2.update(int(sec_since_boot() * 1e9), False)
    self.CS.update(self.cp, self.cp_cam, self.cp_cam2)
    # create message
    ret = car.CarState.new_message()
    # speeds
    ret.vEgo = self.CS.v_ego
    ret.vEgoRaw = self.CS.v_ego_raw
    ret.aEgo = self.CS.a_ego
    ret.yawRate = self.CS.yaw_rate
    ret.standstill = self.CS.standstill
    ret.wheelSpeeds.fl = self.CS.v_wheel_fl
    ret.wheelSpeeds.fr = self.CS.v_wheel_fr
    ret.wheelSpeeds.rl = self.CS.v_wheel_rl
    ret.wheelSpeeds.rr = self.CS.v_wheel_rr

    # gear shifter
    ret.gearShifter = self.CS.gear_shifter_cluster

    # gas pedal
    ret.gas = self.CS.car_gas
    ret.gasPressed = self.CS.pedal_gas > 1e-3   # tolerance to avoid false press reading

    # brake pedal
    ret.brake = self.CS.user_brake
    ret.brakePressed = self.CS.brake_pressed != 0
    ret.brakeLights = self.CS.brake_lights

    # steering wheel
    ret.steeringAngle = self.CS.angle_steers
    ret.steeringRate = self.CS.angle_steers_rate  # it's unsigned

    ret.steeringTorque = self.CS.steer_torque_driver
    ret.steeringPressed = self.CS.steer_override

    # cruise state
    ret.cruiseState.enabled = self.CS.pcm_acc_status != 0
    if self.CS.pcm_acc_status != 0:
      ret.cruiseState.speed = self.CS.cruise_set_speed
    else:
      ret.cruiseState.speed = 0
    ret.cruiseState.available = bool(self.CS.main_on)
    ret.cruiseState.standstill = False

    # TODO: button presses
    buttonEvents = []

    if self.CS.left_blinker_on != self.CS.prev_left_blinker_on:
      be = car.CarState.ButtonEvent.new_message()
      be.type = 'leftBlinker'
      be.pressed = self.CS.left_blinker_on != 0
      buttonEvents.append(be)

    if self.CS.right_blinker_on != self.CS.prev_right_blinker_on:
      be = car.CarState.ButtonEvent.new_message()
      be.type = 'rightBlinker'
      be.pressed = self.CS.right_blinker_on != 0
      buttonEvents.append(be)

    ret.buttonEvents = buttonEvents
    ret.leftBlinker = bool(self.CS.left_blinker_on)
    ret.rightBlinker = bool(self.CS.right_blinker_on)

    ret.doorOpen = not self.CS.door_all_closed
    ret.seatbeltUnlatched = not self.CS.seatbelt


    # low speed steer alert hysteresis logic (only for cars with steer cut off above 10 m/s)
    if ret.vEgo < (self.CP.minSteerSpeed + 2.) and self.CP.minSteerSpeed > 10.:
      self.low_speed_alert = True
    if ret.vEgo > (self.CP.minSteerSpeed + 4.):
      self.low_speed_alert = False

    # events
    events = []
    if not self.CS.can_valid:
      self.can_invalid_count += 1
      if self.can_invalid_count >= 5:
        events.append(create_event('commIssue', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))
    else:
      self.can_invalid_count = 0
    # Try all 3 gear selector locations, as some cars miss one or 2 of them inconsistently
    if (self.CS.gear_shifter != 'drive') and (self.CS.gear_tcu != 'drive') and (self.CS.gear_shifter_cluster != 'drive'):
      events.append(create_event('wrongGear', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if ret.doorOpen:
      events.append(create_event('doorOpen', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if ret.seatbeltUnlatched:
      events.append(create_event('seatbeltNotLatched', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if self.CS.esp_disabled:
      events.append(create_event('espDisabled', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if not self.CS.main_on:
      events.append(create_event('wrongCarMode', [ET.NO_ENTRY, ET.USER_DISABLE]))
    if ret.gearShifter == 'reverse':
      events.append(create_event('reverseGear', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))
    if self.CS.steer_error:
      events.append(create_event('steerTempUnavailable', [ET.NO_ENTRY, ET.WARNING]))

    if ret.cruiseState.enabled and not self.cruise_enabled_prev:
      events.append(create_event('pcmEnable', [ET.ENABLE]))
    elif not ret.cruiseState.enabled:
      events.append(create_event('pcmDisable', [ET.USER_DISABLE]))

    # disable on pedals rising edge or when brake is pressed and speed isn't zero
    if (ret.brakePressed and (not self.brake_pressed_prev or ret.vEgoRaw > 0.1)):
      events.append(create_event('pedalPressed', [ET.NO_ENTRY, ET.USER_DISABLE]))

    if ret.gasPressed:
      events.append(create_event('pedalPressed', [ET.PRE_ENABLE]))

    if self.low_speed_alert:
      events.append(create_event('belowSteerSpeed', [ET.WARNING]))

    ret.events = events
    ret.canMonoTimes = canMonoTimes

    self.gas_pressed_prev = ret.gasPressed
    self.brake_pressed_prev = ret.brakePressed
    self.cruise_enabled_prev = ret.cruiseState.enabled

    return ret.as_reader()

  def apply(self, c):

    hud_alert = get_hud_alerts(c.hudControl.visualAlert, c.hudControl.audibleAlert)

    self.CC.update(self.sendcan, c.enabled, self.CS, c.actuators,
                   c.cruiseControl.cancel, hud_alert)

    return False
