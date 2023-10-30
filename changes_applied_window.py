#!/sw/bin/python

# This is the Changes Applied window of the Atomic Farm UI. Shows message saying
# the changes made have been applied and asks if you would like to do more changes.
# Created using PyQt5
# Please only adjust values if totally sure of what you are doing!
#
# Created by Guillermo Aguero - Render TD

import json
import os
import subprocess
import urllib2
import sys

from time import sleep
from datetime import *
from functools import partial
from qtpy import QtWidgets, QtCore, QtGui
from qtpy.QtWidgets import QApplication


class Ui_changesApplied_MainWindow(object):

    # Window Main Settings
    def setupUi(self, changesApplied_MainWindow, config_file_path_name,
                contents_dict, tmp_file_name, backup_folder,
                new_values_dict, farm_name):
        """ Sets up the user interface of the changesApplied_MainWindow window.

            Parameters:
                self: The object instance.
                changesApplied_MainWindow (QMainWindow): The main window object.
                config_file_path_name (str): The path and name of the config file.
                contents_dict (dict): A dictionary containing the contents of
                the config file.
                tmp_file_name (str): The name of the temporary file.
                backup_folder (str): The folder where backup files are stored.
                new_values_dict (dict): A dictionary containing new values.
                farm_name (str): The name of the farm.

            Returns:
                None
        """

        self.contents_dict = contents_dict

        # the UI from PyQt understands
        _translate = QtCore.QCoreApplication.translate  # DO NOT CHANGE THIS
        # Creating all fonts
        self.create_fonts()

        changes_applied_window = self.changes_applied_window_setup(
            changesApplied_MainWindow, _translate)

        # Main Group Box creation which then contains all other items in the UI.
        changes_applied_groupBox = self.groupBox_creation(_translate)

        self.label_creation(_translate, changes_applied_groupBox)
        self.button_creation(_translate, changesApplied_MainWindow,
                             config_file_path_name, tmp_file_name, backup_folder,
                             new_values_dict, farm_name,
                             changes_applied_groupBox)

        QtCore.QMetaObject.connectSlotsByName(changes_applied_window)

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

    def changes_applied_window_setup(self, changes_applied_window, _translate):
        """ Sets up the changes applied window with the specified properties.
             It sets the object name, window size, style sheet, and window title.

            Parameters:
                changes_applied_window (QMainWindow): The changes applied window
                object.
                _translate (function): The translation function used for window
                title.

            Returns:
                QMainWindow: The changes applied window with the desired setup.
        """

        changes_applied_window.setObjectName("changesApplied_MainWindow")
        # Window Size can be adjusted here
        changes_applied_window.setFixedSize(463, 161)
        # Using this style sheet the theme can be changed
        changes_applied_window.setStyleSheet(
            "background-color: rgb(46, 52, 54);\n""color: rgb(238, 238, 236);")
        self.centralwidget = QtWidgets.QWidget(changes_applied_window)

        # Title of the Main Window can be changed here.
        changes_applied_window.setWindowTitle(
            _translate("changesApplied_MainWindow", "Write File Window"))
        changes_applied_window.setCentralWidget(self.centralwidget)

        def center(changesApplied_MainWindow):
            qr = changesApplied_MainWindow.frameGeometry()
            screen = QApplication.desktop().screenNumber(
                QApplication.desktop().cursor().pos())
            cp = QApplication.desktop().screenGeometry(screen).center()
            qr.moveCenter(cp)
            changesApplied_MainWindow.move(qr.topLeft())

        center(changes_applied_window)

        return changes_applied_window

    def groupBox_creation(self, _translate):
        """ Creates a Group Box widget within the main window to hold all the UI
            elements related to the Changes Applied Window.

            Parameters:
                self (object): instance of a class.
                _translate (function): translation function.

            Returns:
                changes_applied_groupBox (QGroupBox): the created group box.
        """

        changes_applied_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        changes_applied_groupBox.setGeometry(QtCore.QRect(10, 10, 441, 141))
        changes_applied_groupBox.setFont(self.l_font)
        # Title of the Group Box
        changes_applied_groupBox.setTitle(
            _translate("changesApplied_MainWindow", "Write to File Or Make More "
                                                    "Changes"))

        return changes_applied_groupBox

    def label_creation(self, _translate, changes_applied_groupBox):
        """ Creates labels inside the main group box

            Parameters:
                _translate (function): The translation function used for label text.
                changes_applied_groupBox (QGroupBox): The group box object.

            Returns:
                None
        """

        question_label = QtWidgets.QLabel(changes_applied_groupBox)
        question_label.setGeometry(QtCore.QRect(10, 35, 271, 61))
        question_label.setFont(self.s_font)
        question_label.setWordWrap(True)
        question_label.setObjectName("question_label")
        question_label.setText(
            _translate("changesApplied_MainWindow",
                       "Would you like to write to Config File or make more "
                       "changes?"))

    def button_creation(self, _translate, changesApplied_MainWindow,
                        config_file_path_name, tmp_file_name, backup_folder,
                        new_values_dict, farm_name, changes_applied_groupBox):
        """ Creates buttons inside the changes applied group box.

            Parameters:
                _translate (function): The translation function used for button
                text.
                changesApplied_MainWindow (QMainWindow): The main window object.
                config_file_path_name (str): The path and name of the config file.
                tmp_file_name (str): The name of the temporary file.
                backup_folder (str): The path of the backup folder.
                new_values_dict (dict): Dictionary containing new values.
                farm_name (str): The name of the farm.
                changes_applied_groupBox (QGroupBox): The group box object.

            Returns:
                None
        """

        moreChanges_pushButton = QtWidgets.QPushButton(changes_applied_groupBox)
        moreChanges_pushButton.setGeometry(QtCore.QRect(160, 110, 121, 22))
        moreChanges_pushButton.setFont(self.s_font)
        moreChanges_pushButton.setObjectName("moreChanges_pushButton")
        moreChanges_pushButton.setStyleSheet('color : yellow')
        # Text can be changed here
        moreChanges_pushButton.setText(_translate("changesApplied_MainWindow",
                                                  "More Changes"))
        moreChanges_pushButton.clicked.connect(self.moreChanges_button_clicked)
        moreChanges_pushButton.clicked.connect(changesApplied_MainWindow.close)

        exit_pushButton = QtWidgets.QPushButton(changes_applied_groupBox)
        exit_pushButton.setGeometry(QtCore.QRect(310, 110, 121, 22))
        exit_pushButton.setFont(self.s_font)
        exit_pushButton.setObjectName("exit_pushButton")
        exit_pushButton.setStyleSheet('color : #D21404')
        # Text can be changed here
        exit_pushButton.setText(_translate("changesApplied_MainWindow",
                                           "Discard/Exit"))

        def delete_tmp(tmp):
            os.remove(tmp)

        exit_pushButton.clicked.connect(partial(delete_tmp, tmp_file_name))
        exit_pushButton.clicked.connect(changesApplied_MainWindow.close)

        write_button = QtWidgets.QPushButton(changes_applied_groupBox)
        write_button.setGeometry(QtCore.QRect(10, 110, 121, 22))
        write_button.setFont(self.s_font)
        write_button.setObjectName("write_button")
        write_button.setStyleSheet('color : #A7F432')
        # Text can be changed here
        write_button.setText(_translate("changesApplied_MainWindow", "Write"))

        # backup_folder, new_values_dict, farm_name, changes_applied_groupBox
        def write_to_config(cfpn, tmp, contents_dict, bf, nvd, fn):
            """ Writes contents to the config file and performs config file
                reload.

                Parameters:
                    cfpn (str): The path and name of the config file.
                    tmp (str): The name of the temporary file.
                    contents_dict (dict): Dictionary containing the contents to
                    write.
                    bf (str): The path of the backup folder.
                    nvd (dict): Dictionary containing new values.
                    fn (str): The name of the farm.

                Returns:
                    None
            """

            print("The write_to_config() method has started")

            # Creates the Backup file for the config file and then deletes
            # the temporary one used while the tool is running
            if os.path.exists(cfpn):
                backup_file_name = \
                    '{}{}-{}.config'.format(
                        bf, date.today(), datetime.now().strftime("%H:%M:%S"))

                os.rename(cfpn, backup_file_name)
                os.remove(tmp)

            json.dump(contents_dict, open(cfpn, mode='w'), indent=4)
            sleep(5)

            return_code = subprocess.call(['tq', 'reloadconfig', '--limits'])
            if return_code != 0:
                print("Command failed with error code: ", return_code)
                print("Tryin again with os.system()")
                os.system('tq reloadconfig --limits')  # , shell=True
                sleep(10)
            else:
                print("Command executed successfully")

            index = 1

            # Loading website containing the updated '.config' file info
            web_info = urllib2.urlopen(
                "http://tractor-engine/Tractor/queue?q=limits")
            web_info_dict = json.load(web_info)
            print("Config-file website has just been fully loaded!")

            # Iterates through the 'New Values Directory' sent from the
            # previous window and compares every value to those in the
            # 'Tractor Limits' website.
            for show, percentage in nvd.items():

                full_number = float(percentage)
                web_value = float(
                    web_info_dict['Limits'][fn]['Shares'][show]['nominal']) * 100

                web_value = round(web_value, 1)
                print("Show: {}".format(show))
                print("Full Number | Web Value")
                print(full_number, web_value)

                while web_value != full_number:

                    web_info = urllib2.urlopen(
                        "http://tractor-engine/Tractor/queue?q=limits")

                    web_info_dict = json.load(web_info)
                    web_value = float(
                        web_info_dict['Limits'][fn]['Shares'][show][
                            'nominal']) * 100

                    web_value = round(web_value, 1)
                    print("Show: {}".format(show))
                    print("Full Number | Web Value")
                    print(full_number, web_value)

                    index += 1

                    if 1 < index <= 7:

                        return_code = \
                            subprocess.call(['tq', 'reloadconfig', '--limits'])

                        print("Amount of config-reloads: {}".format(index))

                        sleep(10)
                        if return_code != 0:
                            print("Command failed with error code: ", return_code)
                            print("Trying again with os.system()")
                            os.system('tq reloadconfig --limits')  # , shell=True
                            sleep(10)
                        else:
                            print("Command executed successfully")


                    elif index == 8:
                        print "The Config was reloaded too many times before " \
                              "this change could be properly applied. " \
                              "Attempt to reload manually."
                        sys.exit()

        write_button.clicked.connect(
            partial(write_to_config, config_file_path_name, tmp_file_name,
                    self.contents_dict, backup_folder, new_values_dict, farm_name))

        write_button.clicked.connect(changesApplied_MainWindow.close)

    def moreChanges_button_clicked(self):
        """ Handles the click event of the 'More Changes' button and goes back
            to the first window so the user can make more changes to the current
            TMP file.

            Parameters:
                self: The object instance.

            Returns:
                None
        """

        from main_farm_selection_window import ui_AtomicCartoonsFarm_MainWindow
        self.farm_selection_window = QtWidgets.QMainWindow()
        self.ui = ui_AtomicCartoonsFarm_MainWindow()
        self.ui.setupUi(self.farm_selection_window)
        self.farm_selection_window.show()


