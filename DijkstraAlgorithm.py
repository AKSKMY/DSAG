# import heapq

# def dijkstra(graph, start, end):
#     # Initialize distances with infinity
#     distances = {node: float('infinity') for node in graph}
#     # Distance to the start node is 0
#     distances[start] = 0
#     # Priority queue to hold (distance, node) tuples
#     priority_queue = [(0, start)]
#     # Dictionary to store the shortest path tree
#     predecessors = {node: None for node in graph}

#     while priority_queue:
#         # Get the node with the smallest distance
#         current_distance, current_node = heapq.heappop(priority_queue)

#         # If we reached the end node, we can reconstruct the path and return the result
#         if current_node == end:
#             path = []
#             while current_node is not None:
#                 path.append(current_node)
#                 current_node = predecessors[current_node]
#             path.reverse()
#             return distances[end], path

#         # If the distance is greater than the recorded smallest distance, skip it
#         if current_distance > distances[current_node]:
#             continue

#         # Iterate over neighbors
#         for neighbor, weight in graph[current_node].items():
#             distance = current_distance + weight

#             # Only consider this new path if it's better
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 predecessors[neighbor] = current_node
#                 heapq.heappush(priority_queue, (distance, neighbor))

#     # If we reach here, it means there is no path from start to end
#     return float('infinity'), []

# # Example graph
# graph = {
#     'A': {'B': 1, 'C': 4},
#     'B': {'A': 1, 'C': 2, 'D': 5},
#     'C': {'A': 4, 'B': 2, 'D': 1},
#     'D': {'B': 5, 'C': 1}
# }

# # Example usage
# start_node = 'A'
# end_node = 'D'
# distance, path = dijkstra(graph, start_node, end_node)
# print(f"Shortest distance from {start_node} to {end_node}: {distance}")
# print(f"Path: {' -> '.join(path)}")
import pandas as pd
import math
import pprint

# Load data from CSV file
df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")

# Calculate distance between two nodes
def calculate_distance(node1, node2):
    return math.sqrt((node1['X'] - node2['X'])**2 + (node1['Y'] - node2['Y'])**2 + (node1['Z'] - node2['Z'])**2)

# Create the graph
graph = {}

# Define min and max x coordinates excluding stairs nodes
non_stairs_df = df[df['Group'] != 'Stairs']
min_x = min(non_stairs_df['X'])
max_x = max(non_stairs_df['X'])
min_y = min(non_stairs_df['Y'])

# Process nodes to create graph edges based on requirements
for index, node in df.iterrows():
    node_id = node['Item']
    graph[node_id] = {}

    for index2, other_node in df.iterrows():
        other_node_id = other_node['Item']

        # Skip if it's the same node
        if node_id == other_node_id:
            continue

        # Do not add distance if nodes are from different z-axis
        if node['Z'] != other_node['Z']:
            continue

        # Nodes in the same z-axis with non-extreme x can only move within the same y axis
        if (node['X'] not in (min_x, max_x) and node['X'] == other_node['X'] and node['Y'] == other_node['Y']):
            distance = calculate_distance(node, other_node)
            graph[node_id][other_node_id] = distance

        # Nodes with smallest and largest x can move up or down the y axis
        if (node['X'] in (min_x, max_x)):
            if (node['X'] == other_node['X'] and abs(node['Y'] - other_node['Y']) == 2):
                distance = calculate_distance(node, other_node)
                graph[node_id][other_node_id] = distance

        # Nodes can move left, right, up, down
        if (abs(node['X'] - other_node['X']) == 2 and node['Y'] == other_node['Y']):
            distance = calculate_distance(node, other_node)
            graph[node_id][other_node_id] = distance

# Add stairs distances
stairs_nodes = df[df['Group'] == 'Stairs']
for index, stairs_node in stairs_nodes.iterrows():
    stairs_id = stairs_node['Item']
    graph[stairs_id] = {}

    # Calculate distance to other stairs nodes
    for index2, other_stairs in stairs_nodes.iterrows():
        if stairs_id != other_stairs['Item']:
            distance = calculate_distance(stairs_node, other_stairs)
            graph[stairs_id][other_stairs['Item']] = distance

    # Calculate distance to the closest non-stairs node and add to both directions
    min_distance = float('inf')
    closest_node_id = None
    for index2, node in df.iterrows():
        if node['Group'] != 'Stairs' and node['Z'] == stairs_node['Z']:
            distance = calculate_distance(stairs_node, node)
            if distance < min_distance:
                min_distance = distance
                closest_node_id = node['Item']
    
    if closest_node_id:
        graph[stairs_id][closest_node_id] = min_distance
        if closest_node_id in graph:
            graph[closest_node_id][stairs_id] = min_distance
        else:
            graph[closest_node_id] = {stairs_id: min_distance}

# Print the graph
pprint.pprint(graph)
