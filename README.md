# EcoFly Dashboard
To run the dashboard locally you first need to create a python enviroment with these packages:

- pandas
- matplotlib
- seaborn
- openpyxl
- numpy
- shiny
- shinylive
- sympy
- faicons


Then in the command line, run shiny with:   
`shiny run --port 39649 --reload --autoreload-port 46499 app.py`

The main data comes from the COL1 GROUP 1 Excel file, the data is copied from that into the Data.xlsx and Data/Data.csv for ease of use with pandas. sym.py is used to calculate a quadratic model for CO2 emissions over time.
