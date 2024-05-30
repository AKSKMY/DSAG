import math
from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__, template_folder="templates")


df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")
# Create a dictionary from the Cleaned and Processed sDataFrame
nodes = dict(zip(df['Item'], zip(df['X'], df['Y'])))
print(nodes)
    
# # Define node positions
# nodes = {
#     'A': (0, 0),
#     'B': (5, 0),
#     'C': (-3, 0),
#     'D': (0, -4),
#     'E': (8, 0),
#     'F': (5, -4),
#     'G': (-3, -4)
# }

# def euclidean_distance(node1, node2):
    
#     # Find the minimum and maximum x-coordinates among all nodes
#     min_x = min(node[0] for node in nodes.values())
#     max_x = max(node[0] for node in nodes.values())

#     # Find all nodes with the minimum and maximum x-coordinates
#     most_left_nodes = [node for node, (x, _) in nodes.items() if x == min_x]
#     most_right_nodes = [node for node, (x, _) in nodes.items() if x == max_x]
    
#     x1, y1 = nodes[node1]
#     x2, y2 = nodes[node2]
    
#     # Check if node1 or node2 is an extreme node
#     if node1 in most_left_nodes or node1 in most_right_nodes or node2 in most_left_nodes or node2 in most_right_nodes:
#         # Check if the nodes are directly above or below each other and the difference in their x-coordinates is not zero
#         print("1"+node1)
#         print("2"+node2)
#         if abs(x1 - x2) == 0:
#             distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             return distance if distance.is_integer() else None
#         elif abs(y1 - y2) == 0:
#             distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             return distance if distance.is_integer() else None
#     else:
#         if abs(y1 - y2) == 0:
#             distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#             return distance if distance.is_integer() else None
    
#     return None  # Return None if conditions are not met


# Initialize the graph
# graph = {}

# # Calculate distances and populate the graph
# for node1 in nodes:
#     graph[node1] = {}
#     for node2 in nodes:
#         if node1 != node2:  # Exclude self-connections
#             distance = euclidean_distance(node1, node2)
#             if distance is not None:
#                 graph[node1][node2] = int(distance)

# print(graph)

# def create_plot():
    # fig = go.Figure()

    # # Add nodes as markers
    # for node, (x, y) in nodes.items():
    #     fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=10), name=node, text=node))
    
    # # Add lines connecting nodes A to B to F
    # fig.add_trace(go.Scatter(x=[nodes['A'][0], nodes['B'][0], nodes['F'][0], None], 
    #                           y=[nodes['A'][1], nodes['B'][1], nodes['F'][1], None], 
    #                           mode='lines', 
    #                           name='Pathing'))

    # fig.update_layout(title='Node Plot', xaxis=dict(title='X', visible=False), yaxis=dict(title='Y', visible=False), showlegend=True)
    
    # return fig

# Route to display the plot
@app.route('/')
def index():
    # fig = create_plot()
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=False)
