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
    
def groupingItems():
    # Define the groups
    groups = {
        'Fresh Food':['Soda', 'Pickles', 'Salmon', 'Potatoes', 'Cereal', 'Chips', 'Water', 'Ketchup', 'Cheese', 'Ice Cream', 'Bread', 'Butter', 'Rice', 'Eggs', 'Yogurt', 'Banana', 'Beef', 'Chicken', 'Shrimp', 'Tuna', 'Milk', 'Apple', 'Orange', 'Tomatoes', 'Carrots', 'Onions', 'Spinach'],
        'Home Care': ['Cleaning Spray', 'Shaving Cream', 'Insect Repellent', 'Hair Gel', 'Bath Towels','Dish Soap', 'Sponges', 'Toilet Paper', 'Laundry Detergent', 'Ironing Board', 'Feminine Hygiene Products', 'Razors', 'Garden Hose', 'Hand Sanitizer', 'Toothbrush', 'Shower Gel', 'Soap', 'Shampoo', 'Baby Wipes', 'Dustpan', 'Deodorant', 'Vacuum Cleaner', 'Broom', 'Mop', 'Trash Bags', 'Trash Cans', 'Diapers'],
        'Pantry and Household Supplies': ['Plant Fertilizer', 'Lawn Mower', 'Paper Towels', 'Cleaning Rags', 'Tea', 'Coffee', 'Honey', 'Peanut Butter', 'Olive Oil', 'Pancake Mix', 'Tissues', 'Pasta', 'Cereal Bars', 'Vinegar', 'Canned Soup', 'Light Bulbs', 'Power Strips', 'Extension Cords', 'Dishware', 'Toothpaste', 'Air Freshener', 'Jam', 'Syrup', 'Mayonnaise', 'Mustard', 'BBQ Sauce', 'Iron']
    }

    # Load the CSV file
    df = pd.read_csv('Dataset\item_list_with_categories.csv')

    # Add the new column
    df['Group'] = df['Item'].apply(lambda x: next((group for group, items in groups.items() if x in items), None))

    # Save the updated CSV file
    df.to_csv('Dataset\items_updated.csv', index=False)
    
def add_item_location():
    df = pd.read_csv(r"Dataset\items_updated.csv")
    
    # Add the missing coordinates for each z-level
    missing_items = [
        {'Item': 'Missing Item 1', 'Group': 'Fresh Food', 'X': 15, 'Y': 10, 'Z': 2},
        {'Item': 'Missing Item 2', 'Group': 'Home Care', 'X': 15, 'Y': 10, 'Z': 7},
        {'Item': 'Missing Item 3', 'Group': 'Pantry and Household Supplies', 'X': 15, 'Y': 10, 'Z': 12}
    ]
    
    # Convert the missing items list to DataFrame and append to existing DataFrame
    missing_df = pd.DataFrame(missing_items)
    df = pd.concat([df, missing_df], ignore_index=True)

    # Rearrange the dataset by group
    df = df.sort_values(by='Group').reset_index(drop=True)
    
    # Initialize the starting coordinates of the first item
    start_x, start_y = 3, 4
    items_per_aisle = 4
    current_group = None
    group_index = 0

    # Function to assign coordinates 
    def assign_coordinates(index, group):
        nonlocal start_x
        nonlocal current_group
        nonlocal group_index
        if group != current_group:
            start_x = 3
            current_group = group
            group_index = 0
        aisle = group_index // items_per_aisle
        position_in_aisle = group_index % items_per_aisle
        x = start_x + (aisle * 2)
        y = start_y + (position_in_aisle * 2)
        z = {'Fresh Food': 2, 'Home Care': 7, 'Pantry and Household Supplies': 12}[group]
        group_index += 1
        return (x, y, z)

    # Assign coordinates to each item
    for i in range(len(df)):
        group = df.loc[i, 'Group']
        x, y, z = assign_coordinates(i, group)
        df.loc[i, 'X'] = x
        df.loc[i, 'Y'] = y
        df.loc[i, 'Z'] = z

    stairs1 = pd.DataFrame({'Item': ['Stairs 1'], 'Group': ['Stairs'], 'X': [2], 'Y': [3], 'Z': [2]})
    stairs2 = pd.DataFrame({'Item': ['Stairs 2'], 'Group': ['Stairs'], 'X': [2], 'Y': [3], 'Z': [7]})
    stairs3 = pd.DataFrame({'Item': ['Stairs 3'], 'Group': ['Stairs'], 'X': [2], 'Y': [3], 'Z': [12]})

    df = pd.concat([df, stairs1, stairs2, stairs3], ignore_index=True)
    
    # Write the updated DataFrame to a new CSV file
    df.to_csv('Dataset\item_list_with_coordinates.csv', index=False)
    
def convert_to_nodes():
    df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")
    # Create a dictionary from the DataFrame
    df = dict(zip(df['Item'], zip(df['X'], df['Y'], df['Z'])))

# convert_to_nodes()
add_item_location()
