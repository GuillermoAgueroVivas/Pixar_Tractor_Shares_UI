#!/sw/bin/python

# This window opens up when selected through the 'Farm_Selection_Window' of
# the Atomic Farm UI.
# Represents the Linux Farm section selected in the previous window.
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


class ui_LinuxFarm_MainWindow(object):
    # Creates main interface for everything else to live on
    def setupUi(self, LinuxFarmUI_MainWindow, farm_name, config_file_path_name,
                temp_folder, backup_folder, linux_farm_sections):

        """ Sets up UI of the LinuxFarmUI_MainWindow by loading data from a
            configuration file and initializing all UI elements.

            Parameters:
                LinuxFarmUI_MainWindow (QWidget): The main window object.
                farm_name (str): The name of the farm inside the
                configuration file.
                config_file_path_name (str): The path and name of the
                configuration file.
                temp_folder (str): The path of the temporary folder.
                backup_folder (str): The path of the backup folder.
                linux_farm_sections (list): all Linux Farm sections currently in
                the config file.

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

        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS

        self.create_fonts()
        shows = self.get_shows()
        linuxFarm_mainWindow = self.linux_farm_window_setup(
            LinuxFarmUI_MainWindow, _translate)

        # Main Group Box creation which then contains all other items in the UI.
        linuxFarm_groupBox, cleaned_name = self.groupBox_creation(_translate)
        spinBoxes_list, spinBoxes_hardcap_list, current_values_full_dict, \
        current_values_cap_full_dict = self.groupBox_info_creation(
            _translate, shows, linuxFarm_mainWindow, linuxFarm_groupBox)

        self.info_label_creation(_translate, linuxFarm_groupBox, cleaned_name)

        self.button_creation(_translate, shows, linuxFarm_mainWindow,
                             linuxFarm_groupBox, spinBoxes_list,
                             spinBoxes_hardcap_list,
                             current_values_full_dict, current_values_cap_full_dict,
                             config_file_path_name, temp_folder, backup_folder,
                             linux_farm_sections)

        # Upper Menu
        self.upper_menu_creation(linuxFarm_mainWindow, _translate)
        QtCore.QMetaObject.connectSlotsByName(linuxFarm_mainWindow)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles
                s_font (QFont): smaller size font used for everything else.
        """

        # FONTS
        self.l_font = QtGui.QFont()  # Larger Font for Titles
        self.l_font.setFamily("Cantarell")
        self.l_font.setPointSize(14)
        self.l_font.setBold(True)
        self.l_font.setItalic(True)
        self.l_font.setUnderline(True)
        self.m_font = QtGui.QFont()  # Medium text with bold and underline for
        # smaller titles
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
        avoid = ['default', 'MollyOfDenali', 'NightAtTheMuseum', 'RND']
        for key in self.contents_dict['Limits'][self.farm_name]['Shares'].keys():
            if all(word not in key for word in avoid):
                shows.append(key)

        return shows

    def linux_farm_window_setup(self, linuxFarm_mainWindow, _translate):
        """ Sets up the main window of the Windows Farm application.

            Parameters:
                linuxFarm_mainWindow (QtWidgets.QMainWindow): The main
                window widget of the application.
                _translate (function): The function to translate Python
                strings into a 'language' the PyQt UI understands.

            Returns:
                LinuxFarmUI_MainWindow (QtWidgets.QMainWindow): The main
                window widget of the application.
        """

        self.y_axis_window_size = 390  # Initial window height 390
        # Window Size can be adjusted here
        linuxFarm_mainWindow.setFixedSize(740, self.y_axis_window_size)
        linuxFarm_mainWindow.setObjectName("LinuxFarmUI_MainWindow")
        # Using this style sheet the theme can be changed
        linuxFarm_mainWindow.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(linuxFarm_mainWindow)
        # This is needed to translate the Python strings into a 'language' the

        # Title of the Main Window can be changed here.
        linuxFarm_mainWindow.setWindowTitle(_translate("LinuxFarmUI_MainWindow",
                                                       "Linux Farm Window"))
        linuxFarm_mainWindow.setCentralWidget(self.centralwidget)

        def center(LinuxFarmUI_MainWindow):
            qr = LinuxFarmUI_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            LinuxFarmUI_MainWindow.move(qr.topLeft())

        center(linuxFarm_mainWindow)

        return linuxFarm_mainWindow

    def groupBox_creation(self, _translate):
        """ Creates a Group Box widget within the main window to hold all the UI
            elements related to the Linux Farm.

            Parameters:
                self (object): instance of a class.
                _translate (function): translation function.
                box after cleaning up the farm_name.

            Returns:
                linuxFarm_groupBox (QGroupBox): the created group box.
        """

        linuxFarm_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        linuxFarm_groupBox.setGeometry(QtCore.QRect(10, 10, 721, 348))
        linuxFarm_groupBox.setFont(self.l_font)
        linuxFarm_groupBox.setObjectName("linuxFarm_groupBox")

        # Title of the Group Box

        def cleaning_up_name(farm_name):
            """ Static method that cleans up a farm name by capitalizing the
                first letter of each word and removing underscores, and adding a
                space between the word "farm" and any number that follows it.

                Parameters:
                    farm_name (str): The name of the farm to be cleaned up.

                Returns:
                    new_name (str): The cleaned up name of the farm.
            """

            new_name = re.split('(farm)', farm_name)
            if new_name[2]:
                number = new_name[2]
                number = number.replace('_', '')
                new_name = new_name[0].capitalize() + ' ' + new_name[
                    1].capitalize() + ' ' + number
            else:
                new_name = new_name[0].capitalize() + ' ' + new_name[1].capitalize()
            return new_name

        cleaned_name = cleaning_up_name(self.farm_name)
        linuxFarm_groupBox.setTitle(
            _translate("LinuxFarmUI_MainWindow", cleaned_name))

        return linuxFarm_groupBox, cleaned_name

    def groupBox_info_creation(self, _translate, shows, linuxFarm_mainWindow,
                               linuxFarm_groupBox):

        """ This function adjusts the size and position of the group box and
            creates sliders and spin boxes for each show.

            Parameters:
                _translate (function): A function used to translate text in the UI.
                shows (list): A list of shows to create sliders and spin
                boxes for.
                linuxFarm_mainWindow (QtWidgets.QMainWindow): The main window
                of the program.
                linuxFarm_groupBox (QtWidgets.QGroupBox): The group box
                containing the sliders and spin boxes.

            Returns:
                spinBoxes_list (list): A list of spin boxes created for each show.
                spinBoxes_hardcap_list (list): A list of spin boxes created for
                each show with a maximum value.
                current_values_full_dict (dict): A dictionary containing the
                current percentage value for each slider.
                current_values_cap_full_dict (dict): A dictionary containing the
                current percentage value for each slider with a maximum value.
        """

        y_axis_value = 70
        sliders_list = []
        spinBoxes_list = []
        spinBoxes_hardcap_list = []
        current_values_full_dict = dict()
        current_values_cap_full_dict = dict()

        # These are all the show labels inside the Group Box
        def label_creation(_translate, show, y_axis_value):
            """ Creates a QLabel object with the provided show title and sets its
                properties.

                Parameters:
                    _translate (function): Translation function for the label text.
                    show (str): The title of the show.
                    y_axis_value (int): The y-axis value where the label will
                    be created.

                Returns:
                    label (QLabel): The QLabel object created
            """

            # Tests
            l_case_show = show.lower()
            label = QtWidgets.QLabel(linuxFarm_groupBox)
            label.setGeometry(QtCore.QRect(270, y_axis_value, 35, 20))
            label.setFont(self.m_font)
            label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
            label.setScaledContents(False)
            label.setWordWrap(True)
            label.setObjectName("{}_label".format(l_case_show))
            label.setText(_translate("LinuxFarmUI_MainWindow", show))

            return label

        # Creating all spin boxes
        def spin_box_creation(linuxFarm_groupBox, show, y_axis_value):
            """ Creates two QDoubleSpinBoxes for a show and its hard cap value

                Parameters:
                    show (str): name of the show
                    y_axis_value (int): y-axis value for positioning
                    the spin boxes

                Returns:
                    spinBox (QDoubleSpinBox): QDoubleSpinBox for the
                    show
                    hardCapSpinBox (QDoubleSpinBox): QDoubleSpinBox
                    for the hard cap value of the show
            """
            minimum = 0
            maximum = 100

            l_case_show = show.lower()
            spinBox = QtWidgets.QDoubleSpinBox(linuxFarm_groupBox)
            spinBox.setGeometry(QtCore.QRect(570, y_axis_value, 57, 22))
            spinBox.setFont(self.s_font)
            spinBox.setObjectName("{}_spinBox".format(l_case_show))
            spinBox.setDecimals(1)
            spinBox.setMinimum(minimum)
            spinBox.setMaximum(maximum)

            hardCap_spinBox = QtWidgets.QDoubleSpinBox(linuxFarm_groupBox)
            hardCap_spinBox.setGeometry(QtCore.QRect(640, y_axis_value, 60, 22))
            hardCap_spinBox.setFont(self.s_font)
            hardCap_spinBox.setObjectName(
                "{}_hardCap_spinBox".format(l_case_show))
            hardCap_spinBox.setDecimals(1)
            hardCap_spinBox.setMinimum(minimum)
            hardCap_spinBox.setMaximum(maximum)

            return spinBox, hardCap_spinBox

        # Creating all sliders
        def sliders_creation(linuxFarm_groupBox, show, y_axis_value):
            """ Creates a horizontal slider widget and sets its properties.

                Parameters:
                    show (str): A string representing the name of the
                    slider.
                    y_axis_value (int): An integer representing the
                    y-axis value of the slider.

                Returns:
                    slider (QSlider): A horizontal slider widget with
                    a specified range and name.
            """

            # Minimum and Maximum for all sliders
            minimum = 0
            maximum = 100
            # Setting up
            l_case_show = show.lower()
            slider = QtWidgets.QSlider(linuxFarm_groupBox)
            slider.setGeometry(
                QtCore.QRect(310, y_axis_value, 251, 20))  # Location in window
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
                    spin_box (QSpinBox): the spin box to be connected to the slider.
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

        for show in shows:
            label_creation(_translate, show, y_axis_value)
            spin_box, hardCap_spinBox = spin_box_creation(linuxFarm_groupBox,
                                                          show, y_axis_value)
            slider = sliders_creation(linuxFarm_groupBox, show, y_axis_value)
            # Connecting all sliders to their Spin Boxes and vice versa
            connect_parts(spin_box, slider)
            # Getting current Percentages per show to be able to pass it to the
            # Confirmation Window
            current_values_full_dict, current_values_cap_full_dict = \
                self.current_values_show(
                    show, slider, spin_box, hardCap_spinBox,
                    current_values_full_dict,
                    current_values_cap_full_dict)

            sliders_list.append(slider)
            spinBoxes_list.append(spin_box)
            spinBoxes_hardcap_list.append(hardCap_spinBox)
            y_axis_value = y_axis_value + 40

        # If the size of the y-axis being used to create all the sliders,
        # labels and boxes is greater than the window size minus 50 then it
        # increases the size of both the Window and
        # the groupbox.

        if y_axis_value > (self.y_axis_window_size - 50):
            while y_axis_value > (self.y_axis_window_size - 50):
                self.y_axis_window_size = self.y_axis_window_size + 35  # 90
                linuxFarm_mainWindow.setFixedSize(740, self.y_axis_window_size)

            self.y_axis_window_size = self.y_axis_window_size - 42
            linuxFarm_groupBox.setGeometry(
                QtCore.QRect(10, 10, 721, self.y_axis_window_size))

        return spinBoxes_list, spinBoxes_hardcap_list, current_values_full_dict, \
               current_values_cap_full_dict

    def current_values_show(self, show, slider, spinbox, spinbox_hardcap,
                            current_values_full_dict, current_values_cap_full_dict):
        """ Function to update the current percentage values for the nominal and
            hard cap for a given show.

            Parameters:
                show (str): The show name.
                slider (QSlider): The slider for the nominal percentage.
                spinbox (QSpinBox): The spin box for the nominal percentage.
                spinbox_hardcap (QSpinBox): The spin box for the hard cap
                percentage.
                current_values_full_dict (dict): The dictionary of
                current nominal percentage values for all farm shares.
                current_values_cap_full_dict (dict): The dictionary of
                current hard cap percentage values for all farm shares.

            Returns:
                current_values_full_dict (dict): The updated dictionary
                of current nominal percentage values for all farm shares.
                current_values_cap_full_dict (dict): The updated
                dictionary of current hard cap percentage values for all
                farm shares.
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

    # These are all the info labels inside the Group Box
    def info_label_creation(self, _translate, linuxFarm_groupBox, cleaned_name):
        """ Creates and sets text for various labels in the
            WindowsFarmUI_MainWindow.

            Parameters:
                _translate (function): function used for translating text to the
                appropriate language
                cleaned_name (str): the name to be displayed on the group
                box after cleaning up the farm_name.
                linuxFarm_groupBox (QtWidgets.QGroupBox): the group box
                that contains the labels

            Returns:
                None
        """

        # Main Definition label
        linux_def_label = QtWidgets.QLabel(linuxFarm_groupBox)
        linux_def_label.setGeometry(QtCore.QRect(10, 50, 191, 71))
        linux_def_label.setFont(self.s_font)
        linux_def_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        linux_def_label.setScaledContents(False)
        linux_def_label.setWordWrap(True)
        linux_def_label.setObjectName("linux_def_label")

        if self.farm_name == 'linuxfarm':
            linux_def_label.setText(
                _translate("LinuxFarmUI_MainWindow",
                           "To the right side you will see a list of all current "
                           "working shows in the Linux Farm as a whole."))
        else:
            linux_def_label.setText(
                _translate("LinuxFarmUI_MainWindow",
                           "To the right side you will see a list of all current "
                           "working shows in the {} section.".format(cleaned_name)))

        # Second Definition Label
        linux_def_sliders_label = QtWidgets.QLabel(linuxFarm_groupBox)
        linux_def_sliders_label.setGeometry(QtCore.QRect(10, 140, 201, 81))
        linux_def_sliders_label.setFont(self.s_font)
        linux_def_sliders_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        linux_def_sliders_label.setScaledContents(False)
        linux_def_sliders_label.setWordWrap(True)
        linux_def_sliders_label.setObjectName("linux_def_sliders_label")

        linux_def_sliders_label.setText(
            _translate("LinuxFarmUI_MainWindow",
                       "Utilizing the available sliders, please select "
                       "how much allocation each show should be receiving: "))

        # Nominal and Hard Cap labels
        nominal_label = QtWidgets.QLabel(linuxFarm_groupBox)
        nominal_label.setGeometry(QtCore.QRect(410, 40, 61, 20))
        nominal_label.setFont(self.m_font)
        nominal_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        nominal_label.setScaledContents(False)
        nominal_label.setWordWrap(True)
        nominal_label.setObjectName("nominal_label")
        nominal_label.setStyleSheet('color: yellow')
        nominal_label.setText(_translate("LinuxFarmUI_MainWindow", "Nominal"))

        cap_label = QtWidgets.QLabel(linuxFarm_groupBox)
        cap_label.setGeometry(QtCore.QRect(636, 40, 71, 20))
        cap_label.setFont(self.m_font)
        cap_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        cap_label.setScaledContents(False)
        cap_label.setWordWrap(True)
        cap_label.setObjectName("cap_label")
        cap_label.setStyleSheet('color: yellow')
        cap_label.setText(_translate("LinuxFarmUI_MainWindow", "Hard Cap"))

    # Creates Submit and Cancel button
    def button_creation(self, _translate, shows, linuxFarm_mainWindow,
                        linuxFarm_groupBox, spinBoxes_list,
                        spinBoxes_hardcap_list, current_values_full_dict,
                        current_values_cap_full_dict, config_file_path_name,
                        temp_folder, backup_folder, linux_farm_sections):

        """ Creates and sets up the Submit and Cancel buttons. The Submit button
            does a check to see if the values add up to 100 and creates new
            dictionaries with the new values. The Cancel button returns the user
            to the previous window.

            Parameters:
                self (object): The current instance of the class.
                _translate (function): A function that translates text to
                the specified language.
                shows (list): A list of shows to be displayed.
                linuxFarm_mainWindow (object): The instance of the
                linuxFarm_mainWindow class that the button is being
                created in.
                linuxFarm_groupBox (object): The instance of the groupBox
                that the buttons are being added to.
                spinBoxes_list (list): A list of QSpinBoxes that the user
                will input values into.
                spinBoxes_hardcap_list (list): A list of QSpinBoxes for
                setting hardcap values.
                current_values_full_dict (dict): A dictionary containing
                the current values for each show.
                current_values_cap_full_dict (dict): A dictionary
                containing the current hardcap values for each show.
                config_file_path_name (str): The file path and name for
                the configuration file.
                temp_folder (str): The file path to the temporary folder.
                backup_folder (str): The file path to the backup folder.
                linux_farm_sections (list): all Linux Farm sections currently in
                the config file.

            Returns:
                None
        """

        submit_pushButton = QtWidgets.QPushButton(linuxFarm_groupBox)
        # Takes in the y-axis created by the GroupBox Creation minus 30
        submit_pushButton.setGeometry(
            QtCore.QRect(510, (linuxFarm_groupBox.frameGeometry().height()
                               - 30), 91, 22))

        submit_pushButton.setFont(self.s_font)
        submit_pushButton.setObjectName("submit_pushButton")
        submit_pushButton.setText(_translate("linuxFarm_mainWindow",
                                             "Submit"))  # Name can be changed here

        # Runs when submit button is clicked
        # config_file_path_name, temp_folder, backup_folder, linux_farm_sections
        def submit_button_clicked(spinBoxes, spinBoxes_hardcap, shows,
                                  linuxFarm_groupBox, cfpn, tf, bf, lfs):
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
                error_label = QtWidgets.QLabel(linuxFarm_groupBox)

                error_label.setGeometry(QtCore.QRect(10, (
                        linuxFarm_groupBox.frameGeometry().height() - 30), 350, 20))

                error_label.setFont(self.s_font)
                error_label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
                error_label.setScaledContents(False)
                error_label.setWordWrap(True)
                error_label.setObjectName("error_label")
                error_label.setStyleSheet('color: red')
                error_label.setText(
                    _translate("linuxFarm_mainWindow",
                               "The newly set values do not add up to 100! "
                               "Try again."))
                error_label.show()

            else:
                new_values_dict = dict(zip(shows, new_values_list))
                new_hard_values_dict = dict(zip(shows, new_hard_values_list))
                self.changesConfirmation_window = QtWidgets.QMainWindow()
                self.ui = ui_confirmFarmChanges_MainWindow()

                # This check is needed for the following window to choose whether
                # to display the "Stage All" button or not
                linux_check = True

                self.ui.setupUi(self.changesConfirmation_window,
                                current_values_full_dict, new_values_dict,
                                current_values_cap_full_dict,
                                new_hard_values_dict, self.farm_name,
                                self.contents_dict, cfpn, tf, bf, linux_check,
                                lfs)

                linuxFarm_mainWindow.close()
                self.changesConfirmation_window.show()

        submit_pushButton.clicked.connect(
            partial(submit_button_clicked, spinBoxes_list, spinBoxes_hardcap_list,
                    shows, linuxFarm_groupBox, config_file_path_name,
                    temp_folder, backup_folder, linux_farm_sections))

        cancel_pushButton = QtWidgets.QPushButton(linuxFarm_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(
            620, (linuxFarm_groupBox.frameGeometry().height() - 30), 91, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        cancel_pushButton.setText(_translate("linuxFarm_mainWindow",
                                             "Cancel"))  # Name can be changed here

        cancel_pushButton.clicked.connect(self.cancel_button_clicked)
        cancel_pushButton.clicked.connect(linuxFarm_mainWindow.close)

    # Runs when the 'cancel' button is clicked
    def cancel_button_clicked(self):
        from main_farm_selection_window import ui_AtomicCartoonsFarm_MainWindow
        self.farm_selection_windows = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsFarm_MainWindow()
        self.ui.setupUi(self.farm_selection_windows)
        self.farm_selection_windows.show()

    # Creating the upper menu
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
        self.menuLoad_Setup.setTitle(
            _translate("LinuxFarmUI_MainWindow", "Load Setup"))
        self.menubar.addAction(self.menuLoad_Setup.menuAction())

        self.actionSelect_file_to_load = QtWidgets.QAction(UI)
        self.actionSelect_file_to_load.setFont(self.s_font)
        self.actionSelect_file_to_load.setAutoRepeat(True)
        self.actionSelect_file_to_load.setObjectName("actionSelect_file_to_load")
        self.actionSelect_file_to_load.setText(
            _translate("LinuxFarmUI_MainWindow", "Select File to Load"))
        self.menuLoad_Setup.addAction(self.actionSelect_file_to_load)

