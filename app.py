# Import necessary libraries for this dashboard
from shiny.express import input, render, ui     # For creating the interactive web UI elements
from faicons import icon_svg                    # For using icons in the UI
from pathlib import Path                        # For handling file paths in a cross-platform way
BASE_DIR = Path(__file__).parent



# Import all data and functions from data.py
from data import *                              # Imports data and functions needed for this dashboard from 'data.py'
import seaborn as sns                           # For creating statistical plots in the dashboard

# --- Define the user interface (UI) layout and elements ---

# Set the title of the web page to "EcoFly Dashboard" and allow it to fill the screen
ui.page_opts(title="EcoFly Dashboard", fillable=True)

# Start defining the content of the sidebar
with ui.sidebar(title="Options", open='closed'):
    # Create a slider named "year" for selecting a year from 2025 to 2070, starting at 2025
    ui.input_slider("year", 'Select Year', min=2025, max=2070, value=2025, sep='')
    ui.input_slider("saf", "Select SAF%", min=0, max=100, value=14, post='%')

with ui.nav_panel("Home"):

    with ui.layout_columns(col_widths=(8, 4),fill=False):

        with ui.layout_column_wrap(fill=False):
            with ui.card():
                ui.card_header("Baseline CO2e Distribution")
                @render.plot
                def piechart():
                    return plot_pie_chart()
                
        with ui.layout_column_wrap(fill=False):
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
            def fr():
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
        "Using 80% HEFA SAF by 2050 will reach EcoFly's goal of reducing CO2 Emmissions by half. "
        "The cost of Carbon Credits in 2050 is the reason why the price of higher SAF blends decrease. "
        "No Network or Aircraft changes have to be done to utilize this strategy."

    with ui.layout_columns(col_widths=(6,6), fill=False):
        with ui.card():
            ui.card_header("Strategy Comparison")

