import sys
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings
import itertools

# Ignore warnings
warnings.filterwarnings("ignore")

# Load the dataset (adjust the path accordingly)
df = pd.read_csv(r"path/to/combined_WPI_data_final.csv")

# Parse dates and set the index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Function to perform ARIMA forecasting
def perform_forecasting(commodity_name):
    # Filter data for the given commodity
    df_commodity = df[df['COMM_NAME'] == commodity_name]

    # Split the data into training and test sets
    train_size = int(len(df_commodity) * 0.8)
    train, test = df_commodity.iloc[:train_size], df_commodity.iloc[train_size:]

    # Define the p, d, and q parameters to take any value between 0 and 2
    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))

    best_rmse = float('inf')
    best_params = None
    for param in pdq:
        try:
            model = ARIMA(train['WPI'], order=param)
            model_fit = model.fit()
            forecast_test = model_fit.forecast(steps=len(test))
            rmse = np.sqrt(mean_squared_error(test['WPI'], forecast_test))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = param
        except:
            continue

    # Fit the best ARIMA model on the full dataset
    model = ARIMA(df_commodity['WPI'], order=best_params)
    model_fit = model.fit()
    forecast_steps = 12  # Number of periods to forecast (e.g., 12 months for the next year)
    forecast_next_year = model_fit.forecast(steps=forecast_steps)

    # Create a date range for the forecast period
    last_date = df_commodity.index[-1]
    forecast_dates = pd.date_range(last_date, periods=forecast_steps + 1, freq='M')[1:]

    # Print the forecasted values for the next year and return as CSV format
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted WPI': forecast_next_year})
    forecast_df.to_csv(sys.stdout, index=False, header=False)

# Entry point
if __name__ == '__main__':
    # Accept commodity name from command-line argument
    commodity_name = sys.argv[1]
    perform_forecasting(commodity_name)
