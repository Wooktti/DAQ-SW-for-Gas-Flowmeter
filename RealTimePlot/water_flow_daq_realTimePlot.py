import numpy as np
import serial
import pyqtgraph as pg
from pyqtgraph.Qt.QtCore import QTimer, pyqtSignal, pyqtSlot, QObject
from pyqtgraph.Qt.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QGraphicsProxyWidget
from typing import List, Optional, Tuple
from datetime import datetime
import csv
import os
import threading
import struct


class RealTimePlot(QObject):
    """
    A class used to plot real-time data from a serial port using PyQtGraph.

    Attributes
    ----------
    _num_of_data : int
        The number of data series to plot.
    _max_size : int
        The maximum number of data points to display on the plot.
    _app : QApplication
        The PyQtGraph application.
    _ser : Serial
        The serial port.
    _win : GraphicsLayoutWidget
        The PyQtGraph window.
    _plots : list
        The list of PlotItem objects.
    _curves : list
        The list of PlotDataItem objects.
    _datas_x : list
        The list of x data arrays.
    _datas_y : list
        The list of y data arrays.
    _update_rate : int
        The rate at which the plot updates, in milliseconds.
    _time : int
        The current time, in milliseconds.
    _timer : QTimer
        The timer that triggers the plot updates.
    _file_path : str
        The file path where the data is stored. Only created when _write_to_file is True.
    _write_to_file : bool
        Whether to create the file or not.

    Methods
    -------
    __init__(port: str, datas: List[str], window_title="Real-time Plotting", update_rate=50, max_size=250)
        Initializes the RealTimePlot object.
    __update() -> None
        Updates the plot with new data from the serial port.
    __get_data(self, sep=",") -> List[float]
        Get the decoded data from the serial port.
    run() -> None
        Starts the PyQtGraph application.
    __write_to_csv(self, row: List[float]) -> None:
        Write a row of data to a CSV file.
    """

    data_sent = pyqtSignal(tuple)

    def __init__(
        self,
        data_set: List[str],
        port: str,
        update_rate=50,
        sensor_rate=50,
        baud_rate=115200,
        window_title="Real-time Plotting",
        file_name=None,
        file_directory_name="csv_files",
        max_size=250,
        write_to_file=True,
    ):
        """
        Initializes the RealTimePlot object.

        This method sets up the PyQtGraph application, opens the serial port, creates the PyQtGraph window,
        creates the plots and curves, initializes the data arrays, and starts the timer that triggers the plot updates.

        Parameters
        ----------
        data_set : List[str]
            The list of data series to plot. If the first element of data_set is "time", then
            the time data is extracted from the serial port. Otherwise, elapsed time is calulated here.
        port : str
            The name of the serial port to read data from.
        baud_rate : int, optional
            The baud rate of the serial port to read data from (default is 9600).
        window_title : str, optional
            The title of the PyQtGraph window (default is "Real-time Plotting").
        file_name: str, optional
            The name of the file where data is stored (default is "data_%Y-%m-%d,%H-%M-%S.csv").
        file_directory_name: str, optional
            The name of the directory where data is stored (default is "csv_files").
        update_rate : int, optional
            The rate at which the plot updates, in milliseconds (default is 50).
        max_size : int, optional
            The maximum number of data points to display on the plot (default is 250).
        write_to_file : bool, optional
            If True, data is written to a file named file_name. If False, no data is written (default is True).
        """
        QObject.__init__(self)
        self.data_sent.connect(self.__update)

        # Set the update rate and initialize the current time
        self._update_rate = update_rate
        self._sensor_rate = sensor_rate
        self._time = 0
        self._time_from_serial = False

        # If time data comes from the serial port
        if data_set[0] == "time (ms)":
            self._time_from_serial = True
            data_set = data_set[1:]

        # Set the number of data series and the maximum number of data points
        self._num_of_data = len(data_set)
        self._max_size = max_size

        # Create the PyQtGraph application
        self._app = pg.mkQApp()

        # Open the serial port
        self._ser = serial.Serial(port, baud_rate)
        self._data_packet = bytearray(24)

        # Create the PyQtGraph window
        self._win = pg.GraphicsLayoutWidget(show=True)
        self._win.resize(1200, 600)
        self._win.setWindowTitle(window_title)

        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)

        # Enable antialiasing for smoother plot lines
        pg.setConfigOptions(antialias=True)

        # Create the plots
        self._plots = []
        for i, data in enumerate(data_set):
            self._plots.append(self._win.addPlot(title=data))
            if (i + 1) % 3 == 0:
                self._win.nextRow()

        # Create the curves
        self._curves = [plot.plot(pen="y") for plot in self._plots]

        # Initialize the data arrays
        self._datas_x = [np.array([])] * self._num_of_data
        self._datas_y = [np.array([])] * self._num_of_data

        # Create the timer
        self._timer = QTimer()

        # Set the option parameter
        self._write_to_file = write_to_file

        # Initialize the csv file if write_to_file is True.
        if self._write_to_file:
            # Create the directory where the data results are written
            os.makedirs(file_directory_name, exist_ok=True)

            # Set the default file name if file name is None
            if file_name is None:
                file_name = datetime.now().strftime("data_%Y-%m-%d,%H-%M-%S.csv")

            # Open the file
            self._file_path = os.path.join(file_directory_name, file_name)
            with open(self._file_path, "w", newline="") as file:
                csv.writer(file).writerow(["time"] + data_set)

    @pyqtSlot(tuple)
    def __update(self, data: Tuple[Optional[int], list[float]]) -> None:
        """
        Updates the plot with new data from the serial port.

        This method is called every `_update_rate` milliseconds by a QTimer object.
        It reads a line from the serial port, decodes it, and splits it into a list of float values.
        Each value is appended to the corresponding y data array, and the current time is appended to each x data array.
        If the length of a data array exceeds `_max_size`, the oldest data point is removed.
        Finally, the data for each curve is updated with the new x and y data arrays.
        """
        # Check if there is data available to read from the serial port
        current_time, values = data

        if values:
            # Append each value to the corresponding y data array
            self._datas_y = [
                np.append(data_y, value) for data_y, value in zip(self._datas_y, values)
            ]
            # Append the current time to each x data array
            self._datas_x = [
                np.append(data_x, current_time / 1000) for data_x in self._datas_x
            ]

            # If the length of a data array exceeds max_size, remove the oldest data point
            if len(self._datas_y[0]) > self._max_size:
                self._datas_y = [data_y[1:] for data_y in self._datas_y]
                self._datas_x = [data_x[1:] for data_x in self._datas_x]

            # Update the data for each curve with the new x and y data arrays
            for curve, data_x, data_y in zip(
                self._curves, self._datas_x, self._datas_y
            ):
                curve.setData(data_x, data_y)

    @pyqtSlot()
    def __get_data(self, sep=",") -> None:
        """
        Get the decoded data from the serial port.

        Parameters
        ----------
        sep : str, optional
            The separator used to split the serial readings (default is ",").

        Returns
        -------
        Tuple[Optional[int], List[float]]
            Current time and a list of float values each representing data values.
        """
        count = 0
        while True:
            data = None, []
            if self._ser.in_waiting > 0:
                count += 1
                self._ser.readinto(self._data_packet)
                # print(self._data_packet)
                timeStamp = struct.unpack('I', self._data_packet[0:4])[0] # unit: ms
                press1Bar = struct.unpack('f', self._data_packet[4:8])[0] # unit: bar
                press2Bar = struct.unpack('f', self._data_packet[8:12])[0] # unit: bar
                fm_gps = struct.unpack('f', self._data_packet[12:16])[0] # unit: g/s
                temp1C = struct.unpack('f', self._data_packet[16:20])[0] # unit: degC
                temp2C = struct.unpack('f', self._data_packet[20:24])[0] # unit: degC

                # values = line.decode().strip().split(sep)
                raw_data = [timeStamp, press1Bar, press2Bar, fm_gps, temp1C, temp2C]
                if self._time_from_serial:
                    data = raw_data[0], raw_data[1:]
                else:
                    self._time += self._update_rate
                    data = self._time, raw_data

                # Write value to CSV file.
                if self._write_to_file:
                    self.__write_to_csv(raw_data)

                if count == self._update_rate // self._sensor_rate:
                    self.data_sent.emit(data)
                    count = 0

    def run(self) -> None:
        """
        Display the plot to the pyqtgraph window.
        """
        # Connect the timer to the update method
        threading.Thread(target=self.__get_data, daemon=True).start()
        # execute the pygtgraph
        pg.exec()

    def __write_to_csv(self, row: List[float]) -> None:
        """
        Write a row of data to a CSV file.

        Parameters
        ----------
        row : List[float]
            A list of float values representing a row of data.
        """
        with open(self._file_path, "a", newline="") as file:
            csv.writer(file).writerow(row)


if __name__ == "__main__":
    # Test code. Reads 6 values from the serial and plot each data.
    # Modify the parameters of the `RealtimePlot` to fit your project.
    datas = [
        "time (ms)",
        "PT1 (barg)",
        "PT2 (barg)",
        "FM (g/s)",
        "TC1 (degC)",
        "TC2 (degC)",
    ]  # list of datas.
    plotter = RealTimePlot(data_set=datas, port="/dev/tty.usbmodem146659901", update_rate=25, sensor_rate=10)
    plotter.run()
