# Import necessary libraries for this dashboard
import pandas as pd # Used for reading and manipulating data, like CSV and Excel files
import matplotlib.pyplot as plt # Used for creating static, interactive, and animated visualizations in Python

# Load data into pandas DataFrames
#KPI = pd.read_csv(r"Data/Data.csv") # Reads flight data from 'Data.csv' into the KPI DataFrame
shorthaul = pd.read_excel(r"Data.xlsx")
longhaul = pd.read_excel(r"Data.xlsx", sheet_name=1)

# Join and remove unused Columns
KPI = pd.concat([shorthaul, longhaul], ignore_index=True)
KPI = KPI.drop(["Unnamed: 5"], axis=1)
KPI.to_csv(r"Data/Data.csv")

Dashboard_KPI = pd.read_excel("Data.xlsx", sheet_name=2) # Reads the third sheet of 'Data.xlsx' for dashboard KPIs

# Groups KPI data by 'TYPE' for potential long-haul(_LH) and short-haul(_SH) analysis
KPI_TYPE = KPI.groupby("Type")

# Prepare data for "Top 10 CO2 Emitting Flights" plot
# Sorts the KPI data by 'kgCO2e per year' in descending order and selects the top 10 rows
KPI_10 = KPI.sort_values(by=['kgCO2e per year'], ascending=False).head(10)

# Calculate the overall CO2 emissions per Available Seat Kilometer (ASK)
# Divides the total CO2 emissions by the total ASK across all flights
CO2_ASK = KPI["kgCO2e per year"].sum()/KPI["ASK/year"].sum()

# Define a function to estimate CO2 emissions for a given year
def co2_for_year(year: int) -> float:
    # Calculates the estimated CO2 using a predefined quadratic formula based on the input 'year'
    return ((-621765841/9000) * year**2 + (177837343907630/660893) * year - 1043944847030/4)

# Functions returning CO2 emissions for each SAF with a given Blend Ratio
def hefa(ratio, cost: bool = False):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = 1.3

    PRICE_JA1 = 1.3
    PRICE_SAF = 1.3

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    else:
        return round(co2, 2)

def gas(ratio, cost: bool = False):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = -0.51

    PRICE_JA1 = 1.3
    PRICE_SAF = 3.2

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    else:
        return round(co2, 2)

def alc(ratio, cost: bool = False):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = -0.86

    PRICE_JA1 = 1.3
    PRICE_SAF = 3.2

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    else:
        return round(co2, 2)

def syn(ratio, cost: bool = False):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = 1.14

    PRICE_JA1 = 1.3
    PRICE_SAF = 3.2

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    else:
        return round(co2, 2)

def safplot():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import seaborn as sns
    
    # Create a range of SAF ratios from 0% to 100%
    ratios = np.linspace(0, 1, 101)  # 101 points from 0 to 1
    
    # Create data for plotting
    data = []
    for r in ratios:
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'HEFA', 'CO2 Emissions': hefa(r)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Gas-to-Liquid', 'CO2 Emissions': gas(r)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Alcohol-to-Jet', 'CO2 Emissions': alc(r)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Synthetic', 'CO2 Emissions': syn(r)})
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot all SAF types at once
    plot = sns.lineplot(data=df, x='SAF Percentage', y=df['CO2 Emissions']/10**6, hue='SAF Type', palette='viridis')
    
    # Set labels and title
    plot.set_xlabel('SAF Percentage (%)')
    plot.set_ylabel(r'CO2 Emissions ($10^6$ kg)')
    plot.ticklabel_format(axis='y', style='plain')
    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    return plt.gcf()

def costplot():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import seaborn as sns
    
    # Create a range of SAF ratios from 0% to 100%
    ratios = np.linspace(0, 1, 101)  # 101 points from 0 to 1
    
    # Create data for plotting
    data = []
    for r in ratios:
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'HEFA', 'Cost': hefa(r, cost=True)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Gas-to-Liquid', 'Cost': gas(r, cost=True)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Alcohol-to-Jet', 'Cost': alc(r, cost=True)})
        data.append({'SAF Percentage': r * 100, 'SAF Type': 'Synthetic', 'Cost': syn(r, cost=True)})
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot all SAF types at once
    plot = sns.lineplot(data=df, x='SAF Percentage', y=df['Cost']/10**6, hue='SAF Type', palette='viridis')
    
    # Set labels and title
    plot.set_xlabel('SAF Percentage (%)')
    plot.set_ylabel('Cost (Million $)')
    plot.ticklabel_format(axis='y', style='plain')
    
    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    return plt.gcf()

def saf_for_year(year: int, saf_coefficient):
    fuel = KPI['Fuel/y'].sum()
    C_SAF = saf_coefficient
    ratio = (co2_for_year(year)/fuel - 3.84)/(C_SAF-3.84)
    return ratio if ratio < 1 else 1

def saf_ratio_over_time_plot():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import seaborn as sns
    
    # Define the years range
    years = range(2025, 2071)  # 5-year intervals from 2025 to 2070
    
    # Define SAF coefficients
    saf_types = {
        'HEFA': 1.3,
        'Gas-to-Liquid': -0.51,
        'Alcohol-to-Jet': -0.86,
        'Synthetic': 1.14
    }
    
    # Create data for plotting
    data = []
    for year in years:
        for saf_type, coefficient in saf_types.items():
            # Skip cases where saf_coefficient - 3.84 is very close to zero (would cause division by zero)
            if abs(coefficient - 3.84) < 0.01:
                continue
                
            ratio = saf_for_year(year, coefficient)
            data.append({'Year': year, 'SAF Type': saf_type, 'Required Blend Ratio (%)': ratio * 100, 'CO2': co2_for_year(year)})
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create the plot
    plt.figure(figsize=(12, 7))
    
    # Plot all SAF types
    plot = sns.lineplot(data=df, x='Year', y='Required Blend Ratio (%)', 
                        hue='SAF Type', palette='viridis')
    
    # Set labels and title
    plot.set_xlabel('Year')
    plot.set_ylabel('Required SAF Blend (%)')
    plot.set_title('Required SAF Blend Percentage to Reach ADL Standards')
    
    # Set y-axis to show percentages from 0-100
    plt.ylim(0, 100)
    
    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    return plt.gcf()
