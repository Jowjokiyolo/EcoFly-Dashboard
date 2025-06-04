from shiny.express import input, render, ui
from faicons import icon_svg
from data import *
import seaborn as sns

# Make UI
ui.page_opts(title="EcoFly Dashboard", fillable=True)

with ui.sidebar():
    ui.input_slider("year", 'Select Year', min=2025, max=2070, value=2025, sep='')

with ui.layout_columns(fill=False, col_widths=(1, 11)):
    with ui.card():
        with ui.div(style="margin-top: 2em;"):
            icon_svg(
                name="plane",
                fill="url(#plane-gradient)",
                height="5em",
                style="solid"
            )
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

    with ui.card(fill=True):
        @render.data_frame
        def kpi():
            return KPI_DASH

with ui.layout_columns(fill=False, width=1/2):
    with ui.card():
        ui.card_header("Top 10 CO2 Emitting Flights")

        @render.plot
        def emissionplot():
            import matplotlib.pyplot as plt
            plot = sns.barplot(KPI_10, x="Airport", y=KPI_10["kgCO2e per year"]/10**6, palette='viridis')
            plot.set_xlabel("Airport")
            plot.set_ylabel(r"$1\cdot{}10^6$ kgCO2e per year")
            plot.ticklabel_format(axis="y", style='plain')
            plt.title("Annual CO2 Emissions by Airport")
            return plot.figure
    
    with ui.card(fill=True):
        ui.card_header("Further KPI's")
        @render.ui
        def year_display():
            return ui.div(
                {"style": "text-align: center; font-weight: bold; font-size: 24px; margin: 15px 0;"},
                f"{input.year()}"
            )
            
        with ui.value_box(showcase=icon_svg("plane-departure")):
            "kgCO2e/ASK (10^6 kg)"
            @render.text
            def co2_ask():
                return f"{co2_for_year(input.year())/10**6:.1f}"
            
        with ui.value_box(showcase=icon_svg("fire-flame-simple")):
            "CO2 Reduction Compared to 2025"
            @render.text
            def co2reduc():
                return f"{25}%"