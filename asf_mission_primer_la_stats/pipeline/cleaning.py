from asf_mission_primer_la_stats.getters.getting import get_emissions, get_regions


def form_emissions_data():

    emissions = get_emissions()
    regions = get_regions()

    region_emissions = emissions.merge(regions, on="la_code")

    # Extract total domestic emissions
    domestic_emissions = (
        emissions[emissions.sector == "Domestic"]
        .groupby(["la_name", "year"])
        .agg(total_emissions=("emissions", sum))
        .reset_index()
    )

    # Extract LA populations and areas
    la_pop_area = (
        region_emissions[["la_name", "la_code", "year", "population", "area", "region"]]
        .groupby(["la_name", "year"])
        .head(1)
        .reset_index(drop=True)
    )

    # Merge
    all_emissions_area = la_pop_area.merge(domestic_emissions, on=["la_name", "year"])

    # Add additional columns
    all_emissions_area["emissions_per_capita"] = all_emissions_area[
        "total_emissions"
    ] / (all_emissions_area["population"])
    all_emissions_area["population_density"] = (
        1000 * all_emissions_area["population"] / all_emissions_area["area"]
    )

    return all_emissions_area


def form_percentage_changes():
    full = form_emissions_data()

    extremes = full[[year in [2005, 2019] for year in full["year"]]]

    def percentage_decrease(df):
        return 100 - (df.iloc[1] / df.iloc[0]) * 100

    percentage_changes = extremes.groupby("la_name").agg(
        total_percentage_decrease=("total_emissions", percentage_decrease),
        pc_percentage_decrease=("emissions_per_capita", percentage_decrease),
        pc_absolute_decrease=("emissions_per_capita", lambda x: x.iloc[0] - x.iloc[1]),
        total_emissions_2005=("total_emissions", lambda x: x.iloc[0]),
        pc_emissions_2005=("emissions_per_capita", lambda x: x.iloc[0]),
        region=("region", lambda x: x.iloc[0]),
    )

    return percentage_changes
