import matplotlib.pyplot as plt
import numpy as np


class VirtualPowerPlant:
    def __init__(
        self,
        p_load: int = 10,
        p_ev: int = 2,
        p_pv: int = 5,
        p_bess: int = 5,
        p_ev_charge_capacity: float = 1.0,
        primary_voltage: float = 13.2,
        feeder_len: int = 5,
        num_feeders: int = 2,
    ):
        self.p_load = p_load
        self.p_ev = p_ev
        self.p_pv = p_pv
        self.p_bess = p_bess
        self.p_ev_charge_capacity = p_ev_charge_capacity
        self.primary_voltage = primary_voltage
        self.feeder_len = feeder_len
        self.num_feeders = num_feeders

    # def _calculate_p_ev(self) -> float:

    #     print(p_ev)

    #     return p_ev

    def calculate_p_feed(
        self,
        is_vpp_dispatch: bool,
        is_winter: bool = False,
    ) -> tuple[float, float]:
        # Calculate p_ev
        p_ev = self.p_ev / self.num_feeders

        # If is_vpp_dispatch is False, bess values are 0
        if not is_vpp_dispatch:
            p_feed = self.p_load + p_ev

        # Adjust p_ev and calculate bess values if vpp_dispatch is True
        else:
            # Adjust p_ev by available controllable capacity
            p_ev *= self.p_ev_charge_capacity

            # Calculate the bess discharge rate
            p_bess_discharge = self.p_bess / self.num_feeders

            # If wintertime, the bess charge rate is 0
            # Else, adjust the bess charging rate if needed
            if is_winter:
                p_bess_charge = 0

            else:
                p_bess_charge = self.p_bess / self.num_feeders

            p_feed = self.p_load + p_ev - self.p_pv - p_bess_discharge + p_bess_charge

        p_sub = p_feed * self.num_feeders

        return p_feed, p_sub
