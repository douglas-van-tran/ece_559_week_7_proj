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
# Moderate load, assume 6 MW per feeder
# Partial BESS charging, assume 2 MW per sub
# No EV charging, 0 MW per sub
scenario_2 = ece_559_week_7_proj.VirtualPowerPlant(
    p_load=6,
    p_ev=0,
    p_pv=5,
    p_bess=2,
)

# Scenario 3
# Assumptions:
#   - Load = 8 MW per feeder
#   - EV Charging = 2 MW per sub
#   - PV = 2 MW per feeder
#   - EV is paused when VPP is dispatched

# Define transfer load (MW)
transfer_load = 4

# Define the p_ev per feeder
scenario_3_p_ev_per_feeder = 1
scenario_3 = ece_559_week_7_proj.VirtualPowerPlant(
    p_load=8,
    p_ev=2,
    p_pv=2,
    p_bess=-10,
)


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
print("The parameters for scenario 2 are:")
print(f2, s2, f2_vpp, s2_vpp)


f3, s3 = scenario_3.calculate_p_feed(
    is_vpp_dispatch=False,
)
f3_vpp, s3_vpp = scenario_3.calculate_p_feed(
    is_vpp_dispatch=True,
)

# Adjust values based on the scenario
f3 += transfer_load
s3 = f3

f3_vpp += transfer_load - scenario_3_p_ev_per_feeder
s3_vpp = f3_vpp

print("The parameters for scenario 3 are:")
print(f3, s3, f3_vpp, s3_vpp)
