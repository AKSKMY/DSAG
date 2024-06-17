from flask import Flask, render_template_string
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io
import base64

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

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data[x_column_name], data[y_column_name], data[z_column_name], c=data['cluster'], cmap='viridis')
    
    # Add item names/IDs as labels with a small offset
    for i in range(data.shape[0]):
        ax.text(data[x_column_name][i] + 0.1, data[y_column_name][i] + 0.1, data[z_column_name][i] + 0.1, 
                data[item_column_name][i], size=8, zorder=1, color='k')
    
    ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], s=300, c='red', marker='x')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.set_title('3D K-means Clustering of Items')

    # Convert plot to PNG image
    png_image = io.BytesIO()
    plt.savefig(png_image, format='png')
    png_image.seek(0)
    png_image_b64_string = "data:image/png;base64," + base64.b64encode(png_image.read()).decode()

    # HTML template
    template = """
    <!doctype html>
    <html>
    <head>
        <title>3D K-means Clustering Visualization</title>
    </head>
    <body>
        <h1>3D K-means Clustering Visualization</h1>
        <img src="{{image}}" alt="3D K-means Clustering">
    </body>
    </html>
    """

    return render_template_string(template, image=png_image_b64_string)

if __name__ == '__main__':
    app.run(debug=True)