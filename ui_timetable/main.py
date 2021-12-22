import PyQt5.QtWidgets
import psycopg2
import sys
import datetime

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


def week():
    d1 = datetime.date(2021, 11, 22)
    d2 = datetime.date.today()
    result = (d2 - d1).days // 7
    if result % 2 == 0:
        result = 'up'
    else:
        result = 'down'
    return result


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_sch_tab()
        self._create_teach_tab()
        self._create_schedule_up_tab()
        self._create_schedule_down_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="sch_db",
                                     user="postgres",
                                     password="admin",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_sch_tab(self):
        self.sch_tab = QTabWidget()
        self.tabs.addTab(self.sch_tab, 'Расписание')

    def _create_teach_tab(self):
        self.teach_tab = QTabWidget()
        self.tabs.addTab(self.teach_tab, 'Преподаватели')
        self.teach_gbox = QGroupBox('Список')

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)

        self.shbox1.addWidget(self.teach_gbox)

        self._create_teach_table()
        self.update_schedule_button = QPushButton("Обновить")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.insert_teach_button = QPushButton("Добавить")
        self.shbox3.addWidget(self.insert_teach_button)
        self.insert_teach_button.clicked.connect(self._insert_teach)

        self.delete_teacher_button = QPushButton("Удалить")
        self.shbox4.addWidget(self.delete_teacher_button)
        self.delete_teacher_button.clicked.connect(self._delete_teacher)

        self.teach_tab.setLayout(self.svbox)

    def _create_teach_table(self):
        self.teach_table = QTableWidget()
        self.teach_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teach_table.setColumnCount(4)
        self.teach_table.setHorizontalHeaderLabels(["Имя", "Предмет", "", "Комментарий"])

        self._update_teach_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teach_table)
        self.teach_gbox.setLayout(self.mvbox)

    def _update_teach_table(self):
        self.cursor.execute("SELECT * FROM sch.teacher ORDER BY id")
        records = list(self.cursor.fetchall())

        self.teach_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.teach_table.setItem(i, 0,
                                     QTableWidgetItem(str(r[1])))
            self.teach_table.setItem(i, 1,
                                     QTableWidgetItem(str(r[2])))
            self.teach_table.setCellWidget(i, 2, joinButton)
            if str(r[3]) != 'None':
                self.teach_table.setItem(i, 3,
                                         QTableWidgetItem(str(r[3])))
            else:
                self.teach_table.setItem(i, 3,
                                         QTableWidgetItem(''))
            joinButton.clicked.connect(
                lambda: self._change_teach_from_table(i))

        self.teach_table.resizeRowsToContents()

    def _create_subject_tab(self):
        self.subject_tab = QTabWidget()
        self.tabs.addTab(self.subject_tab, 'Предметы')
        self.subject_gbox = QGroupBox('Список')

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)

        self.shbox1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.update_schedule_button = QPushButton("Обновить")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.insert_subject_button = QPushButton("Добавить")
        self.shbox3.addWidget(self.insert_subject_button)
        self.insert_subject_button.clicked.connect(self._insert_subject)

        self.delete_subject_button = QPushButton("Удалить")
        self.shbox4.addWidget(self.delete_subject_button)
        self.delete_subject_button.clicked.connect(self._delete_subject)

        self.subject_tab.setLayout(self.svbox)

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(3)
        self.subject_table.setHorizontalHeaderLabels(["Название", "", "Комментарий"])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM sch.subject")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setCellWidget(i, 1, joinButton)
            if str(r[1]) != 'None':
                self.subject_table.setItem(i, 2,
                                           QTableWidgetItem(str(r[1])))
            else:
                self.subject_table.setItem(i, 2,
                                           QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_subject_from_table(i))

        self.subject_table.resizeRowsToContents()

    def _create_schedule_up_tab(self):
        self.schedule_up_tab = QWidget()
        self.sch_tab.addTab(self.schedule_up_tab, "Расписание верхней недели")

        self.monday_gbox = QGroupBox("Понедельник")
        self.tuesday_gbox = QGroupBox("Вторник")
        self.wednesday_gbox = QGroupBox("Среда")
        self.thursday_gbox = QGroupBox("Четверг")
        self.friday_gbox = QGroupBox("Пятница")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.svbox.addLayout(self.shbox5)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)

        self._create_monday_table_up()
        self._create_tuesday_table_up()
        self._create_wednesday_table_up()
        self._create_thursday_table_up()
        self._create_friday_table_up()

        self.update_schedule_button = QPushButton("Обновить")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.insert_schedule_button = QPushButton("Добавить")
        self.shbox3.addWidget(self.insert_schedule_button)
        self.insert_schedule_button.clicked.connect(self._insert_schedule)

        self.delete_schedule_button = QPushButton("Удалить")
        self.shbox4.addWidget(self.delete_schedule_button)
        self.delete_schedule_button.clicked.connect(self._delete_schedule)

        if week() == 'up':
            self.week = PyQt5.QtWidgets.QLabel('Сейчас верхняя неделя')
        else:
            self.week = PyQt5.QtWidgets.QLabel('Сейчас нижняя неделя')
        self.shbox5.addWidget(self.week)

        self.schedule_up_tab.setLayout(self.svbox)

    def _create_schedule_down_tab(self):
        self.schedule_down_tab = QWidget()
        self.sch_tab.addTab(self.schedule_down_tab, "Расписание нижней недели")

        self.monday_gbox = QGroupBox("Понедельник")
        self.tuesday_gbox = QGroupBox("Вторник")
        self.wednesday_gbox = QGroupBox("Среда")
        self.thursday_gbox = QGroupBox("Четверг")
        self.friday_gbox = QGroupBox("Пятница")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.shbox3 = QHBoxLayout()
        self.shbox4 = QHBoxLayout()
        self.shbox5 = QHBoxLayout()


        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.svbox.addLayout(self.shbox3)
        self.svbox.addLayout(self.shbox4)
        self.svbox.addLayout(self.shbox5)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)

        self._create_monday_table_down()
        self._create_tuesday_table_down()
        self._create_wednesday_table_down()
        self._create_thursday_table_down()
        self._create_friday_table_down()

        self.update_schedule_button = QPushButton("Обновить")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.insert_schedule_button = QPushButton("Добавить")
        self.shbox3.addWidget(self.insert_schedule_button)
        self.insert_schedule_button.clicked.connect(self._insert_schedule)

        self.delete_schedule_button = QPushButton("Удалить")
        self.shbox4.addWidget(self.delete_schedule_button)
        self.delete_schedule_button.clicked.connect(self._delete_schedule)

        if week() == 'up':
            self.week = PyQt5.QtWidgets.QLabel('Сейчас верхняя неделя')
        else:
            self.week = PyQt5.QtWidgets.QLabel('Сейчас нижняя неделя')
        self.shbox5.addWidget(self.week)

        self.schedule_down_tab.setLayout(self.svbox)

    def _create_monday_table_up(self):
        self.monday_table_up = QTableWidget()
        self.monday_table_up.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table_up.setColumnCount(4)
        self.monday_table_up.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_monday_table_up()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table_up)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table_up(self):
        self.tuesday_table_up = QTableWidget()
        self.tuesday_table_up.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table_up.setColumnCount(4)
        self.tuesday_table_up.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_tuesday_table_up()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table_up)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table_up(self):
        self.wednesday_table_up = QTableWidget()
        self.wednesday_table_up.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table_up.setColumnCount(4)
        self.wednesday_table_up.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_wednesday_table_up()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table_up)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table_up(self):
        self.thursday_table_up = QTableWidget()
        self.thursday_table_up.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table_up.setColumnCount(4)
        self.thursday_table_up.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_thursday_table_up()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table_up)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table_up(self):
        self.friday_table_up = QTableWidget()
        self.friday_table_up.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table_up.setColumnCount(4)
        self.friday_table_up.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_friday_table_up()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table_up)
        self.friday_gbox.setLayout(self.mvbox)

    def _create_monday_table_down(self):
        self.monday_table_down = QTableWidget()
        self.monday_table_down.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table_down.setColumnCount(4)
        self.monday_table_down.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_monday_table_down()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table_down)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table_down(self):
        self.tuesday_table_down = QTableWidget()
        self.tuesday_table_down.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table_down.setColumnCount(4)
        self.tuesday_table_down.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_tuesday_table_down()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table_down)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table_down(self):
        self.wednesday_table_down = QTableWidget()
        self.wednesday_table_down.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table_down.setColumnCount(4)
        self.wednesday_table_down.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_wednesday_table_down()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table_down)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table_down(self):
        self.thursday_table_down = QTableWidget()
        self.thursday_table_down.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table_down.setColumnCount(4)
        self.thursday_table_down.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_thursday_table_down()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table_down)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table_down(self):
        self.friday_table_down = QTableWidget()
        self.friday_table_down.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table_down.setColumnCount(4)
        self.friday_table_down.setHorizontalHeaderLabels(["Предмет", "Время", "", "Комментарий"])

        self._update_friday_table_down()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table_down)
        self.friday_gbox.setLayout(self.mvbox)

    def _update_monday_table_up(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Понедельник' AND week = 'up' OR day = 'Понедельник' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.monday_table_up.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.monday_table_up.setItem(i, 0,
                                         QTableWidgetItem(str(r[2])))
            self.monday_table_up.setItem(i, 1,
                                         QTableWidgetItem(str(r[4])))
            self.monday_table_up.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.monday_table_up.setItem(i, 3,
                                             QTableWidgetItem(str(r[6])))
            else:
                self.monday_table_up.setItem(i, 3,
                                             QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_up(i, "Понедельник", 'up'))

        self.monday_table_up.resizeRowsToContents()

    def _update_tuesday_table_up(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Вторник' AND week = 'up' OR day = 'Вторник' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.tuesday_table_up.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.tuesday_table_up.setItem(i, 0,
                                          QTableWidgetItem(str(r[2])))
            self.tuesday_table_up.setItem(i, 1,
                                          QTableWidgetItem(str(r[4])))
            self.tuesday_table_up.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.tuesday_table_up.setItem(i, 3,
                                              QTableWidgetItem(str(r[6])))
            else:
                self.tuesday_table_up.setItem(i, 3,
                                              QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_up(i, "Вторник", 'up'))

        self.tuesday_table_up.resizeRowsToContents()

    def _update_wednesday_table_up(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Среда' AND week = 'up' OR day = 'Среда' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.wednesday_table_up.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.wednesday_table_up.setItem(i, 0,
                                            QTableWidgetItem(str(r[2])))
            self.wednesday_table_up.setItem(i, 1,
                                            QTableWidgetItem(str(r[4])))
            self.wednesday_table_up.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.wednesday_table_up.setItem(i, 3,
                                                QTableWidgetItem(str(r[6])))
            else:
                self.wednesday_table_up.setItem(i, 3,
                                                QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_up(i, "Среда", 'up'))

        self.wednesday_table_up.resizeRowsToContents()

    def _update_thursday_table_up(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Четверг' AND week = 'up' OR day = 'Четверг' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.thursday_table_up.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.thursday_table_up.setItem(i, 0,
                                           QTableWidgetItem(str(r[2])))
            self.thursday_table_up.setItem(i, 1,
                                           QTableWidgetItem(str(r[4])))
            self.thursday_table_up.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.thursday_table_up.setItem(i, 3,
                                               QTableWidgetItem(str(r[6])))
            else:
                self.thursday_table_up.setItem(i, 3,
                                               QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_up(i, "Четверг", 'up'))

        self.thursday_table_up.resizeRowsToContents()

    def _update_friday_table_up(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Пятница' AND week = 'up' OR day = 'Пятница' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.friday_table_up.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.friday_table_up.setItem(i, 0,
                                         QTableWidgetItem(str(r[2])))
            self.friday_table_up.setItem(i, 1,
                                         QTableWidgetItem(str(r[4])))
            self.friday_table_up.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.thursday_table_up.setItem(i, 3,
                                               QTableWidgetItem(str(r[6])))
            else:
                self.thursday_table_up.setItem(i, 3,
                                               QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_up(i, "Пятница", 'up'))

        self.friday_table_up.resizeRowsToContents()

    def _update_monday_table_down(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Понедельник' AND week = 'down' OR day = 'Понедельник' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.monday_table_down.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.monday_table_down.setItem(i, 0,
                                           QTableWidgetItem(str(r[2])))
            self.monday_table_down.setItem(i, 1,
                                           QTableWidgetItem(str(r[4])))
            self.monday_table_down.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.monday_table_down.setItem(i, 3,
                                               QTableWidgetItem(str(r[6])))
            else:
                self.monday_table_down.setItem(i, 3,
                                               QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_down(i, "Понедельник", 'down'))

        self.monday_table_down.resizeRowsToContents()

    def _update_tuesday_table_down(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Вторник' AND week = 'down' OR day = 'Вторник' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.tuesday_table_down.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.tuesday_table_down.setItem(i, 0,
                                            QTableWidgetItem(str(r[2])))
            self.tuesday_table_down.setItem(i, 1,
                                            QTableWidgetItem(str(r[4])))
            self.tuesday_table_down.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.tuesday_table_down.setItem(i, 3,
                                                QTableWidgetItem(str(r[6])))
            else:
                self.tuesday_table_down.setItem(i, 3,
                                                QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_down(i, "Вторник", 'down'))

        self.tuesday_table_down.resizeRowsToContents()

    def _update_wednesday_table_down(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Среда' AND week = 'down' OR day = 'Среда' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.wednesday_table_down.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.wednesday_table_down.setItem(i, 0,
                                              QTableWidgetItem(str(r[2])))
            self.wednesday_table_down.setItem(i, 1,
                                              QTableWidgetItem(str(r[4])))
            self.wednesday_table_down.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.wednesday_table_down.setItem(i, 3,
                                                  QTableWidgetItem(str(r[6])))
            else:
                self.wednesday_table_down.setItem(i, 3,
                                                  QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_down(i, "Среда", 'down'))

        self.wednesday_table_down.resizeRowsToContents()

    def _update_thursday_table_down(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Четверг' AND week = 'down' OR day = 'Четверг' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.thursday_table_down.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.thursday_table_down.setItem(i, 0,
                                             QTableWidgetItem(str(r[2])))
            self.thursday_table_down.setItem(i, 1,
                                             QTableWidgetItem(str(r[4])))
            self.thursday_table_down.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.thursday_table_down.setItem(i, 3,
                                                 QTableWidgetItem(str(r[6])))
            else:
                self.thursday_table_down.setItem(i, 3,
                                                 QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_down(i, "Четверг", 'down'))

        self.thursday_table_down.resizeRowsToContents()

    def _update_friday_table_down(self):
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = 'Пятница' AND week = 'down' OR day = 'Пятница' AND week = 'all' ORDER BY start_num")
        records = list(self.cursor.fetchall())

        self.friday_table_down.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            self.friday_table_down.setItem(i, 0,
                                           QTableWidgetItem(str(r[2])))
            self.friday_table_down.setItem(i, 1,
                                           QTableWidgetItem(str(r[4])))
            self.friday_table_down.setCellWidget(i, 2, joinButton)
            if str(r[6]) != 'None':
                self.friday_table_down.setItem(i, 3,
                                               QTableWidgetItem(str(r[6])))
            else:
                self.friday_table_down.setItem(i, 3,
                                               QTableWidgetItem(''))

            joinButton.clicked.connect(
                lambda: self._change_day_from_table_down(i, "Пятница", 'down'))

        self.friday_table_down.resizeRowsToContents()

    def _change_day_from_table_up(self, rowNum, day, week):
        row = list()
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = '%s' AND week = '%s' OR day = '%s' AND week = 'all' ORDER BY start_num" % (
            day, week, day))
        records = list(self.cursor.fetchall())
        if day == 'Понедельник':
            for j in range(rowNum + 1):
                for i in range(self.monday_table_up.columnCount()):
                    try:
                        row.append(self.monday_table_up.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Вторник':
            for j in range(rowNum + 1):
                for i in range(self.tuesday_table_up.columnCount()):
                    try:
                        row.append(self.tuesday_table_up.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Среда':
            for j in range(rowNum + 1):
                for i in range(self.wednesday_table_up.columnCount()):
                    try:
                        row.append(self.wednesday_table_up.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Четверг':
            for j in range(rowNum + 1):
                for i in range(self.thursday_table_up.columnCount()):
                    try:
                        row.append(self.thursday_table_up.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Пятница':
            for j in range(rowNum + 1):
                for i in range(self.friday_table_up.columnCount()):
                    try:
                        row.append(self.friday_table_up.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []

    def _change_day_from_table_down(self, rowNum, day, week):
        row = list()
        self.cursor.execute(
            "SELECT * FROM sch.timetable WHERE day = '%s' AND week = '%s' OR day = '%s' AND week = 'all' ORDER BY start_num" % (
            day, week, day))
        records = list(self.cursor.fetchall())
        if day == 'Понедельник':
            for j in range(rowNum + 1):
                for i in range(self.monday_table_down.columnCount()):
                    try:
                        row.append(self.monday_table_down.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Вторник':
            for j in range(rowNum + 1):
                for i in range(self.tuesday_table_down.columnCount()):
                    try:
                        row.append(self.tuesday_table_down.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Среда':
            for j in range(rowNum + 1):
                for i in range(self.wednesday_table_down.columnCount()):
                    try:
                        row.append(self.wednesday_table_down.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Четверг':
            for j in range(rowNum + 1):
                for i in range(self.thursday_table_down.columnCount()):
                    try:
                        row.append(self.thursday_table_down.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []
        elif day == 'Пятница':
            for j in range(rowNum + 1):
                for i in range(self.friday_table_down.columnCount()):
                    try:
                        row.append(self.friday_table_down.item(j, i).text())
                    except:
                        row.append(None)
                try:
                    self.cursor.execute(
                        "UPDATE sch.timetable SET subject = '%s', start_time = '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                    self.conn.commit()
                except:
                    self.cursor.execute("rollback")
                    QMessageBox.about(self, 'Error', 'Enter all fields')
                    break
                row = []

    def _change_teach_from_table(self, rowNum):
        row = list()
        self.cursor.execute("SELECT * FROM sch.teacher ORDER BY start_num")
        records = list(self.cursor.fetchall())
        for j in range(rowNum + 1):
            for i in range(self.teach_table.columnCount()):
                try:
                    row.append((self.teach_table.item(j, i).text()))
                except:
                    row.append(None)
            try:
                self.cursor.execute("UPDATE sch.teacher SET full_name = '%s', subject= '%s', comment = '%s' WHERE id = '%s'" % (
                        str(row[0]), str(row[1]), str(row[3]), int(records[j][0])))
                self.conn.commit()
            except:
                self.cursor.execute("rollback")
                QMessageBox.about(self, 'Error', 'Enter all fields')
                break
            row = []

    def _change_subject_from_table(self, rowNum):
        row = list()
        self.cursor.execute("SELECT * FROM sch.subject")
        records = list(self.cursor.fetchall())
        for j in range(rowNum + 1):
            for i in range(self.subject_table.columnCount()):
                try:
                    row.append((self.subject_table.item(j, i).text()))
                except:
                    row.append(None)
            try:
                self.cursor.execute("UPDATE sch.subject SET comment = '%s' WHERE name = '%s'" % (
                        str(row[2]), str(records[j][0])))
                self.conn.commit()
            except:
                self.cursor.execute("rollback")
                QMessageBox.about(self, 'Error', 'Enter all fields')
                break
            row = []

    def _update_schedule(self):
        self._update_monday_table_up()
        self._update_tuesday_table_up()
        self._update_wednesday_table_up()
        self._update_thursday_table_up()
        self._update_friday_table_up()
        self._update_monday_table_down()
        self._update_tuesday_table_down()
        self._update_wednesday_table_down()
        self._update_thursday_table_down()
        self._update_friday_table_down()
        self._update_teach_table()
        self._update_subject_table()

    def _insert_schedule(self):
        i = 0
        insert = []
        ex = 1
        while ex != 0:
            if i == 0:
                print('Выберите день недели:\n'
                      '1. Понедельник\n'
                      '2. Вторник\n'
                      '3. Среда\n'
                      '4. Четверг\n'
                      '5. Пятница\n')
                d = {'1': 'Понедельник', '2': 'Вторник', '3': 'Среда', '4': 'Четверг', '5': 'Пятница'}
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
                d = {}
            if i == 1:
                self.cursor.execute("SELECT * FROM sch.subject")
                records = list(self.cursor.fetchall())
                message = 'Выберите предмет:\n'
                for j, r in enumerate(records):
                    message += (str(j+1) + '.' + ' ' + r[0] + '\n')
                    d[str(j+1)] = r[0]
                print(message)
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
            if i == 2:
                x = input('Введите номер кабинета:\n')
                insert.append(x)
                i += 1
            if i == 3:
                print('Выберите время пары:\n'
                      '1. 9:30-11:05\n'
                      '2. 11:20-12:55\n'
                      '3. 13:10-14:45\n'
                      '4. 15:25-17:00\n'
                      '5. 17:15-18:50')
                d = {'1': '9:30-11:05', '2': '11:20-12:55', '3': '13:10-14:45', '4': '15:25-17:00', '5': '17:15-18:50'}
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                insert.append(int(x))
                i += 1
            if i == 4:
                print('Выберите на какой неделе пара:\n'
                      '1. На всех\n'
                      '2. На верхней\n'
                      '3. На нижней\n')
                d = {'1': 'all', '2': 'up', '3': 'down'}
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
            if i == 5:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - добавить в таблицу\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "INSERT INTO sch.timetable (day, subject, room_numb, start_time, week, start_num) VALUES ('%s', '%s', '%s', '%s', '%s', %s)"
                        % (insert[0], insert[1], insert[2], insert[3], insert[5], insert[4]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0

    def _insert_teach(self):
        i = 0
        ex = 1
        insert = []
        while ex != 0:
            if i == 0:
                x = input('Введите имя преподавателя:\n')
                insert.append(x)
                i += 1
            if i == 1:
                d = {}
                self.cursor.execute("SELECT * FROM sch.subject")
                records = list(self.cursor.fetchall())
                message = 'Выберите предмет:\n'
                for j, r in enumerate(records):
                    message += (str(j + 1) + '.' + ' ' + r[0] + '\n')
                    d[str(j + 1)] = r[0]
                print(message)
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
            if i == 2:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - добавить в таблицу\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "INSERT INTO sch.teacher (full_name, subject) VALUES ('%s', '%s')"
                        % (insert[0], insert[1]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0

    def _insert_subject(self):
        i = 0
        ex = 1
        insert = []
        while ex != 0:
            if i == 0:
                x = input('Введите название предмета:\n')
                insert.append(x)
                i += 1
            if i == 1:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - добавить в таблицу\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "INSERT INTO sch.subject (name) VALUES ('%s')"
                        % (insert[0]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0

    def _delete_schedule(self):
        i = 0
        insert = []
        ex = 1
        while ex != 0:
            if i == 0:
                print('Выберите день недели:\n'
                      '1. Понедельник\n'
                      '2. Вторник\n'
                      '3. Среда\n'
                      '4. Четверг\n'
                      '5. Пятница\n')
                d = {'1': 'Понедельник', '2': 'Вторник', '3': 'Среда', '4': 'Четверг', '5': 'Пятница'}
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
                d = {}
            if i == 1:
                d = {}
                self.cursor.execute("SELECT * FROM sch.timetable WHERE day = '%s'" % insert[0])
                records = list(self.cursor.fetchall())
                message = 'Выберите пару:\n'
                for j, r in enumerate(records):
                    message += (str(j + 1) + '.' + ' ' + str(r[2]) + ' ' + str(r[4]) + '\n')
                    d[str(j + 1)] = r[2], r[4]
                print(message)
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)][0])
                insert.append(d[str(x)][1])
                i += 1
            if i == 2:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - удалить из таблицы\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "DELETE FROM sch.timetable WHERE day = '%s' AND subject = '%s' AND start_time = '%s'"
                        % (insert[0], insert[1], insert[2]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0

    def _delete_subject(self):
        i = 0
        insert = []
        ex = 1
        while ex != 0:
            if i == 0:
                d = {}
                self.cursor.execute("SELECT * FROM sch.subject")
                records = list(self.cursor.fetchall())
                message = 'Выберите запись:\n'
                for j, r in enumerate(records):
                    message += (str(j + 1) + '.' + ' ' + str(r[0]) + '\n')
                    d[str(j + 1)] = r[0]
                print(message)
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)])
                i += 1
            if i == 1:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - удалить из таблицы\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "DELETE FROM sch.subject WHERE name = '%s'"
                        % (insert[0]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0

    def _delete_teacher(self):
        i = 0
        insert = []
        ex = 1
        while ex != 0:
            if i == 0:
                d = {}
                self.cursor.execute("SELECT * FROM sch.teacher ORDER BY id")
                records = list(self.cursor.fetchall())
                message = 'Выберите запись:\n'
                for j, r in enumerate(records):
                    message += (str(j + 1) + '.' + ' ' + str(r[1]) + ' ' + str(r[2]) + '\n')
                    d[str(j + 1)] = r[1], r[2]
                print(message)
                flag = 0
                while flag != 1:
                    x = input('Введите номер: \n')
                    if x in d.keys():
                        flag = 1
                    else:
                        print('Некорректные данные')
                insert.append(d[str(x)][0])
                insert.append(d[str(x)][1])
                i += 1
            if i == 1:
                print('Проверьте данные:\n')
                message = ''
                for i in insert:
                    message += (str(i) + ' ')
                print(message)
                print('\nВерные ли данные?\n'
                      '1. Да - удалить из таблицы\n'
                      '2. Нет - заполнить заново\n'
                      '3. Отменить редактирование')
                flag = 0
                while flag != 1:
                    x = int(input('Введите номер: \n'))
                    if x in [1, 2, 3]:
                        flag = 1
                    else:
                        print('Некорректные данные')
                if x == 1:
                    self.cursor.execute(
                        "DELETE FROM sch.teacher WHERE full_name = '%s' AND subject = '%s'"
                        % (insert[0], insert[1]))
                    self.conn.commit()
                    ex = 0
                elif x == 2:
                    insert = []
                    message = ''
                    i = 0
                elif x == 3:
                    insert = []
                    message = ''
                    ex = 0













app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
