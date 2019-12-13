"""
    Python implementation of PSO (Particle Swarm Optimization) algorithm.
    Copyright (C) 2019  Dušan Erdeljan, Dimitrije Karanfilović

    This file is part of pso.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from PyQt5 import Qt
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
import sys
from window import Window
from log_window import LogWindow
from math import inf
from Benchmark import ackley, griewank, michalewicz, easom
import matplotlib.pyplot as plt
from PSO import PSO
from Test import benchmark
import threading


class MainWindow(QMainWindow):
    """
    Class that combines options windows and log window.
    text_update_needed: signal which is emitted when log window needs a text update during the algorithm execution,
    because otherwise text isn't updated in real time
    """
    text_update_needed = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.functions = [ackley, griewank, michalewicz]

        self.text_update_needed.connect(self.update_text)

        self.options_window = Window()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setWidget(self.options_window)

        self.menubar = self.menuBar()
        self.view_menu = self.menubar.addMenu("View")
        self.dark_mode = self.view_menu.addAction("Dark mode")
        self.dark_mode.setCheckable(True)
        self.dark_mode.triggered.connect(self.change_mode)

        self.docked = QDockWidget("Log window", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.log_window = LogWindow()
        self.docked.setWidget(self.log_window)
        self.docked.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.docked.setMinimumWidth(300)
        self.setMinimumHeight(400)
        self.setFixedHeight(500)

        self.setCentralWidget(self.scroll_area)
        self.setWindowTitle("PSO optimization")
        self.show()

        self.log_window.clear_btn.clicked.connect(lambda: self.log_window.text_area.clear())
        #self.log_window.run_btn.clicked.connect(self.create_options)
        self.log_window.run_btn.clicked.connect(self.start_thread)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

    def log_pso_algorithm(self, iteration, global_best):
        self.log_window.text_area.append("Iter #{}, GBEST: {}".format(iteration, global_best))

    def create_options(self):
        # self.log_window.text_area.clear()
        # self.log_window.text_area.append("Optimization process started. Please wait...")
        self.text_update_needed.emit("Optimization process started. Please wait...")
        dimension = self.options_window.spin_box.value()
        objfunc = self.functions[self.options_window.combo_box.currentIndex()]
        function = self.options_window.combo_box.currentText()
        options = self.load_options()

        global_best, global_best_position, history = benchmark(objfunc, function, dimension, options,
                                                               self.log_pso_algorithm)
        # self.log_window.text_area.append("Optimization process finished.")
        self.text_update_needed.emit("Optimization process finished.")
        # self.log_window.text_area.append("f(x*) = {}".format(global_best))
        self.text_update_needed.emit("f(x*) = {}".format(global_best))
        # self.log_window.text_area.append("x* = ")
        self.text_update_needed.emit("x* = ")
        for x in global_best_position:
            # self.log_window.text_area.append("  {}".format(x))
            self.text_update_needed.emit("  {}".format(x))

        if options.plot:
            plt.scatter([_ for _ in range(1, options.niter + 1)], history, marker='x')
            plt.title("{} function".format(function))
            plt.xlabel("Iteration")
            plt.ylabel("Global best")
            plt.show()

    def load_options(self):
        options = PSO.Options()
        options.plot = self.options_window.plot_box.isChecked()
        options.log = self.options_window.log_box.isChecked()
        if not self.options_window.default_npart.isChecked():
            options.npart = int(self.options_window.npart_input.text())

        if not self.options_window.default_niter.isChecked():
            options.niter = int(self.options_window.niter_input.text())

        if not self.options_window.default_ind_best.isChecked():
            options.cpi = float(self.options_window.ind_best_start_input.text())
            options.cpf = float(self.options_window.ind_best_end_input.text())

        if not self.options_window.default_global_best.isChecked():
            options.cgi = float(self.options_window.global_best_start_input.text())
            options.cgf = float(self.options_window.global_best_end_input.text())

        if not self.options_window.default_inertia.isChecked():
            options.wi = float(self.options_window.inertia_start_input.text())
            options.wf = float(self.options_window.inertia_end_input.text())

        if not self.options_window.default_v_max.isChecked():
            options.vmax = int(self.options_window.v_max_input.text())

        if not self.options_window.default_init_offset.isChecked():
            options.initoffset = int(self.options_window.init_offset_input.text())

        if not self.options_window.default_init_span.isChecked():
            options.initspan = int(self.options_window.init_span_input.text())

        if not self.options_window.default_vspan.isChecked():
            options.vspan = int(self.options_window.vspan_input.text())
        return options

    def change_mode(self):
        if self.dark_mode.isChecked():
            self.setStyleSheet("background-color: #2D2D30; color: white;")
            self.options_window.setStyleSheet("background-color: #2D2D30; color: white;")
            self.log_window.setStyleSheet("background-color: #2D2D30; color: white;")
            self.docked.setStyleSheet("background-color: #2D2D30; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.options_window.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.log_window.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.docked.setStyleSheet("background-color: #FFFFFF; color: black;")

    def update_text(self, text):
        self.log_window.text_area.append(text)

    def start_thread(self):
        self.c_thread = threading.Thread(target=self.create_options)
        self.c_thread.start()


if __name__ == '__main__':
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
