## Dashboard Structure Overview

The EcoFly Dashboard is organized into two files

- **`data.py`**  
    Handles all data processing, including:
    - Loading and cleaning datasets
    - Generating plots and figures
    - Creating dataframes and computed variables  
    This module prepares all data and visualizations required by the front-end.

- **`app.py`**  
    Manages the front-end using [Shiny for Python](https://shiny.posit.co/py/), including:
    - Defining the user interface layout
    - Integrating plots and tables from `data.py`
    - Handling user interactions and callbacks
