#!/sw/bin/python

# This is the Changes Confirmation window of the Atomic Farm UI. Helps the user
# see the changes to be made before they are applied.

# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json
from functools import partial
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import QApplication
from changes_applied_window import Ui_changesApplied_MainWindow

class ui_confirmFarmChanges_MainWindow(object):

    # Window Main Settings
    def setupUi(self, confirmFarmChanges_MainWindow, current_values_dict,
                new_values_dict, current_values_cap_dict, new_hard_values_dict,
                farm_name, contents_dict, config_file_path_name, temp_folder,
                backup_folder, linux_check, farm_sections):
        """ Sets up the UI for the Confirm Farm Changes window.

            Parameters:
                confirmFarmChanges_MainWindow (QtWidgets.QMainWindow): The main
                window object for the "Confirm Farm Changes" window.
                current_values_dict (dict): A dictionary containing the current
                values.
                new_values_dict (dict): A dictionary containing the new values.
                current_values_cap_dict (dict): A dictionary containing the
                current hard cap values.
                new_hard_values_dict (dict): A dictionary containing the new
                hard cap values.
                farm_name (str): The name of the farm.
                contents_dict (dict): A dictionary containing the contents.
                config_file_path_name (str): The path and name of the config file.
                temp_folder (str): The path of the temporary folder.
                backup_folder (str): The path of the backup folder.

            Returns:
                None
        """

        # Farm name coming from the other windows
        self.farm_name = farm_name
        self.contents_dict = contents_dict

        # This is needed to translate the Python strings into a 'language'
        # the UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS
        # Creating all fonts
        self.create_fonts()

        changes_confirmation_window = self.changes_confirmation_window_setup(
            confirmFarmChanges_MainWindow, _translate)

        # Main Group Box creation which then contains all other items in the UI.
        changes_confirmation_groupBox = self.groupBox_creation(_translate)
        # All the following functions create all the different parts of the UI
        # inside the Group Box above.
        self.label_creation(_translate, changes_confirmation_groupBox)
        self.textBrowser_creation(_translate, changes_confirmation_groupBox,
                                  current_values_dict, current_values_cap_dict,
                                  new_values_dict, new_hard_values_dict)
        self.button_creation(_translate, changes_confirmation_window,
                             changes_confirmation_groupBox, config_file_path_name,
                             temp_folder, backup_folder, new_values_dict,
                             new_hard_values_dict, linux_check, farm_sections)

        QtCore.QMetaObject.connectSlotsByName(confirmFarmChanges_MainWindow)

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

    def changes_confirmation_window_setup(self, confirmFarmChanges_MainWindow,
                                          _translate):
        """ Sets up the Changes Confirmation Window.

            Parameters:
                confirmFarmChanges_MainWindow (QtWidgets.QMainWindow): The main
                window object for the changes_confirmation_window.
                _translate (function): The translation function for translating strings.

            Returns:
                QtWidgets.QMainWindow: The main window object for the changes_
                _confirmation_window.
        """

        confirmFarmChanges_MainWindow.setObjectName("confirmFarmChanges_MainWindow")
        # Window Size can be adjusted here
        confirmFarmChanges_MainWindow.setFixedSize(463, 349)
        # Using this style sheet the theme can be changed
        confirmFarmChanges_MainWindow.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(confirmFarmChanges_MainWindow)
        # Title of the Main Window can be changed here.
        confirmFarmChanges_MainWindow.setWindowTitle(
            _translate("confirmFarmChanges_MainWindow",
                       "Changes Confirmation Window"))
        confirmFarmChanges_MainWindow.setCentralWidget(self.centralwidget)

        def center(confirmFarmChanges_MainWindow):
            qr = confirmFarmChanges_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            confirmFarmChanges_MainWindow.move(qr.topLeft())

        center(confirmFarmChanges_MainWindow)

        return confirmFarmChanges_MainWindow

    def groupBox_creation(self, _translate):
        """ Creates a group box for reviewing changes.

            Parameters:
                _translate (function): The translation function for translating strings.

            Returns:
                changes_confirmation_groupBox (QtWidgets.QGroupBox): The created
                group box for reviewing changes.
        """

        changes_confirmation_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        changes_confirmation_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 331))
        changes_confirmation_groupBox.setFont(self.l_font)
        # Title of the Group Box
        changes_confirmation_groupBox.setTitle(
            _translate("confirmFarmChanges_MainWindow", "Review Your Changes"))

        return changes_confirmation_groupBox

    def label_creation(self, _translate, changes_confirmation_groupBox):
        """ Creates labels inside the main group box

            Parameters:
                _translate (function): The translation function used for
                label text.
                changes_confirmation_groupBox (QGroupBox): The group box object.

            Returns:
                None
        """

        review_changes_label = QtWidgets.QLabel(changes_confirmation_groupBox)
        review_changes_label.setGeometry(QtCore.QRect(10, 40, 421, 61))
        review_changes_label.setFont(self.s_font)
        review_changes_label.setWordWrap(True)
        review_changes_label.setObjectName("review_changes_label")
        # Text inside the label can be changed here
        review_changes_label.setText(
            _translate("confirmFarmChanges_MainWindow",
                       "Please take a close look below to compare the changes you "
                       "have made against the previous settings before you "
                       "fully apply them:"))

        before_label = QtWidgets.QLabel(changes_confirmation_groupBox)
        before_label.setGeometry(QtCore.QRect(10, 110, 61, 20))
        before_label.setFont(self.l_font)
        before_label.setWordWrap(True)
        before_label.setObjectName("before_label")
        before_label.setStyleSheet('color : #D21404')
        before_label.setText(_translate("confirmFarmChanges_MainWindow",
                                        "Before:"))

        after_label = QtWidgets.QLabel(changes_confirmation_groupBox)
        after_label.setGeometry(QtCore.QRect(230, 110, 51, 20))
        after_label.setFont(self.l_font)
        after_label.setWordWrap(True)
        after_label.setObjectName("after_label")
        after_label.setStyleSheet('color : #A7F432')
        after_label.setText(_translate("confirmFarmChanges_MainWindow",
                                       "After:"))

    def textBrowser_creation(self, _translate, changes_confirmation_groupBox,
                             current_values_dict, current_values_cap_dict,
                             new_values_dict, new_hard_values_dict):

        """ Creates text browsers to display values before and after changes.

            Parameters:
                _translate (function): The translation function for translating
                strings.
                changes_confirmation_groupBox (QtWidgets.QGroupBox): The group
                box where the text browsers will be placed.
                current_values_dict (dict): A dictionary containing the current
                values.
                current_values_cap_dict (dict): A dictionary containing the
                current hard cap values.
                new_values_dict (dict): A dictionary containing the new values.
                new_hard_values_dict (dict): A dictionary containing the new
                hard cap values.

            Returns:
                None
        """

        # Sorted dictionaries
        sorted_current_values_dict = dict(
            sorted(current_values_dict.items()))
        sorted_current_values_cap_dict = dict(
            sorted(current_values_cap_dict.items()))

        before_textBrowser = QtWidgets.QTextBrowser(changes_confirmation_groupBox)
        before_textBrowser.setGeometry(QtCore.QRect(10, 140, 141, 131))
        before_textBrowser.setFont(self.s_font)
        before_textBrowser.setReadOnly(True)
        before_textBrowser.setObjectName("before_textBrowser")
        # This is how the shows are displayed in the Text Browser
        before_textBrowser.append('Nominal:\n')
        for show, percentage in sorted_current_values_dict.items():
            before_textBrowser.append('{}: {}%'.format(show, percentage))
        before_textBrowser.append('\nHard Cap:\n')
        for show, percentage in sorted_current_values_cap_dict.items():
            before_textBrowser.append('{}: {}%'.format(show, percentage))

        before_textBrowser.horizontalScrollBar().setValue(0)

        # Sorted dictionaries
        sorted_new_values_dict = dict(sorted(new_values_dict.items()))
        sorted_new_hard_values_dict = dict(sorted(new_hard_values_dict.items()))

        after_textBrowser = QtWidgets.QTextBrowser(changes_confirmation_groupBox)
        after_textBrowser.setGeometry(QtCore.QRect(230, 140, 141, 131))
        after_textBrowser.setFont(self.s_font)
        after_textBrowser.setReadOnly(True)
        after_textBrowser.setObjectName("after_textBrowser")
        # This is how the shows are displayed in the Text Browser
        after_textBrowser.append('Nominal:\n')
        for show, percentage in sorted_new_values_dict.items():
            after_textBrowser.append('{}: {}%'.format(show, percentage))
        after_textBrowser.append('\nHard Cap:\n')
        for show, percentage in sorted_new_hard_values_dict.items():
            after_textBrowser.append('{}: {}%'.format(show, percentage))

    def button_creation(self, _translate, changes_confirmation_window,
                        changes_confirmation_groupBox, config_file_path_name,
                        temp_folder, backup_folder, new_values_dict,
                        new_hard_values_dict, linux_check, farm_sections):

        """ Creates buttons for staging changes and canceling the operation.

            Parameters:
                _translate (function): The translation function for translating
                strings.
                changes_confirmation_window (QtWidgets.QMainWindow): The window.
                changes_confirmation_groupBox (QtWidgets.QGroupBox): The group
                box where the buttons will be placed.
                config_file_path_name (str): The path to the configuration file.
                temp_folder (str): The path to the temporary folder.
                backup_folder (str): The path to the backup folder.
                new_values_dict (dict): A dictionary containing the new values.
                new_hard_values_dict (dict): A dictionary containing the new
                hard cap values.

            Returns:
                None
        """

        tmpFile_pushButton = QtWidgets.QPushButton(changes_confirmation_groupBox)
        tmpFile_pushButton.setGeometry(QtCore.QRect(160, 300, 121, 22))
        tmpFile_pushButton.setFont(self.s_font)
        tmpFile_pushButton.setObjectName("tmpFile_pushButton")
        tmpFile_pushButton.setText(_translate("confirmFarmChanges_MainWindow",
                                              "Stage"))

        # config_file_path_name, temp_folder, backup_folder, new_values_dict,
        # new_hard_values_dict
        def tmp_pushButton_clicked(cfpn, tf, bf, nvd, nhvd):

            tmp_file_name = '{}temp.config'.format(tf)

            for show, percentage in nvd.items():
                self.contents_dict['Limits'][self.farm_name]['Shares'][show]['nominal'] = \
                    round(percentage / 100, 3)

            for show, percentage in nhvd.items():
                self.contents_dict['Limits'][self.farm_name]['Shares'][show]['cap'] = \
                    round(percentage / 100, 3)

            json.dump(self.contents_dict, open(tmp_file_name, mode='w'), indent=4)

            self.changesApplied_window = QtWidgets.QMainWindow()
            self.ui = Ui_changesApplied_MainWindow()
            self.ui.setupUi(self.changesApplied_window, cfpn, self.contents_dict,
                            tmp_file_name, bf, nvd, self.farm_name)
            self.changesApplied_window.show()

        tmpFile_pushButton.clicked.connect(
            partial(tmp_pushButton_clicked, config_file_path_name, temp_folder,
                    backup_folder, new_values_dict, new_hard_values_dict))

        tmpFile_pushButton.setStyleSheet('color: yellow')
        tmpFile_pushButton.clicked.connect(changes_confirmation_window.close)

        if linux_check:

            applyToAll_pushButton = QtWidgets.QPushButton(changes_confirmation_groupBox)
            # Takes in the y-axis created by the GroupBox Creation minus 30
            applyToAll_pushButton.setGeometry(
                QtCore.QRect(10, 300, 121, 22))

            applyToAll_pushButton.setFont(self.s_font)
            applyToAll_pushButton.setObjectName("applyToAll_pushButton")
            # Name can be changed here
            applyToAll_pushButton.setText(_translate("linuxFarm_mainWindow",
                                                     "Stage All"))

            # config_file_path_name, temp_folder, backup_folder, new_values_dict,
            # new_hard_values_dict, linux_farm_sections
            def applyToAll_pushButton_clicked(cfpn, tf, bf, nvd, nhvd, lfs):

                tmp_file_name = '{}temp.config'.format(tf)

                for section in lfs:

                    for show, percentage in nvd.items():
                        self.contents_dict['Limits'][section]['Shares'][show][
                            'nominal'] = \
                            round(percentage / 100, 3)

                    for show, percentage in nhvd.items():
                        self.contents_dict['Limits'][section]['Shares'][show][
                            'cap'] = \
                            round(percentage / 100, 3)

                json.dump(self.contents_dict, open(tmp_file_name, mode='w'), indent=4)

                self.changesApplied_window = QtWidgets.QMainWindow()
                self.ui = Ui_changesApplied_MainWindow()
                self.ui.setupUi(self.changesApplied_window, cfpn, self.contents_dict,
                                tmp_file_name, bf, nvd, self.farm_name)
                self.changesApplied_window.show()

            applyToAll_pushButton.clicked.connect(
                partial(applyToAll_pushButton_clicked, config_file_path_name,
                        temp_folder, backup_folder, new_values_dict,
                        new_hard_values_dict, farm_sections))

            applyToAll_pushButton.setStyleSheet('color: orange')
            applyToAll_pushButton.clicked.connect(changes_confirmation_window.close)

        cancel_pushButton = QtWidgets.QPushButton(changes_confirmation_groupBox)
        cancel_pushButton.setGeometry(QtCore.QRect(310, 300, 121, 22))
        cancel_pushButton.setFont(self.s_font)
        cancel_pushButton.setObjectName("cancel_pushButton")
        cancel_pushButton.setText(_translate("confirmFarmChanges_MainWindow",
                                             "Cancel"))
        cancel_pushButton.clicked.connect(self.cancel_button_clicked)
        cancel_pushButton.clicked.connect(changes_confirmation_window.close)

    def cancel_button_clicked(self):
        from main_farm_selection_window import ui_AtomicCartoonsFarm_MainWindow
        self.farm_selection_window = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsFarm_MainWindow()
        self.ui.setupUi(self.farm_selection_window)
        self.farm_selection_window.show()


