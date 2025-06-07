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

with ui.nav_panel("Baseline"):

    # Create a column layout with one narrow column (1 unit) and one wide column (11 units)
    with ui.layout_columns(fill=False, col_widths=(2, 10)):
        # Start a card component (a boxed section) in the first column
        with ui.card():
            # Create a container with a top margin inside the card
            with ui.div(style="margin-top: 2em; text-align: center;"):
                # Display a plane icon, colored with a gradient defined below
                icon_svg(
                name="plane",
                fill="url(#plane-gradient)",
                height="5em",
                style="solid"
                )
                # Embed SVG code to define the 'plane-gradient' for the icon's color
                ui.HTML('''
                <svg width="0" height="0">
                <defs>
                <linearGradient id="plane-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#4caf50"/>
                    <stop offset="100%" stop-color="#2196f3"/>
                </linearGradient>
                </defs>
                </svg>
                ''')

        # Start a card component that fills the remaining space in the column layout
        with ui.card(fill=True):
            @render.data_frame # Indicates that the 'kpi' function will render a data frame
            def kpi():
                # Display the 'KPI_DASH' data as a table in this card (All values formatted with 2 decimals)
                return Dashboard_KPI.round(2)
            "CO2 emissions are in kton"

    # Create another column layout with a width of half the available space
    with ui.layout_columns(fill=False, width=1/2):
        # Start a card component for the top 10 CO2 emitting flights
        with ui.card():
            # Set the header for this card
            ui.card_header("Top 10 CO2 Emitting Flights")

            # Indicates that the 'emissionplot' function will render a plot
            @render.plot
            def emissionplot():
                import matplotlib.pyplot as plt # Import matplotlib for plot customization (specifically for title/labels)

                # Create a bar plot from 'KPI_10' data, showing Airport vs. scaled CO2 emissions
                plot = sns.barplot(KPI_10, x="Destination",
                                y=KPI_10["kgCO2e per year"]/10**6, 
                                hue="Destination",palette='viridis')
                plot.set_xlabel("Airport") # Set x-axis label for the plot
                plot.set_ylabel(r"CO2e per year ($10^6$ kg)")  # Set y-axis label for the plot
                plot.ticklabel_format(axis="y", style='plain') # Format the y-axis label to display as plain numbers
                plt.title("Baseline CO2 Emissions by Airport") # Set title of the plot
                return plot.figure # Return the generated plot figure for display
        
        # Start another card component that fills the remaining space in this column layout
        with ui.card(fill=True):
            # Set the header for this card
            ui.card_header("Further KPI's")
            with ui.layout_column_wrap(width=1/2, height="0.5em"):
            # Indicates that the 'year_display' function will render a UI element
                @render.ui
                def year_text():
                # Display the currently selected year from the slider input
                    return ui.div(
                        {"style": "text-align: center; font-size: 20px; margin: 0.5em 0;"},
                        ui.HTML(f"Year:") # Get the current year value from the slider and make it bold
                    )
                @render.ui
                def year_display():
                    return ui.div(
                        {"style": "text-align: center; font-size: 20px; margin: 0.5em 0;"},
                        ui.HTML(f"<strong>{input.year()}</strong>")
                    )


            # Create a value box displaying an icon for 'kton CO2 per year'    
            with ui.value_box(showcase=icon_svg("plane-departure")):
                # Set the text label for this value box
                "kton CO2 per year"
                # Decorator to indicate that the 'co2_ask' function will render text
                @render.text
                def co2_ask():
                    # Calculate and display the kton CO2 for the selected year, formatted
                    return f"{co2_for_year(input.year())/10**6:.1f}"
                
            # Create another value box displaying an icon for 'CO2 Reduction'
            with ui.value_box(showcase=icon_svg("fire-flame-simple")):
                # Set the text label for this value box
                "CO2 Reduction Compared to 2025"
                # Indicates that the 'co2reduc' function will render text
                @render.text
                def co2reduc():
                    # Display a hardcoded 25% CO2 reduction value
                    return f"{100-100*co2_for_year(input.year())/co2_for_year(2025):.1f}%"
                


with ui.nav_panel("SAF Utilization"):
    with ui.layout_column_wrap(fill = False, width=1/2):
        with ui.card():
            ui.card_header("CO2 Emissions vs SAF Percentage")
            
            @render.plot
            def local_safplot():
                return safplot()
        
        with ui.card():
            ui.card_header("Total Cost vs SAF Percentage")
            
            @render.plot
            def local_costplot():
                return costplot()
        
    with ui.layout_column_wrap(fill=False, width=1/2):
    
        with ui.card():
            ui.card_header("Required SAF Blend Over Time")
            
            @render.plot
            def saf_ratio_plot():
                return saf_ratio_over_time_plot()
            
        with ui.card():
            ui.card_header("SAF Feasibility")

            @render.data_frame
            def local_saf_feasability():
                return SAF_PLUS_MINUS
            with ui.value_box(showcase=icon_svg("dollar-sign")):
                "Total Cost for HEFA Blend (2050 Price)"
                @render.text
                def local_total_cost_hefa():
                    return f"${hefa(input.saf()/100, True):,.2f}"
                
                @render.text
                def local_blend():
                    return f"with {input.saf()}% HEFA Blend"



with ui.nav_panel("KPI's"):
    with ui.layout_column_wrap(fill=False):
        with ui.card():
            ui.card_header("Strategy KPI's")

            @render.data_frame
            def local_kpi_table():
                return KPI_SUST_FEASB

# End of the code
