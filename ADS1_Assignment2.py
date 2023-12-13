# import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def data_read_clean_process(filename, countries_list, indicators_list):
    """
    Process the data by filtering specified countries and indicators.

    Parameters:
    - filename (pd.DataFrame): The original data.
    - countries_list (list): List of countries to filter.
    - indicators_list (list): List of indicators to filter.

    Returns:
    - cleaned_data (pd.DataFrame): Cleaned data with specified countries and
      indicators.
    - transposed_data (pd.DataFrame): Transposed and cleaned data.
    """
    cleaned_data = filename[
        (filename['Country Name'].isin(countries_list)) &
        (filename['Indicator Name'].isin(indicators_list))
    ]

    cleaned_data = cleaned_data.drop(['Country Code', 'Indicator Code'],
                                     axis=1)

    transposed_data = cleaned_data.transpose()
    transposed_data.columns = transposed_data.iloc[0]
    transposed_data = transposed_data.iloc[1:]
    transposed_data = transposed_data[transposed_data.index.astype(str)
                                      .str.isnumeric()]
    transposed_data.columns.name = 'Years'
    return cleaned_data, transposed_data

def correlation_heatmap(data, countries, years, indicators):
    """
    Create a correlation heatmap between indicators.

    Parameters:
    - data (pd.DataFrame): The data.
    - countries (list): List of countries.
    - years (list): List of years.
    - indicators (list): List of indicators.
    """
    indicator_data = data.pivot_table(index='Country Name',
                                      columns='Indicator Name', values=year)
    correlation_data = indicator_data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap between Indicators')
    plt.xlabel('Indicator Name')
    plt.ylabel('Indicator Name')
    plt.savefig('heatmap.png', bbox_inches='tight')
    plt.show()

def line_plot_creation(data, countries, indicator, years):
    """
    Create a line plot for the specified indicator over years.

    Parameters:
    - data (pd.DataFrame): The data.
    - countries (list): List of countries.
    - indicator (str): The indicator for the line plot.
    - years (list): List of years.
    """
    plt.figure(figsize=(12, 8))

    for year in years:
        plt.plot(countries, data[data['Indicator Name'] == indicator][year].
                 values, marker='o', label=f'{year}')

    plt.title(f'Line Plot for {indicator} Over Years')
    plt.xlabel('Country')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('lineplot.png')
    plt.show()

def bar_plot_creation(data, countries, indicator, years):
    """
    Create a bar plot for the specified indicator over years.

    Parameters:
    - data (pd.DataFrame): The data.
    - countries (list): List of countries.
    - indicator (str): The indicator for the bar plot.
    - years (list): List of years.
    """
    plt.figure(figsize=(12, 8))
    bar_width = 0.09  # Width of the bars
    bar_positions = np.arange(len(countries))  # Bar positions on x-axis

    for i, year in enumerate(years):
        values = data[data['Indicator Name'] == indicator][year].values
        plt.bar(bar_positions + i * (bar_width), values, width=bar_width,
                label=f'{year}')

    plt.title(f'Bar Plot for {indicator} Over Years')
    plt.xlabel('Country')
    plt.ylabel('Value')
    plt.xticks(bar_positions + ((len(years) - 1) * (bar_width)) / 2, countries)
    plt.legend()
    plt.savefig('barplot.png')
    plt.show()

def histogram_creation(data, indicator, bins=15):
    """
    Create a histogram for the specified indicator.

    Parameters:
    - data (pd.DataFrame): The data.
    - indicator (str): The indicator for the histogram.
    - bins (int): Number of bins in the histogram.
    """
    plt.figure(figsize=(12, 8))
    values = data[data['Indicator Name'] == indicator]['2002'].astype(float)
    plt.hist(values, bins=bins, color='blue', edgecolor='black',
             label=indicator)
    plt.title(f'Histogram of {indicator} in 2002')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(loc='upper left')
    plt.savefig('hist.png')
    plt.show()

def statistics_calculation(data):
    """
    Calculate and display summary statistics, skewness, and kurtosis f
    or the data.

    Parameters:
    - data (pd.DataFrame): The data.
    """
    statis_data = data.describe()
    print("statis_summary :")
    print(statis_data)
    skew_result = statis_data.skew()
    print("Skew : ")
    print(skew_result)
    kurt_result = statis_data.kurt()
    print("Kurt : ")
    print(kurt_result)
    

# Read the CSV file into a DataFrame
filename = pd.read_csv("/Users/diya/Desktop/API_19_DS2_en_csv_v2_5998250.csv",
                       skiprows=4)

# Specify the list of countries to analyze
countries_list = ['India', 'United Kingdom', 'China', 'United States',
                  'Bangladesh']

# Specify the list of indicators to analyze
indicators_list = ['Agricultural land (sq. km)','Cereal yield (kg per hectare)'
                   ,'Urban population', 'Population growth (annual %)', 
                   'CO2 emissions from liquid fuel consumption (% of total)']

# Specify the list of years for analysis
year_list = ['1990', '1995', '2000', '2005', '2010']

# Specify a specific year for analysis
year = ['1999']

# Clean and process the data
cleaned_data, transposed_data = data_read_clean_process(filename,
                                            countries_list, indicators_list)

# Create a correlation heatmap between selected indicators for a specific year
correlation_heatmap(cleaned_data, countries_list, year, indicators_list)

# Create a line plot for 'Urban population' over the specified years
line_plot_creation(cleaned_data, countries_list, 'Urban population', year_list)

# Create a line plot for 'Population growth (annual %)' over the specified years
line_plot_creation(cleaned_data, countries_list, 'Population growth (annual %)',
                   year_list)

# Create a bar plot for 'Urban population' over the specified years
bar_plot_creation(cleaned_data, countries_list, 'Urban population', year_list)

# Create a bar plot for 'Agricultural land (sq. km)' over the specified years
bar_plot_creation(cleaned_data, countries_list, 'Agricultural land (sq. km)',
                  year_list)

# Create a histogram for 'CO2 emissions from liquid fuel consumption (% of total)' in 2002
histogram_creation(cleaned_data, 
                   'CO2 emissions from liquid fuel consumption (% of total)')

# Calculate and display summary statistics for the cleaned data
statistics_calculation(cleaned_data)



