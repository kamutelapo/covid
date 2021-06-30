import logging
import os 

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

BASEDIR = os.path.dirname(__file__)

# Checking matplotlib version:
assert matplotlib.__version__.split('.')[1] == '4', "To run this script you need to have matplotlib > 3.4"

# Daily data for all countries fetched from datahub.io
COVID_DATA_URL = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv'

# Country poulation data from wikipedia:
EU_COUNTRY_WIKI = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'

# List of countries of interest:
COUNTRIES = [
    'Austria',
    'Romania',
    'Slovakia',
    'Hungary',
    'Slovenia',
    'Croatia',
    'Czech Republic'
]

def get_country_pop_map() -> dict:
    """This function fetches table from wikipedia and gets population data

    Params: None
    Returns:
        dict(): "country": population in 100k (float)
    """

    # Fetching country stats from wikipedia:
    eu_population = (
        pd.read_html(EU_COUNTRY_WIKI)[0]
        .rename(columns={'Country': 'country', '2020Eurostat figure[1]': 'pop'})
    )

    # Generating population map:
    country_pop_map = {country: eu_population[eu_population.country == country]['pop'].iloc[0] / 100_000 for country in COUNTRIES}

    return country_pop_map

def get_process_covid_data(country_pop_map: dict) -> pd.DataFrame:
    """Fetches and cleans COVID data

    Params:
        country_pop_map (dict): population information of the countries of interst
    Returns:
        pd.DataFrame: cleaned and processed daily covid data from the countries of interest
    """

    # Fetching and cleaning covid data:
    daily_covid_data = pd.read_csv(COVID_DATA_URL, sep=',')

    processed_death = (
        daily_covid_data

        # WTF?? -> in the source data, the country name is not correct.
        .assign(country=lambda df: df.Country.str.replace('Czechia', 'Czech Republic'))

        # Filter for country
        .loc[lambda df: df.country.isin(COUNTRIES)]
        .rename(columns={'Date': 'date', 'Deaths': 'deaths'})

        # A trick to move data from the previous row (has a side effect though as all countries are in one dataset):
        .assign(previous_day_death=lambda df: [0] + df.deaths.tolist()[:-1])

        # Calculate the number of death a given day:
        .assign(daily_death=lambda df: df.deaths - df.previous_day_death)

        # Daily death per 100k people:
        .assign(daily_death_100k=lambda df: df.daily_death / df.country.map(country_pop_map))

        # Cumulative death per 100k people:
        .assign(deaths_100k=lambda df: df.deaths / df.country.map(country_pop_map))

        # Dropping the first day - it got :
        .loc[lambda df: df.date != '2020-01-22']

        # Set date column as datetime object:
        .astype({'date': 'datetime64'})

        # Select columns:
        [['date', 'country', 'deaths_100k', 'daily_death_100k']]

        # Set multi-index:
        .set_index(['country', 'date'])
    )

    return processed_death


def daily_death_plot(df: pd.DataFrame, plot_file_name: str) -> None:
    """ Creating the multiplot with the daily death values.

    Param:
        df (pd.DataFrame): daily death numbers per 100 people.
        plo_filename (str): filename of the generated plot
    Return:
        None
    """

    # Initialize plot:
    fig = plt.figure(figsize=(12, 8), dpi=100, facecolor='w', edgecolor='k')
    gs = fig.add_gridspec(6, hspace=0, ncols=1)
    axs = gs.subplots(sharex=True, sharey=True)
    fig.text(0.08, 0.5, 'Halálozás / százezer fő', va='center', rotation='vertical', fontsize=15)
    fig.suptitle('Napi halálozás, heti mozgó átlag', fontsize=20)

    i = 0
    for country in COUNTRIES:

        # Skipping Hungary:
        if country == 'Hungary':
            continue

        # Calculate rolling average for a country => plot:
        axs[i].plot(
            df
            .loc[country]
            .rename(columns={'daily_death_100k': country})
            [country]
            .iloc[1:]
            .rolling('7d').mean(),
            label=country
        )

        # Calculate rolling average for Hungary => plot
        axs[i].plot(
            df
            .loc['Hungary']
            .rename(columns={'daily_death_100k': 'Hungary'})
            ['Hungary']
            .iloc[1:]
            .rolling('7d').mean(),
            label='Hungary'
        )

        # Adding legend:
        axs[i].legend(loc='upper left', frameon=False)
        i += 1

    plt.savefig(plot_file_name, dpi=100)


def main():

    # Get country population map:
    country_pop_map = get_country_pop_map()

    # Get processed COVID data:
    processed_death = get_process_covid_data(country_pop_map)

    # Generate plot:
    daily_death_plot(processed_death, f'{BASEDIR}/képek/NapiHalalozasKontextus.png')


if __name__ == '__main__':
    main()
