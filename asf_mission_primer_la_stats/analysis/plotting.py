from asf_mission_primer_la_stats.pipeline.cleaning import (
    form_emissions_data,
    form_percentage_changes,
)
from asf_mission_primer_la_stats.pipeline.plotting_functions import (
    line_region_plot,
    scatter_with_trendline,
    line_plot,
    multi_line_plot,
    highlight_ni_scatter,
    line_region_plot,
    multi_line_region_plot,
)

full = form_emissions_data()

#### OVERALL

# Total emissions over time

overall_total = full.groupby("year")["total_emissions"].sum()

line_plot(
    data=overall_total,
    ylim_max=160000,
    xlabel="Year",
    ylabel="Total domestic CO2 emissions (kt)",
    title="Total UK domestic CO2 emissions",
    filename="total.png",
)


# Per capita emissions over time

overall_per_capita = full.groupby("year")[["total_emissions", "population"]].sum()
overall_per_capita["emissions_per_capita"] = (
    overall_per_capita["total_emissions"] / overall_per_capita["population"]
)
overall_per_capita = overall_per_capita.drop(columns=["total_emissions", "population"])

line_plot(
    data=overall_per_capita,
    ylim_max=2.6,
    xlabel="Year",
    ylabel="Domestic CO2 emissions per capita (tons)",
    title="Overall UK domestic CO2 emissions per capita",
    filename="per_capita.png",
    colour="orange",
)


#### REGIONAL

region_sums = (
    full.groupby(["region", "year"])
    .agg(
        total_domestic_emissions=("total_emissions", sum),
        total_population=("population", sum),
    )
    .reset_index()
)

region_sums["domestic_emissions_per_capita"] = (
    region_sums["total_domestic_emissions"] / region_sums["total_population"]
)

# Total emissions by region

multi_line_region_plot(
    data=region_sums,
    line_1="South East",
    line_2="Northern Ireland",
    col_1="green",
    col_2="red",
    factor="total_domestic_emissions",
    ylim_max=22500,
    x_label="Year",
    y_label="Total domestic CO2 emissions (kilotons)",
    title="Total domestic CO2 emissions by region",
    filename="regions_totals.png",
)

# Per capita emissions by region

multi_line_region_plot(
    data=region_sums,
    line_1="Northern Ireland",
    line_2="London",
    col_1="red",
    col_2="blue",
    factor="domestic_emissions_per_capita",
    ylim_max=3,
    x_label="Year",
    y_label="Domestic CO2 emissions per capita (tons)",
    title="Domestic CO2 emissions per capita by region",
    filename="regions_per_capita.png",
)

# Scaled to 2005 values

values_05 = region_sums.groupby("region").agg(
    total_05=("total_domestic_emissions", lambda x: x.iloc[0]),
    pc_05=("domestic_emissions_per_capita", lambda x: x.iloc[0]),
)

regions_with_05_vals = region_sums.merge(values_05, on="region")
regions_with_05_vals["total_as_perc_05"] = (
    regions_with_05_vals["total_domestic_emissions"] / regions_with_05_vals["total_05"]
)
regions_with_05_vals["pc_as_perc_05"] = (
    regions_with_05_vals["domestic_emissions_per_capita"]
    / regions_with_05_vals["pc_05"]
)

# Total emissions, scaled

line_region_plot(
    data=regions_with_05_vals,
    line1="Northern Ireland",
    factor="total_as_perc_05",
    x_label="Year",
    y_label="Total domestic CO2 emissions,\nas a percentage of 2005 value",
    title="Total domestic CO2 emissions by region",
    filename="scaled_total_region.png",
)

# Per capita emissions, scaled

line_region_plot(
    data=regions_with_05_vals,
    line1="Northern Ireland",
    factor="pc_as_perc_05",
    x_label="Year",
    y_label="Domestic CO2 emissions per capita,\nas a percentage of 2005 value",
    title="Domestic CO2 emissions per capita by region",
    filename="scaled_pc_region.png",
)


#### INDIVIDUAL LOCAL AUTHORITIES

# Biggest total emitters in 2005

big_total_emitters_2005 = (
    full[full["year"] == 2005].sort_values("total_emissions").tail()["la_name"]
)

multi_line_plot(
    data=full,
    las=big_total_emitters_2005,
    x_factor="year",
    y_factor="total_emissions",
    ave_data=overall_total / 380,
    ave_label="LA average",
    ylim_max=2500,
    xlabel="Year",
    ylabel="Total domestic CO2 emissions (kt)",
    title="Domestic emissions of the five local authorities\nwith the highest total emissions in 2005",
    filename="biggest_emitters_total.png",
)


# Highest per capita emissions in 2005

big_per_capita_emitters_2005 = (
    full[full["year"] == 2005].sort_values("emissions_per_capita").tail()["la_name"]
)

multi_line_plot(
    data=full,
    las=big_per_capita_emitters_2005,
    x_factor="year",
    y_factor="emissions_per_capita",
    ave_data=overall_per_capita,
    ave_label="UK overall",
    ylim_max=4.5,
    xlabel="Year",
    ylabel="Domestic CO2 emissions per capita (tons)",
    title="Domestic emissions of the five local authorities\nwith the highest per capita emissions in 2005",
    filename="biggest_emitters_per_capita.png",
)


# Percentage decrease 2005-19

percentage_changes = form_percentage_changes()

