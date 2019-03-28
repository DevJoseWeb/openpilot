const int HYUNDAI_MAX_STEER = 255;             // like stock
const int HYUNDAI_MAX_RT_DELTA = 112;          // max delta torque allowed for real time checks
const int32_t HYUNDAI_RT_INTERVAL = 250000;    // 250ms between real time checks
const int HYUNDAI_MAX_RATE_UP = 6;
const int HYUNDAI_MAX_RATE_DOWN = 8;
const int HYUNDAI_DRIVER_TORQUE_ALLOWANCE = 50;
const int HYUNDAI_DRIVER_TORQUE_FACTOR = 2;

int hyundai_camera_detected = 0;
int hyundai_camera_bus = 0;
int hyundai_rt_torque_last = 0;
int hyundai_desired_torque_last = 0;
int hyundai_cruise_engaged_last = 0;
uint32_t hyundai_ts_last = 0;
struct sample_t hyundai_torque_driver;         // last few driver torques measured

static void hyundai_rx_hook(CAN_FIFOMailBox_TypeDef *to_push) {
  int bus = (to_push->RDTR >> 4) & 0xFF;
  uint32_t addr;
  if (to_push->RIR & 4) {
    // Extended
    // Not looked at, but have to be separated
    // to avoid address collision
    addr = to_push->RIR >> 3;
  } else {
    // Normal
    addr = to_push->RIR >> 21;
  }

  // check if stock camera ECU is still online
  if (bus == 0 && addr == 832) {
    hyundai_camera_detected = 1;
    controls_allowed = 0;
  }

}

static int hyundai_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {

  // There can be only one! (camera)
  if (hyundai_camera_detected) {
    return 0;
  }

  uint32_t addr;
  if (to_send->RIR & 4) {
    // Extended
    addr = to_send->RIR >> 3;
  } else {
    // Normal
    addr = to_send->RIR >> 21;
  }

  return true;
}

static int hyundai_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  int addr = to_fwd->RIR>>21;

  // Car CAN -- Send everything to LKAS
  if (bus_num == 0) {
    return (uint8_t)(1);
  }

  // LKAS CAN -- Send everything to Car 
  if (bus_num == 1) {
    if (addr == 832) return -1;  // Except LKAS11
    return (uint8_t)(0);
  }

  // MDPS CAN -- Send everything to Car
  if (bus_num == 2) {
    return (uint8_t)(0);
  }

  return -1;
}
static int hyundai_fwd_hook2(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) { 
  int addr = to_fwd->RIR>>21;

  // Car CAN -- Send everything to MDPS
  if (bus_num == 0) {
    if (addr == 790) return -1;  // Except EMS11
    if (addr == 912) return -1;  // Except SPAS11
    if (addr == 1268) return -1; // Except SPAS12
    return (uint8_t)(2);
  }

  // LKAS CAN -- Send everything to MDPS
  if (bus_num == 1) {
    if (addr == 832) return -1;  // Except LKAS11
    return (uint8_t)(2);
  }

  // MDPS CAN -- Send everything to LKAS
  if (bus_num == 2) {
    if (addr == 593) return -1;  // Except MDPS11
    return (uint8_t)(1);
  }

  return -1;
}


static void hyundai_init(int16_t param) {
  controls_allowed = 0;
}

const safety_hooks hyundai_hooks = {
  .init = hyundai_init,
  .rx = hyundai_rx_hook,
  .tx = hyundai_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .ignition = default_ign_hook,
  .fwd = hyundai_fwd_hook,
  .fwd2 = hyundai_fwd_hook2,
};
 