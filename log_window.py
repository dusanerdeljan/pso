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

from PyQt5.Qt import *
import sys


class LogWindow(QWidget):
    """
    Class that contains an area for pso algorithm output to be displayed, as well as
    run and clear buttons.
    """
    def __init__(self):
        super(LogWindow, self).__init__()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.clear_btn = QPushButton("Clear")
        self.run_btn = QPushButton("Run")

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setWidget(self.text_area)

        v_box = QVBoxLayout()
        v_box.addWidget(self.text_area)
        h1 = QHBoxLayout()
        h1.addWidget(self.run_btn)
        h1.addWidget(self.clear_btn)
        v_box.addLayout(h1)
        self.setLayout(v_box)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LogWindow()
    sys.exit(app.exec_())
