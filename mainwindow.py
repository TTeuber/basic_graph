# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot
from basic_graph import Ui_MainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import sqlite3


class Chart(FigureCanvas):
    def __init__(self, parent):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        # three important lines for transparency
        self.figure.patch.set_facecolor("None")
        self.ax.set_facecolor("None")
        self.setStyleSheet("background-color:transparent;")

        self.setParent(parent)
        self.update_chart()

    def update_chart(self):
        self.ax.clear()
        with sqlite3.connect("test.db") as conn:
            c = conn.cursor()
            c.execute(
                "SELECT x FROM test"
            )
            x = c.fetchall()
            c.execute(
                "SELECT y FROM test"
            )
            y = c.fetchall()
            self.ax.plot(x, y, marker="o", linewidth=5, color="green", alpha=0.5)
        x_limit = 5 if len(x) < 5 else len(x) + 1
        self.ax.set_xlim(1, x_limit)
        self.ax.set_ylim(0, 11)
        self.draw()

    def clear_chart(self):
        self.ax.clear()
        self.ax.set_xlim(1, 5)
        self.ax.set_ylim(0, 11)
        with sqlite3.connect("test.db") as conn:
            c = conn.cursor()
            c.execute(
                "DELETE FROM test"
            )
            c.execute(
                "UPDATE SQLITE_SEQUENCE SET SEQ= '0' WHERE NAME='test';"
            )
        self.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.widget = self.ui.widget
        self.slider = self.ui.slider
        self.slider_label = self.ui.slider_label

        self.submit_button = self.ui.submit_button
        self.submit_button.clicked.connect(self.update_chart)

        self.reset_button = self.ui.reset_button
        self.reset_button.clicked.connect(self.reset_chart)

        self.slider.valueChanged.connect(self.update_slider_label)

        self.chart = Chart(self.widget)

    def update_chart(self):
        with sqlite3.connect("test.db") as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO test(y) VALUES(?)", (self.slider.value(),)
            )
            conn.commit()
        self.chart.update_chart()

    def reset_chart(self):
        self.chart.clear_chart()

    @Slot()
    def update_slider_label(self):
        self.slider_label.setText(str(self.slider.value()))


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
