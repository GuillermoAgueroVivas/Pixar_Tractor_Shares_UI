#!/sw/bin/python

# This window opens up when selected through the 'Farm_Selection_Window' of the
# Atomic Farm UI.
# Represents the Windows Farm as a whole.
# Created using PyQt5.
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json
import os
import re
from collections import OrderedDict
from functools import partial
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtWidgets import QApplication
from changes_confirmation_window import ui_confirmFarmChanges_MainWindow

class ui_WindowsFarm_MainWindow(object):

    def setupUi(self, WindowsFarmUI_MainWindow, farm_name, config_file_path_name,
                temp_folder, backup_folder):

        """ Sets up UI of the WindowsFarmUI_MainWindow by loading data from a
            configuration file and initializing all UI elements.

            Parameters:
                WindowsFarmUI_MainWindow (QWidget): The main window object.
                farm_name (str): The name of the farm inside the configuration file.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path of the temporary folder.
                backup_folder (str): The path of the backup folder.

            Returns:
                None.
        """

        # THIS IS IMPORTANT : This is the current name of this farm inside the
        # config file.
        self.farm_name = farm_name

        if os.path.exists(temp_folder + 'temp.config'):
            # Opening config file
            with open(temp_folder + 'temp.config', 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
        else:
            # Opening config file
            with open(config_file_path_name, 'r') as i:
                self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)

        # This is needed to translate the Python strings into a 'language' the
        # UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        shows = self.get_shows()
        windowsfarm_window = self.windowsfarm_window_setup(
            WindowsFarmUI_MainWindow, _translate)
        windowsfarm_groupBox = self.groupBox_creation(_translate)

        spinBoxes_list, spinBoxes_hardcap_list, current_values_full_dict, \
        current_values_cap_full_dict = self.groupBox_info_creation(
            _translate, shows, windowsfarm_window, windowsfarm_groupBox)

        self.info_label_creation(_translate, windowsfarm_groupBox)
        self.button_creation(_translate, shows, windowsfarm_window,
                             windowsfarm_groupBox, spinBoxes_list,
                             spinBoxes_hardcap_list, current_values_full_dict,
                             current_values_cap_full_dict, config_file_path_name,
                             temp_folder, backup_folder)

        # Upper Menu
        self.upper_menu_creation(windowsfarm_window, _translate)
        QtCore.QMetaObject.connectSlotsByName(windowsfarm_window)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles.
                s_font (QFont): smaller size font used for everything else.
        """

        self.l_font = QtGui.QFont()  # Larger Font for Titles
        self.l_font.setFamily("Cantarell")
        self.l_font.setPointSize(14)
        self.l_font.setBold(True)
        self.l_font.setItalic(True)
        self.l_font.setUnderline(True)
        # Medium text with bold and underline for smaller titles
        self.m_font = QtGui.QFont()
        self.m_font.setFamily("Cantarell")
        self.m_font.setPointSize(11)
        self.m_font.setBold(True)
        self.m_font.setUnderline(True)
        self.s_font = QtGui.QFont()  # Smaller Font for most text
        self.s_font.setFamily("Cantarell")
        self.s_font.setPointSize(11)

    def get_shows(self):
        """ Generates a list of show names that the farm has access to.

                Returns: shows (list): A list of show names
        """

        # This generates a list of all shows for this farm
        shows = []
        avoid = ['default']
        for key in self.contents_dict['Limits'][self.farm_name]['Shares'].keys():
            if all(word not in key for word in avoid):
                shows.append(key)

        return shows

    def windowsfarm_window_setup(self, WindowsFarmUI_MainWindow, _translate):
        """ Sets up the main window of the Windows Farm application.

            Parameters:
                WindowsFarmUI_MainWindow (QtWidgets.QMainWindow): The main
                window widget of the application.
                _translate (function): The function to translate Python strings
                into a 'language' the PyQt UI understands.

            Returns:
                WindowsFarmUI_MainWindow (QtWidgets.QMainWindow): The main
                window widget of the application.
        """

        self.y_axis_window_size = 390  # Initial window height 515
        # Window Size can be adjusted here
        WindowsFarmUI_MainWindow.setFixedSize(740, self.y_axis_window_size)
        WindowsFarmUI_MainWindow.setObjectName("WindowsFarmUI_MainWindow")
        # Using this style sheet the theme can be changed
        WindowsFarmUI_MainWindow.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(WindowsFarmUI_MainWindow)

        # Title of the Main Window can be changed here.
        WindowsFarmUI_MainWindow.setWindowTitle(
            _translate("WindowsFarmUI_MainWindow", "Windows Farm Window"))
        WindowsFarmUI_MainWindow.setCentralWidget(self.centralwidget)

        def center(WindowsFarmUI_MainWindow):
            """ Centers the main window of the WindowsFarmUI_MainWindow object to
                the center of the screen.

                Parameters:
                    WindowsFarmUI_MainWindow (object): The main window of the
                    WindowsFarmUI.

                Returns:
                    None.
            """

            qr = WindowsFarmUI_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            WindowsFarmUI_MainWindow.move(qr.topLeft())

        center(WindowsFarmUI_MainWindow)

        return WindowsFarmUI_MainWindow

    def groupBox_creation(self, _translate):
        """ Creates a Group Box widget within the main window to hold all
            the UI elements related to the Windows Farm.

            Parameters:
                _translate (PyQt function): a function that translates Python
                strings into a format readable by PyQt UI elements.

            Returns:
                windowsFarm_groupBox (PyQt widget): a Group Box widget that
                holds all the UI elements related to the Windows Farm
        """

        windowsFarm_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        windowsFarm_groupBox.setGeometry(QtCore.QRect(10, 10, 721, 348))
        windowsFarm_groupBox.setFont(self.l_font)
        windowsFarm_groupBox.setObjectName("windowsFarm_groupBox")
        # Title of the Group Box
        windowsFarm_groupBox.setTitle(_translate("WindowsFarmUI_MainWindow",
                                                 "Windows Farm"))

        return windowsFarm_groupBox

    def groupBox_info_creation(self, _translate, shows, windowsfarm_window,
                               windowsFarm_groupBox):

        """ This function adjusts the size and position of the group box and
            creates sliders and spin boxes for each show.

            Parameters:
                _translate (function): A function used to translate text in the UI
                shows (list): A list of shows to create sliders and spin boxes for
                windowsfarm_window (QtWidgets.QMainWindow): The main window of
                the program.
                windowsFarm_groupBox (QtWidgets.QGroupBox): The group box
                containing the sliders and spin boxes.

            Returns:
                spinBoxes_list (list): A list of spin boxes created for each show
                spinBoxes_hardcap_list (list): A list of spin boxes created for
                each show with a maximum value.
                current_values_full_dict (dict): A dictionary containing the
                current percentage value for each slider.
                current_values_cap_full_dict (dict): A dictionary containing the
                current percentage value for each slider with a maximum value.
        """

        labels_y_axis_value = 70
        slider_box_y_axis_value = 100
        sliders_list = []
        spinBoxes_list = []
        spinBoxes_hardcap_list = []
        current_values_full_dict = dict()
        current_values_cap_full_dict = dict()

        def label_creation(_translate, show, labels_y_axis_value):
            """ Creates a QLabel object with the provided show title and sets
                its properties.

                Parameters:
                    _translate (function): Translation function for the label
                    text.
                    show (str): The title of the show
                    labels_y_axis_value (int): The y-axis value where the label
                    will be created.

                Returns:
                    label (QLabel): The QLabel object created
            """

            label = QtWidgets.QLabel(windowsFarm_groupBox)
            label.setGeometry(QtCore.QRect(270, labels_y_axis_value, 180, 20))
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)
            spaced_out_label = re.sub(r"(\w)([A-Z])", r"\1 \2", show)
            label.setText(_translate("WindowsFarmUI_MainWindow",
                                     spaced_out_label))

            return label

        def spin_box_creation(show, slider_box_y_axis_value):
            """ Creates two QDoubleSpinBoxes for a show and its hard cap value

                Parameters:
                    show (str): name of the show
                    slider_box_y_axis_value (int): y-axis value for positioning
                    the spin boxes.

                Returns:
                    spinBox (QDoubleSpinBox): QDoubleSpinBox for the show
                    hardCapSpinBox (QDoubleSpinBox): QDoubleSpinBox for the
                    hard cap value of the show.
            """

            # Minimum and Maximum for all spin boxes
            minimum = 0
            maximum = 100

            l_case_show = show.lower()
            spinBox = QtWidgets.QDoubleSpinBox(windowsFarm_groupBox)
            spinBox.setGeometry(QtCore.QRect(570, slider_box_y_axis_value, 57, 22))
            spinBox.setFont(self.s_font)
            spinBox.setObjectName("{}_spinBox".format(l_case_show))
            spinBox.setDecimals(1)
            spinBox.setMinimum(minimum)
            spinBox.setMaximum(maximum)

            hardCapSpinBox = QtWidgets.QDoubleSpinBox(windowsFarm_groupBox)
            hardCapSpinBox.setGeometry(QtCore.QRect(
                640, slider_box_y_axis_value, 60, 22))
            hardCapSpinBox.setFont(self.s_font)
            hardCapSpinBox.setObjectName("{}_hardCapSpinBox".format(l_case_show))
            hardCapSpinBox.setDecimals(1)
            hardCapSpinBox.setMinimum(minimum)
            hardCapSpinBox.setMaximum(maximum)

            return spinBox, hardCapSpinBox

        def sliders_creation(show, slider_box_y_axis_value):
            """ Creates a horizontal slider widget and sets its properties.

                Parameters:
                    show (str): A string representing the name of the slider.
                    slider_box_y_axis_value (int): An integer representing the
                    y-axis value of the slider.

                Returns:
                    slider (QSlider): A horizontal slider widget with a specified
                    range and name.
            """

            # Minimum and Maximum for all sliders
            minimum = 0
            maximum = 100
            # Setting up
            l_case_show = show.lower()
            slider = QtWidgets.QSlider(windowsFarm_groupBox)
            slider.setGeometry(QtCore.QRect(270, slider_box_y_axis_value, 251, 20))
            slider.setTracking(True)
            slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
            slider.setObjectName("{}_slider".format(l_case_show))
            slider.setMinimum(minimum)
            slider.setMaximum(maximum)

            return slider

        def connect_parts(spin_box, slider):
            """ Connects a Spin Box and Slider in PyQt5 to update each other's
                values.

                Parameters:
                    spin_box (QSpinBox): the spin box to be connected to the
                    slider.
                    slider (QSlider): the slider to be connected to the spin box.

                Returns:
                    None
            """
            def _update_slider(slide, value):
                slide.setValue(value)

            def _update_box(box, value):
                box.setValue(value)

            spin_box.valueChanged.connect(partial(_update_slider, slider))
            slider.valueChanged.connect(partial(_update_box, spin_box))

        # This "for" loop individually sets-up every single show in the list of shows.
        for show in shows:

            label_creation(_translate, show, labels_y_axis_value)

            spin_box, hardCap_spinBox = spin_box_creation(
                show, slider_box_y_axis_value)

            slider = sliders_creation(show, slider_box_y_axis_value)
            # Connecting all sliders to their Spin Boxes and vice versa
            connect_parts(spin_box, slider)

            # Getting current Percentages per show to be able to pass it to the
            # Confirmation Window
            current_values_full_dict, current_values_cap_full_dict = \
                self.current_values_show(show, slider, spin_box, hardCap_spinBox,
                                         current_values_full_dict,
                                         current_values_cap_full_dict)

            sliders_list.append(slider)
            spinBoxes_list.append(spin_box)
            spinBoxes_hardcap_list.append(hardCap_spinBox)
            labels_y_axis_value = labels_y_axis_value + 60
            slider_box_y_axis_value = slider_box_y_axis_value + 60

        # If the size of the y-axis being used to create all the sliders,
        # labels and boxes is greater than the window size minus 50 then it
        # increases the size of both the Window and the groupbox.

        if labels_y_axis_value > (self.y_axis_window_size - 50):
            self.y_axis_window_size = self.y_axis_window_size + 120
            windowsfarm_window.setFixedSize(740, self.y_axis_window_size)
            self.y_axis_window_size = self.y_axis_window_size - 42
            windowsFarm_groupBox.setGeometry(
                QtCore.QRect(10, 10, 721, self.y_axis_window_size))

        return spinBoxes_list, spinBoxes_hardcap_list, \
               current_values_full_dict, current_values_cap_full_dict

    def current_values_show(self, show, slider, spinbox, spinbox_hardcap,
                            current_values_full_dict,
                            current_values_cap_full_dict):

        """ Function to update the current percentage values for the nominal
            and hard cap for a given show.

            Parameters:
                show (str): The show name.
                slider (QSlider): The slider for the nominal percentage.
                spinbox (QSpinBox): The spin box for the nominal percentage.
                spinbox_hardcap (QSpinBox): The spin box for the hard cap
                percentage.
                current_values_full_dict (dict): The dictionary of current
                nominal percentage values for all farm shares.
                current_values_cap_full_dict (dict): The dictionary of current
                hard cap percentage values for all farm shares.

            Returns:
                current_values_full_dict (dict): The updated dictionary of
                current nominal percentage values for all farm shares.
                current_values_cap_full_dict (dict): The updated dictionary of
                current hard cap percentage values for all farm shares.
        """

        # Nominal
        current_value = \
            self.contents_dict['Limits'][self.farm_name]['Shares'][show]['nominal']
        current_perc = round(current_value * 100, 1)
        slider.setValue(current_perc)
        spinbox.setValue(current_perc)
        current_values_full_dict.update({show: current_perc})
        # Hard Cap
        current_cap_value = \
            self.contents_dict['Limits'][self.farm_name]['Shares'][show]['cap']
        current_cap_perc = round(current_cap_value * 100, 1)
        spinbox_hardcap.setValue(current_cap_perc)
        current_values_cap_full_dict.update({show: current_cap_perc})

        return current_values_full_dict, current_values_cap_full_dict

    def info_label_creation(self, _translate, windowsfarm_groupBox):
        """ Creates and sets text for various labels in the
            WindowsFarmUI_MainWindow.

            Parameters:
                _translate (function): function used for translating text to
                the appropriate language
                windowsfarm_groupBox (QtWidgets.QGroupBox): the group box that
                contains the labels.

            Returns:
                None
        """

        # Main Definition label
        window_def_label = QtWidgets.QLabel(windowsfarm_groupBox)
        window_def_label.setGeometry(QtCore.QRect(10, 50, 191, 71))
        window_def_label.setFont(self.s_font)
        window_def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        window_def_label.setScaledContents(False)
        window_def_label.setWordWrap(True)
        window_def_label.setObjectName("window_def_label")
        window_def_label.setText(
            _translate("WindowsFarmUI_MainWindow",
                       "To the right side you will see a list of all current "
                       "working shows in the Windows Farm as a whole."))

        # Second Definition Label
        window_def_sliders_label = QtWidgets.QLabel(windowsfarm_groupBox)
        window_def_sliders_label.setGeometry(QtCore.QRect(10, 140, 201, 81))
        window_def_sliders_label.setFont(self.s_font)
        window_def_sliders_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        window_def_sliders_label.setScaledContents(False)
        window_def_sliders_label.setWordWrap(True)
        window_def_sliders_label.setObjectName("window_def_sliders_label")
        window_def_sliders_label.setText(
            _translate("WindowsFarmUI_MainWindow",
                       "Utilizing the available sliders, please select how much "
                       "allocation each show should be receiving: "))

        # Nominal and Hard Cap labels
        nominal_label = QtWidgets.QLabel(windowsfarm_groupBox)
        nominal_label.setGeometry(QtCore.QRect(410, 40, 61, 20))
        nominal_label.setFont(self.m_font)
        nominal_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        nominal_label.setScaledContents(False)
        nominal_label.setWordWrap(True)
        nominal_label.setObjectName("nominal_label")
        nominal_label.setStyleSheet('color: yellow')
        nominal_label.setText(_translate("WindowsFarmUI_MainWindow", "Nominal"))

        cap_label = QtWidgets.QLabel(windowsfarm_groupBox)
        cap_label.setGeometry(QtCore.QRect(636, 40, 71, 20))
        cap_label.setFont(self.m_font)
        cap_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        cap_label.setScaledContents(False)
        cap_label.setWordWrap(True)
        cap_label.setObjectName("cap_label")
        cap_label.setStyleSheet('color: yellow')
        cap_label.setText(_translate("WindowsFarmUI_MainWindow", "Hard Cap"))

    def button_creation(self, _translate, shows, windowsfarm_window,
                        windowsfarm_groupBox, spinBoxes_list,
                        spinBoxes_hardcap_list, current_values_full_dict,
                        current_values_cap_full_dict, config_file_path_name,
                        temp_folder, backup_folder):

        """ Creates and sets up the Submit and Cancel buttons. The Submit button
            does a check to see if hte values add up to 100 and creates new
            dictionaries with the new values. The Cancel button returns the user
            to the previous window.

            Parameters:
                self (object): The current instance of the class.
                _translate (function): A function that translates text to the
                specified language.
                shows (list): A list of shows to be displayed.
                windowsfarm_window (object): The instance of the
                WindowsFarmUI_MainWindow class that the button is being created in.
                windowsfarm_groupBox (object): The instance of the groupBox
                that the buttons are being added to.
                spinBoxes_list (list): A list of QSpinBoxes that the user will
                input values into.
                spinBoxes_hardcap_list (list): A list of QSpinBoxes for setting
                hardcap values.
                current_values_full_dict (dict): A dictionary containing the
                current values for each show.
                current_values_cap_full_dict (dict): A dictionary containing
                the current hardcap values for each show.
                config_file_path_name (str): The file path and name for the
                configuration file.
                temp_folder (str): The file path to the temporary folder.
                backup_folder (str): The file path to the backup folder.

            Returns:
                None
        """

        submit_pushButton = QtWidgets.QPushButton(windowsfarm_groupBox)
        # Takes in the y-axis created by the GroupBox Creation minus 30
        submit_pushButton.setGeometry(
            QtCore.QRect(510, (windowsfarm_groupBox.frameGeometry().height()
                               - 30), 91, 22))
        submit_pushButton.setFont(self.s_font)
        submit_pushButton.setObjectName("submit_pushButton")
        # Name can be changed here
        submit_pushButton.setText(_translate("WindowsFarmUI_MainWindow",
                                             "Submit"))

        def submit_button_clicked(spinBoxes, spinBoxes_hardcap, shows_list,
                                  windowsFarm_groupBox, cfpn, tf, bf):
            """ Handles the event when the submit button is clicked.

                Parameters:
                    spinBoxes (list): A list of QSpinBox objects representing
                    the input spin boxes.
                    spinBoxes_hardcap (list): A list of QSpinBox objects
                    representing the hard cap spin boxes.
                    shows_list (list): A list of strings representing the shows.
                    windowsFarm_groupBox (QGroupBox): The group box containing
                    the UI elements.
                    cfpn (str): The path and name of the config file.
                    tf (str): The name of the temporary file.
                    bf (str): The name of the backup file.

                Returns:
                    None
            """

            new_values_list = []
            for box in spinBoxes:
                new_value = box.value()
                new_values_list.append(new_value)

            new_hard_values_list = []
            for box in spinBoxes_hardcap:
                new_hard_value = box.value()
                new_hard_values_list.append(new_hard_value)

            big_sum = round(sum(new_values_list), 1)

            if big_sum < 100.0 or big_sum > 100.0:
                error_label = QtWidgets.QLabel(windowsFarm_groupBox)

                error_label.setGeometry(QtCore.QRect(
                    10, (windowsfarm_groupBox.frameGeometry().height()
                         - 30), 350, 20))

                error_label.setFont(self.s_font)
                error_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
                error_label.setScaledContents(False)
                error_label.setWordWrap(True)
                error_label.setObjectName("error_label")
                error_label.setStyleSheet('color: red')
                error_label.setText(_translate("WindowsFarmUI_MainWindow",
                                               "The newly set values do not add "
                                               "up to 100! Try again."))
                error_label.show()

            else:
                new_values_dict = dict(zip(shows_list, new_values_list))
                new_hard_values_dict = dict(zip(shows_list, new_hard_values_list))
                self.changesConfirmation_window = QtWidgets.QMainWindow()
                self.ui = ui_confirmFarmChanges_MainWindow()

                # This check is needed for the following window to choose whether
                # to display the "Stage All" button or not
                linux_check = False
                farm_sections = []

                self.ui.setupUi(self.changesConfirmation_window,
                                current_values_full_dict, new_values_dict,
                                current_values_cap_full_dict, new_hard_values_dict,
                                self.farm_name, self.contents_dict, cfpn, tf, bf,
                                linux_check, farm_sections)

                # Closes this window and then shows the next one
                windowsfarm_window.close()
                self.changesConfirmation_window.show()

        submit_pushButton.clicked.connect(
            partial(submit_button_clicked, spinBoxes_list, spinBoxes_hardcap_list,
                    shows, windowsfarm_groupBox, config_file_path_name,
                    temp_folder, backup_folder))

        cancel_pushButton = QtWidgets.QPushButton(windowsfarm_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(
            620, (windowsfarm_groupBox.frameGeometry().height()
                  - 30), 91, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        # Name can be changed here
        cancel_pushButton.setText(_translate("WindowsFarmUI_MainWindow",
                                             "Cancel"))

        def cancel_button_clicked():
            """ Handles the event when the cancel button is clicked.

                Returns:
                    None
            """

            from main_farm_selection_window import \
                ui_AtomicCartoonsFarm_MainWindow
            self.farm_selection_windows = QtWidgets.QMainWindow()
            self.ui = ui_AtomicCartoonsFarm_MainWindow()
            self.ui.setupUi(self.farm_selection_windows)
            self.farm_selection_windows.show()

        cancel_pushButton.clicked.connect(cancel_button_clicked)
        cancel_pushButton.clicked.connect(windowsfarm_window.close)

    def upper_menu_creation(self, UI, _translate):
        """ Creates the upper menu bar of the main window with options for
            loading a setup file.

            Parameters:
                self (class object): instance of the class
                UI (class object): instance of the main window UI
                _translate (function): function used for translating UI text

            Returns:
                None
        """

        # Main bar at the top
        self.menubar = QtWidgets.QMenuBar(UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 22))
        self.menubar.setFont(self.s_font)
        self.menubar.setObjectName("menubar")
        UI.setMenuBar(self.menubar)

        self.menuLoad_Setup = QtWidgets.QMenu(self.menubar)
        self.menuLoad_Setup.setFont(self.s_font)
        self.menuLoad_Setup.setObjectName("menuLoad_Setup")
        self.menuLoad_Setup.setTitle(_translate("WindowsFarmUI_MainWindow",
                                                "Load Setup"))
        self.menubar.addAction(self.menuLoad_Setup.menuAction())

        self.actionSelect_file_to_load = QtWidgets.QAction(UI)
        self.actionSelect_file_to_load.setFont(self.s_font)
        self.actionSelect_file_to_load.setAutoRepeat(True)
        self.actionSelect_file_to_load.setObjectName("actionSelect_file_to_load")
        self.actionSelect_file_to_load.setText(
            _translate("WindowsFarmUI_MainWindow", "Select File to Load"))
        self.menuLoad_Setup.addAction(self.actionSelect_file_to_load)

