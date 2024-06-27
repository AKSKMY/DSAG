import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Load the dataset
df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")

# Create a dictionary from the DataFrame
TSPnodes = dict(zip(df['Item'], zip(df['X'], df['Y'], df['Z'])))

# Create a list of item names
item_names = list(TSPnodes.keys())

# Extract coordinates for each item
coordinates = np.array(list(TSPnodes.values()))

# Calculate the distance matrix
distance_matrix = squareform(pdist(coordinates))

# Function to get the x-coordinate bounds for nodes in the same y and z coordinates
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
# Greedy Algorithm
def nearest_neighbor_tsp(distance_matrix, start, end):
    n = distance_matrix.shape[0]
    start_index = item_names.index(start)
    end_index = item_names.index(end)
    unvisited = list(range(n))
    unvisited.remove(start_index)
    path = [start_index]  # Start from the given start point
    current = start_index
    end_item_z = TSPnodes[end][2]
    end_item_y = TSPnodes[end][1]
    start_item_z = TSPnodes[start][2]
    
    while unvisited:
        currentCoordinates = coordinates[current]
        
        # If current Node is at stairs
        if "Stairs" in item_names[current]:
            stairs_indices = [i for i in unvisited if "Stairs" in item_names[i]]
            if stairs_indices:
                # Travel through stairs if it's not at the correct level
                if end_item_z != currentCoordinates[2]:
                    nearest = min(stairs_indices, key=lambda x: distance_matrix[current, x])
                # Else find the nearest node
                else:
                    nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
            else:
                nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
                
        # If Node is not at stairs
        else:
            min_x, max_x = get_x_bounds_for_yz(current, coordinates, item_names)
            nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
            
            # If starting items is on the same level as the end item
            if start_item_z == end_item_z:
                nearest_neighbors = sorted(unvisited, key=lambda x: distance_matrix[current, x])[:4]
                candidates = []
                
                for node in nearest_neighbors:
                    # Get nodes that is in the z axis
                    if coordinates[node][2] == currentCoordinates[2]:
                        # Get Nodes if its already in the correct shelf or if they're in the start or end of shelf
                        if coordinates[node][1] == currentCoordinates[1] or coordinates[current][0] in [min_x, max_x]:
                            dist_to_end = distance_matrix[node, end_index]
                            candidates.append((node, dist_to_end))
                
                if candidates:
                    # If start or end of shelf
                    if currentCoordinates[0] in [min_x, max_x]:
                        # If already in correct shelf
                        if end_item_y == currentCoordinates[1]:
                            MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]
                            if MovabaleNode:
                                nearest = min(MovabaleNode, key=lambda x: distance_matrix[current, x])
                        # Else move to correct shelf
                        else:
                            filtered_candidates = [c for c in candidates if coordinates[c[0]][0] == currentCoordinates[0]]
                            if filtered_candidates:
                                nearest = min(filtered_candidates, key=lambda x: x[1])[0]
                            else:
                                nearest = min(candidates, key=lambda x: x[1])[0]
                    else:
                        # Find candidates with min_x and max_x
                        min_x_candidates = [c for c in candidates if coordinates[c[0]][0] == min_x]
                        max_x_candidates = [c for c in candidates if coordinates[c[0]][0] == max_x]

                        if min_x_candidates and max_x_candidates:
                            # Calculate distances to min_x and max_x candidates
                            closest_min_x_candidate = min(min_x_candidates, key=lambda x: x[1])
                            closest_max_x_candidate = min(max_x_candidates, key=lambda x: x[1])

                            # Choose the closer candidate
                            if closest_min_x_candidate[1] < closest_max_x_candidate[1]:
                                nearest = closest_min_x_candidate[0]
                            else:
                                nearest = closest_max_x_candidate[0]
                        elif min_x_candidates:
                            nearest = min(min_x_candidates, key=lambda x: x[1])[0]
                        elif max_x_candidates:
                            nearest = min(max_x_candidates, key=lambda x: x[1])[0]
                        else:
                            nearest = min(candidates, key=lambda x: x[1])[0]
                else:
                    nearest = min(nearest_neighbors, key=lambda x: distance_matrix[current, x])
            
            # If they're on the right level
            elif end_item_z == currentCoordinates[2]:
                # If at correct shelf
                if end_item_y == currentCoordinates[1]:
                    MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]
                    if MovabaleNode:
                        nearest = min(MovabaleNode, key=lambda x: distance_matrix[current, x])
                # Try to move to correct shelf
                else:
                    if currentCoordinates[0] != min_x or currentCoordinates[0] != max_x:
                        nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
                    elif "Stairs" in item_names[nearest]:
                        pass
                    else:
                        unvisited = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] or "Stairs" in item_names[i]]
                        same_z_nodes_excluding_current_y = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] and coordinates[i][1] != currentCoordinates[1] and "Stairs" not in item_names[i]]
                        if currentCoordinates[1] != end_item_y:
                            if same_z_nodes_excluding_current_y:
                                nearest = min(same_z_nodes_excluding_current_y, key=lambda x: distance_matrix[current, x])
            
            # If the nearest node is the stairs, let it proceed on
            elif "Stairs" in item_names[nearest]:
                pass
        
        path.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        if current == end_index:
            break
    
    return path

# Specify start and end points
start_item = 'Bread'
end_item = ['Mop', 'Honey', 'Hair Gel']

def itemSort(start_item, end_item, TSPnodes):
    # List to store the result
    result_list = [start_item]

    # Remaining items to be added to the result list
    remaining_items = end_item.copy()

    while remaining_items:
        # Get the coordinates of the current last item in the result list
        current_item_coordinates = TSPnodes[result_list[-1]]
        current_z = current_item_coordinates[2]
        
        # Check for any remaining item with the same z-coordinate as the current item
        same_z_items = [item for item in remaining_items if TSPnodes[item][2] == current_z]
        
        if same_z_items:
            # If there is an item with the same z-coordinate, add it to the result list
            next_item = same_z_items[0]
        else:
            # If no items with the same z-coordinate, find the item with the closest z-coordinate
            next_item = min(remaining_items, key=lambda item: abs(TSPnodes[item][2] - current_z))
        
        result_list.append(next_item)
        remaining_items.remove(next_item)
    return result_list

shortest_path = itemSort(start_item, end_item, TSPnodes)

# Initialize item list to store the complete path
itemlist = []

# Generate the full path using Nearest Neighbor TSP for each segment
for i in range(len(end_item)):
    if i == 0:
        path_indices = nearest_neighbor_tsp(distance_matrix, shortest_path[i], shortest_path[i+1])       
        path = [item_names[j] for j in path_indices]
        for item in path:
            itemlist.append(item)
            print(f"{item}: {TSPnodes[item]}")
            # print(f"{item}")
    else:
        path_indices = nearest_neighbor_tsp(distance_matrix, shortest_path[i], shortest_path[i+1])  
        path1 = [item_names[j] for j in path_indices]
        for item in path1:
            itemlist.append(item)
            print(f"{item}: {TSPnodes[item]}")
            # print(f"{item}")

# Get the path using nearest neighbor algorithm
# path_indices = nearest_neighbor_tsp(distance_matrix, start_item, end_item)
# path = [item_names[i] for i in path_indices]

# # Output the path
# print(path)
# print("\nCoordinates for each item in the path:")
# for item in path:
#     print(f"{item}: {TSPnodes[item]}")