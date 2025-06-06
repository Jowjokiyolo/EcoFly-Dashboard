# Import necessary libraries for this dashboard
import pandas as pd # Used for reading and manipulating data, like CSV and Excel files
import matplotlib.pyplot as plt # Used for creating static, interactive, and animated visualizations in Python

# Load data into pandas DataFrames
KPI = pd.read_csv(r"Data/Data.csv") # Reads flight data from 'Data.csv' into the KPI DataFrame
KPI_DASH = pd.read_excel("Data.xlsx", sheet_name=2) # Reads the third sheet of 'Data.xlsx' for dashboard KPIs

# Groups KPI data by 'TYPE' for potential long-haul(_LH) and short-haul(_SH) analysis
# KPI_LH = KPI.groupby("TYPE")
# KPI_SH = KPI.groupby("TYPE")

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

