import pandas as pd
import geopandas as gpd
import folium

data_read = pd.read_csv("../wikidata/data6.csv")

# Convert linjerLabel to string and fill missing values with 'No data'
data_read['linjerLabel'] = data_read['linjerLabel'].astype(str).fillna('No data')

grouped = data_read.groupby(['geoLatitude', 'geoLongitude']).agg({
    'station': 'first',
    'stationLabel': 'first',
    'address': 'first',
    'connectingLineLabel': 'first',
    'årstal': 'first',
    'linjerLabel': lambda x: ', '.join(set(x))
}).reset_index()

gdf = gpd.GeoDataFrame(grouped, geometry=gpd.points_from_xy(grouped.geoLongitude, grouped.geoLatitude))

m = folium.Map(location=[grouped['geoLatitude'].mean(), grouped['geoLongitude'].mean()], zoom_start=10)

for idx, row in gdf.iterrows():
    popup_html = """
    <b style="color: blue;">Station:</b> {}<br>
    <b style="color: green;">Linjer:</b> {}<br>
    <b style="color: red;">Forbindelser:</b> {}<br>
    <a style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px; transition-duration: 0.4s;" href="https://www.google.com/maps/search/?api=1&query={},{}" target="_blank">Åbn i Google maps</a>
    """.format(row['stationLabel'], row['linjerLabel'], row['connectingLineLabel'], row['geoLatitude'], row['geoLongitude'])

    popup = folium.Popup(folium.IFrame(html=popup_html, width=200, height=200), max_width=200)

    folium.Marker(location=[row['geoLatitude'], row['geoLongitude']], popup=popup).add_to(m)

m.save('jernbane-kort.html')
