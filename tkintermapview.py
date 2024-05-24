import tkinter as tk
from tkinter import messagebox, ttk
import tkintermapview
import geopy.geocoders
from geopy.geocoders import Nominatim
import geopy.distance

# Function to convert location name to coordinates
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Function to find intersections within a given radius
def find_intersections(center_coordinates, radius):
    # This function is a placeholder. You will need to implement logic to find intersections
    # based on your specific requirements. For now, let's create some dummy data for illustration.
    intersections = [
        (center_coordinates[0] + 0.001, center_coordinates[1] + 0.001),
        (center_coordinates[0] - 0.001, center_coordinates[1] - 0.001),
        (center_coordinates[0] + 0.001, center_coordinates[1] - 0.001),
        (center_coordinates[0] - 0.001, center_coordinates[1] + 0.001)
    ]
    return intersections

# Function to set map position to the entered location
def set_location():
    location_name = location_entry.get()
    coordinates = get_coordinates(location_name)
    if coordinates:
        map_widget.set_position(coordinates[0], coordinates[1])
        map_widget.set_marker(coordinates[0], coordinates[1], text="Destination")
        messagebox.showinfo("Coordinates", f"Coordinates of {location_name} are {coordinates}")

        # Find and place pins at intersections within the radius
        radius = 0.01  # 1km radius for example
        intersections = find_intersections(coordinates, radius)

        # Clear existing table rows
        for row in table.get_children():
            table.delete(row)

        for intersection in intersections:
            map_widget.set_marker(intersection[0], intersection[1], text="Intersection")
            table.insert("", "end", values=intersection)
        
        # Here you can call the function to start Dijkstra's Algorithm
        # start_dijkstra_algorithm(coordinates)
    else:
        messagebox.showerror("Error", "Location not found")

# Dijkstra's Algorithm (you will need to implement this based on your specific use case)
def start_dijkstra_algorithm(start_coordinates):
    pass  # Implement your Dijkstra's Algorithm here

# Create tkinter window
root_tk = tk.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("Map View Example")

# Create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=400, corner_radius=0)
map_widget.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Create entry widget for location input
location_entry = tk.Entry(root_tk, width=50)
location_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Create button to set location
location_button = tk.Button(root_tk, text="Set Location", command=set_location)
location_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Create table to display intersection coordinates
columns = ("Latitude", "Longitude")
table = ttk.Treeview(root_tk, columns=columns, show='headings')
for col in columns:
    table.heading(col, text=col)
table.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

# Set initial zoom level
map_widget.set_zoom(15)

# Run the Tkinter main loop
root_tk.mainloop()
