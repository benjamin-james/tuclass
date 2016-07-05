#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon
import classes


class ClassUI(QWidget):

        def __init__(self):
                super().__init__()
                self.initUI()

        def initUI(self):
                self.layout = QSplitter()
                self.in_layout = QVBoxLayout()
                self.table = QTableWidget()
                self.headers = ['Class', 'Title', 'Edition', 'ISBN', 'Publisher', 'Author', 'Suggested Retail Price', 'Comments', 'Required']
                self.table.setColumnCount(len(self.headers))
                self.table.setHorizontalHeaderLabels(self.headers)
                self.le = []
                self.le.append(QLineEdit(self))
                self.le.append(QLineEdit(self))
                self.le.append(QLineEdit(self))
                self.le.append(QLineEdit(self))
                self.le.append(QLineEdit(self))
                self.table.setRowCount(len(self.le))
                #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                self.submit_btn = QPushButton('Submit', self)
                self.submit_btn.clicked.connect(self.submit)
                self.add_btn = QPushButton('+', self)
                self.add_btn.clicked.connect(self.add_le)
                self.rm_btn = QPushButton('-', self)
                self.rm_btn.clicked.connect(self.rm_le)
                self.btn_layout = QHBoxLayout()
                self.in_layout.addWidget(self.submit_btn)
                self.btn_layout.addWidget(self.add_btn)
                self.btn_layout.addWidget(self.rm_btn)
                self.in_layout.addLayout(self.btn_layout)
                for l in self.le:
                        self.in_layout.addWidget(l)
                lside = QWidget(self)
                lside.setLayout(self.in_layout)
                self.layout.addWidget(lside)
                self.layout.addWidget(self.table)
                l = QVBoxLayout()
                l.addWidget(self.layout)
                self.setLayout(l)
                app_icon = QIcon()
                app_icon.addFile('tulsa.jpg')
                self.setWindowIcon(app_icon)
                self.setGeometry(300, 300, 800, 600)
                self.setWindowTitle('Tulsa class info')
                self.show()

        def add_le(self):
                l = QLineEdit(self)
                self.in_layout.addWidget(l)
                self.le.append(l)

        def rm_le(self):
                l = self.le.pop()
                self.in_layout.removeWidget(l)
                l.deleteLater()
                l = None

        def set_table_item(self, x, y, s):
                self.table.setItem(x, y, QTableWidgetItem(s))

        def submit(self):

                regex = re.compile("^[A-Z]{2,4}-\d{4}")
                data = [l.text() for l in self.le if regex.match(l.text())]
                schedule = classes.do_stuff(data)
                self.table.clear()
                self.table.setHorizontalHeaderLabels(self.headers)
                cur_row = 0
                for key in schedule:
                        for book in schedule[key]:
                                self.table.setRowCount(cur_row + 1)
                                self.set_table_item(cur_row, 0, key)
                                self.set_table_item(cur_row, 1, book['Book Title'])
                                self.set_table_item(cur_row, 2, book['Edition'])
                                self.set_table_item(cur_row, 3, book['ISBN'])
                                self.set_table_item(cur_row, 4, book['Publisher'])
                                self.set_table_item(cur_row, 5, book['Author'])
                                self.set_table_item(cur_row, 6, book['Publishers Suggested Retail Price'])
                                self.set_table_item(cur_row, 7, book['Comments'])
                                self.set_table_item(cur_row, 8, book['Required'])
                                cur_row += 1


if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = ClassUI()
        sys.exit(app.exec_())
