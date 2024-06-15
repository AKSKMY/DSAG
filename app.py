import math
from flask import Flask, render_template, render_template_string
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__, template_folder="templates")

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Warehouse Management</title>
</head>
<body>
    <h1>Plotly Graphs</h1>
    {% for key, plot in plots.items() %}
        <div>{{ plot | safe }}</div>
    {% endfor %}
</body>
</html>
'''

# Route to display the plot
@app.route('/')
def index():
    # Read the CSV file
    df = pd.read_csv(r"Dataset\item_list_with_coordinates.csv")

    # Separate DataFrame based on unique values in 'Z' column
    separated_dfs = separate_df(df, 'Z')

    # Create plots for each group
    plots = {}
    plot_titles = {2.0: 'Level 1', 7.0: 'Level 2', 12.0: 'Level 3'}  # Adjust according to actual Z values
    for key, value in separated_dfs.items():
        title = plot_titles.get(key, f'Group {key}')  # Default title if key is not in plot_titles
        fig = px.scatter(value, x='X', y='Y', text='Item', title=title)
        plots[key] = pio.to_html(fig, full_html=False)

    return render_template_string(template, plots=plots, plot_titles=plot_titles)

def separate_df(df, column_name):
    unique_values = df[column_name].unique()
    separated_dfs = {value: df[df[column_name] == value] for value in unique_values}
    return separated_dfs

if __name__ == '__main__':
    app.run(debug=False)
