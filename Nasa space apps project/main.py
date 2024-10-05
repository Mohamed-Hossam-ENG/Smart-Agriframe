import sys
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
import os
from datetime import datetime
import threading
import keyboard  # Library for detecting key presses
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QPushButton, QDialog)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush  # Make sure QPixmap is included here
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import folium
from nasr import LivePlotCanvas  # Import the class for graphs from nasr

# Path to CSV files for live data
csv_file_temperature = 'temperature_data.csv'
csv_file_humidity = 'humidity_data.csv'
csv_file_soil_moisture = 'soil_moisture_data.csv'

temp = 0 
humidty = 0
moisture = 0

# Data collection functions for temperature, humidity, and soil moisture
def collect_temperature_data():
    while True:
        temperature_value = random.uniform(15.0, 30.0)
        temp = temperature_value
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        df = pd.DataFrame([[timestamp, temperature_value]], columns=['Timestamp', 'Temperature'])
        if not os.path.isfile(csv_file_temperature):
            df.to_csv(csv_file_temperature, index=False)
        else:
            df.to_csv(csv_file_temperature, mode='a', header=False, index=False)
        time.sleep(1)

def collect_humidity_data():
    while True:
        humidity_value = random.uniform(40.0, 70.0)
        humidty = humidity_value
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        df = pd.DataFrame([[timestamp, humidity_value]], columns=['Timestamp', 'Humidity'])
        if not os.path.isfile(csv_file_humidity):
            df.to_csv(csv_file_humidity, index=False)
        else:
            df.to_csv(csv_file_humidity, mode='a', header=False, index=False)
        time.sleep(1)

def collect_soil_moisture_data():
    while True:
        soil_moisture_value = random.uniform(20.0, 60.0)
        moisture = soil_moisture_value
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        df = pd.DataFrame([[timestamp, soil_moisture_value]], columns=['Timestamp', 'Soil Moisture'])
        if not os.path.isfile(csv_file_soil_moisture):
            df.to_csv(csv_file_soil_moisture, index=False)
        else:
            df.to_csv(csv_file_soil_moisture, mode='a', header=False, index=False)
        time.sleep(1)

class LivePlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)  # Corrected constructor call

    def plot(self, data, title, ylabel):
        self.axes.cla()  # Clear the plot
        self.axes.plot(data['Timestamp'], data.iloc[:, 1], marker='o', color='b')
        self.axes.set_title(title)
        self.axes.set_ylabel(ylabel)
        self.axes.set_xlabel("Timestamp")
        self.axes.tick_params(axis='x', rotation=45)
        self.draw()

class SmartAgriframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.set_background('arora.webp')

        # Main layout
        main_layout = QVBoxLayout()
        self.add_team_name(main_layout)

        # Button to show graphs
        self.graph_button = QPushButton("Graph Data", self)
        self.graph_button.setFont(QFont("Arial", 18))
        self.graph_button.setStyleSheet("background-color: #A1F1A1; color: black; border-radius: 5px; padding: 10px;")
        self.graph_button.clicked.connect(self.show_graphs)  # Connect to the method
        main_layout.addWidget(self.graph_button, alignment=Qt.AlignCenter)  # Add button to the layout

        # Content layout for live data and map sections
        content_layout = QHBoxLayout()
        self.create_left_data_section(content_layout)
        self.create_map_selection_section(content_layout)
        main_layout.addLayout(content_layout)

        # Set the main widget and layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize a placeholder for graph widget
        self.graph_widget = None

    def set_background(self, background_image_path):
        """Set the Northern Lights background image, scaled to the window size."""
        palette = QPalette()
        pixmap = QPixmap(background_image_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def add_team_name(self, layout):
        """Add the team name at the top center."""
        team_name_label = QLabel("Smart Agriframe", self)
        team_name_label.setFont(QFont("Arial", 48, QFont.Bold))
        team_name_label.setAlignment(Qt.AlignCenter)
        team_name_label.setStyleSheet("color: #A1F1A1; padding: 20px;")
        layout.addWidget(team_name_label)

    def create_left_data_section(self, layout):
        """Create the section on the left for live data display."""
        live_data_frame = QFrame(self)
        live_data_frame.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px; padding: 20px;")
        live_data_layout = QVBoxLayout(live_data_frame)

        live_data_label = QLabel("Live Data", self)
        live_data_label.setFont(QFont("Arial", 28))
        live_data_label.setStyleSheet("color: #A1F1A1;")
        live_data_layout.addWidget(live_data_label)

        self.temperature_label = QLabel(f"Temperature: {temp} \u00B0C", self)
        self.humidity_label = QLabel(f"Humidity: {humidty} %", self)
        self.soil_moisture_label = QLabel(f"Soil Moisture: {moisture} %", self)

        for label in [self.temperature_label, self.humidity_label, self.soil_moisture_label]:
            label.setFont(QFont("Arial", 18))
            label.setStyleSheet("color: white; padding: 5px;")
            live_data_layout.addWidget(label)

        layout.addWidget(live_data_frame, alignment=Qt.AlignLeft)

    def create_map_selection_section(self, layout):
        """Create the map selection area on the right."""
        map_frame = QFrame(self)
        map_frame.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px; padding: 20px;")
        map_layout = QVBoxLayout(map_frame)

        # Placeholder image for the map
        self.map_image = QLabel(self)
        self.map_image.setPixmap(QPixmap("placeholder_map.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.map_image.setAlignment(Qt.AlignCenter)
        map_layout.addWidget(self.map_image)

        # Button to open map
        self.map_button = QPushButton("Choose Location", self)
        self.map_button.setFont(QFont("Arial", 18))
        self.map_button.setStyleSheet(""" 
            background-color: #A1F1A1; 
            color: black; 
            border-radius: 5px; 
            padding: 10px; 
            border: none; 
        """)
        self.map_button.clicked.connect(self.open_map_dialog)
        map_layout.addWidget(self.map_button)

        self.coordinates_label = QLabel("Coordinates: N/A", self)
        self.coordinates_label.setFont(QFont("Arial", 14))
        self.coordinates_label.setStyleSheet("color: white; padding: 5px;")
        map_layout.addWidget(self.coordinates_label)

        layout.addWidget(map_frame, alignment=Qt.AlignRight)

    def show_graphs(self):
        """Display the graphs in the main window."""
        # Remove any existing graph widget
        if self.graph_widget:
            self.graph_widget.deleteLater()  # Properly delete the existing widget

        # Create a new graph widget and set layout
        self.graph_widget = QWidget(self)
        graph_layout = QVBoxLayout(self.graph_widget)

        # Create instances of the LivePlotCanvas for the graphs
        self.temperature_plot = LivePlotCanvas(self.graph_widget, width=5, height=4)
        self.humidity_plot = LivePlotCanvas(self.graph_widget, width=5, height=4)
        self.soil_moisture_plot = LivePlotCanvas(self.graph_widget, width=5, height=4)

        # Add the plots to the graph layout
        graph_layout.addWidget(self.temperature_plot)
        graph_layout.addWidget(self.humidity_plot)
        graph_layout.addWidget(self.soil_moisture_plot)

        # Display the graphs
        self.graph_widget.setLayout(graph_layout)
        self.graph_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px; padding: 20px;")
        self.centralWidget().layout().addWidget(self.graph_widget, alignment=Qt.AlignCenter)  # Add to the main layout

        # Start updating the graphs
        threading.Thread(target=self.update_graphs, daemon=True).start()

    def update_graphs(self):
        """Update the graphs with new data every few seconds."""
        while True:
            # Ensure data files exist and update the graphs accordingly
            if os.path.isfile(csv_file_temperature):
                df_temperature = pd.read_csv(csv_file_temperature)
                self.temperature_plot.plot(df_temperature, "Temperature", "\u00B0C")

            if os.path.isfile(csv_file_humidity):
                df_humidity = pd.read_csv(csv_file_humidity)
                self.humidity_plot.plot(df_humidity, "Humidity", "%")

            if os.path.isfile(csv_file_soil_moisture):
                df_soil_moisture = pd.read_csv(csv_file_soil_moisture)
                self.soil_moisture_plot.plot(df_soil_moisture, "Soil Moisture", "%")
            
            time.sleep(5)  # Update every 5 seconds

    def open_map_dialog(self):
        """Open a dialog with the map for the user to select a location."""
        dialog = MapDialog(self)
        dialog.exec_()

    def update_coordinates(self, latitude, longitude, map_image_path):
        """Update the coordinates and display the map snippet."""
        self.coordinates_label.setText(f"Coordinates: {latitude}, {longitude}")
        self.map_image.setPixmap(QPixmap(map_image_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

class MapDialog(QDialog):
    def __init__(self, parent=None):
        super(MapDialog, self).__init__(parent)

        self.setWindowTitle("Select Location")
        self.setFixedSize(800, 600)

        # Set up web engine for rendering the map
        self.map_view = QWebEngineView(self)

        # Create map and save it as an HTML file with click capture
        self.create_interactive_map()

        # Load the map into the web view
        self.map_view.load(QUrl.fromLocalFile(os.path.abspath("map.html")))

        layout = QVBoxLayout(self)
        layout.addWidget(self.map_view)

        select_button = QPushButton("Select Location")
        select_button.clicked.connect(self.select_location)
        layout.addWidget(select_button)

    def create_interactive_map(self):
        """Create an interactive map using folium with zoom functionality."""
        map_ = folium.Map(location=[20.0, 0.0], zoom_start=2, control_scale=True)

        # Add JavaScript to capture click events and enable zoom controls
        click_js = '''
        function onMapClick(e) {
            var lat = e.latlng.lat;
            var lng = e.latlng.lng;
            localStorage.setItem('selectedLat', lat);
            localStorage.setItem('selectedLng', lng);
            alert("Selected coordinates: " + lat + ", " + lng);
        }
        map.on('click', onMapClick);
        '''

        # Adding JavaScript to the map
        map_.get_root().script.add_child(folium.Element(click_js))

        # Save the map to 'map.html'
        map_.save("map.html")
        print("Map saved as map.html")

    def select_location(self):
        """Capture the selected location from the local storage and close the dialog."""
        lat = self.get_coordinates_from_local_storage()
        if lat is not None:
            self.latitude = lat
            self.longitude = self.longitude
            print(f"Selected Coordinates: {self.latitude}, {self.longitude}")
            self.save_map_snippet(self.latitude, self.longitude)

            # Pass the coordinates and map image to the main window
            self.parent().update_coordinates(self.latitude, self.longitude, "map_snippet.png")

        self.accept()

    def get_coordinates_from_local_storage(self):
        """Fetch coordinates from local storage using JavaScript."""
        js_code = '''
        var lat = localStorage.getItem('selectedLat');
        var lng = localStorage.getItem('selectedLng');
        return lat && lng ? { lat: parseFloat(lat), lng: parseFloat(lng) } : null;
        '''
        self.map_view.page().runJavaScript(js_code, self.handle_coordinates)

    def handle_coordinates(self, result):
        """Handle the coordinates retrieved from the local storage."""
        if result:
            self.latitude = result['lat']
            self.longitude = result['lng']
            print(f"Coordinates retrieved: {self.latitude}, {self.longitude}")
        else:
            self.latitude = None
            self.longitude = None
            print("No coordinates found.")

    def save_map_snippet(self, latitude, longitude):
        """Generate and save a small map centered around the selected coordinates."""
        map_snippet = folium.Map(location=[latitude, longitude], zoom_start=12)
        map_snippet.save("map_snippet.html")
        print(f"Map snippet saved for coordinates: {latitude}, {longitude}")

        # Placeholder for now, you may need to capture this as an image using a screenshot tool
        self.map_snippet_image_path = "placeholder_map.png"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartAgriframe()

    # Start data collection threads
    threading.Thread(target=collect_temperature_data, daemon=True).start()
    threading.Thread(target=collect_humidity_data, daemon=True).start()
    threading.Thread(target=collect_soil_moisture_data, daemon=True).start()

    window.show()
    sys.exit(app.exec_())