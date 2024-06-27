import heapq

def dijkstra(graph, start, end):
    # Initialize distances with infinity
    distances = {node: float('infinity') for node in graph}
    # Distance to the start node is 0
    distances[start] = 0
    # Priority queue to hold (distance, node) tuples
    priority_queue = [(0, start)]
    # Dictionary to store the shortest path tree
    predecessors = {node: None for node in graph}

    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we reached the end node, we can reconstruct the path and return the result
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = predecessors[current_node]
            path.reverse()
            return distances[end], path

        # If the distance is greater than the recorded smallest distance, skip it
        if current_distance > distances[current_node]:
            continue

        # Iterate over neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # If we reach here, it means there is no path from start to end
    return float('infinity'), []

# Example graph
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Example usage
start_node = 'A'
end_node = 'D'
distance, path = dijkstra(graph, start_node, end_node)
print(f"Shortest distance from {start_node} to {end_node}: {distance}")
print(f"Path: {' -> '.join(path)}")
