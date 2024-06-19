import pandas as pd
from stockpyl.eoq import economic_order_quantity


file_path = "Dataset\item_count.csv"
data = pd.read_csv(file_path)


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

EOQ()