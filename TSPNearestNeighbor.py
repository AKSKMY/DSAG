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
    start_item_z = TSPnodes[start][2]
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
            min_x, max_x = get_x_bounds_for_yz(current, coordinates, item_names)
            nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
            # If the nearest node is the stairs let it proceed on
            # If it isn't check whether we're at the correct level
            if start_item_z == end_item_z:
                nearest_neighbors = sorted(unvisited, key=lambda x: distance_matrix[current, x])[:4]
                candidates = []
                    
                for node in nearest_neighbors:
                    if coordinates[node][2] == currentCoordinates[2]:
                        if coordinates[node][1] == currentCoordinates[1] or coordinates[current][0] in [min_x, max_x]:
                            dist_to_end = distance_matrix[node, end_index]
                            candidates.append((node, dist_to_end))
                    
                if candidates:
                    if currentCoordinates[0] in [min_x, max_x]:
                        if end_item_y == currentCoordinates[1]:
                            MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]
                            # print(MovabaleNode, '1', item_names[43])
                            if MovabaleNode != []:     
                                nearest = min(MovabaleNode, key=lambda x: distance_matrix[current, x])
                        else:
                            filtered_candidates = [c for c in candidates if coordinates[c[0]][0] == currentCoordinates[0]]
                            if filtered_candidates:
                                nearest = min(filtered_candidates, key=lambda x: x[1])[0]
                            else:
                                nearest = min(candidates, key=lambda x: x[1])[0]
                    else:
                        nearest = min(candidates, key=lambda x: x[1])[0]
                else:
                    nearest = min(nearest_neighbors, key=lambda x: distance_matrix[current, x])
                    
            elif end_item_z == currentCoordinates[2]:
                # If it is check whether it is at the correct shelf
                if end_item_y == currentCoordinates[1]:
                    MovabaleNode = [i for i in unvisited if coordinates[i][1] == currentCoordinates[1] and coordinates[i][2] == currentCoordinates[2]]
                    # print(MovabaleNode, '1', item_names[43])
                    if MovabaleNode != []:     
                        nearest = min(MovabaleNode, key=lambda x: distance_matrix[current, x])
                else:
                    if(currentCoordinates[0] != min_x or currentCoordinates[0] != max_x):
                        nearest = nearest = min(unvisited, key=lambda x: distance_matrix[current, x])
                    elif "Stairs" in item_names[nearest]:
                        pass
                    else: 
                        unvisited = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] or "Stairs" in item_names[i]]
                        same_z_nodes_excluding_current_y = [i for i in unvisited if coordinates[i][2] == currentCoordinates[2] and coordinates[i][1] != currentCoordinates[1] and "Stairs" not in item_names[i]]
                        if currentCoordinates[1] != end_item_y: 
                            if same_z_nodes_excluding_current_y != []:
                                nearest = min(same_z_nodes_excluding_current_y, key=lambda x: distance_matrix[current, x])
            
            elif "Stairs" in item_names[nearest]:
                pass
                            
        
        # print(path)
        path.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        if current == end_index:
            break
    return path

# Specify start and end points
start_item = 'Shampoo'
end_item = ['Bread', 'Carrots', 'Honey']

def find_shortest_path(start_item, end_items, TSPnodes):
    # Retrieve the coordinates for the start item
    start_coord = TSPnodes[start_item]
    
    # Retrieve the coordinates for the end items
    end_coords = [TSPnodes[item] for item in end_items]
    
    # Combine start and end coordinates
    all_coords = [start_coord] + end_coords
    
    # Calculate the distance matrix
    distance_matrix = squareform(pdist(all_coords))
    
    # Initialize the path with the start item
    path = [start_item]
    
    # Track remaining items to visit
    remaining_items = end_items[:]
    
    # Start with the current index of the start item (0)
    current_index = 0
    
    while remaining_items:
        # Calculate distances from the current item to each remaining item
        distances = [(distance_matrix[current_index, i + 1], i) for i in range(len(remaining_items))]
        
        # Find the closest item
        closest_distance, closest_index = min(distances, key=lambda x: x[0])
        
        # Update the path with the closest item
        closest_item = remaining_items[closest_index]
        path.append(closest_item)
        
        # Update the current index to the index of the closest item
        current_index = end_items.index(closest_item) + 1
        
        # Remove the closest item from the remaining items
        remaining_items.pop(closest_index)
    # print(path)
    
    return path

shortest_path = find_shortest_path(start_item, end_item, TSPnodes)
itemlist = []
for i in range(len(end_item)):
    if i == 0:
        path_indices = nearest_neighbor_tsp(distance_matrix, shortest_path[i], shortest_path[i+1])       
        path = [item_names[j] for j in path_indices]
        for item in path:
            # print(f"{item}: {TSPnodes[item]}")
            # print(f"{item}")
            itemlist.append(item)
    else:
        path_indices = nearest_neighbor_tsp(distance_matrix, shortest_path[i], shortest_path[i+1])  
        path1 = [item_names[j] for j in path_indices]
        for item in path1:
            # print(f"{item}: {TSPnodes[item]}")
            # print(f"{item}")
            itemlist.append(item)


# print(shortest_path)

# Get the path using nearest neighbor algorithm
# path_indices = nearest_neighbor_tsp(distance_matrix, start_item, end_item)
# path = [item_names[i] for i in path_indices]

# # Output the path
# print(path)
# print("\nCoordinates for each item in the path:")
# for item in path:
#     print(f"{item}: {TSPnodes[item]}")