# EcoFly Dashboard - Data Processing and Analysis Module
# This file handles all the data loading, processing, and visualization functions
# for the dashboard

# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up our file paths - keeping everything organized
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "Data"

# Load the main Excel file with all our aviation data
# This contains multiple sheets with different types of flight data
excel_path = BASE_DIR / "Data.xlsx"
shorthaul = pd.read_excel(excel_path)  # First sheet - short distance flights
longhaul = pd.read_excel(excel_path, sheet_name=1)  # Second sheet - long distance flights

# Combine short and long haul data into one dataframe
KPI = pd.concat([shorthaul, longhaul], ignore_index=True)
KPI = KPI.drop(["Unnamed: 5"], axis=1)
KPI.to_csv(DATA_DIR / "Data.csv")  # Save data

# Load additional data sheets for our analysis
SAF_PLUS_MINUS = pd.read_excel(excel_path, sheet_name=3)  # SAF impact data

# Baseline KPI data - this is our starting point for comparisons
baseline_kpi = pd.read_excel(excel_path, sheet_name=2)
baseline_kpi_table = baseline_kpi[["Type", "Seats", "Cargo (t)"]]  # Just the essentials

# Final KPI table
KPI_SUST_FEASB= pd.read_csv(DATA_DIR / "KPITABLE.csv", index_col=0)

def strategy_costs():
    #reading excel
    costs_data = pd.read_csv(DATA_DIR / "costplots.csv")

    #figsize
    plt.figure(figsize=(12,8))

    #barplot code
    sns.barplot(data=costs_data,x='strategy',y='costs', hue='strategy', palette='viridis')
    plt.xlabel('Strategy')
    plt.ylabel('Costs in billions of euros')
    plt.title('Costs for Strategies')

    return plt.gcf()

# Create a pie chart showing baseline CO2 emissions
def plot_pie_chart():
    # Filter to get only the total emissions row
    df = baseline_kpi[baseline_kpi["Type"]=="TOTAL"]
    # Remove columns we don't need for the pie chart
    df = df.drop(columns=["Type", "Aircraft", "Flight/y", "Fuel  (t)", "kton CO2e/y", "Total CO2e", "Seats", "Cargo (t)"])
    
    # Use a nice color palette - viridis_r looks professional
    colors = sns.color_palette("viridis_r")
    values = df.iloc[0].values
    labels = df.columns
    
    # Create the pie chart with percentages
    plt.pie(values, labels=labels, colors=colors, autopct="%.0f%%")
    plt.title(r"Baseline CO2e Emissions: $675.84\cdot{}10^6$ kg") 
    return plt.gcf()

# Compare current fleet vs new fleet emissions
# This shows the impact of fleet renewal on our carbon footprint
def fleet_renewal():
    # Group by aircraft type and sum up emissions
    grouped = KPI.groupby("Type").sum()
    colors = sns.color_palette("viridis_r")

    fig, ax = plt.subplots()
    width = 0.35  # Width of the bars
    x = np.arange(len(grouped.index))

    # Current fleet vs new fleet (assuming 20% reduction with new aircraft)
    ax.bar(x - width/2, grouped["kgCO2e per year"], width, label='Current Fleet', color=colors[5], alpha=0.8)
    ax.bar(x + width/2, 0.8 * grouped["kgCO2e per year"], width, label='New Fleet', color=colors[0], alpha=0.8)
    
    # Add labels
    ax.set_xlabel('Aircraft Type')
    ax.set_ylabel('CO2 Emissions (kg per year)')
    ax.set_title("Fleet Renewal impact on Scope-1 Emissions")
    ax.set_xticks(x)
    ax.set_xticklabels(grouped.index)
    ax.legend()

    # Return the full figure
    return plt.gcf()

# Calculate CO2 emissions target for any given year
def co2_for_year(year: int) -> float:
    return ((-621765841/9000) * year**2 + (177837343907630/660893) * year - 1043944847030/4)

# SAF (Sustainable Aviation Fuel) analysis functions
# Each function calculates emissions and costs for different SAF types

# HEFA SAF - made from waste oils and fats (first generation biofuel)
def hefa(ratio, cost=False):
    fuel = KPI["Fuel/y"].sum()  # Total fuel consumption
    JA1, SAF = 3.84, 1.3  # CO2 coefficients for regular jet fuel vs HEFA SAF
    PRICE_JA1, PRICE_SAF = 1.3, 1.3  # Price per unit (SAF costs the same as JA1 here)
    
    # Calculate weighted CO2 emissions based on fuel mix
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        # Calculate total cost including fuel and carbon pricing
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:  # Add carbon tax if we're still emitting
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

# Gas-to-Liquid SAF - synthetic fuel from natural gas
def gas(ratio, cost=False):
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, -0.51
    PRICE_JA1, PRICE_SAF = 1.3, 3.2
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