highlight_ni_scatter(
    data=percentage_changes,
    x_factor="total_emissions_2005",
    y_factor="total_percentage_decrease",
    xlim_max=2500,
    ylim_max=60,
    x_label="Total domestic emissions in 2005 (kt CO2)",
    y_label="Percentage reduction in total\ndomestic CO2 emissions, 2005-19",
    title="Local authorities' domestic CO2 reductions from 2005 to 2019\nvs their total domestic emissions in 2005",
    filename="la_percentage_reductions_by_total.png",
)

highlight_ni_scatter(
    data=percentage_changes,
    x_factor="pc_emissions_2005",
    y_factor="pc_percentage_decrease",
    xlim_max=4.5,
    ylim_max=70,
    x_label="Domestic CO2 emissions per capita in 2005 (tons)",
    y_label="Percentage reduction in domestic\nCO2 emissions per capita, 2005-19",
    title="Local authorities' domestic CO2 reductions from 2005 to 2019\nvs their domestic emissions per capita in 2005",
    filename="la_percentage_reduction_per_capita.png",
)

# Standout LAs

percentage_changes[percentage_changes.total_percentage_decrease < 30]

percentage_changes[
    (percentage_changes.total_percentage_decrease > 45)
    & (percentage_changes.total_emissions_2005 > 1300)
]

percentage_changes[
    (percentage_changes.pc_percentage_decrease > 45)
    & (percentage_changes.pc_emissions_2005 > 3.5)
]


# Population density vs per capita emissions

emissions_area_2019 = full[full.year == 2019]

scatter_with_trendline(
    data=emissions_area_2019,
    x_factor="population_density",
    y_factor="emissions_per_capita",
    s=3,
    ylim_max=2.5,
    xlabel="2019 population density (people/km2)",
    ylabel="2019 household emissions per capita (t CO2 per person)",
    title="Local authorities' household CO2 emissions\nper capita vs population density",
    filename="emissions_vs_pop_density.png",
)


# Population density vs percentage reduction in emissions

full_pcs_19 = (
    full.groupby("la_name")
    .tail(1)
    .drop(columns="region")
    .join(percentage_changes, on="la_name")
)

scatter_with_trendline(
    data=full_pcs_19,
    x_factor="population_density",
    y_factor="pc_percentage_decrease",
    s=3,
    ylim_max=65,
    xlabel="2019 population density (people/$km^2$)",
    ylabel="Percentage decrease in domestic\nCO2 emissions per capita, 2005-19",
    title="Local authorities' percentage decrease in\nper capita emissions vs population density",
    filename="population_density_pc.png",
)


# Highest and lowest emitters per capita in 2019

emissions_per_capita_2019 = emissions_area_2019.sort_values(
    "emissions_per_capita", ascending=False
)[["la_name", "emissions_per_capita"]]
emissions_per_capita_2019.head(10)
emissions_per_capita_2019.tail(10)


# fig, ax = plt.subplots()

# for la in set(full['Local Authority']):
#     la_data = full[full['Local Authority'] == la]
#     x = la_data['Calendar Year']
#     y = la_data['Domestic emissions per capita (t CO2 per person)']
#     ax.plot(x, y, c = 'grey', linewidth = 0.5)


# full_12_13 = full[[year in [2012, 2013] for year in full['Calendar Year']]]
# diffs = (
#     full_12_13
#     .groupby(['Local Authority'])
#     .agg(diff = ('Domestic emissions per capita (t CO2 per person)', lambda df: df.iloc[1] - df.iloc[0]))
#     .sort_values('diff', ascending=False)
# )


# values in "(thousands)" cols are surely not in thousands - otherwise billions of households in UK!

# gas_grid = pd.read_csv('inputs/gas_grid.csv', na_values='..')
# gas_grid['total_properties'] = gas_grid['Number of properties (thousands)']
# gas_grid['off_gas_properties'] = gas_grid['Estimated number of properties not connected to the gas network (thousands)']

# la_gas_grid = (
#     gas_grid
#     .groupby('Local Authority Name')
#     .agg(
#         total_properties = ('total_properties', sum),
#         off_gas_properties = ('off_gas_properties', sum)
#     )
# )

# la_gas_grid['off_gas_prop'] = la_gas_grid['off_gas_properties'] / la_gas_grid['total_properties']

# full_gas = full_pcs_19.join(la_gas_grid, on='Local Authority')

# x = full_gas['off_gas_prop']
# y = full_gas['pc_percentage_decrease']

# fig, ax = plt.subplots()

# ax.scatter(x, y, s=3)


# x = full_gas['off_gas_prop']
# y = full_gas['total_percentage_decrease']


# leps = pd.read_excel('inputs/LEPs.xls', skiprows = 8, header = 1, skipfooter = 4).dropna().reset_index(drop=True)[['LEP', 'ONS LA (District/ Unitary) Code (NEW)']]


# lep_emissions = (
#     leps
#     .merge(emissions_merged, how='left', left_on='ONS LA (District/ Unitary) Code (NEW)', right_on='Local Authority Code')
#     .drop(columns=['ONS LA (District/ Unitary) Code (NEW)', 'index', 'Population density (people per km2)', 'Emissions per capita (t CO2 per person)'])
# )

# lep_sums = lep_emissions.groupby('LEP')[['Total emissions (kt CO2)', 'Mid-year Population (thousands)']].sum()
# lep_sums['Domestic emissions per capita (t CO2 per person)'] = lep_sums['Total emissions (kt CO2)'] / lep_sums['Mid-year Population (thousands)']
# lep_sums.sort_values('Domestic emissions per capita (t CO2 per person)', ascending = False)
