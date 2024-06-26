import pandas as pd
import numpy as np
#from abc_analysis import abc_analysis, abc_plot


# Load the datasets
file_path = r"Dataset\Retail_Transactions_Dataset.zip"
data = pd.read_csv(file_path)

file_path = r"Dataset\item_count.csv"
item = pd.read_csv(file_path)


# Get the number of total sales for each product
#def countItems():
    # Split by quotation marks and count the occurrences of each item
    # Will count , [ and ] symbols as well
    #itemCount = data['Product'].str.split('\'').explode().value_counts()
    #print(itemCount)

    # Write wordCounts to a CSV file
    #itemCount.to_csv('itemCount.csv')


def ABC():
    global item
    item['Total_Cost'] = item['Price'] * item['Count']
    # sort in descending 
    item = item.sort_values(by='Total_Cost', ascending = False)
    #calculate percentage
    item['Item_percent'] = (item['Total_Cost'] / item['Total_Cost'].sum()) * 100

    #sort into class A, B and C using 70-20-10
    total = 0
    indexA = -1
    indexB = -1

    for i in range(len(item['Item_percent'])):
        total += item["Item_percent"].iloc[i] 
        if total <= 70:
            indexA = i
        elif total <= 90:
            indexB = i

    # create new column A,B or C for items
    

    # Plot the ABC analysis
    #abc = abc_analysis(item['AddCost'], True)

    # idnex position of A, B, and C Segmentations
    #a_index = abc['Aind']
    #b_index = abc['Bind']
    #c_index = abc['Cind']

    # New Column indicating A, B, or C
    #cond_list = [item.index.isin(a_index),
                #item.index.isin(b_index),
                #item.index.isin(c_index)]

    #choice_list = ['A','B','C']

    #item['abc'] = np.select(cond_list, choice_list)
    #item.sort_values(by=['AddCost'], ascending=False)

    print(item.head(20))

ABC()