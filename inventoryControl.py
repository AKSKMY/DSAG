import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

file_main = "Dataset\Retail_Transactions_Dataset.csv"
data = pd.read_csv(file_main)

file_count = "Dataset\item_count.csv"
dataSales = pd.read_csv(file_count)

file_stock = "Dataset\item_stock.csv"
dataStock = pd.read_csv(file_stock)

# Get the number of total sales for each product
def countItems():
    # Split by quotation marks and count the occurrences of each item
    # Will count , [ and ] symbols as well
    itemCount = data['Product'].str.split('\'').explode().value_counts()
    itemCount = itemCount.iloc[3:]
    print(itemCount)

    return itemCount
    # Write wordCounts to a CSV file
    # itemCount.to_csv('itemCount1.csv')

# Generate random numbers as stock for each item
def stockItems():
    file_path = "Dataset\item_count.csv"
    dataStock = pd.read_csv(file_path)

    # Let's say we want the random number to be between 1 and 100
    dataStock['Stock'] = np.random.randint(1, 750 + 1, size=len(dataStock))
    
    # Write the updated DataFrame to a new CSV file
    dataStock.to_csv('item_stock.csv', index=False)


def splitDate():
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Extract the month and year from the 'Date' column
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month


def historicSales(data, product):
    # Filter the data for the specified product
    data = data[data['Product'].str.contains(product)]

    # Group by 'Year' and 'Month', and sum the counts for the same month-year
    itemSales = data.groupby(['Year', 'Month']).size().reset_index(name='Sales')

    # print("Historic Sales for: " + product)
    
    return itemSales


def linearRegression(data):
    # Initialize a dataframe to store the predictions and evaluation metrics
    prediction_df = pd.DataFrame()

    # Iterate over each unique product
    for product in dataSales['Product'].unique():
        # Get historic sales data for the product
        product_data = historicSales(data, product)
        
        # Define features and target
        x = product_data[['Month', 'Year']]
        y = product_data['Sales']
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        
        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Compare actual vs predicted values
        # results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
        # results.head()

        # Calculate evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Plot actual vs predicted sales
        # plt.figure(figsize=(10, 6))
        # plt.plot(results['Actual'].values, label='Actual Sales', marker='o')
        # plt.plot(results['Predicted'].values, label='Predicted Sales', marker='x')
        # plt.title('Actual vs Predicted Sales')
        # plt.xlabel('Sample Index')
        # plt.ylabel('Sales')
        # plt.legend()
        # plt.show()

        # Predict sales for the next month
        latest_year = product_data['Year'].iloc[-1]
        latest_month = product_data['Month'].iloc[-1]
        if latest_month == 12:
            next_month = 1
            next_year = latest_year + 1
        else:
            next_month = latest_month + 1
            next_year = latest_year
        next_month_data = pd.DataFrame({'Month': [next_month], 'Year': [next_year]})
        next_month_prediction = model.predict(next_month_data)
        
        # Append the results to the DataFrame
        # Create a new_row with the product, metrics, and predictions
        new_row = {
            'Product': product,
            # 'MAE': mae,
            # 'RMSE': rmse,
            'Prediction': round(next_month_prediction[0]),
            'NextYear': next_year,
            'NextMonth': next_month
        }

        # Convert new_row to a DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Adding new_row_df to prediction_df
        prediction_df = pd.concat([prediction_df, new_row_df], ignore_index=True, axis=0)

        # print(f"Predicted sales for {next_year}-{next_month:02d}: {round(next_month_prediction[0])}")
    
    # Return the predictions and metrics for all products
    return prediction_df


# Will need demand forecast and current inventory data. Meant to be automated
# Just-in-Time (JIT) inventory management
def JIT(data, demand_forecast):
    # Merge inventory and forecast data
    merged_data = pd.merge(data, demand_forecast, on='Product')

    # Calculate the difference between current inventory and forecasted demand
    # If the difference is negative, order the absolute value of the difference
    # If the difference is positive or zero, order nothing
    merged_data['Order'] = (merged_data['Stock'] - merged_data['Prediction']).apply(lambda x: abs(x) if x < 0 else 0)

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
            'Demand Rate': demand_rate,
            'EOQ': round(EOQ),
            'TotalOrderCost': round(total_cost, 2)
        }

        # Convert new_row to a DataFrame
        new_row_df = pd.DataFrame([new_row])

        # Adding new_row_df to prediction_df
        EOQ_df = pd.concat([EOQ_df, new_row_df], ignore_index=True, axis=0)

    return EOQ_df


def graph():
    # Constants
    D = 1000  # Demand rate (units per year)
    S = 100   # Setup or order cost ($ per order)
    H = 2.5   # Holding cost ($ per unit per year)

    # Function to calculate total cost
    def total_cost(Q, D, S, H):
        ordering_cost = D / Q * S
        carrying_cost = Q / 2 * H
        return ordering_cost + carrying_cost

    # Generate a range of order quantities
    Q_values = np.arange(1, 1001, 10)  # From 1 to 1000 in steps of 10

    # Calculate total cost for each Q
    TC_values = [total_cost(Q, D, S, H) for Q in Q_values]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(Q_values, TC_values, marker='o', linestyle='-', color='b')
    plt.title('Total Cost vs. Order Quantity')
    plt.xlabel('Order Quantity (Q)')
    plt.ylabel('Total Cost')
    plt.grid(True)
    plt.show()

splitDate()
# print(historicSales(data, "Toothpaste"))
print(JIT(dataStock, linearRegression(data)))

# print(EOQ())
