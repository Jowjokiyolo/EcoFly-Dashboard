import pandas as pd
import matplotlib.pyplot as plt

KPI = pd.read_csv(r"Data/Data.csv")
KPI_DASH = pd.read_excel("Data.xlsx", sheet_name=2)

# KPI_LH = KPI.groupby("TYPE")
# KPI_SH = KPI.groupby("TYPE")

KPI_10 = KPI.sort_values(by=['kgCO2e per year'], ascending=False).head(10)

CO2_ASK = KPI["kgCO2e per year"].sum()/KPI["ASK/year"].sum()

def co2_for_year(year: int) -> float:
    return ((-621765841/9000) * year**2 + (177837343907630/660893) * year - 1043944847030/4)
