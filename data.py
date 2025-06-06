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

def hefa(ratio):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = 1.3

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio
    return round(co2, 2)

def gas(ratio):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = -0.51

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio
    return round(co2, 2)

def alc(ratio):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = -0.86

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio
    return round(co2, 2)

def syn(ratio):
    fuel = KPI["Fuel/y"].sum()
    JA1 = 3.84
    SAF = 1.14

    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio
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
                plot.set_ylabel(r'CO2 Emissions ($10^6kg$)')
                plot.ticklabel_format(axis='y', style='plain')
                # Add grid for better readability
                plt.grid(True, linestyle='--', alpha=0.7)
                
                return plt.gcf()