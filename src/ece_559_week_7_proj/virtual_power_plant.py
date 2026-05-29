import matplotlib.pyplot as plt
import numpy as np


class VirtualPowerPlant:
    def __init__(
        self,
        pv: int,
        ev_control_capacity: float = 1.0,
        num_feeders: int = 2,
        peak_load: int = 10,
        primary_volt: float = 13.2,
        feeder_len: int = 5,
        bess: int = 5,
        ev_charge_load: int = 2,
    ):
        self.pv = pv
        self.ev_control_capacity = ev_control_capacity
        self.num_feeders = num_feeders
        self.peak_load = peak_load
        self.primary_volt = primary_volt
        self.feeder_len = feeder_len
        self.bess = bess
        self.ev_charge_load = ev_charge_load

    def _calculate_p_ev(self) -> float:
        p_ev = self.ev_charge_load / self.num_feeders

        return p_ev

    def calculate_p_feed(
        self,
        is_vpp_dispatch: bool,
        bess_charge_adj: float = 1.0,
        is_winter: bool = False,
    ) -> tuple[float, float]:
        # Calculate p_ev
        p_ev = self._calculate_p_ev()

        # Adjust p_ev and calculate bess values if vpp_dispatch is True
        if is_vpp_dispatch:
            # Adjust p_ev by available controllable capacity
            p_ev *= self.ev_control_capacity

            # Calculate the bess discharge rate
            p_bess_discharge = self.bess / self.num_feeders

            # If not wintertime, adjust the bess charging rate if needed
            # Else, the bess charge rate is 0
            if not is_winter:
                p_bess_charge = (self.bess / self.num_feeders) * bess_charge_adj
            else:
                p_bess_charge = 0

        # If is_vpp_dispatch is False, bess values are 0
        else:
            p_bess_discharge = 0
            p_bess_charge = 0

        p_feed = self.peak_load + p_ev - self.pv - p_bess_discharge + p_bess_charge

        p_sub = p_feed * self.num_feeders

        return p_feed, p_sub
