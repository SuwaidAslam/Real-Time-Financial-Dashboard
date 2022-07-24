# Real Time Financial Dashboard
A Live Financial Dashboard, developed to show financial data live and we can also view data from the past. This dashboard is based on two python scripts, one script gets the data from the API and saves it into Mysql database, and the other script has all the code for the dashboard. Dashboard script gets the data from Mysql database which is inserted every 5 seconds in the database, and displays that real time financial information onto the dashboard, using Line charts and Tree Maps.

Tree Map charts sizes are not fixed, the height of the Tree Maps as the data for Tree Maps changes.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![pythonbadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# Demo

https://user-images.githubusercontent.com/45914161/180661299-e03f9679-c404-429e-b826-b9617adcf812.mp4


## Technology Stack 

1. Python 
2. Plotly Dash 
3. Pandas
4. Plotly
5. Mysql

# How to Run

To see the project working, you need to have Alpaca Finance Market API keys. If you have those, then you are good to go with the following steps :)

- Clone the repository
- Setup Virtual environment
```
$ python3 -m venv env
```
- Activate the virtual environment
```
$ source env/Source/activate
```
- Install dependencies using
```
$ pip install -r requirements.txt
```
- Run Streamlit
```
$ streamlit run app.py
```

## Contact

For any feedback or queries, please reach out to me at [suwaidaslam@gmail.com](suwaidaslam@gmail.com).
