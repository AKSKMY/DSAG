import pandas as pd


def convert_to_unique_item():
    df = pd.read_csv(r"Dataset\Retail_Transactions_Dataset.csv")
    items_column = df['Product']
    all_items = []

    # Loop through each row in the items column
    for items in items_column:
        # Split the items by comma and strip any extra whitespace replace [ ] and ' ' 
        individual_items = [item.replace("[", "").replace("]", "").replace("'", "").strip() for item in items.split(',')]
        # Add on into the all items list with all the individual items
        all_items.extend(individual_items)

    # Remove duplicates
    unique_items = list(set(all_items))

    # Convert to pd
    items_df = pd.DataFrame(unique_items, columns=['Item'])

    # Write to new CSV file
    items_df.to_csv('Dataset\Item_List.csv', index=False)
    
def add_item_location():
    df = pd.read_csv(r"Dataset\Item_List.csv")
    
    # Initialize the starting coordinates of the first time
    start_x, start_y = 3, 3
    aisles = 10
    items_per_aisle = len(df) // aisles + (len(df) % aisles > 0)

    # Function to assign coordinates 
    def assign_coordinates(index):
        aisle = index // items_per_aisle
        position_in_aisle = index % items_per_aisle
        x = start_x + aisle
        y = start_y + position_in_aisle
        return (x, y)

    # Assign coordinates to each item
    df['X'], df['Y'] = zip(*[assign_coordinates(i) for i in range(len(df))])

    # Write the updated DataFrame to a new CSV file
    df.to_csv('Dataset\item_list_with_coordinates.csv', index=False)
    
def convert_to_nodes():
    df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")
    # Create a dictionary from the DataFrame
    nodes = dict(zip(df['Item'], zip(df['X'], df['Y'])))
    print(nodes)

convert_to_nodes()