# Alcohol-to-Jet SAF - made from ethanol or other alcohols
def alc(ratio, cost=False):
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, -0.86
    PRICE_JA1, PRICE_SAF = 1.3, 3.2
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

# Synthetic SAF - made from captured CO2 and renewable energy
def syn(ratio, cost=False):
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, 1.14
    PRICE_JA1, PRICE_SAF = 1.3, 3.2
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

# Create a comprehensive plot showing CO2 emissions for different SAF types
# This helps visualize which SAF performs best at different blend ratios
def safplot():
    ratios = np.linspace(0, 1, 101)  # From 0% to 100% SAF in 1% increments
    
    # Generate data for all SAF types across all ratios
    data = []
    for r in ratios:
        data.append({"SAF Percentage": r * 100, "SAF Type": "HEFA", "CO2 Emissions": hefa(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Gas-to-Liquid", "CO2 Emissions": gas(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Alcohol-to-Jet", "CO2 Emissions": alc(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Synthetic", "CO2 Emissions": syn(r)})
    
    # Create a line plot
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    
    plot = sns.lineplot(data=df, x="SAF Percentage", y=df["CO2 Emissions"]/10**6, hue="SAF Type", palette="viridis")
    plot.set_xlabel("SAF Percentage (%)")
    plot.set_ylabel("CO2 Emissions (10⁶ kg)")  # Converting to millions for readability
    plot.set_title("CO2 emissions per SAF")
    plot.ticklabel_format(axis="y", style="plain")  # No scientific notation
    plt.grid(True, linestyle="--", alpha=0.7)  # Subtle grid lines
    
    return plt.gcf()

# Similar plot but for costs
def costplot():
    ratios = np.linspace(0, 1, 101)
    
    # Generate cost data for all SAF types
    data = []
    for r in ratios:
        data.append({"SAF Percentage": r * 100, "SAF Type": "HEFA", "Cost": hefa(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Gas-to-Liquid", "Cost": gas(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Alcohol-to-Jet", "Cost": alc(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Synthetic", "Cost": syn(r, cost=True)})
    
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    
    plot = sns.lineplot(data=df, x="SAF Percentage", y=df["Cost"]/10**6, hue="SAF Type", palette="viridis")
    plot.set_xlabel("SAF Percentage (%)")
    plot.set_ylabel("Cost (Million $)")
    plot.set_title("Cost of SAF Utilization")
    plot.ticklabel_format(axis="y", style="plain")
    plt.grid(True, linestyle="--", alpha=0.7)
    
    return plt.gcf()

# Calculate what SAF blend ratio we need for a specific year to meet targets
def saf_for_year(year, saf_coefficient):
    fuel = KPI["Fuel/y"].sum()
    # Solve for the ratio needed to hit our CO2 target
    ratio = (co2_for_year(year)/fuel - 3.84)/(saf_coefficient-3.84)
    return min(ratio, 1)  # Can't exceed 100% SAF blend

def saf_ratio_over_time_plot():
    years = range(2025, 2071)  # Long-term planning horizon
    saf_types = {
        "HEFA": 1.3,
        "Gas-to-Liquid": -0.51,
        "Alcohol-to-Jet": -0.86,
        "Synthetic": 1.14
    }

    # Calculate required blend ratios for each SAF type over time
    data = []
    for year in years:
        for saf_type, coef in saf_types.items():
            if abs(coef - 3.84) < 0.01:  # Skip if coefficient is too close to regular fuel
                continue
            ratio = saf_for_year(year, coef)
            data.append({"Year": year, "SAF Type": saf_type, "Required Blend Ratio (%)": ratio * 100})

    # Create the main plot
    df = pd.DataFrame(data)
    plt.figure(figsize=(12, 7))
    plot = sns.lineplot(data=df, x="Year", y="Required Blend Ratio (%)", hue="SAF Type", palette="viridis")
    plot.set_xlabel("Year")
    plot.set_ylabel("Required SAF Blend (%)")
    plot.set_title("Required SAF Blend to Reach ADL")
    sns.move_legend(obj=plot, loc="center left")
    plt.ylim(0, 100)  # Percentage scale
    plt.grid(True, linestyle="--", alpha=0.7)

    # Add a second y-axis to show the CO2 trajectory we're trying to follow
    ax2 = plt.twinx()
    unique_years = sorted(df["Year"].unique())
    co2_values = [co2_for_year(year)/1e6 for year in unique_years]  # Convert to millions
    ax2.plot(unique_years, co2_values, color="red", linestyle="--", label="CO2 Target")
    ax2.set_ylabel("CO2 Emissions (10⁶ kg)")
    ax2.tick_params(axis="y")

    plt.legend()

    return plt.gcf()