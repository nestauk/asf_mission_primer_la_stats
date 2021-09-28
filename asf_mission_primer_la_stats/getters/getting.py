import pandas as pd

def get_emissions():
    emissions = (
        pd.read_csv("inputs/LA_emissions.csv")[
            [
                "Country",
                "Local Authority",
                "Local Authority Code",
                "Calendar Year",
                "LA CO2 Sector",
                "LA CO2 Sub-sector",
                "Territorial emissions (kt CO2)",
                "Mid-year Population (thousands)",
                "Area (km2)"
            ]
        ].rename(columns={
            "Country": "country",
            "Local Authority": "la_name",
            "Local Authority Code": "la_code",
            "Calendar Year": "year",
            "LA CO2 Sector": "sector",
            "LA CO2 Sub-sector": "subsector",
            "Territorial emissions (kt CO2)": "emissions",
            "Mid-year Population (thousands)": "population",
            "Area (km2)": "area"
            }
        ).dropna(subset = ['la_code'])
    )

    # Drop unallocated emissions - only care about ones allocated to LAs
    unallocated = emissions[["Unallocated" in string for string in emissions.la_name]]
    emissions = emissions.drop(index = unallocated.index)
    
    return emissions


def get_regions():
    regions = (
        pd.read_csv('inputs/la_all_codes.csv')[
            [
                'LADCD', 
                'RGNNM', 
                'CTRYNM'
            ]
        ].rename(columns={
            'LADCD': "la_code",
            'RGNNM': "region",
            'CTRYNM': "country"
        })
    )

    # Make one column combining English region / devolved nation
    regions.region = regions.region.fillna(regions.country)
    regions = regions.drop(columns = 'country')
    
    return regions

