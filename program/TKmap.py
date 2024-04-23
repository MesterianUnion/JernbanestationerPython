import tkinter as tkinter
import tkintermapview
import pandas as pd

data_df = pd.read_csv("../wikidata/data6.csv")

root_tk = tkinter.Tk()
root_tk.geometry(f"{1280}x{720}")
root_tk.title("Station's Kort")
root_tk.iconbitmap("images/tkBLUEicon.ico")

map_widget = tkintermapview.TkinterMapView(root_tk, width=1280, height=720, corner_radius=20)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

map_widget.set_position(55.811062, 12.473690)

data_dict = {}

for index, row in data_df.iterrows():
    station_label = row["stationLabel"]
    linjer_label = row["linjerLabel"]
    latitude = row["geoLatitude"]
    longitude = row["geoLongitude"]

    if linjer_label not in data_dict:
        data_dict[linjer_label] = []
    data_dict[linjer_label].append((latitude, longitude, station_label))

# Create search bar
search_var = tkinter.StringVar()
search_bar = tkinter.Entry(root_tk, textvariable=search_var)
search_bar.pack()

# Create Listbox for search results
search_results = tkinter.Listbox(root_tk)
search_results.pack()

def update_results(*args):
    search_term = search_var.get()

    search_results.delete(0, tkinter.END)


    results = data_df[(data_df['stationLabel'].str.contains(search_term)) |
                      (data_df['linjerLabel'].str.contains(search_term)) |
                      (data_df['connectingLineLabel'].str.contains(search_term))]

    for index, row in results.iterrows():
        search_results.insert(tkinter.END, row['linjerLabel'])


search_var.trace('w', update_results)

def display_all_markers():
    map_widget.delete_all_marker()
    for marker_list in data_dict.values():
        for latitude, longitude, station_label in marker_list:
            map_widget.set_marker(latitude, longitude, station_label)

def update_markers(*args):
    # If the search bar is cleared, display all markers
    if not search_var.get():
        display_all_markers()
        return
    # Otherwise, display only the markers that match the selected search result
    selected_result = search_results.get(search_results.curselection())
    if selected_result in data_dict:
        # Clear all markers
        map_widget.delete_all_marker()
        # Display the matching markers
        for latitude, longitude, station_label in data_dict[selected_result]:
            map_widget.set_marker(latitude, longitude, station_label)

search_results.bind('<<ListboxSelect>>', update_markers)

display_all_markers()

root_tk.mainloop()
