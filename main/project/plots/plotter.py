import os.path
import sys
import json
import matplotlib.pyplot as plt

class Plotter:

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "plot")

    def __init__(self, file):
        self.file = os.path.join(self.path, file)
        self.plot_data = []

    def plot_file(self):
        with open(self.file, "r") as f:
            self.plot_data = json.load(f)
        fig, ax = plt.subplots()
        ax.plot(self.plot_data[0]["frecuencias"], self.plot_data[0]["potencias"])
        ax.set_ylim(top=-30)

    def plot_graphics(self):
        plt.grid(True)
        plt.xlabel('MHz')
        plt.ylabel('dBm')
        pointer = round(515 / 2)
        x_point = self.plot_data[0]["frecuencias"][pointer]
        y_point = self.plot_data[0]["potencias"][pointer]
        plt.scatter(x_point, y_point, color='red', label=f'Portadora ({x_point} MHz, {y_point} dBm)')
        plt.legend()
        plt.show()

carrier = Plotter(sys.argv[1])
carrier.plot_file()
carrier.plot_graphics()