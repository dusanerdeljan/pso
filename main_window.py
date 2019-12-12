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
import sys
from window import Window
from log_window import LogWindow
from math import inf
from Benchmark import ackley, griewank, michalewicz, easom
from PSO import PSO


class MainWindow(QMainWindow):
    """
    Class that combines options windows and log window.
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.functions = [ackley, griewank, michalewicz, easom]

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
        self.docked.setTitleBarWidget(QLabel("<center>Log window</center>"))
        self.docked.setFeatures(QDockWidget.DockWidgetFloatable |
                                QDockWidget.DockWidgetMovable)

        self.docked.setMinimumWidth(300)
        self.docked.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.setMinimumHeight(400)
        self.setFixedHeight(500)

        self.setCentralWidget(self.scroll_area)
        self.setWindowTitle("PSO optimization")
        self.show()

        self.log_window.clear_btn.clicked.connect(lambda: self.log_window.text_area.clear())
        self.log_window.run_btn.clicked.connect(self.create_options)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

    def create_options(self):
        self.options = PSO.Options()
        self.options.plot = self.options_window.plot_box.isChecked()
        self.options.log = self.options_window.log_box.isChecked()
        self.dimension = self.options_window.spin_box.value()
        self.function = self.functions[self.options_window.combo_box.currentIndex()]

        if not self.options_window.default_npart.isChecked():
            self.options.npart = int(self.options_window.npart_input.text())

        if not self.options_window.default_niter.isChecked():
            self.options.niter = int(self.options_window.niter_input.text())

        if not self.options_window.default_ind_best.isChecked():
            self.options.cpi = float(self.options_window.ind_best_start_input.text())
            self.options.cpf = float(self.options_window.ind_best_end_input.text())

        if not self.options_window.default_global_best.isChecked():
            self.options.cgi = float(self.options_window.global_best_start_input.text())
            self.options.cgf = float(self.options_window.global_best_end_input.text())

        if not self.options_window.default_inertia.isChecked():
            self.options.wi = float(self.options_window.inertia_start_input.text())
            self.options.wf = float(self.options_window.inertia_end_input.text())

        if not self.options_window.default_v_max.isChecked():
            self.options.vmax = int(self.options_window.v_max_input.text())

        if not self.options_window.default_init_offset.isChecked():
            self.options.initoffset = int(self.options_window.init_offset_input.text())

        if not self.options_window.default_init_span.isChecked():
            self.options.initspan = int(self.options_window.init_span_input.text())

        if not self.options_window.default_vspan.isChecked():
            self.options.vspan = int(self.options_window.vspan_input.text())

    def change_mode(self):
        if self.dark_mode.isChecked():
            self.setStyleSheet("background-color: #2D2D30; color: white;")
            self.options_window.setStyleSheet("background-color: #2D2D30; color: white;")
            self.log_window.setStyleSheet("background-color: #2D2D30; color: white;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.options_window.setStyleSheet("background-color: #FFFFFF; color: black;")
            self.log_window.setStyleSheet("background-color: #FFFFFF; color: black;")


if __name__ == '__main__':
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
