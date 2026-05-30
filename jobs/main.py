import ece_559_week_7_proj

# def main():

# Define scenarios
scenario_1 = ece_559_week_7_proj.VirtualPowerPlant(p_pv=0, ev_charging_capacity=0.5)
a, b = scenario_1.calculate_p_feed(
    is_vpp_dispatch=False,
    is_winter=True,
)
c, d = scenario_1.calculate_p_feed(
    is_vpp_dispatch=True,
    is_winter=True,
)

# # Scenario 2
# # Assume "high PV output with moderate load" is 6 MW
scenario_2 = ece_559_week_7_proj.VirtualPowerPlant(p_pv=5, peak_load=6, ev_charging_capacity=0)
e, f = scenario_2.calculate_p_feed(is_vpp_dispatch=False, bess_charge_adj=0.4)
g, h = scenario_2.calculate_p_feed(is_vpp_dispatch=True, bess_charge_adj=0.4)

# # Scenario 3
# # Feeder fault; assume PV output is 8 MW
# scenario_3 = ece_559_week_7_proj.VirtualPowerPlant(pv=8)


# if __name__ == "__main__":
#     main()
