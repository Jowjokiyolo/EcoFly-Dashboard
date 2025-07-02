# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define base directory - this helps us find files regardless of where the script is run from
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "Data"

# Load data from Excel file with multiple sheets
excel_path = BASE_DIR / "Data.xlsx"
shorthaul = pd.read_excel(excel_path)  # Default sheet (first one)
longhaul = pd.read_excel(excel_path, sheet_name=1)  # Second sheet

# Join and clean the data
KPI = pd.concat([shorthaul, longhaul], ignore_index=True)  # Combine short and long haul data
KPI = KPI.drop(["Unnamed: 5"], axis=1)  # Remove unwanted column
KPI.to_csv(DATA_DIR / "Data.csv")  # Save cleaned data as CSV for backup

# Load additional data sheets for SAF analysis and baseline values
SAF_PLUS_MINUS = pd.read_excel(excel_path, sheet_name=3)

baseline_kpi = pd.read_excel(excel_path, sheet_name=2)
baseline_kpi_table = baseline_kpi[["Type", "Seats", "Cargo (t)"]]  # Extract only relevant columns for display

# Final KPI Table - this contains our strategy comparison results
KPI_SUST_FEASB= pd.read_csv(DATA_DIR / "KPITABLE.csv")

# Piechart Plot for baseline CO2 emissions
def plot_pie_chart():
    # Get the total row which contains our baseline emissions breakdown
    df = baseline_kpi[baseline_kpi["Type"]=="TOTAL"]
    # Remove columns we don't want in the pie chart
    df = df.drop(columns=["Type", "Aircraft", "Flight/y", "Fuel  (t)", "kton CO2e/y", "Total CO2e", "Seats", "Cargo (t)"])
    colors = sns.color_palette("viridis_r")  # Use reversed viridis color palette
    values = df.iloc[0].values  # Get the first (and only) row's values
    labels = df.columns  # Column names become our pie slice labels
    plt.pie(values, labels=labels, colors=colors, autopct="%.0f%%")
    plt.title(r"Baseline CO2e Emissions: $675.84\cdot{}10^6$ kg")  # Use LaTeX formatting for scientific notation
    return plt.gcf()

def fleet_renewal():
    # Group by aircraft type and sum up emissions for each type
    grouped = KPI.groupby("Type").sum()
    colors = sns.color_palette("viridis_r")

    fig, ax = plt.subplots()
    width = 0.35  # Width of the bars
    x = np.arange(len(grouped.index))  # Position of bars on x-axis

    # Create side-by-side bars showing current vs new fleet emissions
    ax.bar(x - width/2, grouped["kgCO2e per year"], width, label='Current Fleet', color=colors[5], alpha=0.8)
    ax.bar(x + width/2, 0.8 * grouped["kgCO2e per year"], width, label='New Fleet', color=colors[0], alpha=0.8)  # 20% reduction
    ax.set_xlabel('Aircraft Type')
    ax.set_ylabel('CO2 Emissions (kg per year)')
    ax.set_title("Fleet Renewal impact on Scope-1 Emissions")
    ax.set_xticks(x)
    ax.set_xticklabels(grouped.index)
    ax.legend()

    return plt.gcf()

# CO2 reduction trajectory - this is our mathematical model for emissions reduction over time
def co2_for_year(year: int) -> float:
    # Quadratic equation that models our CO2 reduction goal from 2025 to 2050
    return ((-621765841/9000) * year**2 + (177837343907630/660893) * year - 1043944847030/4)

# SAF functions - these calculate emissions and costs for different SAF types
def hefa(ratio, cost=False):
    """HEFA (Hydroprocessed Esters and Fatty Acids) SAF calculations"""
    fuel = KPI["Fuel/y"].sum()  # Total fuel consumption per year
    JA1, SAF = 3.84, 1.3  # CO2 coefficients for Jet A-1 and HEFA SAF (kg CO2 per kg fuel)
    PRICE_JA1, PRICE_SAF = 1.3, 1.3  # Prices per kg of fuel
    
    # Calculate total CO2 emissions with given SAF blend ratio
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        # Calculate total cost including fuel costs and carbon credits
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2  # Additional carbon credit cost
        return round(price, 2)
    return round(co2, 2)

def gas(ratio, cost=False):
    """Gas-to-Liquid SAF calculations"""
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, -0.51  # Note: negative coefficient means net CO2 reduction
    PRICE_JA1, PRICE_SAF = 1.3, 3.2  # Gas-to-liquid is more expensive
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

def alc(ratio, cost=False):
    """Alcohol-to-Jet SAF calculations"""
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, -0.86  # Best CO2 reduction coefficient
    PRICE_JA1, PRICE_SAF = 1.3, 3.2
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

