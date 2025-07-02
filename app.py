# Import necessary libraries for this dashboard
from shiny.express import input, render, ui     # For creating the interactive web UI elements
from pathlib import Path                        # For handling file paths in a cross-platform way
BASE_DIR = Path(__file__).parent



# SHINY FRAMEWORK NOTES:

# Dashboard built with Shiny for Python framework.
# The Shiny package consists of three main classes:
# - ui:       defines layout (cards, columns, navigation)
# - render:   creates reactive outputs (plots, data frames)
# - input:    handles user interactions (sliders, dropdowns)



# Import all data and functions from data.py
from data import *

# Set the title of the web page to "EcoFly Dashboard" and allow it to fill the screen
ui.page_opts(title="EcoFly Dashboard", fillable=True)

# Create a bar at the top with the title and a "Home" page.
with ui.nav_panel("Home"):

    # Make a dedicated row for the baseline
    with ui.layout_columns(col_widths=(8, 4),fill=False):

        # Make a card with a header and a plot
        with ui.card():
            ui.card_header("Baseline CO2e Distribution")
            # Makes the the piechart plot
            @render.plot
            def piechart():
                # The plot for the pie chart is located inside the data.py file
                return plot_pie_chart()
                
        with ui.card():
            ui.card_header("Baseline Values")
            @render.data_frame
            def table1():
                return baseline_kpi_table
            "EcoFly has established a baseline annual CO2e emissions level of 675.84 kilotons. "
            "The current fleet consists of Airbus A320ceo and Boeing 777-200ER aircraft. "
            "At present, EcoFly does not utilize Sustainable Aviation Fuel (SAF). "
            "The operational network has a total of 10,628 flights annually."
        
    with ui.layout_columns(col_widths=(6, 6), fill=False):
        with ui.card():
            ui.card_header("Strategy: Fleet Renewal")
            @render.plot
            def figure0():
                return fleet_renewal()
            

        with ui.card():
            ui.card_header("Fleet Renewal Info")
            "Fleet renewal decreases fuel usage by 20% using the A320neo and A350. "
            "The lower fuel consumption leads to lower emissions. "
            "These aircraft also have a higher payload capacity, increasing the seats per year by 295544. "
            "This strategy does not meet the 2050 Goal."

    with ui.layout_columns(col_widths=(6,6), fill=False):

        with ui.layout_column_wrap():
            with ui.card():
                ui.card_header("Strategy: SAF")
                @render.plot
                def safplot():
                    return saf_ratio_over_time_plot()
        
        with ui.layout_column_wrap(fill=False):
            with ui.card():
                ui.card_header("SAF Cost in 2050")
                @render.plot
                def figure1():
                    return costplot()
                
    with ui.card(fill=False):
        "Using 80% HEFA SAF will reach EcoFly's goal of reducing CO2 Emmissions by half. "
        "The cost of Carbon Credits and Jet-A1 in 2050 is the reason why the price of higher SAF blends decrease. "
        "For that reason, EcoFly will utilize a 100% HEFA SAF blend per 2050"
        "No Network or Aircraft changes have to be done to utilize this strategy."

    with ui.layout_columns(col_widths=(5,7), fill=False):
        with ui.card():
            ui.card_header("Strategy Comparison")
            @render.data_frame
            def table2():
                return KPI_SUST_FEASB
            
        with ui.card():
            @render.plot
            def figure2():
                return strategy_costs()
            
            "The cost of the A320neo and A350 are considered including 14% HEFA saf as this is mandatory by 2030. "
            "For Carbon Conversion, the impacts of carring tons Lithium Nitrate significantly reduce the"
            "available payload that can be carried and thus reduces the revenue. The cost is also high as the "
            "material is expensive and entire propulsion systems need to be modified for the conversion to take place."

