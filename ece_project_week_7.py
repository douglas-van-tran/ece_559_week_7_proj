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


def main():
    # ---------------------------------------------------------------------------------------------------
    # DEFINE SCENARIOS
    # ---------------------------------------------------------------------------------------------------

    # Scenario 1
    # PV = 0 MW
    # EV charging capacity is 50%
    scenario_1 = VirtualPowerPlant(p_load=10, p_ev=2, p_pv=0, p_ev_charge_capacity=0.5)

    # Scenario 2
    # Moderate load, assume 6 MW per feeder
    # Partial BESS charging, assume 2 MW per sub
    # No EV charging, 0 MW per sub
    scenario_2 = VirtualPowerPlant(p_load=6, p_ev=0, p_pv=5, p_bess=2)

    # Scenario 3
    # Assumptions:
    #   - Load = 8 MW per feeder
    #   - EV Charging = 2 MW per sub
    #   - PV = 2 MW per feeder
    #   - EV is paused when VPP is dispatched
    scenario_3 = VirtualPowerPlant(p_load=8, p_ev=2, p_pv=2, p_bess=-10)

    # ---------------------------------------------------------------------------------------------------
    # QUESTION 1
    # ---------------------------------------------------------------------------------------------------

    f1, s1, f1_vpp, s1_vpp = scenario_1.calculate_p_feed()
    f2 = f1
    f2_vpp = f1_vpp
    peak_red = scenario_1.calculate_peak_reduction(s1, s1_vpp)
    i_1_no_vpp, v_drop_1_no_vpp = scenario_1.calcuate_i_v(f1)
    i_1_vpp, v_drop_1_vpp = scenario_1.calcuate_i_v(f1_vpp)

    print("------------------------- PARAMETERS FOR SCENARIO 1 -------------------------\n")
    print(f"The power for feeder 1 without vpp for scenario 1 is: {f1:.2f} MW")
    print(f"The power for feeder 2 without vpp for scenario 1 is: {f2:.2f} MW")
    print(f"The power for the substation without vpp for scenario 1 is: {s1:.2f} MW")
    print()
    print(f"The power for feeder 1 with vpp for scenario 1 is: {f1_vpp:.2f} MW")
    print(f"The power for feeder 2 with vpp for scenario 1 is: {f2_vpp:.2f} MW")
    print(f"The power for the substation with vpp for scenario 1 is: {s1_vpp:.2f} MW")
    print()
    print(f"The peak reduction for scenario 1 is {peak_red:.2f}%")
    print()
    print(f"The current without vpp for scenario 1 is: {i_1_no_vpp:.2f} A")
    print(f"The current with vpp for scenario 1 is: {i_1_vpp:.2f} A")
    print()
    print(f"The voltage drop without vpp for scenario 1 is: {v_drop_1_no_vpp:.5f}%")
    print(f"The voltage drop with vpp for scenario 1 is: {v_drop_1_vpp:.5f}%")
    print()

    f1, s1, f1_vpp, s1_vpp = scenario_2.calculate_p_feed()
    f2 = f1
    f2_vpp = f1_vpp
    i_1_no_vpp, v_drop_1_no_vpp = scenario_2.calcuate_i_v(f1)
    i_1_vpp, v_drop_1_vpp = scenario_2.calcuate_i_v(f1_vpp)
    peak_red = scenario_2.calculate_peak_reduction(s1, s1_vpp, True)
    print("------------------------- PARAMETERS FOR SCENARIO 2 -------------------------\n")
    print(f"The power for feeder 1 without vpp for scenario 2 is: {f1:.2f} MW")
    print(f"The power for feeder 2 without vpp for scenario 2 is: {f2:.2f} MW")
    print(f"The power for the substation without vpp for scenario 2 is: {s1:.2f} MW")
    print()
    print(f"The power for feeder 1 with vpp for scenario 2 is: {f1_vpp:.2f} MW")
    print(f"The power for feeder 2 with vpp for scenario 2 is: {f2_vpp:.2f} MW")
    print(f"The power for the substation with vpp for scenario 2 is: {s1_vpp:.2f} MW")
    print()
    print(f"The peak reduction for scenario 2 is {peak_red:.2f}%")
    print()
    print(f"The current without vpp for scenario 1 is: {i_1_no_vpp:.2f} A")
    print(f"The current with vpp for scenario 1 is: {i_1_vpp:.2f} A")
    print()
    print(f"The voltage drop without vpp for scenario 1 is: {v_drop_1_no_vpp:.5f}%")
    print(f"The voltage drop with vpp for scenario 1 is: {v_drop_1_vpp:.5f}%")
    print()

    f1, s1, f1_vpp, s1_vpp = scenario_3.calculate_p_feed()

    # Adjust values based on the scenario
    transfer_load = 4
    scenario_3_p_ev_per_feeder = 1
    f1 += transfer_load
    s1 = f1
    f2 = 0
    f1_vpp += transfer_load - scenario_3_p_ev_per_feeder
    f2_vpp = 0
    s1_vpp = f1_vpp

    peak_red = scenario_3.calculate_peak_reduction(s1, s1_vpp)
    i_1_no_vpp, v_drop_1_no_vpp = scenario_1.calcuate_i_v(f1)
    i_1_vpp, v_drop_1_vpp = scenario_1.calcuate_i_v(f1_vpp)
    print("------------------------- PARAMETERS FOR SCENARIO 3 -------------------------\n")
    print(f"The power for feeder 1 without vpp for scenario 2 is: {f1:.2f} MW")
    print(f"The power for feeder 2 without vpp for scenario 2 is: {f2:.2f} MW")
    print(f"The power for the substation without vpp for scenario 2 is: {s1:.2f} MW")
    print()
    print(f"The power for feeder 1 with vpp for scenario 2 is: {f1_vpp:.2f} MW")
    print(f"The power for feeder 2 with vpp for scenario 2 is: {f2_vpp:.2f} MW")
    print(f"The power for the substation with vpp for scenario 2 is: {s1_vpp:.2f} MW")
    print()
    print(f"The peak reduction for scenario 2 is {peak_red:.2f}%")
    print()
    print(f"The current without vpp for scenario 1 is: {i_1_no_vpp:.2f} A")
    print(f"The current with vpp for scenario 1 is: {i_1_vpp:.2f} A")
    print()
    print(f"The voltage drop without vpp for scenario 1 is: {v_drop_1_no_vpp:.5f}%")
    print(f"The voltage drop with vpp for scenario 1 is: {v_drop_1_vpp:.5f}%")


if __name__ == "__main__":
    main()
