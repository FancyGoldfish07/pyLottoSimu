#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyLottoSimu

# Copyright (C) <2012-2015> Markus Hackspacher

# This file is part of pyLottoSimu.

# pyLottoSimu is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyLottoSimu is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyLottoSimu.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtSvg import QSvgWidget

__author__ = 'mar'


class LottoSettingsDialog(QtWidgets.QDialog):
    """The GUI of Settings.

    :param sysdat: Lotto setting
    :type sysdat: string
    :param parent: parent window
    :type parent: string
    """
    def __init__(self, sysdat, parent=None):
        """Inital user interface and slots
        """
        super(LottoSettingsDialog, self).__init__(parent)

        # Set up the user interface from Designer.
        self.ui = uic.loadUi(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]),
            "pylottosimu", "dialog", "lottosystem.ui")))
        self.ui.setWindowIcon(
            QtGui.QIcon(os.path.abspath(os.path.join(
                os.path.dirname(sys.argv[0]),
                "misc", "pyLottoSimu.svg"))))

        self.imageLabel = QSvgWidget()
        self.imageLabel.renderer().load(os.path.abspath(os.path.join(
                os.path.dirname(sys.argv[0]),
                "pylottosimu", "lottokugel.svg")))
        self.ui.scrollArea.setWidget(self.imageLabel)

        self.systemdata = sysdat
        for systemname in self.systemdata.data:
            self.ui.combo_name.addItem(systemname['name'])
        self.ui.combo_name.currentIndexChanged.connect(self.setvalues)
        self.ui.check_with_addit.clicked.connect(self.with_addit)
        self.ui.check_sep_addit_numbers.clicked.connect(self.sep_addit_numbers)

        self.setvalues()

    def sep_addit_numbers(self):
        check = self.ui.check_sep_addit_numbers.isChecked()
        self.ui.label_max_addit.setEnabled(check)
        self.ui.spinBox_max_addit.setEnabled(check)

    def with_addit(self):
        check = self.ui.check_with_addit.isChecked()
        self.ui.spinBox_addit_numbers.setEnabled(check)
        self.ui.label_addit_numbers.setEnabled(check)
        self.ui.label_sep_addit_numbers.setEnabled(check)
        self.ui.check_sep_addit_numbers.setEnabled(check)
        if check is not True:
            self.ui.check_sep_addit_numbers.setChecked(False)
        self.sep_addit_numbers()

    def setvalues(self):
        """Set Values"""
        index = self.ui.combo_name.currentIndex()
        self.ui.spinBox_max_draw.setValue(
            self.systemdata.data[index]['max_draw'])
        self.ui.spinBox_draw_numbers.setValue(
            self.systemdata.data[index]['draw_numbers'])
        self.ui.check_with_addit.setChecked(
            self.systemdata.data[index]['with_addit'])
        self.ui.spinBox_addit_numbers.setValue(
            self.systemdata.data[index]['addit_numbers'])
        self.ui.check_sep_addit_numbers.setChecked(
            self.systemdata.data[index]['sep_addit_numbers'])
        self.ui.spinBox_max_addit.setValue(
            self.systemdata.data[index]['max_addit'])
        self.with_addit()

    def values(self):
        """Values"""
        return (str(self.ui.combo_name.currentText()),
                self.ui.spinBox_max_draw.valueFromText(
                    self.ui.spinBox_max_draw.text()),
                self.ui.spinBox_draw_numbers.valueFromText(
                    self.ui.spinBox_draw_numbers.text()),
                self.ui.check_with_addit.isChecked(),
                self.ui.spinBox_addit_numbers.valueFromText(
                    self.ui.spinBox_addit_numbers.text()),
                self.ui.check_sep_addit_numbers.isChecked(),
                self.ui.spinBox_max_addit.valueFromText(
                    self.ui.spinBox_max_addit.text()))

    @staticmethod
    def getValues(sysdat, parent=None):
        """static method to create the dialog and return
        (dialog.values, accepted)

        :param sysdat: Lotto setting
        :type sysdat: string
        :returns: dialog.values, accepted
        :rtype: array of int, bool
        """
        dialog = LottoSettingsDialog(sysdat, parent)
        result = dialog.ui.exec_()
        return (dialog.values(), result == QtWidgets.QDialog.Accepted)