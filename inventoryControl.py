import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


file_path = "Dataset\item_count.csv"
dataSales = pd.read_csv(file_path)

def splitDate():
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract the month and year from the 'Date' column
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month


# Economic Order Quantity (EOQ) calculation
def EOQ():
    eoqValues = []
    costValues = []
    for index, row in data.iterrows():
        price = row['Price']
        count = row['Count']
        
        Q, cost = economic_order_quantity(fixed_cost=price, holding_cost=(price * 0.1), demand_rate=count)
        eoqValues.append(Q)
        costValues.append(cost)

    data['EOQ'] = eoqValues
    data['Cost'] = costValues
    print(data.head(20))

# Just-in-Time (JIT) inventory management
def JIT(data, demand_forecast):
    # Merge inventory and forecast data
    merged_data = pd.merge(data, demand_forecast, on='Product')

    # Calculate the difference between current inventory and forecasted demand
    merged_data['Difference'] = merged_data['Inventory'] - merged_data['Forecast']

    # If the difference is negative, order the absolute value of the difference
    # If the difference is positive or zero, order nothing
    merged_data['Order'] = merged_data['Difference'].apply(lambda x: abs(x) if x < 0 else 0)

    return merged_data


# Economic Order Quantity (EOQ) calculation
# Find out the optimal order quantity that minimizes the total inventory costs
def EOQ():
    # Initialize a dataframe to store the EOQ values
    EOQ_df = pd.DataFrame()

    # Iterate over each unique product
    for product in dataSales['Product'].unique():
        product_data = historicSales(data, product)

        demand_rate = product_data[-12:]['Sales'].sum()
        fixed_cost = dataSales[dataSales['Product'] == product]['Price'].values[0]
        holding_cost = fixed_cost * 0.1

        # Holding cose is 10% of the price for now. Change?
        EOQ = math.sqrt((2 * demand_rate * fixed_cost) / holding_cost)
        total_cost = (demand_rate * fixed_cost / EOQ) + (EOQ / 2 * holding_cost)

        # Append the results to the DataFrame
        # Create a new_row with the product and EOQ values
        new_row = {
            'Product': product,
            'EOQ': round(EOQ),
            'TotalOrderCost': round(total_cost, 2)
        }

        # Convert new_row to a DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Adding new_row_df to prediction_df
        EOQ_df = pd.concat([EOQ_df, new_row_df], ignore_index=True, axis=0)

    return EOQ_df


splitDate()
# print(historicSales(data, "Jam"))
# print(linearRegression(data))
# JIT(data, linearRegression(data))

print(EOQ())
