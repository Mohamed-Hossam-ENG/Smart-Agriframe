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
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import folium

# Path to CSV files for live data
csv_file_temperature = 'temperature_data.csv'
csv_file_humidity = 'humidity_data.csv'
csv_file_soil_moisture = 'soil_moisture_data.csv'

# Global variable to control plotting
plotting_active = True

# Data collection functions for temperature, humidity, and soil moisture
def collect_temperature_data():
    while True:
        temperature_value = random.uniform(15.0, 30.0)
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
        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        df = pd.DataFrame([[timestamp, soil_moisture_value]], columns=['Timestamp', 'Soil Moisture'])
        if not os.path.isfile(csv_file_soil_moisture):
            df.to_csv(csv_file_soil_moisture, index=False)
        else:
            df.to_csv(csv_file_soil_moisture, mode='a', header=False, index=False)
        time.sleep(1)

# Custom plot canvas for embedding Matplotlib plots into PyQt5
class LivePlotCanvas(FigureCanvas):
    def _init_(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(LivePlotCanvas, self)._init_(fig)

    def plot(self, data, title, ylabel):
        self.axes.cla()  # Clear the plot
        self.axes.plot(data['Timestamp'], data.iloc[:, 1], marker='o', color='b')
        self.axes.set_title(title)
        self.axes.set_ylabel(ylabel)
        self.axes.set_xlabel("Timestamp")
        self.axes.tick_params(axis='x', rotation=45)
        self.draw()

# Main application window class
class SmartAgriframe(QMainWindow):
    def _init_(self):
        super()._init_()
        self.showFullScreen()

        # Set background image
        self.set_background('arora.webp')

        # Main layout
        main_layout = QVBoxLayout()
        self.add_team_name(main_layout)

        # Content layout for live data and map sections
        content_layout = QHBoxLayout()

        # Create left live data section with graph
        self.create_left_data_section(content_layout)

        # Create map selection section
        self.create_map_selection_section(content_layout)

        # Add content layout to main layout
        main_layout.addLayout(content_layout)

        # Set the main widget and layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Start live data collection
        self.start_live_data_threads()

    def set_background(self, background_image_path):
        """Set the background image."""
        palette = QPalette()
        pixmap = QPixmap(background_image_path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def add_team_name(self, layout):
        """Add team name at the top."""
        team_name_label = QLabel("Smart Agriframe", self)
        team_name_label.setFont(QFont("Arial", 48, QFont.Bold))
        team_name_label.setAlignment(Qt.AlignCenter)
        team_name_label.setStyleSheet("color: #A1F1A1; padding: 20px;")
        layout.addWidget(team_name_label)

    def create_left_data_section(self, layout):
        """Create the left section for live data display and graphs."""
        live_data_frame = QFrame(self)
        live_data_frame.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 10px; padding: 20px;")
        live_data_layout = QVBoxLayout(live_data_frame)

        live_data_label = QLabel("Live Data", self)
        live_data_label.setFont(QFont("Arial", 28))
        live_data_label.setStyleSheet("color: #A1F1A1;")
        live_data_layout.addWidget(live_data_label)

        # Temperature plot
        self.temperature_plot = LivePlotCanvas(self, width=5, height=4)
        live_data_layout.addWidget(self.temperature_plot)

        # Humidity plot
        self.humidity_plot = LivePlotCanvas(self, width=5, height=4)
        live_data_layout.addWidget(self.humidity_plot)

        # Soil Moisture plot
        self.soil_moisture_plot = LivePlotCanvas(self, width=5, height=4)
        live_data_layout.addWidget(self.soil_moisture_plot)

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
        self.map_button.setStyleSheet("background-color: #A1F1A1; color: black; border-radius: 5px; padding: 10px;")
        self.map_button.clicked.connect(self.open_map_dialog)
        map_layout.addWidget(self.map_button)

        self.coordinates_label = QLabel("Coordinates: N/A", self)
        self.coordinates_label.setFont(QFont("Arial", 14))
        self.coordinates_label.setStyleSheet("color: white; padding: 5px;")
        map_layout.addWidget(self.coordinates_label)

        layout.addWidget(map_frame, alignment=Qt.AlignRight)

    def open_map_dialog(self):
        """Open a dialog with the map for the user to select a location."""
        dialog = MapDialog(self)
        dialog.exec_()

    def update_coordinates(self, latitude, longitude, map_image_path):
        """Update the coordinates and display the map snippet."""
        self.coordinates_label.setText(f"Coordinates: {latitude}, {longitude}")
        self.map_image.setPixmap(QPixmap(map_image_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def start_live_data_threads(self):
        """Start threads to collect and plot live data."""
        threading.Thread(target=self.update_plots, daemon=True).start()

    def update_plots(self):
        """Update the plots with new data every few seconds."""
        while True:
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

class MapDialog(QDialog):
    def _init_(self, parent=None):
        super()._init_(parent)
        self.setWindowTitle("Select Location")
        self.setGeometry(100, 100, 800, 600)

        self.map_view = QWebEngineView(self)
        layout = QVBoxLayout()
        layout.addWidget(self.map_view)
        self.setLayout(layout)

        # Create a sample map
        m = folium.Map(location=[20, 0], zoom_start=2)
        map_path = "map.html"
        m.save(map_path)

        # Load the map in the web view
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(map_path)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartAgriframe()

    # Start data collection threads
    threading.Thread(target=collect_temperature_data, daemon=True).start()
    threading.Thread(target=collect_humidity_data, daemon=True).start()
    threading.Thread(target=collect_soil_moisture_data, daemon=True).start()

    window.show()
    sys.exit(app.exec_())