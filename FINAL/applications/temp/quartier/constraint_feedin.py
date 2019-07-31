def add_constraint(om, res_share):

    conventional = [('commodity_hard_coal', 'hard_coal'),
        ('commodity_gas', 'gas'),
        ('commodity_waste', 'waste'),
        ('commodity_uranium', 'uranium'),
        ('commodity_lignite', 'lignite')]

    renewable = [('biomass_st', 'electricity'),
        ('wind_onshore', 'electricity'),
        ('wind_offshore', 'electricity'),
        ('pv', 'electricity'),
        ('geothermal', 'electricity'),
        ('runofriver', 'electricity')]

    excess = [('electricity', 'electricity_excess')]

    # add new constraint
    om.new_resource_constraint = po.Constraint(expr=(
        (1 - res_share) * (
            sum(om.w[i, o, t] for i, o in conventional for t in om.timesteps) +
            sum(om.w[i, o, t] for i, o in renewable for t in om.timesteps) -
            sum(om.w[i, o, t] for i, o in excess for t in om.timesteps)) -
        sum(om.w[i, o, t] for i, o in conventional for t in om.timesteps)
        >= 0.0))

    return

	
	        add_constraint(om, 0.8)
			
def add_constraint(om, max_feedin):

    feedin = [('flow(house_2_bel_pv_house_2_feedin')]
        ('commodity_gas', 'gas'),
        ('commodity_waste', 'waste'),
        ('commodity_uranium', 'uranium'),
        ('commodity_lignite', 'lignite')]

    renewable = [('biomass_st', 'electricity'),
        ('wind_onshore', 'electricity'),
        ('wind_offshore', 'electricity'),
        ('pv', 'electricity'),
        ('geothermal', 'electricity'),
        ('runofriver', 'electricity')]

    excess = [('electricity', 'electricity_excess')]

    # add new constraint
    om.new_resource_constraint = po.Constraint(expr=(
            om.w[i, o, t] for i, o in flow(house_2_bel_pv_house_2_feedin) for t in om.timesteps
        <= InvestmentFlow_invest(house_1_pv_house_1_bel_pv) * max_feedin))

    return

	
	        add_constraint(om, 0.8)