# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
shorthaul = pd.read_excel("Data.xlsx")
longhaul = pd.read_excel("Data.xlsx", sheet_name=1)

# Join and clean
KPI = pd.concat([shorthaul, longhaul], ignore_index=True)
KPI = KPI.drop(["Unnamed: 5"], axis=1)
KPI.to_csv("Data/Data.csv")

SAF_PLUS_MINUS = pd.read_excel("Data.xlsx", sheet_name=3)

Dashboard_KPI = pd.read_excel("Data.xlsx", sheet_name=2)

# Top 10 CO2 emitters
KPI_10 = KPI.sort_values(by=["kgCO2e per year"], ascending=False).head(10)

# CO2 per ASK
CO2_ASK = KPI["kgCO2e per year"].sum()/KPI["ASK/year"].sum()

# CO2 reduction trajectory
def co2_for_year(year: int) -> float:
    return ((-621765841/9000) * year**2 + (177837343907630/660893) * year - 1043944847030/4)

# SAF functions
def hefa(ratio, cost=False):
    fuel = KPI["Fuel/y"].sum()
    JA1, SAF = 3.84, 1.3
    PRICE_JA1, PRICE_SAF = 1.3, 1.3
    
    co2 = fuel*(JA1)*(1-ratio) + fuel*(SAF)*ratio

    if cost:
        price = fuel*(1-ratio)*PRICE_JA1 + fuel*ratio*PRICE_SAF + 0.5 * co2
        if co2 > 0:
            price += 0.5 * co2
        return round(price, 2)
    return round(co2, 2)

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

def safplot():
    ratios = np.linspace(0, 1, 101)
    
    data = []
    for r in ratios:
        data.append({"SAF Percentage": r * 100, "SAF Type": "HEFA", "CO2 Emissions": hefa(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Gas-to-Liquid", "CO2 Emissions": gas(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Alcohol-to-Jet", "CO2 Emissions": alc(r)})
        data.append({"SAF Percentage": r * 100, "SAF Type": "Synthetic", "CO2 Emissions": syn(r)})
    
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    
    plot = sns.lineplot(data=df, x="SAF Percentage", y=df["CO2 Emissions"]/10**6, hue="SAF Type", palette="viridis")
    plot.set_xlabel("SAF Percentage (%)")
    plot.set_ylabel("CO2 Emissions (10⁶ kg)")
    plot.set_title("CO2 emissions per SAF")
    plot.ticklabel_format(axis="y", style="plain")
    plt.grid(True, linestyle="--", alpha=0.7)
    
    return plt.gcf()

def costplot():
    ratios = np.linspace(0, 1, 101)
    
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

def saf_for_year(year, saf_coefficient):
    fuel = KPI["Fuel/y"].sum()
    ratio = (co2_for_year(year)/fuel - 3.84)/(saf_coefficient-3.84)
    return min(ratio, 1)

def saf_ratio_over_time_plot():
    years = range(2025, 2071)
    saf_types = {
        "HEFA": 1.3,
        "Gas-to-Liquid": -0.51,
        "Alcohol-to-Jet": -0.86,
        "Synthetic": 1.14
    }

    data = []
    for year in years:
        for saf_type, coef in saf_types.items():
            if abs(coef - 3.84) < 0.01:
                continue
            ratio = saf_for_year(year, coef)
            data.append({"Year": year, "SAF Type": saf_type, "Required Blend Ratio (%)": ratio * 100})

    df = pd.DataFrame(data)
    plt.figure(figsize=(12, 7))
    plot = sns.lineplot(data=df, x="Year", y="Required Blend Ratio (%)", hue="SAF Type", palette="viridis")
    plot.set_xlabel("Year")
    plot.set_ylabel("Required SAF Blend (%)")
    plot.set_title("Required SAF Blend to Reach ADL")
    sns.move_legend(obj=plot, loc="center left")
    plt.ylim(0, 100)
    plt.grid(True, linestyle="--", alpha=0.7)

    ax2 = plt.twinx()
    unique_years = sorted(df["Year"].unique())
    co2_values = [co2_for_year(year)/1e6 for year in unique_years]
    ax2.plot(unique_years, co2_values, color="red", linestyle="--", label="CO2 Target")
    ax2.set_ylabel("CO2 Emissions (10⁶ kg)")
    ax2.tick_params(axis="y")

    plt.legend()
    return plt.gcf()