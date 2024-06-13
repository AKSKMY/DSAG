import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")
# Create a dictionary from the DataFrame
TSPnodes = dict(zip(df['Item'], zip(df['X'], df['Y'], df['Z'])))

# Create a list of item names
item_names = list(TSPnodes.keys())

# Extract coordinates for each item
coordinates = np.array(list(TSPnodes.values()))

# Calculate the distance matrix
distance_matrix = squareform(pdist(coordinates))

def get_x_bounds_for_yz(current, coordinates, item_names):
    current_y = coordinates[current][1]
    current_z = coordinates[current][2]
    nodes_in_same_yz = [i for i in range(len(coordinates)) 
                        if coordinates[i][1] == current_y and coordinates[i][2] == current_z and "Stairs" not in item_names[i]]
    
    if not nodes_in_same_yz:
        return None, None  # or some default values or handling

    x_values = [coordinates[i][0] for i in nodes_in_same_yz]
    return min(x_values), max(x_values)

# Nearest Neighbor TSP algorithm with specified start and end points
def nearest_neighbor_tsp(distance_matrix, start, end):
    n = distance_matrix.shape[0]
    start_index = item_names.index(start)
    end_index = item_names.index(end)
    unvisited = list(range(n))
    unvisited.remove(start_index)
    # unvisited.remove(end_index)
    path = [start_index]  # Start from the given start point
    current = start_index
    end_item_z = TSPnodes[end][2]
    end_item_y = TSPnodes[end][1]
    end_item_x = TSPnodes[end][0]
    while unvisited:
        currentCoordinates = coordinates[current]
        # If current Node is at stairs
        if "Stairs" in item_names[current]:
            stairs_indices = [i for i in unvisited if "Stairs" in item_names[i]]
            if stairs_indices:
                # Travel through stairs if its not at the correct level
                if end_item_z != currentCoordinates[2]:
                    nearest = min(stairs_indices, key=lambda x: distance_matrix[current, x])
                # Else find the nearest node
                else:
                    nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
            else:
                nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
        # If Node not at stairs
        else:
            nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
            # If the nearest node is the stairs let it proceed on
            if "Stairs" in item_names[nearest]:
                print("Proceed")
            # If it isn't check whether we're at the correct level
            elif end_item_z == currentCoordinates[2]:
                # If it is check whether it is at the correct shelf
                if end_item_y == currentCoordinates[1]:
                    MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]
                    print(MovabaleNode, '1', item_names[43])
                    if MovabaleNode != []:     
                        nearest = min(MovabaleNode, key=lambda x: distance_matrix[current, x])
                # If it isn't we move to the correct shelf 
                else:
                    min_x, max_x = get_x_bounds_for_yz(current, coordinates, item_names)
                    unvisited = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] or "Stairs" in item_names[i]]
                    same_z_nodes_excluding_current_y = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] and coordinates[i][1] != currentCoordinates[1] and "Stairs" not in item_names[i]]
                    MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]   
                    if currentCoordinates[1] != end_item_y: 
                        if same_z_nodes_excluding_current_y != []:
                            nearest = min(same_z_nodes_excluding_current_y, key=lambda x: distance_matrix[current, x])
                        
                            
        
        print(path)
        path.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        if current == end_index:
            break
    return path

# Specify start and end points
start_item = 'Pickles'
end_item = 'Coffee'

# Get the path using nearest neighbor algorithm
path_indices = nearest_neighbor_tsp(distance_matrix, start_item, end_item)
path = [item_names[i] for i in path_indices]

# Output the path
print(path)
print("\nCoordinates for each item in the path:")
for item in path:
    print(f"{item}: {TSPnodes[item]}")