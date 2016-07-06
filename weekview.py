from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QColor
import time


class WeekView(QTableWidget):

        def __init__(self):
                super().__init__()
                self.initUI()

        def initUI(self):
                self.headers = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                v = []
                self.hour_begin = 8
                self.hour_end = 20
                for hour in range(self.hour_begin, self.hour_end):
                        for m in range(4):
                                s = "%02d:%02d - " % (hour % 12, m * 15)
                                m += 1
                                if m == 4:
                                        hour += 1
                                s += "%02d:%02d" % (hour % 12, (m * 15) % 60)
                                v.append(s)
                self.vert_headers = v
                self.setColumnCount(len(self.headers))
                self.setHorizontalHeaderLabels(self.headers)
                self.setRowCount(len(self.vert_headers))
                self.setVerticalHeaderLabels(self.vert_headers)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def nearest_row(self, tm):
                hour = int(time.strftime('%H', tm))
                raw_min = int(time.strftime('%M', tm))
                secs = float(raw_min) * 60.0
                minute = int(round(secs / 900.0))
                if minute == 4:
                        minute = 0
                        hour += 1
                row = (hour - self.hour_begin) * 4 + minute
                return row

        def refresh(self):
                self.clear()
                self.setColumnCount(len(self.headers))
                self.setHorizontalHeaderLabels(self.headers)
                self.setRowCount(len(self.vert_headers))
                self.setVerticalHeaderLabels(self.vert_headers)

        def add_event(self, begin, end, title, sub, color=QColor(100, 100, 150)):
                weekday = time.strftime('%A', begin)
                column = self.headers.index(weekday)
                row_begin = self.nearest_row(begin)
                row_end = self.nearest_row(end)
                for r in range(row_begin, row_end):
                        s = ""
                        if r == row_begin:
                                s = title
                        elif r == row_begin+1:
                                s = sub
                        self.setItem(r, column, QTableWidgetItem(s))
                        self.item(r, column).setBackground(color)
                        self.item(r, column).setForeground(QColor(255, 255, 255))
