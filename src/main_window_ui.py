# Form implementation generated from reading ui file '.\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(786, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.iteration_time_label = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.iteration_time_label.sizePolicy().hasHeightForWidth()
        )
        self.iteration_time_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.iteration_time_label.setFont(font)
        self.iteration_time_label.setText("")
        self.iteration_time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.iteration_time_label.setObjectName("iteration_time_label")
        self.verticalLayout_3.addWidget(self.iteration_time_label)
        self.canvas = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setText("")
        self.canvas.setObjectName("canvas")
        self.verticalLayout_3.addWidget(self.canvas)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout_3.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.maze_radius_spin_box = QtWidgets.QSpinBox(parent=self.widget)
        self.maze_radius_spin_box.setMinimum(4)
        self.maze_radius_spin_box.setObjectName("maze_radius_spin_box")
        self.gridLayout.addWidget(self.maze_radius_spin_box, 0, 10, 1, 1)
        self.start_button = QtWidgets.QPushButton(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setObjectName("start_button")
        self.gridLayout.addWidget(self.start_button, 0, 3, 1, 1)
        self.rl_algorithm_combo_box = QtWidgets.QComboBox(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rl_algorithm_combo_box.sizePolicy().hasHeightForWidth()
        )
        self.rl_algorithm_combo_box.setSizePolicy(sizePolicy)
        self.rl_algorithm_combo_box.setObjectName("rl_algorithm_combo_box")
        self.rl_algorithm_combo_box.addItem("")
        self.rl_algorithm_combo_box.addItem("")
        self.gridLayout.addWidget(self.rl_algorithm_combo_box, 0, 1, 1, 1)
        self.generate_maze_button = QtWidgets.QPushButton(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.generate_maze_button.sizePolicy().hasHeightForWidth()
        )
        self.generate_maze_button.setSizePolicy(sizePolicy)
        self.generate_maze_button.setObjectName("generate_maze_button")
        self.gridLayout.addWidget(self.generate_maze_button, 0, 7, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem3, 0, 20, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem4, 0, 5, 1, 1)
        self.maze_generator_combo_box = QtWidgets.QComboBox(parent=self.widget)
        self.maze_generator_combo_box.setObjectName("maze_generator_combo_box")
        self.maze_generator_combo_box.addItem("")
        self.maze_generator_combo_box.addItem("")
        self.gridLayout.addWidget(self.maze_generator_combo_box, 0, 6, 1, 1)
        self.verticalLayout_3.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.rl_algorithm_combo_box.setItemText(
            0, _translate("MainWindow", "Q_Learning")
        )
        self.rl_algorithm_combo_box.setItemText(
            1, _translate("MainWindow", "Policy Iteration")
        )
        self.generate_maze_button.setText(_translate("MainWindow", "Generate Maze"))
        self.maze_generator_combo_box.setItemText(
            0, _translate("MainWindow", "Kruskal")
        )
        self.maze_generator_combo_box.setItemText(
            1, _translate("MainWindow", "Recursive Walk")
        )
