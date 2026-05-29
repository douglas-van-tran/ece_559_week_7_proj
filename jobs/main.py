import ece_559_week_7_proj

# def main():

# Define scenarios
scenario_1 = ece_559_week_7_proj.VirtualPowerPlant(pv=0, ev_control_capacity=0.5)
p_feed_1_no_vpp, p_sub_1_no_vpp = scenario_1.calculate_p_feed(
    is_vpp_dispatch=False, is_winter=True
)
p_feed_1_vpp, p_sub_1_vpp = scenario_1.calculate_p_feed(
    is_vpp_dispatch=True, is_winter=True
)

# # Scenario 2
# # Assume "high PV output with moderate load" is 6 MW
scenario_2 = ece_559_week_7_proj.VirtualPowerPlant(
    pv=5, peak_load=6, ev_control_capacity=0
)
x, y = scenario_2.calculate_p_feed(is_vpp_dispatch=False, bess_charge_adj=0.4)
z, a = scenario_2.calculate_p_feed(is_vpp_dispatch=True, bess_charge_adj=0.4)

# # Scenario 3
# # Feeder fault; assume PV output is 8 MW
# scenario_3 = ece_559_week_7_proj.VirtualPowerPlant(pv=8)


# if __name__ == "__main__":
#     main()
