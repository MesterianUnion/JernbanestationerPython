import tkinter as tkinter
import tkintermapview
import pandas as pd

data_df = pd.read_csv("../wikidata/data6.csv")

root_tk = tkinter.Tk()
root_tk.geometry(f"{1280}x{720}")
root_tk.title("Station's Kort")

map_widget = tkintermapview.TkinterMapView(root_tk, width=1280, height=720, corner_radius=20)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

map_widget.set_position(55.811062, 12.473690)

for index, row in data_df.iterrows():
    station_label = row["stationLabel"]
    latitude = row["geoLatitude"]
    longitude = row["geoLongitude"]

    map_widget.set_marker(latitude, longitude, station_label)

root_tk.mainloop()
