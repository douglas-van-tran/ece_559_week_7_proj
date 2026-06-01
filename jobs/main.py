import ece_559_week_7_proj

# def main():

# if __name__ == "__main__":
#     main()

# Scenario 1
# PV = 0 MW
# EV charging capacity is 50%
scenario_1 = ece_559_week_7_proj.VirtualPowerPlant(
    p_load=10,
    p_ev=2,
    p_pv=0,
    p_ev_charge_capacity=0.5,
)

# Scenario 2
# Moderate load, assume 6 MW
# Partial BESS charging, assume 2 MW
# No EV charging, 0 MW
scenario_2 = ece_559_week_7_proj.VirtualPowerPlant(
    p_load=6,
    p_ev=0,
    p_pv=5,
    p_bess=2,
)

# Scenario 3
# Assumptions:
#   - Load = 16 MW
#   - EV Charging = 2 MW
#   -

f1, s1 = scenario_1.calculate_p_feed(
    is_vpp_dispatch=False,
)
f1_vpp, s1_vpp = scenario_1.calculate_p_feed(
    is_vpp_dispatch=True,
)
print("The parameters for scenario 1 are:")
print(f1, s1, f1_vpp, s1_vpp)

f2, s2 = scenario_2.calculate_p_feed(
    is_vpp_dispatch=False,
)
f2_vpp, s2_vpp = scenario_2.calculate_p_feed(
    is_vpp_dispatch=True,
)
print("The parameters for scenario 1 are:")
print(f2, s2, f2_vpp, s2_vpp)
