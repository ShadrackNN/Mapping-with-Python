# Import necessary libraries
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
import osmnx as ox
import networkx as nx
import libpysal as lps
import h3
import rasterio
import leafmap
from geojson import Point


# Class 01: Getting Started
def load_and_visualize_data():
    # Sample data: GeoDataFrame with point geometries
    data = {'city': ['NYC', 'LA', 'Chicago'],
            'population': [8419000, 3980400, 2716000],
            'geometry': [Point(-74.006, 40.7128), Point(-118.2437, 34.0522), Point(-87.6298, 41.8781)]}
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Plotting
    gdf.plot()
    plt.title('Sample City Data')
    plt.show()


# Class 02: Loading, Exploring, Visualizing Data
def explore_data():
    # Load sample GeoDataFrame
    gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    # Exploring the data
    print(gdf.head())

    # Create static visualization
    gdf.plot()
    plt.title('Cities of the World')
    plt.show()

    # Create interactive visualization
    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.GeoJson(gdf).add_to(m)
    m.save('interactive_map.html')


# Class 04: Geoprocessing
def geoprocess_data():
    # Sample data
    gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Manipulate data: select polygons for Africa
    africa = gdf[gdf['continent'] == 'Africa']

    # Reshape data: buffer operation
    africa['geometry'] = africa.buffer(1)

    # Combine datasets (Example using self-merge)
    combined = gpd.sjoin(africa, africa, how='inner', op='intersects')

    # Plotting
    combined.plot()
    plt.title('Buffered Africa Polygons')
    plt.show()


# Class 06: Measuring Distance
def calculate_distances():
    # Download and plot street network from OSM for Manhattan
    G = ox.graph_from_place('Manhattan, New York, USA', network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G)
    edges.plot()
    plt.title('Manhattan Street Network')
    plt.show()

    # Calculate shortest path between two points
    orig_node = ox.distance.nearest_nodes(G, X=-73.9857, Y=40.7484)  # Example coordinates (Empire State Building)
    dest_node = ox.distance.nearest_nodes(G, X=-73.9851, Y=40.7580)  # Example coordinates (Times Square)
    shortest_path = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
    print(f"Shortest path length: {shortest_path} meters")


# Class 08: Supervised Classification using EO Data
def classify_raster_data():
    # Load sample raster data
    with rasterio.open('path_to_raster.tif') as src:
        raster = src.read(1)

    # Simple threshold classification
    classified = (raster > 100).astype(int)

    # Plotting
    plt.imshow(classified, cmap='gray')
    plt.title('Classified Raster Data')
    plt.show()


# Main function to execute all class sections
if __name__ == "__main__":
    load_and_visualize_data()
    explore_data()
    geoprocess_data()
    calculate_distances()
    classify_raster_data()
