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

from PyQt5.QtWidgets import *
import sys


class Window(QWidget):

    """
    Class that enables the user a graphical interface to change pso algorithm options, select the
    function and dimension
    """
    def __init__(self):
        super(Window, self).__init__()
        self.options_label = QLabel("Options")
        self.options_label.setStyleSheet("font: 14pt Times New Roman")

        separators = []

        for i in range(12):
            s = QFrame()
            s.setFrameShape(QFrame.HLine)
            s.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            s.setLineWidth(1)
            separators.append(s)

        h1 = QHBoxLayout()
        self.default_npart = QRadioButton("Use default (30)")
        self.default_npart.setChecked(True)
        self.other_npart = QRadioButton("Other")
        self.npart_input = QLineEdit()
        self.npart_input.setDisabled(True)
        self.npart_group = QButtonGroup()
        self.npart_group.addButton(self.default_npart)
        self.npart_group.addButton(self.other_npart)
        h1.addWidget(self.other_npart)
        h1.addWidget(self.npart_input)

        self.other_npart.toggled.connect(lambda: self.npart_input.setDisabled(False))
        self.default_npart.toggled.connect(lambda: self.npart_input.setDisabled(True))

        h2 = QHBoxLayout()
        self.default_niter = QRadioButton("Use default (100)")
        self.default_niter.setChecked(True)
        self.other_niter = QRadioButton("Other")
        self.niter_input = QLineEdit()
        self.niter_input.setDisabled(True)
        self.niter_group = QButtonGroup()
        self.niter_group.addButton(self.default_niter)
        self.niter_group.addButton(self.other_niter)
        h2.addWidget(self.other_niter)
        h2.addWidget(self.niter_input)

        self.other_niter.toggled.connect(lambda: self.niter_input.setDisabled(False))
        self.default_niter.toggled.connect(lambda: self.niter_input.setDisabled(True))

        h3 = QHBoxLayout()
        self.default_ind_best = QRadioButton("Use default (2.5 and 0.5)")
        self.default_ind_best.setChecked(True)
        self.other_ind_best = QRadioButton("Other")
        self.ind_best_start_input = QLineEdit()
        self.ind_best_start_input.setPlaceholderText("initial (cpi)")
        self.ind_best_end_input = QLineEdit()
        self.ind_best_end_input.setPlaceholderText("final (cpf)")
        self.ind_best_start_input.setDisabled(True)
        self.ind_best_end_input.setDisabled(True)
        self.in_best_group = QButtonGroup()
        self.in_best_group.addButton(self.default_ind_best)
        self.in_best_group.addButton(self.other_ind_best)
        h3.addWidget(self.other_ind_best)
        h3.addWidget(self.ind_best_start_input)
        h3.addWidget(self.ind_best_end_input)

        self.other_ind_best.toggled.connect(lambda: self.ind_best_start_input.setDisabled(False))
        self.other_ind_best.toggled.connect(lambda: self.ind_best_end_input.setDisabled(False))
        self.default_ind_best.toggled.connect(lambda: self.ind_best_start_input.setDisabled(True))
        self.default_ind_best.toggled.connect(lambda: self.ind_best_end_input.setDisabled(True))

        h4 = QHBoxLayout()
        self.default_global_best = QRadioButton("Use default (0.5 and 2.5)")
        self.default_global_best.setChecked(True)
        self.other_global_best = QRadioButton("Other")
        self.global_best_start_input = QLineEdit()
        self.global_best_start_input.setPlaceholderText("initial (cgi)")
        self.global_best_end_input = QLineEdit()
        self.global_best_end_input.setPlaceholderText("final (cgf)")
        self.global_best_start_input.setDisabled(True)
        self.global_best_end_input.setDisabled(True)
        self.global_best_group = QButtonGroup()
        self.global_best_group.addButton(self.default_global_best)
        self.global_best_group.addButton(self.other_global_best)
        h4.addWidget(self.other_global_best)
        h4.addWidget(self.global_best_start_input)
        h4.addWidget(self.global_best_end_input)

        self.other_global_best.toggled.connect(lambda: self.global_best_start_input.setDisabled(False))
        self.other_global_best.toggled.connect(lambda: self.global_best_end_input.setDisabled(False))
        self.default_global_best.toggled.connect(lambda: self.global_best_start_input.setDisabled(True))
        self.default_global_best.toggled.connect(lambda: self.global_best_end_input.setDisabled(True))

        h5 = QHBoxLayout()
        self.default_inertia = QRadioButton("Use default (0.9 and 0.4)")
        self.default_inertia.setChecked(True)
        self.other_inertia = QRadioButton("Other")
        self.inertia_start_input = QLineEdit()
        self.inertia_start_input.setPlaceholderText("initial (wi)")
        self.inertia_end_input = QLineEdit()
        self.inertia_end_input.setPlaceholderText("final (wf)")
        self.inertia_start_input.setDisabled(True)
        self.inertia_end_input.setDisabled(True)
        self.inertia_group = QButtonGroup()
        self.inertia_group.addButton(self.default_inertia)
        self.inertia_group.addButton(self.other_inertia)
        h5.addWidget(self.other_inertia)
        h5.addWidget(self.inertia_start_input)
        h5.addWidget(self.inertia_end_input)

        self.other_inertia.toggled.connect(lambda: self.inertia_start_input.setDisabled(False))
        self.other_inertia.toggled.connect(lambda: self.inertia_end_input.setDisabled(False))
        self.default_inertia.toggled.connect(lambda: self.inertia_start_input.setDisabled(True))
        self.default_inertia.toggled.connect(lambda: self.inertia_end_input.setDisabled(True))

        h6 = QHBoxLayout()
        self.default_v_max = QRadioButton("Use default (inf)")
        self.default_v_max.setChecked(True)
        self.other_v_max = QRadioButton("Other")
        self.v_max_input = QLineEdit()
        self.v_max_input.setDisabled(True)
        self.v_max_group = QButtonGroup()
        self.v_max_group.addButton(self.default_v_max)
        self.v_max_group.addButton(self.other_v_max)
        h6.addWidget(self.other_v_max)
        h6.addWidget(self.v_max_input)

        self.other_v_max.toggled.connect(lambda: self.v_max_input.setDisabled(False))
        self.default_v_max.toggled.connect(lambda: self.v_max_input.setDisabled(True))

        h7 = QHBoxLayout()
        self.default_init_offset = QRadioButton("Use default (0)")
        self.default_init_offset.setChecked(True)
        self.other_init_offset = QRadioButton("Other")
        self.init_offset_input = QLineEdit()
        self.init_offset_input.setDisabled(True)
        self.init_offset_group = QButtonGroup()
        self.init_offset_group.addButton(self.default_init_offset)
        self.init_offset_group.addButton(self.other_init_offset)
        h7.addWidget(self.other_init_offset)
        h7.addWidget(self.init_offset_input)

        self.default_init_offset.toggled.connect(lambda: self.init_offset_input.setDisabled(True))
        self.other_init_offset.toggled.connect(lambda: self.init_offset_input.setDisabled(False))

        h8 = QHBoxLayout()
        self.default_init_span = QRadioButton("Use default (1)")
        self.default_init_span.setChecked(True)
        self.other_init_span = QRadioButton("Other")
        self.init_span_input = QLineEdit()
        self.init_span_input.setDisabled(True)
        self.init_span_group = QButtonGroup()
        self.init_span_group.addButton(self.default_init_span)
        self.init_span_group.addButton(self.other_init_span)
        h8.addWidget(self.other_init_span)
        h8.addWidget(self.init_span_input)

        self.default_init_span.toggled.connect(lambda: self.init_span_input.setDisabled(True))
        self.other_init_span.toggled.connect(lambda: self.init_span_input.setDisabled(False))

        h9 = QHBoxLayout()
        self.default_vspan = QRadioButton("Use default (1)")
        self.other_vspan = QRadioButton("Other")
        self.default_vspan.setChecked(True)
        self.vspan_input = QLineEdit()
        self.vspan_input.setDisabled(True)
        h9.addWidget(self.other_vspan)
        h9.addWidget(self.vspan_input)

        self.default_vspan.toggled.connect(lambda: self.vspan_input.setDisabled(True))
        self.other_vspan.toggled.connect(lambda: self.vspan_input.setDisabled(False))

        h10 = QHBoxLayout()
        self.plot_box = QCheckBox("Plot")
        self.log_box = QCheckBox("Log")
        h10.addWidget(self.plot_box)
        h10.addWidget(self.log_box)

        self.combo_box = QComboBox()
        self.combo_box.addItem("Ackley")
        self.combo_box.addItem("Griewank")
        self.combo_box.addItem("Michalewicz")
        self.combo_box.addItem("Easom")

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(2)
        self.spin_box.setMaximum(10)
        self.spin_box.setValue(10)

        v_box = QVBoxLayout()

        v_box.addWidget(self.options_label)
        v_box.addWidget(separators[0])

        v_box.addWidget(QLabel("Function"))
        v_box.addWidget(self.combo_box)
        v_box.addWidget(separators[10])

        v_box.addWidget(QLabel("Dimension"))
        v_box.addWidget(self.spin_box)
        v_box.addWidget(separators[11])

        v_box.addWidget(QLabel("Number of particles"))
        v_box.addWidget(self.default_npart)
        v_box.addLayout(h1)
        v_box.addWidget(separators[1])

        v_box.addWidget(QLabel("Number of iterations"))
        v_box.addWidget(self.default_niter)
        v_box.addLayout(h2)
        v_box.addWidget(separators[2])

        v_box.addWidget(QLabel("Initial and final value of individual best acceleration factor"))
        v_box.addWidget(self.default_ind_best)
        v_box.addLayout(h3)
        v_box.addWidget(separators[3])

        v_box.addWidget(QLabel("Initial and final value of global best acceleration factor"))
        v_box.addWidget(self.default_global_best)
        v_box.addLayout(h4)
        v_box.addWidget(separators[4])

        v_box.addWidget(QLabel("Initial and final value of inertia factor"))
        v_box.addWidget(self.default_inertia)
        v_box.addLayout(h5)
        v_box.addWidget(separators[5])

        v_box.addWidget(QLabel("Absolute speed limit"))
        v_box.addWidget(self.default_v_max)
        v_box.addLayout(h6)
        v_box.addWidget(separators[6])

        v_box.addWidget(QLabel("Offset of the initial population"))
        v_box.addWidget(self.default_init_offset)
        v_box.addLayout(h7)
        v_box.addWidget(separators[7])

        v_box.addWidget(QLabel("Span of the initial population"))
        v_box.addWidget(self.default_init_span)
        v_box.addLayout(h8)
        v_box.addWidget(separators[8])

        v_box.addWidget(QLabel("Initial velocity span"))
        v_box.addWidget(self.default_vspan)
        v_box.addLayout(h9)
        v_box.addWidget(separators[9])

        v_box.addWidget(QLabel("Other options"))
        v_box.addLayout(h10)

        self.setLayout(v_box)
        self.setStyleSheet("font: 10pt Times New Roman")

        self.setWindowTitle("Function optimization using PSO")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