def syn(ratio, cost=False):
    """Synthetic SAF calculations"""
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, 1.14  # Still reduces emissions but not as much as bio-SAF
    PRICE_JA1, PRICE_SAF = 1.3, 3.2
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

def safplot():
    """Create a plot showing CO2 emissions vs SAF percentage for different SAF types"""
    ratios = np.linspace(0, 1, 101)  # 0% to 100% SAF in 1% increments
    
    # Build dataset with all combinations of SAF types and ratios
    data = []
    for r in ratios:
        data.append({"SAF Percentage": r * 100, "SAF Type": "HEFA", "CO2 Emissions": hefa(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Gas-to-Liquid", "CO2 Emissions": gas(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Alcohol-to-Jet", "CO2 Emissions": alc(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Synthetic", "CO2 Emissions": syn(r)})
    
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    
    # Create line plot showing emissions reduction for each SAF type
    plot = sns.lineplot(data=df, x="SAF Percentage", y=df["CO2 Emissions"]/10**6, hue="SAF Type", palette="viridis")
    plot.set_xlabel("SAF Percentage (%)")
    plot.set_ylabel("CO2 Emissions (10⁶ kg)")
    plot.set_title("CO2 emissions per SAF")
    plot.ticklabel_format(axis="y", style="plain")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.savefig(r".plots/safplot.pdf")  # Save plot for documentation
    
    return plt.gcf()

def costplot():
    """Create a plot showing costs vs SAF percentage for different SAF types"""
    ratios = np.linspace(0, 1, 101)
    
    # Build cost data for all SAF types and ratios
    data = []
    for r in ratios:
        data.append({"SAF Percentage": r * 100, "SAF Type": "HEFA", "Cost": hefa(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Gas-to-Liquid", "Cost": gas(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Alcohol-to-Jet", "Cost": alc(r, cost=True)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Synthetic", "Cost": syn(r, cost=True)})
    
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    
    # Show how costs change with SAF adoption
    plot = sns.lineplot(data=df, x="SAF Percentage", y=df["Cost"]/10**6, hue="SAF Type", palette="viridis")
    plot.set_xlabel("SAF Percentage (%)")
    plot.set_ylabel("Cost (Million $)")
    plot.set_title("Cost of SAF Utilization")
    plot.ticklabel_format(axis="y", style="plain")
    plt.grid(True, linestyle="--", alpha=0.7)
    
    return plt.gcf()

def saf_for_year(year, saf_coefficient):
    """Calculate what SAF blend ratio is needed in a given year to meet CO2 targets"""
    fuel = KPI["Fuel/y"].sum()
    # Solve for the ratio needed: target_co2 = fuel * (JA1 * (1-ratio) + SAF * ratio)
    ratio = (co2_for_year(year)/fuel - 3.84)/(saf_coefficient-3.84)
    return min(ratio, 1)  # Cap at 100% SAF

def saf_ratio_over_time_plot():
    """Show how SAF blend ratios need to change over time to meet emission targets"""
    years = range(2025, 2071)  # From now until 2070
    saf_types = {
        "HEFA": 1.3,
        "Gas-to-Liquid": -0.51,
        "Alcohol-to-Jet": -0.86,
        "Synthetic": 1.14
    }

    # Calculate required blend ratios for each year and SAF type
    data = []
    for year in years:
        for saf_type, coef in saf_types.items():
            if abs(coef - 3.84) < 0.01:  # Skip if coefficient is too similar to Jet A-1
                continue
            ratio = saf_for_year(year, coef)
            data.append({"Year": year, "SAF Type": saf_type, "Required Blend Ratio (%)": ratio * 100})

    df = pd.DataFrame(data)
    plt.figure(figsize=(12, 7))
    plot = sns.lineplot(data=df, x="Year", y="Required Blend Ratio (%)", hue="SAF Type", palette="viridis")
    plot.set_xlabel("Year")
    plot.set_ylabel("Required SAF Blend (%)")
    plot.set_title("Required SAF Blend to Reach ADL")  # ADL = Ambitious Decarbonization Level
    sns.move_legend(obj=plot, loc="center left")
    plt.ylim(0, 100)
    plt.grid(True, linestyle="--", alpha=0.7)

    # Add secondary y-axis showing the CO2 target trajectory
    ax2 = plt.twinx()
    unique_years = sorted(df["Year"].unique())
    co2_values = [co2_for_year(year)/1e6 for year in unique_years]  # Convert to millions
    ax2.plot(unique_years, co2_values, color="red", linestyle="--", label="CO2 Target")
    ax2.set_ylabel("CO2 Emissions (10⁶ kg)")
    ax2.tick_params(axis="y")

    plt.legend()

    plt.savefig(r".plots/safovertimeplot.pdf")  # Save for documentation

    return