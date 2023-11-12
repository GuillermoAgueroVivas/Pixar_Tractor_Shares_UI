#!/sw/bin/python

# This window is the Initial Window of the Farm UI
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import sys
import json
import re
from collections import OrderedDict
from functools import partial
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtWidgets import QApplication

# These are all the other windows being imported
from windowsfarm_window import ui_WindowsFarm_MainWindow
from linuxfarm_window import ui_LinuxFarm_MainWindow


class ui_AtomicCartoonsFarm_MainWindow(object):

    def setupUi(self, main_farm_selection_window):
        """ Does the initial setup. The location of the main Config file and
            where the temp file and backup files will be created are specified here.
            Opens the Config file to be able to generate a list of all the Farm
            sections while formatting the name. Sets the size of the window as
            well as the style of how it looks. Sets the title of the window and
            creates all the fonts utilized by the rest of the windows.

               Parameters:
                   main_farm_selection_window (window): Main generated QMainWindow.
        """

        # These are the location of both the main Config file and where the temp
        # file and backup files will be created

        config_file_path_name = '/sw/tractor/config/limits.config'
        temp_folder = '/sw/tractor/config/tmp/'
        backup_folder = '/sw/tractor/config/limits_backup/'

        # Opening the config file to be able to generate a list with Farm sections.
        with open(config_file_path_name, 'r') as i:
            self.contents_dict = json.load(i, object_pairs_hook=OrderedDict)
            # Gives visual error here but it runs without issues

        # This is needed to translate the Python strings into a 'language' the
        # UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS
        # Creating all fonts
        self.create_fonts()

        # Building all parts of the UI
        farm_sections = self.farm_sections()

        farm_selection_window = \
            self.farm_selection_window_setup(main_farm_selection_window, _translate)

        farm_select_groupBox = self.groupBox_creation(_translate)

        farm_select_comboBox = \
            self.combo_box_creation(_translate, farm_sections, farm_select_groupBox)

        self.label_creation(_translate, farm_select_groupBox)

        self.button_creation(_translate, farm_selection_window,
                             farm_select_groupBox, farm_select_comboBox,
                             config_file_path_name, temp_folder, backup_folder,
                             farm_sections)

        QtCore.QMetaObject.connectSlotsByName(farm_selection_window)

    def create_fonts(self):
        """ Creates the Large and Small fonts used throughout the window.

            Parameters:
                self: Main object.

            Returns:
                l_font (QFont): larger size font used for titles
                s_font (QFont): smaller size font used for everything else.
        """

        self.l_font = QtGui.QFont()  # Larger Font for Titles
        self.l_font.setFamily("Cantarell")
        self.l_font.setPointSize(14)
        self.l_font.setBold(True)
        self.l_font.setItalic(True)
        self.l_font.setUnderline(True)
        self.s_font = QtGui.QFont()  # Smaller Font for most text
        self.s_font.setFamily("Cantarell")
        self.s_font.setPointSize(11)

    def farm_sections(self):
        """ This function generates a list of all farm sections from a given
            dictionary, sorts them in a natural order, and returns the list.

            Parameters:
                self.contents_dict (dict): A dictionary containing all farm
                sections and their contents

            Returns:
                farm_sections (list): A list of all farm sections that match
                the included criteria and are sorted in natural order.
        """

        # This generates a list of all farm sections
        farm_sections = []
        include = ['linuxfarm', '_windowsfarm']
        for farm_section in self.contents_dict['Limits'].keys():
            for word in include:
                if word in farm_section:
                    farm_sections.append(farm_section)  # IMPORTANT

        def check_if_digit(number):
            return int(number) if number.isdigit() else number

        def natural_keys(fs):  # Farm Sections
            return [check_if_digit(number) for number in re.split(r'(\d+)', fs)]

        # Using this to be able to properly sort the farm sections in the correct
        # order.
        farm_sections.sort(key=natural_keys)

        return farm_sections

    def farm_selection_window_setup(self, farm_selection_window, _translate):
        """ This function sets up the farm selection window, including the size,
            style, and title of the window, as well as centering it on the screen.

            Parameters:
                farm_selection_window (QMainWindow): The main window object that
                the function will set up.
                _translate (QTranslator): A function that returns a translated
                version of a string.

            Returns:
                farm_selection_window (QMainWindow): The now set-up main window
                object.
        """

        farm_selection_window.setObjectName("AtomicCartoonsFarmUI_MainWindow")
        # Window Size can be adjusted here
        farm_selection_window.setFixedSize(463, 182)
        # Using this style sheet the theme can be changed
        farm_selection_window.setStyleSheet("background-color: rgb(46, 52, 54);"
                                            "\n""color: rgb(238, 238, 236);")
        # Title of the Main Window can be changed here.
        farm_selection_window.setWindowTitle(_translate(
            "AtomicCartoonsFarmUI_MainWindow", "Main Farm Selection Window"))

        self.centralwidget = QtWidgets.QWidget(farm_selection_window)
        farm_selection_window.setCentralWidget(self.centralwidget)

        # This function centers the Window in the screen according to what
        # monitor the mouse is hovering over
        def center(fsw):  # farm_selection_window
            qr = fsw.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            fsw.move(qr.topLeft())

        center(farm_selection_window)

        return farm_selection_window

    def groupBox_creation(self, _translate):
        """ Creates a group box widget for farm selection.

            Parameters:
                self (QtWidgets.QGroupBox): The class object
                _translate (QTranslator): A function that returns a translated
                version of a string.

            Returns:
                farm_select_groupBox (QtWidgets.QGroupBox): the group box for
                farm selection.
        """
        farm_select_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        farm_select_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 161))
        farm_select_groupBox.setFont(self.l_font)
        # Title of the Group Box
        farm_select_groupBox.setTitle(
            _translate("AtomicCartoonsFarmUI_MainWindow", "Farm Selection"))

        return farm_select_groupBox

    def label_creation(self, _translate, farm_select_groupBox):
        """ Creates a label with specified properties and text.

            Parameters:
                _translate (QTranslator): A function that returns a translated
                version of a string.
                farm_select_groupBox (QGroupBox): group box widget the label
                will be added to.

            Returns:
                farm_select_label (QLabel): the created label widget
        """

        farm_select_label = QtWidgets.QLabel(farm_select_groupBox)
        farm_select_label.setGeometry(QtCore.QRect(10, 40, 421, 61))
        farm_select_label.setFont(self.s_font)
        farm_select_label.setWordWrap(True)
        farm_select_label.setObjectName("farm_select_label")
        # Text inside the label can be changed here
        farm_select_label.setText(
            _translate("AtomicCartoonsFarmUI_MainWindow",
                       "Utilizing the dropdown menu below, please select the "
                       "portion of the Farm you would like to configure and then "
                       "confirm your choice:"))

        return farm_select_label

    def combo_box_creation(self, _translate, farm_sections, farm_select_groupBox):
        """ Creates a QComboBox widget and adds items to it from the given
            farm sections list

            Parameters:
                _translate (QTranslator): A function that returns a translated
                version of a string.
                farm_sections (list): List of farm sections to be added as items
                to the combo box.
                farm_select_groupBox (QGroupBox): The groupbox where the combo
                box will be added

            Returns:
                farm_select_comboBox (QComboBox): The created and configured
                combo box widget
        """

        farm_select_comboBox = QtWidgets.QComboBox(farm_select_groupBox)
        farm_select_comboBox.setGeometry(QtCore.QRect(10, 120, 201, 22))
        farm_select_comboBox.setFont(self.s_font)
        farm_select_comboBox.setObjectName("farm_select_comboBox")
        # The color of the box can be changed here.
        farm_select_comboBox.setStyleSheet('color : #A7F432')

        # Creating all the slots to be allocated in the Combo Box as well as
        # adding the titles
        index = 0
        for farm_section in farm_sections:
            farm_select_comboBox.addItem("")
            if 'linux' in farm_section:
                capital_name = farm_section.capitalize()
                farm_select_comboBox.setItemText(
                    index, _translate("AtomicCartoonsFarmUI_MainWindow",
                                      capital_name))
                index += 1
            else:
                capital_name = farm_section.split('_')
                capital_name = capital_name[1].capitalize()
                farm_select_comboBox.setItemText(
                    index, _translate("AtomicCartoonsFarmUI_MainWindow",
                                      capital_name))
                index += 1

        return farm_select_comboBox

    def button_creation(self, _translate, farm_selection_window,
                        farm_select_groupBox, farm_select_comboBox,
                        config_file_path_name, temp_folder, backup_folder,
                        farm_sections):
        """Create and set up the button for confirming the farm selection

            Parameters:
                _translate (QTranslator): A function that returns a translated
                version of a string.
                farm_selection_window (QtWidgets.QMainWindow): the parent window
                for the button.
                farm_select_groupBox (QtWidgets.QGroupBox): the group box
                containing the button.
                farm_select_comboBox (QtWidgets.QComboBox): the combo box where
                the selection is made.
                config_file_path_name (str): path and name of the config file
                temp_folder (str): path of the temp folder
                backup_folder (str): path of the backup folder
                farm_sections (list): these are all the farm sections coming
                from the config file itself

           Returns:
               farm_select_pushButton (QtWidgets.QPushButton): the created button
        """

        farm_select_pushButton = QtWidgets.QPushButton(farm_select_groupBox)
        farm_select_pushButton.setGeometry(QtCore.QRect(250, 120, 171, 22))
        farm_select_pushButton.setFont(self.s_font)
        farm_select_pushButton.setObjectName("farm_select_pushButton")
        # Text inside the button can be changed here
        farm_select_pushButton.setText(
            _translate("AtomicCartoonsFarmUI_MainWindow", "Confirm My Selection"))

        # IMPORTANT: This is what happens when the button is pressed to confirm selection
        # Opening the other windows according to the selection of the Combo Box
        def farm_select_button_clicked(cb):  # Combo Box
            current = cb.currentText()
            if 'linux' in current.lower():

                linux_farm_sections = []

                for section in farm_sections:
                    # Doing only linux since we want the option to 'apply all the
                    # same values across the board' just for the Linux Farm.
                    if "windows" not in section:
                        linux_farm_sections.append(section)

                self.open_LinuxFarm_window(current.lower(),
                                           config_file_path_name, temp_folder,
                                           backup_folder, linux_farm_sections)
            elif 'windows' in current.lower():
                self.open_WindowsFarm_window('_{}'.format(current.lower()),
                                             config_file_path_name, temp_folder,
                                             backup_folder)

        farm_select_pushButton.clicked.connect(partial(farm_select_button_clicked,
                                                       farm_select_comboBox))

        farm_select_pushButton.clicked.connect(farm_selection_window.close)

    def open_WindowsFarm_window(self, farm_name, config_file_path_name,
                                temp_folder, backup_folder):

        """ This function creates a new window for the Windows farm and sets up
            its UI.

            Parameters:
                farm_name (str): The name of the Windows farm
                config_file_path_name (str): The path of the config file
                temp_folder (str): The path of the temp folder
                backup_folder (str): The path of the backup folder

            Returns:
                None (Creates a new window)
        """
        self.windowsFarm_window = QtWidgets.QMainWindow()
        self.ui = ui_WindowsFarm_MainWindow()
        self.ui.setupUi(self.windowsFarm_window, farm_name,
                        config_file_path_name, temp_folder, backup_folder)
        self.windowsFarm_window.show()

    def open_LinuxFarm_window(self, farm_name, config_file_path_name,
                              temp_folder, backup_folder, linux_farm_sections):

        """ This function creates a new window for the Linux farm and sets up its UI.

            Parameters:
                farm_name (str): The name of the Linux farm
                config_file_path_name (str): The path of the config file
                temp_folder (str): The path of the temp folder
                backup_folder (str): The path of the backup folder
                linux_farm_sections (list): all Linux Farm sections currently in
                the config file.

            Returns:
                None (Creates a new window)
        """
        self.linuxFarm_window = QtWidgets.QMainWindow()
        self.ui = ui_LinuxFarm_MainWindow()
        self.ui.setupUi(self.linuxFarm_window, farm_name, config_file_path_name,
                        temp_folder, backup_folder, linux_farm_sections)
        self.linuxFarm_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    atomic_farm_selection_window = QtWidgets.QMainWindow()
    ui = ui_AtomicCartoonsFarm_MainWindow()
    ui.setupUi(atomic_farm_selection_window)
    atomic_farm_selection_window.show()
    sys.exit(app.exec_())
