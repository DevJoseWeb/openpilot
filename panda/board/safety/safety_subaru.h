void subaru_rx_hook(CAN_FIFOMailBox_TypeDef *to_push) {}

// FIXME
// *** all output safety mode ***

static void subaru_init(int16_t param) {
  #ifdef PANDA
    lline_relay_init();
  #endif
}

static void subaru_rx_hook(CAN_FIFOMailBox_TypeDef *to_push) {
  int bus_number = (to_push->RDTR >> 4) & 0xFF;
  uint32_t addr = to_push->RIR >> 21;

  if ((addr == 0x119) && (bus_number == 0)){
    int torque_driver_new = ((to_push->RDLR >> 16) & 0x7FF);
    torque_driver_new = to_signed(torque_driver_new, 11);
    // update array of samples
    update_sample(&subaru_torque_driver, torque_driver_new);
  }

  // enter controls on rising edge of ACC, exit controls on ACC off
  if ((addr == 0x240) && (bus_number == 0)) {
    int cruise_engaged = (to_push->RDHR >> 9) & 1;
    if (cruise_engaged && !subaru_cruise_engaged_last) {
      controls_allowed = 1;
    } else if (!cruise_engaged) {
      controls_allowed = 0;
    }
    subaru_cruise_engaged_last = cruise_engaged;
  }
}

static int subaru_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {
  return true;
}

static int subaru_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  
  // shifts bits 29 > 11
  int32_t addr = to_fwd->RIR >> 21;

  // forward CAN 0 > 1
  if (bus_num == 0) {

  // forward CAN 1 > 0, except ES_LKAS
  else if (bus_num == 1) {
    // outback 2015
    if (addr == 0x164) {
      return -1;
    }
    // global platform
    if (addr == 0x122) {
      return -1;
    }
    // ES Distance
    if (addr == 545) {
      return -1;
    }
    // ES LKAS
    if (addr == 802) {
      return -1;
    }

    return 0; // Main CAN
  }

  // fallback to do not forward
  return -1;
}

const safety_hooks subaru_hooks = {
  .init = subaru_init,
  .rx = subaru_rx_hook,
  .tx = subaru_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .ignition = default_ign_hook,
  .fwd = subaru_fwd_hook,
  .relay = alloutput_relay_hook,
};

