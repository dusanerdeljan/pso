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
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import pyqtSignal
from gui.OptionsWindow import OptionsWindow
from gui.LogWindow import LogWindow
from pso.PSO import PSO
from pso.Benchmark import benchmark, ackley, griewank, michalewicz
import threading
import matplotlib.pyplot as plt
from math import inf


class MainWindow(QMainWindow):
    """
    Class that combines options windows and log window.
    text_update_needed: signal which is emitted when log window needs a text update during the algorithm execution,
    because otherwise text isn't updated in real time
    """
    text_update_needed = pyqtSignal(str)
    error_message = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.functions = [ackley, griewank, michalewicz]

        self.text_update_needed.connect(self.update_text)
        self.error_message.connect(self.show_error_message)

        self.options_window = OptionsWindow()
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
        self.setWindowTitle("Continuous function optimization using PSO algorithm")
        self.show()

        self.log_window.clear_btn.clicked.connect(lambda: self.log_window.text_area.clear())
        self.log_window.run_btn.clicked.connect(self.start_thread)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")
        self.dark_mode.trigger()

    def log_pso_algorithm(self, iteration, global_best):
        """
        Callback log function called every 10 iterations of optimization process. Updates log window
        Arguments:
            iteration(int): Current iteration
            global_best(float): Current global optimum
        """
        self.text_update_needed.emit("Iter #{}, GBEST: {}".format(iteration, global_best))

    def create_options(self):
        """
        Starts the optimization process. Plots a graph if plot option is enabled
        """
        dimension = self.options_window.spin_box.value()
        objfunc = self.functions[self.options_window.combo_box.currentIndex()]
        function = self.options_window.combo_box.currentText()
        options = self.load_options()
        if not options:
            return
        self.text_update_needed.emit("Optimization process started. Please wait...")
        self.log_window.run_btn.setDisabled(True)
        self.log_window.clear_btn.setDisabled(True)

        global_best, global_best_position, history = benchmark(objfunc, dimension, options, self.log_pso_algorithm)
        self.text_update_needed.emit("Optimization process finished.")
        self.text_update_needed.emit("\nf(x*) = {}".format(global_best))
        self.text_update_needed.emit("\nx* = \n")
        for x in global_best_position:
            self.text_update_needed.emit("  {}".format(x))

        if options.plot:
            plt.scatter([_ for _ in range(1, options.niter + 1)], history, marker='x')
            plt.title("{} function".format(function))
            plt.xlabel("Iteration")
            plt.ylabel("Global best")
            plt.show()

        self.log_window.run_btn.setEnabled(True)
        self.log_window.clear_btn.setEnabled(True)

    def show_error_message(self, text, title="Invalid parameter value"):
        """
        Displays error message box
        Arguments:
            text(str): Error description
            title(str): Error title
        """
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #2D2D30; color: white;")
        msg.setModal(True)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    def load_options(self):
        """
        Loads user defined algorithm options and checks if options are valid
        Returns:
            options(PSO.Options): User defined options, None if the options are invalid
        """
        options = PSO.Options()
        options.plot = self.options_window.plot_box.isChecked()
        options.log = self.options_window.log_box.isChecked()
        if not self.options_window.default_npart.isChecked():
            try:
                options.npart = int(self.options_window.npart_input.text())
            except ValueError:
                self.error_message.emit("Number of particles must be an integer value.")
                return None

        if not self.options_window.default_niter.isChecked():
            try:
                options.niter = int(self.options_window.niter_input.text())
            except ValueError:
                self.error_message.emit("Number of iterations must be an integer value.")
                return None

        if not self.options_window.default_ind_best.isChecked():
            try:
                options.cpi = float(self.options_window.ind_best_start_input.text())
                options.cpf = float(self.options_window.ind_best_end_input.text())
            except ValueError:
                self.error_message.emit("Cp initial and/or final must be a real value.")
                return None

        if not self.options_window.default_global_best.isChecked():
            try:
                options.cgi = float(self.options_window.global_best_start_input.text())
                options.cgf = float(self.options_window.global_best_end_input.text())
            except ValueError:
                self.error_message.emit("Cg initial and/or final must be a real value")
                return None

        if not self.options_window.default_inertia.isChecked():
            try:
                options.wi = float(self.options_window.inertia_start_input.text())
                options.wf = float(self.options_window.inertia_end_input.text())
            except ValueError:
                self.error_message.emit("Inertia factor initial and/or final must be a real value")
                return None

        if not self.options_window.default_v_max.isChecked():
            try:
                options.vmax = float(self.options_window.v_max_input.text())
            except ValueError:
                if self.options_window.v_max_input.text().lower() == "inf":
                    options.vmax = inf
                else:
                    self.error_message.emit("Absolute max speed must be a real value.")
                    return None

        if not self.options_window.default_init_offset.isChecked():
            try:
                options.initoffset = float(self.options_window.init_offset_input.text())
            except ValueError:
                self.error_message.emit("Initial population span must be a real value")
                return None

        if not self.options_window.default_init_span.isChecked():
            try:
                options.initspan = float(self.options_window.init_span_input.text())
            except ValueError:
                self.error_message.emit("Initial population offset must be a real value.")
                return None

        if not self.options_window.default_vspan.isChecked():
            try:
                options.vspan = float(self.options_window.vspan_input.text())
            except ValueError:
                self.error_message.emit("Initial velocity span must be a real value.")
                return None

        return options

    def change_mode(self):
        """
        Event handler for change mode action. Changes the theme from dark to white and vice versa
        """
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
        """
        Updates log window
        Arguments:
            text(str) Text to be appended
        """
        self.log_window.text_area.append(text)
        self.log_window.text_area.moveCursor(QTextCursor.End)
        self.log_window.text_area.ensureCursorVisible()

    def start_thread(self):
        """
        Event handler for run button click. Starts a new thread which runs the optimization process
        """
        self.log_window.text_area.clear()
        c_thread = threading.Thread(target=self.create_options)
        c_thread.start()
