from flask import Flask, render_template_string
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px

app = Flask(__name__)

# Load the dataset
file_path = r"Dataset\item_list_with_coordinates.csv"
data = pd.read_csv(file_path)

# Ensure column names are consistent with your dataset
x_column_name = 'X'
y_column_name = 'Y'
z_column_name = 'Z'
item_column_name = 'Item'  # Assuming there's a column named 'Item' for item names/IDs

@app.route('/')
def index():
    # Extract coordinates for clustering
    coordinates = data[[x_column_name, y_column_name, z_column_name]]

    # Specify the number of clusters
    num_clusters = 3

    # Initialize and fit KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(coordinates)

    # Get cluster labels and add them to the dataframe
    data['cluster'] = kmeans.labels_

    # Create the plot using Plotly
    fig = px.scatter_3d(data, x=x_column_name, y=y_column_name, z=z_column_name, color='cluster',
                        hover_data=[item_column_name], title='3D K-means Clustering of Items')
    fig.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
    fig.update_layout(scene=dict(xaxis_title='X Coordinate',
                                 yaxis_title='Y Coordinate',
                                 zaxis_title='Z Coordinate'),
                      margin=dict(l=0, r=0, b=0, t=40))
    plot_html = fig.to_html(full_html=False)

    # Cluster analysis summary
    cluster_summary = data.groupby('cluster').agg(
        count=('Item', 'size'),
        avg_x=(x_column_name, 'mean'),
        avg_y=(y_column_name, 'mean'),
        avg_z=(z_column_name, 'mean')
    ).reset_index()

    summary_html = cluster_summary.to_html(classes='table table-striped', index=False)

     # HTML template
    template = """
    <!doctype html>
    <html>
    <head>
        <title>3D K-means Clustering Visualization</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            .table {
                width: 50%;
                margin: 20px auto;
                border-collapse: collapse;
            }
            .table, .table th, .table td {
                border: 1px solid black;
            }
            .table th, .table td {
                padding: 8px;
                text-align: left;
            }
            .table th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>3D K-means Clustering Visualization</h1>
        <div>{{ plot_html|safe }}</div>
        <h2>Cluster Analysis Summary</h2>
        <div>{{ summary_html|safe }}</div>
        <h2>Optimization Recommendations</h2>
        <p>Based on the clustering results, we recommend reorganizing the items within each cluster to reduce picking time. 
        Items frequently picked together should be placed closer to each other to minimize travel distance.</p>
    </body>
    </html>
    """

    return render_template_string(template, plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)
