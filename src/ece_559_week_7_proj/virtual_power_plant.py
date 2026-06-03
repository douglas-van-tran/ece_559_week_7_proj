import numpy as np


class VirtualPowerPlant:
    def __init__(
        self,
        p_load: int = 10,
        p_ev: int = 2,
        p_pv: int = 5,
        p_bess: int = -5,
        p_ev_charge_capacity: float = 1.0,
        voltage_ll: float = 13.2,
        feeder_len: int = 5,
        num_feeders: int = 2,
    ):
        self.p_load = p_load
        self.p_ev = p_ev
        self.p_pv = p_pv
        self.p_bess = p_bess
        self.p_ev_charge_capacity = p_ev_charge_capacity
        self.voltage_ll = voltage_ll
        self.feeder_len = feeder_len
        self.num_feeders = num_feeders

    def calculate_p_feed(self) -> tuple[float, ...]:

        # Calculate feed and substation power without vpp
        p_ev = self.p_ev / self.num_feeders
        p_feed_no_vpp = self.p_load + p_ev - self.p_pv
        p_sub_no_vpp = p_feed_no_vpp * self.num_feeders

        # Adjust p_ev by available controllable capacity
        vpp_p_ev = self.p_ev_charge_capacity * p_ev
        vpp_p_bess = self.p_bess / self.num_feeders

        # Calculate feed and substation power with vpp
        p_feed_vpp = self.p_load + vpp_p_ev - self.p_pv + vpp_p_bess

        p_sub_vpp = p_feed_vpp * self.num_feeders

        return p_feed_no_vpp, p_sub_no_vpp, p_feed_vpp, p_sub_vpp

    def calculate_peak_reduction(self, p_sub_no_vpp, p_sub_vpp, is_battery_charging: bool = False):
        if is_battery_charging:
            return 0
        else:
            return 100 * (p_sub_no_vpp - p_sub_vpp) / p_sub_no_vpp

    def calcuate_i_v(self, power, r: float = 0.03):
        # Convert power to W
        power *= 10**6
        voltage_ll = self.voltage_ll * 10**3

        # Calculate i
        i = power / (np.sqrt(3) * voltage_ll)

        # Calculate resistance
        r_total = r * (self.feeder_len / 2)

        # Calculate voltage
        v = np.sqrt(3) * r_total * i

        # Calculate voltage drop
        v_drop = v / voltage_ll

        return i, v_drop
