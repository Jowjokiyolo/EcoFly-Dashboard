## Dashboard Structure Overview

The EcoFly Dashboard is organized to promote clarity, maintainability, and separation of concerns:

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

### Rationale

- **Separation of Concerns:**  
    By keeping data processing and visualization logic in `data.py`, and UI logic in `app.py`, the codebase remains modular and easier to maintain.

- **Readability:**  
    Rendering plots and managing data in the backend avoids cluttering the UI code, reducing confusion and potential bugs.

- **Scalability:**  
    This structure allows for easier updates, testing, and future feature additions.

### Additional Notes

- If you need to add new plots or data sources, update `data.py` and import the results into `app.py`.
- For UI changes, modify `app.py` without altering the data logic.
- Refer to the project README for setup and deployment instructions.

