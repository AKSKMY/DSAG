import math
from flask import Flask, render_template, render_template_string
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.io as pio
import TSPNearestNeighbor as TSP

app = Flask(__name__, template_folder="templates")

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Warehouse Management</title>
</head>
<body>
    <h1>Warehouse Management</h1>
    {% for key, plot in plots.items() %}
        <div>{{ plot | safe }}</div>
    {% endfor %}
    <h2>Route in Sequence: From {{ shortest_path | safe }}</h2>
    <h3>{{ array | safe }}</h3>
</body>
</html>
'''

# Route to display the plot
# @app.route('/')
# def index():
#     # Read the CSV file
#     df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")

#     # Separate DataFrame based on unique values in 'Z' column
#     separated_dfs = separate_df(df, 'Z')

#     # Create plots for each group
#     plots = {}
#     plot_titles = {2.0: 'Level 1', 7.0: 'Level 2', 12.0: 'Level 3'}  # Adjust according to actual Z values
#     for key, value in separated_dfs.items():
#         title = plot_titles.get(key, f'Group {key}')  # Default title if key is not in plot_titles
#         fig = px.scatter(value, x='X', y='Y', text='Item', title=title)
#         plots[key] = pio.to_html(fig, full_html=False)

#     return render_template_string(template, plots=plots, plot_titles=plot_titles)

# def separate_df(df, column_name):
#     unique_values = df[column_name].unique()
#     separated_dfs = {value: df[df[column_name] == value] for value in unique_values}
#     return separated_dfs

start_item = 'Cheese'
end_item = ['Shampoo', 'Dishware', 'Coffee']
shortest_path = TSP.itemSort(start_item, end_item, TSP.TSPnodes)
itemlist = []
for i in range(len(end_item)):
    if i == 0:
        path_indices = TSP.nearest_neighbor_tsp(TSP.distance_matrix, shortest_path[i], shortest_path[i+1])       
        path = [TSP.item_names[j] for j in path_indices]
        for item in path:
            itemlist.append(item)
    else:
        path_indices = TSP.nearest_neighbor_tsp(TSP.distance_matrix, shortest_path[i], shortest_path[i+1])  
        path1 = [TSP.item_names[j] for j in path_indices]
        for item in path1:
            itemlist.append(item)

# Route to display the plot
@app.route('/')
def index():
    # Read the CSV file
    df = pd.read_csv(r"Dataset/item_list_with_coordinates.csv")

    # Separate DataFrame based on unique values in 'Z' column
    separated_dfs = separate_df(df, 'Z')

    # Create plots for each group
    plots = {}
    plot_titles = {2.0: 'Level 1', 7.0: 'Level 2', 12.0: 'Level 3'}  # Adjust according to actual Z values
    for key, value in separated_dfs.items():
        title = plot_titles.get(key, f'Group {key}')  # Default title if key is not in plot_titles
        fig = go.Figure()

        # Add scatter plot for the items
        fig.add_trace(go.Scatter(x=value['X'], y=value['Y'], mode='markers+text', text=value['Item'], name='Items'))

        # Draw lines between the items in the specified order
        filtered_items = [item for i, item in enumerate(itemlist) if i == 0 or item != itemlist[i-1]]
        for i in range(len(filtered_items) - 1):
            item1 = filtered_items[i]
            item2 = filtered_items[i + 1]
            if item1 in value['Item'].values and item2 in value['Item'].values:
                x0, y0 = value[value['Item'] == item1][['X', 'Y']].values[0]
                x1, y1 = value[value['Item'] == item2][['X', 'Y']].values[0]
                fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(color='blue')))

        fig.update_layout(title=title)
        plots[key] = pio.to_html(fig, full_html=False)
    array = itemlist

    return render_template_string(template, plots=plots, array=array, shortest_path=shortest_path)

def separate_df(df, column_name):
    unique_values = df[column_name].unique()
    separated_dfs = {value: df[df[column_name] == value] for value in unique_values}
    return separated_dfs

if __name__ == '__main__':
    app.run(debug=False)
