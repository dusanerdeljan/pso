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


class MainWindow(QMainWindow):
    """
    Class that combines options windows and log window.
    """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.options_window = Window()
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setWidget(self.options_window)

        self.docked = QDockWidget("Log window", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.log_window = LogWindow()
        self.docked.setWidget(self.log_window)
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

    def create_options(self):

        npart = 0
        niter = 0
        cpi = 0
        cpf = 0
        cgi = 0
        cgf = 0
        wi = 0
        wf = 0
        vmax = 0
        initoffset = 0
        initspan = 0
        vspan = 0

        plot = self.options_window.plot_box.isChecked()
        log = self.options_window.log_box.isChecked()
        dimension = self.options_window.spin_box.value()
        if self.options_window.default_npart.isChecked():
            npart = 30
        else:
            npart = int(self.options_window.npart_input.text())

        if self.options_window.default_niter.isChecked():
            niter = 100
        else:
            niter = int(self.options_window.niter_input.text())

        if self.options_window.default_ind_best.isChecked():
            cpi = 2.5
            cpf = 0.5
        else:
            cpi = float(self.options_window.ind_best_start_input.text())
            cpf = float(self.options_window.ind_best_end_input.text())

        if self.options_window.default_global_best.isChecked():
            cgi = 0.5
            cgf = 2.5
        else:
            cgi = float(self.options_window.global_best_start_input.text())
            cgf = float(self.options_window.global_best_end_input.text())

        if self.options_window.default_inertia.isChecked():
            wi = 0.9
            wf = 0.4
        else:
            wi = float(self.options_window.inertia_start_input.text())
            wf = float(self.options_window.inertia_end_input.text())

        if self.options_window.default_v_max.isChecked():
            vmax = inf
        else:
            vmax = int(self.options_window.v_max_input.text())

        if self.options_window.default_init_offset.isChecked():
            initoffset = 0
        else:
            initoffset = int(self.options_window.init_offset_input.text())

        if self.options_window.default_init_span.isChecked():
            initspan = 1
        else:
            initspan = int(self.options_window.init_span_input.text())

        if self.options_window.default_vspan.isChecked():
            vspan = 1
        else:
            vspan = int(self.options_window.vspan_input.text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
