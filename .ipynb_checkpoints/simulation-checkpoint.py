import pandas as pd

def simulate_10_year_plan(starting_toilets, toilets_per_year, scenarios_df, seniors_df):
    """Calculates the cumulative economic results of adding a given number of public toilets to Den Haag each year for the next 10 years (2025-2034). Takes into account the growing senior population of Den Haag, as well as the cumulative effects of the extra spending done by seniors when more toilets are available. Returns a dataframe.""" 
    results = []
    
    start_accumulation_year = 2025 

    baseline_67_toilets_scenario = scenarios_df[scenarios_df["toilets"] == 67].iloc[0]

    sim_year_counter = 0 

    for i, row in seniors_df.iterrows():
        year = row["year"]
        seniors = row["seniors"]

        in_active_simulation = (year >= start_accumulation_year)

        # Initialize all annual financial components to zero at the start of each year's loop
        annual_toilet_cost_this_year = 0
        additional_senior_spending_this_year = 0
        missed_outings_this_year = 0 
        missed_outing_value_this_year = 0
        net_result_this_year = 0 

        toilets_for_scenario_lookup = starting_toilets # Default for non-active years

        if in_active_simulation:
            sim_year_counter += 1 
            toilets_for_scenario_lookup = starting_toilets + sim_year_counter * toilets_per_year
            
            if toilets_for_scenario_lookup > scenarios_df["toilets"].max():
                toilets_for_scenario_lookup = scenarios_df["toilets"].max()
        
        scenario_row = scenarios_df[scenarios_df["toilets"] == toilets_for_scenario_lookup].iloc[0].copy()
        
        scaling_factor = seniors / seniors_df.iloc[0]["seniors"]

        if in_active_simulation:
            annual_toilet_cost_this_year = toilets_per_year * 200000 
            
            baseline_missed_outings_scaled = baseline_67_toilets_scenario["missed_outings"] * scaling_factor
            missed_outings_this_year = scenario_row["missed_outings"] * scaling_factor
            outings_now_happening = baseline_missed_outings_scaled - missed_outings_this_year
            additional_senior_spending_this_year = outings_now_happening * 22 

            missed_outing_value_this_year = scenario_row["missed_outing_value_eur"] * scaling_factor
            
            net_result_this_year = additional_senior_spending_this_year - annual_toilet_cost_this_year
            
        else:
            # For years before active simulation:
            # financial metrics (like annual_toilet_cost_this_year and net_result_this_year) remain 0 as initialized above.
            baseline_scaled = baseline_67_toilets_scenario.copy()
            missed_outings_this_year = baseline_scaled["missed_outings"] * scaling_factor
            missed_outing_value_this_year = baseline_scaled["missed_outing_value_eur"] * scaling_factor
            # net_result_this_year already initialized to 0

        result = {
            "year": year,
            "total_toilets": toilets_for_scenario_lookup, 
            "seniors": seniors,
            "missed_outings": missed_outings_this_year,
            "missed_outing_value_eur": missed_outing_value_this_year,
            "additional_senior_spending_eur": additional_senior_spending_this_year,
            "cost_new_toilets_eur": annual_toilet_cost_this_year, 
            "net_gain_eur": net_result_this_year, # Using the correctly initialized variable
            
            "cost_new_toilets_eur_for_cumsum": annual_toilet_cost_this_year, 
            "net_gain_for_cumsum": net_result_this_year, 
        }
        results.append(result)

    df = pd.DataFrame(results)

    df['cumulative_toilet_cost_eur'] = 0.0
    df['cum_gain_eur'] = 0.0

    active_sim_mask = (df['year'] >= start_accumulation_year)

    df.loc[active_sim_mask, 'cumulative_toilet_cost_eur'] = df.loc[active_sim_mask, 'cost_new_toilets_eur_for_cumsum'].cumsum()
    df.loc[active_sim_mask, 'cum_gain_eur'] = df.loc[active_sim_mask, 'net_gain_for_cumsum'].cumsum()

    df = df.drop(columns=['cost_new_toilets_eur_for_cumsum', 'net_gain_for_cumsum'])

    return df