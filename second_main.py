# -*- coding: utf-8 -*-
import sys
import sqlite3
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QTabWidget, QComboBox, QDateEdit, QMessageBox, QTimeEdit, QLabel, QHBoxLayout
from PyQt6 import QtGui, QtCore


def create_tables():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone TEXT UNIQUE,
                        password TEXT,
                        last_name TEXT,
                        first_name TEXT,
                        patronymic TEXT,
                        dob TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        last_name TEXT,
                        first_name TEXT,
                        patronymic TEXT,
                        dob TEXT,
                        specialization TEXT,
                        experience TEXT,
                        education TEXT,
                        office_address TEXT,
                        cabinet TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        doctor_id INTEGER,
                        address TEXT,
                        appointment_date TEXT,
                        time TEXT,
                        cabinet TEXT,
                        FOREIGN KEY(patient_id) REFERENCES users(id),
                        FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        service_type TEXT,
                        description TEXT,
                        price TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS analysis_appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        analysis_name TEXT,
                        address TEXT,
                        date TEXT,
                        time TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        service_name TEXT,
                        doctor_name TEXT,
                        address TEXT,
                        appointment_date TEXT,
                        time TEXT,
                        cabinet TEXT)''')

    conn.commit()
    conn.close()


def add_user(phone, password, last_name, first_name, patronymic, dob):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO users (phone, password, last_name, first_name, patronymic, dob)
                      VALUES (?, ?, ?, ?, ?, ?)''', (phone, password, last_name, first_name, patronymic, dob))

    conn.commit()
    conn.close()


def get_users():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()

    conn.close()
    return users


def get_user(phone):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM users WHERE phone = ?''', (phone,))
    user = cursor.fetchone()

    conn.close()
    return user


def delete_patient(patient_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM users WHERE id = ?''', (patient_id,))

    conn.commit()
    conn.close()


def add_doctor(last_name, first_name, patronymic, dob, specialization, experience, education, office_address, cabinet):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO doctors (last_name, first_name, patronymic, dob, specialization, experience,
    education, office_address, cabinet)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (last_name, first_name, patronymic, dob, specialization,
                                                              experience, education, office_address, cabinet))

    conn.commit()
    conn.close()


def get_doctors():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM doctors''')
    doctors = cursor.fetchall()

    conn.close()
    return doctors


def get_doctor_by_specialization(specialization):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM doctors WHERE specialization = ?''', (specialization,))
    doctor = cursor.fetchall()

    conn.close()
    return doctor


def get_doctor_by_id(doctor_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM doctors WHERE id = ?''', (doctor_id,))
    doctor = cursor.fetchall()

    conn.close()
    return doctor


def delete_doctor(doctor_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM doctors WHERE id = ?''', (doctor_id,))

    conn.commit()
    conn.close()


def add_appointment(patient_id, doctor_id, address, appointment_date, time, cabinet):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO appointments (patient_id, doctor_id, address, appointment_date, time, cabinet)
                      VALUES (?, ?, ?, ?, ?, ?)''', (patient_id, doctor_id, address, appointment_date, time, cabinet))

    conn.commit()
    conn.close()


def add_analysis_appointments(patient_id, analysis_name, address, date, time):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO analysis_appointments (patient_id, analysis_name, address, date, time)
                          VALUES (?, ?, ?, ?, ?)''', (patient_id, analysis_name, address, date, time))

    conn.commit()
    conn.close()


def add_user_appointments(patient_id, service_name, doctor_name, address, date, time, cabinet):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO user_appointments (patient_id, service_name, doctor_name,
                      address, appointment_date, time, cabinet)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''', (patient_id, service_name, doctor_name,
                                                                address, date, time, cabinet))

    conn.commit()
    conn.close()


def get_appointments():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM appointments''')
    appointments = cursor.fetchall()

    conn.close()
    return appointments


def get_analysis_appointments():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM analysis_appointments''')
    appointments = cursor.fetchall()

    conn.close()
    return appointments


def get_user_appointments(patient_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT id, service_name, doctor_name, address, appointment_date, time, cabinet
                      FROM user_appointments WHERE patient_id = ?''', (patient_id,))
    appointments = cursor.fetchall()

    conn.close()
    return appointments


def get_appointment(appointment_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM appointments WHERE id = ?''', (appointment_id,))
    appointment = cursor.fetchall()

    conn.close()
    return appointment


def delete_appointment(appointment_id):
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM appointments WHERE id = ?''', (appointment_id,))

    conn.commit()
    conn.close()


def get_services():
    conn = sqlite3.connect('medical_records.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM services''')
    services = cursor.fetchall()

    conn.close()
    return services


def is_valid_phone_number(phone):
    pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
    return re.match(pattern, phone) is not None


class LoginDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(150, 150, 300, 150)

        self.layout = QFormLayout()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addRow("Номер телефона:", self.phone_input)
        self.layout.addRow("Пароль:", self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_register_dialog)

        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def login(self):
        phone = self.phone_input.text()
        password = self.password_input.text()

        user = get_user(phone)
        if user and user[2] == password:
            self.open_user_dialog(phone)
        elif phone == 'admin' and password == '1234':
            self.open_admin_dialog()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    @staticmethod
    def open_register_dialog():
        dialog = RegisterDialog()
        dialog.exec()

    @staticmethod
    def open_user_dialog(phone):
        dialog = UserWindow(phone)
        dialog.exec()

    @staticmethod
    def open_admin_dialog():
        dialog = AdminWindow()
        dialog.exec()


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(150, 150, 300, 300)

        self.layout = QFormLayout()
        self.phone_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.patronymic_input = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd-MM-yyyy")

        self.layout.addRow("Телефон +7 (xxx) xxx-xx-xx:", self.phone_input)
        self.layout.addRow("Пароль:", self.password_input)
        self.layout.addRow("Фамилия:", self.last_name_input)
        self.layout.addRow("Имя:", self.first_name_input)
        self.layout.addRow("Отчество:", self.patronymic_input)
        self.layout.addRow("Дата рождения:", self.dob_input)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.register_button)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def register(self):
        phone = self.phone_input.text()
        password = self.password_input.text()
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        patronymic = self.patronymic_input.text()
        dob = self.dob_input.text()

        user = get_user(phone)
        if user:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует, попробуйте другой")
            return

        if not phone or not password or not first_name or not last_name or not dob:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        if not is_valid_phone_number(phone):
            QMessageBox.warning(self, "Ошибка",
                                "Некорректный формат номера телефона. Используйте формат +7 (123) 456-78-90.")
            return

        add_user(phone, password, last_name, first_name, patronymic, dob)
        QMessageBox.information(self, "Успех", "Регистрация прошла успешно.")
        self.close()


class UserWindow(QDialog):
    def __init__(self, phone):
        super().__init__()
        self.user_phone = phone
        self.setWindowTitle("Личный кабинет")
        self.setGeometry(350, 300, 300, 200)
        self.layout = QVBoxLayout()

        self.main_menu_layout = QHBoxLayout()
        self.services_button = QPushButton("Услуги")
        self.appointments_button = QPushButton("Мои записи")

        self.main_menu_layout.addWidget(self.services_button)
        self.main_menu_layout.addWidget(self.appointments_button)

        self.services_button.clicked.connect(self.open_services_menu)
        self.appointments_button.clicked.connect(self.open_appointments_menu)

        self.layout.addLayout(self.main_menu_layout)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def open_services_menu(self):
        dialog = UserServicesMenu(self.user_phone)
        dialog.exec()

    def open_appointments_menu(self):
        dialog = UserAppointmentsMenu(self.user_phone)
        dialog.exec()


class UserServicesMenu(QDialog):
    def __init__(self, phone):
        super().__init__()
        self.user_phone = phone
        self.setWindowTitle("Список услуг")
        self.setGeometry(0, 0, 1910, 1070)
        self.layout = QVBoxLayout()

        self.services_table = QTableWidget()
        self.services_table.setColumnCount(6)
        self.services_table.setHorizontalHeaderLabels(['ID', 'Услуга', 'Тип услуги', 'Описание', 'Цена', ''])
        self.services_table.setSortingEnabled(True)

        self.layout.addWidget(self.services_table)
        self.setLayout(self.layout)

        self.refresh_services_table()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def refresh_services_table(self):
        services = get_services()
        self.services_table.setRowCount(len(services))
        for row, service in enumerate(services):
            for col, value in enumerate(service):
                self.services_table.setItem(row, col, QTableWidgetItem(str(value)))
        length = self.services_table.rowCount()
        for row in range(length):
            button = QPushButton('Купить')
            button.clicked.connect(lambda _, r=row: self.open_buying_menu(r, self.user_phone))
            self.services_table.setCellWidget(row, 5, button)
        self.services_table.resizeColumnsToContents()

    @staticmethod
    def open_buying_menu(row, phone):
        services = get_services()
        service = services[row]
        if service[2] == 'Анализ':
            dialog = AnalysisMenu(row, phone)
            dialog.exec()
        elif service[2] == 'Консультация':
            dialog = ConsultationMenu(row, phone)
            dialog.exec()


class UserAppointmentsMenu(QDialog):
    def __init__(self, phone):
        super().__init__()
        self.user_phone = phone
        self.setWindowTitle("Мои записи")
        self.setGeometry(100, 100, 900, 600)
        self.layout = QVBoxLayout()

        self.current_date_time = QLabel()
        self.current_date_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.current_date_time.setFont(QtGui.QFont("Calibri", 14))

        self.appointments_table = QTableWidget()
        self.appointments_table.setColumnCount(7)
        self.appointments_table.setHorizontalHeaderLabels(['ID', 'Название услуги', 'Врач', 'Адрес', 'Дата', 'Время',
                                                           'Кабинет'])
        self.appointments_table.setGeometry(10, 200, 100, 100)
        self.appointments_table.setSortingEnabled(True)

        self.layout.addWidget(self.current_date_time)
        self.layout.addWidget(self.appointments_table)
        self.setLayout(self.layout)

        self.refresh_appointments_table()
        self.update_current_date_time()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #003366;
            }
        """)

    def refresh_appointments_table(self):
        service_name = ''
        doctor_name = ''
        address = ''
        date = ''
        time = ''
        cabinet = ''
        user = get_user(self.user_phone)
        user_id = user[0]
        consultation_appointments = get_appointments()
        analysis_appointments = get_analysis_appointments()
        filtered_consultation_appointments = [ap for ap in consultation_appointments if ap[1] == user[0]]
        filtered_analysis_appointments = [ap for ap in analysis_appointments if ap[1] == user[0]]
        self.appointments_table.setRowCount(len(filtered_consultation_appointments) +
                                            len(filtered_analysis_appointments))
        for appointment in filtered_consultation_appointments:
            doctors = get_doctor_by_id(appointment[2])
            for doctor in doctors:
                doctor_name = '{last_name} {first_name} {patronymic}'.format(last_name=doctor[1], first_name=doctor[2],
                                                                             patronymic=doctor[3])
                service_name = 'Консультация {specialization}а'.format(specialization=doctor[5].lower())
            address = appointment[3]
            date = appointment[4]
            time = appointment[5]
            cabinet = appointment[6]

        add_user_appointments(user_id, service_name, doctor_name, address, date, time, cabinet)
        result_consultation = get_user_appointments(user_id)
        for row, appointment in enumerate(result_consultation):
            for col, value in enumerate(appointment):
                self.appointments_table.setItem(row, col, QTableWidgetItem(str(value)))

        for appointment in filtered_analysis_appointments:
            service_name = appointment[2]
            doctor_name = '-'
            address = appointment[3]
            date = appointment[4]
            time = appointment[5]
            cabinet = '101'
        add_user_appointments(user_id, service_name, doctor_name, address, date, time, cabinet)
        result_analysis = get_user_appointments(user_id)
        for row, appointment in enumerate(result_analysis):
            for col, value in enumerate(appointment):
                self.appointments_table.setItem(row, col, QTableWidgetItem(str(value)))
        self.appointments_table.resizeColumnsToContents()

    def update_current_date_time(self):
        current_date = QtCore.QDate.currentDate().toString("dd-MM-yyyy")
        current_time = QtCore.QTime.currentTime().toString("HH:mm")
        self.current_date_time.setText(f"Текущая дата и время: {current_date} {current_time}")


class AnalysisMenu(QDialog):
    def __init__(self, row, phone):
        super().__init__()
        self.user_phone = phone
        self.row = row
        self.setWindowTitle('Запись на сдачу анализов')
        self.setGeometry(400, 400, 300, 200)
        self.layout = QVBoxLayout()

        self.service_info = QLabel()
        self.service_info.setFont(QtGui.QFont("Calibri", 14))

        self.address_combo = QComboBox()
        self.appointment_date_input = QDateEdit()
        self.appointment_date_input.setCalendarPopup(True)
        self.appointment_date_input.setDisplayFormat("dd-MM-yyyy")
        self.time_input = QTimeEdit()

        self.load_service_info()
        self.load_combobox_data()

        self.layout.addWidget(self.service_info)
        self.layout.addWidget(QLabel('Введите адрес:'))
        self.layout.addWidget(self.address_combo)
        self.layout.addWidget(QLabel('Выберите дату:'))
        self.layout.addWidget(self.appointment_date_input)
        self.layout.addWidget(QLabel('Выберите время:'))
        self.layout.addWidget(self.time_input)

        self.save_button = QPushButton("Записаться")
        self.save_button.clicked.connect(self.save_analysis_appointment)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QLabel {
                color: #003366;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QDateEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QTimeEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def load_service_info(self):
        services = get_services()
        service = services[self.row]
        self.service_info.setText(f"{service[1]} - {service[4]} руб")

    def load_combobox_data(self):
        addresses = ["Волгоградский пр-т. 43", "Малая Бронная ул. 12", "Комсомолькая ул. 71"]
        self.address_combo.clear()
        self.address_combo.addItems(addresses)

    def save_analysis_appointment(self):
        patient_id = get_user(self.user_phone)[0]
        services = get_services()
        service = services[self.row]
        address = self.address_combo.currentText()
        appointment_date = self.appointment_date_input.date().toString("dd-MM-yyyy")
        time = self.time_input.text()

        if not appointment_date or not time:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        add_analysis_appointments(patient_id, service[1], address, appointment_date, time)
        QMessageBox.information(self, "Успех", "Вы успешно записались на сдачу анализов")
        self.close()


class ConsultationMenu(QDialog):
    def __init__(self, row, phone):
        super().__init__()
        self.user_phone = phone
        self.row = row
        self.services = get_services()
        self.service = self.services[self.row]
        self.setWindowTitle('Запись на консультацию специалиста')
        self.setGeometry(400, 400, 300, 200)
        self.layout = QVBoxLayout()

        self.service_info = QLabel()
        self.service_info.setFont(QtGui.QFont("Calibri", 14))

        self.doctor_combo = QComboBox()
        self.doctor_id = QLineEdit()
        self.address_combo = QComboBox()
        self.appointment_date_input = QDateEdit()
        self.appointment_date_input.setCalendarPopup(True)
        self.appointment_date_input.setDisplayFormat("dd-MM-yyyy")
        self.time_input = QTimeEdit()
        self.cabinet = QLineEdit()

        self.load_service_info()
        self.load_combobox_data()

        self.layout.addWidget(self.service_info)
        self.layout.addWidget(QLabel('Выберите специалиста:'))
        self.layout.addWidget(self.doctor_combo)
        self.layout.addWidget(QLabel('Выберите адрес:'))
        self.layout.addWidget(self.address_combo)
        self.layout.addWidget(QLabel('Выберите дату:'))
        self.layout.addWidget(self.appointment_date_input)
        self.layout.addWidget(QLabel('Выберите время:'))
        self.layout.addWidget(self.time_input)

        self.save_button = QPushButton("Записаться")
        self.save_button.clicked.connect(self.save_appointment)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QLabel {
                color: #003366;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QDateEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QTimeEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def load_service_info(self):
        self.service_info.setText(f"{self.service[1]} - {self.service[4]} руб")

    def load_combobox_data(self):
        doctors = get_doctor_by_specialization(self.service[1])

        self.doctor_combo.clear()
        self.address_combo.clear()
        for doctor in doctors:
            self.doctor_combo.addItem(f"{doctor[1]} {doctor[2]}")
            self.address_combo.addItem(f"{doctor[8]}")
            self.cabinet.setText(doctor[9])
            self.doctor_id.setText(str(doctor[0]))

    def save_appointment(self):
        patient_id = get_user(self.user_phone)[0]
        doctor_id = self.doctor_id.text()
        address = self.address_combo.currentText()
        appointment_date = self.appointment_date_input.date().toString("dd-MM-yyyy")
        time = self.time_input.text()
        cabinet = self.cabinet.text()

        if not patient_id or not doctor_id or not address or not appointment_date or not time:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        add_appointment(patient_id, doctor_id, address, appointment_date, time, cabinet)
        QMessageBox.information(self, "Успех", "Вы успешно записались на консультацию")
        self.close()


class AdminWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система учёта медицинских записей")
        self.setGeometry(450, 150, 300, 150)
        self.layout = QVBoxLayout()

        self.add_data_button = QPushButton("Добавление данных")
        self.view_data_button = QPushButton("Просмотр добавленных данных")

        self.add_data_button.clicked.connect(self.open_add_data_dialog)
        self.view_data_button.clicked.connect(self.open_view_data_dialog)

        self.layout.addWidget(self.add_data_button)
        self.layout.addWidget(self.view_data_button)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    @staticmethod
    def open_add_data_dialog():
        dialog = AddDataDialog()
        dialog.exec()

    @staticmethod
    def open_view_data_dialog():
        dialog = ViewDataDialog()
        dialog.exec()

    @staticmethod
    def refresh_tables():
        ViewDataDialog.refresh_tables()


class AddDataDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление данных")
        self.setGeometry(150, 150, 450, 300)

        self.tabs = QTabWidget()
        self.add_doctor_tab = AddDoctorTab()
        self.add_appointment_tab = AddAppointmentTab()

        self.tabs.addTab(self.add_doctor_tab, "Добавить врача")
        self.tabs.addTab(self.add_appointment_tab, "Добавить медицинскую запись")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QTabWidget::pane {
                background-color: #f0f8ff;
                border: 1px solid #003366;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background-color: #005799;
            }
        """)


class AddDoctorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.patronymic = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd-MM-yyyy")
        self.specialization_combo = QComboBox()
        self.experience_input = QLineEdit()
        self.education_input = QLineEdit()
        self.office_address_combo = QComboBox()
        self.cabinet_input = QLineEdit()

        specializations = ["Терапевт", "Кардиолог", "Невролог", "Офтальмолог", "Педиатр", "Хирург", "Дерматолог",
                           "Эндокринолог", "Нутрициолог", "Фармаколог"]
        self.specialization_combo.addItems(specializations)

        addresses = ["Волгоградский пр-т. 43", "Малая Бронная ул. 12", "Комсомолькая ул. 71"]
        self.office_address_combo.addItems(addresses)

        self.layout.addRow("Фамилия:", self.last_name_input)
        self.layout.addRow("Имя:", self.first_name_input)
        self.layout.addRow("Отчество:", self.patronymic)
        self.layout.addRow("Дата рождения:", self.dob_input)
        self.layout.addRow("Специализация:", self.specialization_combo)
        self.layout.addRow("Стаж:", self.experience_input)
        self.layout.addRow("Образование:", self.education_input)
        self.layout.addRow("Адрес клиники:", self.office_address_combo)
        self.layout.addRow("Кабинет:", self.cabinet_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_doctor)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QDateEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def save_doctor(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        patronymic = self.patronymic.text()
        dob = self.dob_input.text()
        specialization = self.specialization_combo.currentText()
        experience = self.experience_input.text()
        education = self.education_input.text()
        office_address = self.office_address_combo.currentText()
        cabinet = self.cabinet_input.text()

        if not first_name or not last_name or not patronymic or not specialization or not dob or not experience \
                or not education or not office_address or not cabinet:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        add_doctor(last_name, first_name, patronymic, dob, specialization, experience, education, office_address,
                   cabinet)
        self.close()


class AddAppointmentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()

        self.patient_combo = QComboBox()
        self.doctor_combo = QComboBox()
        self.address_combo = QComboBox()
        self.appointment_date_input = QDateEdit()
        self.appointment_date_input.setCalendarPopup(True)
        self.appointment_date_input.setDisplayFormat("dd-MM-yyyy")
        self.time = QTimeEdit()
        self.cabinet = QLineEdit()

        self.layout.addRow("Пациент:", self.patient_combo)
        self.layout.addRow("Врач:", self.doctor_combo)
        self.layout.addRow("Дата приема:", self.appointment_date_input)
        self.layout.addRow("Время приема:", self.time)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_appointment)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        self.load_combobox_data()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QDateEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QTimeEdit {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def load_combobox_data(self):
        patients = get_users()
        doctors = get_doctors()

        self.patient_combo.clear()
        self.doctor_combo.clear()

        for patient in patients:
            self.patient_combo.addItem(f"{patient[3]} {patient[4]} {patient[1]}", patient[0])

        for doctor in doctors:
            self.doctor_combo.addItem(f"{doctor[1]} {doctor[2]} - {doctor[5]}", doctor[0])
            self.address_combo.addItem(f"{doctor[8]}")
            self.cabinet.setText(doctor[9])

    def save_appointment(self):
        patient_id = self.patient_combo.currentData()
        doctor_id = self.doctor_combo.currentData()
        address = self.address_combo.currentText()
        appointment_date = self.appointment_date_input.date().toString("dd-MM-yyyy")
        time = self.time.text()
        cabinet = self.cabinet.text()

        if not patient_id or not doctor_id or not appointment_date:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        add_appointment(patient_id, doctor_id, address, appointment_date, time, cabinet)
        self.close()


class ViewDataDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр добавленных данных")
        self.setGeometry(150, 150, 900, 600)

        self.tabs = QTabWidget()
        self.patient_table = QTableWidget()
        self.doctor_table = QTableWidget()
        self.appointment_table = QTableWidget()

        self.patient_table.setSortingEnabled(True)
        self.doctor_table.setSortingEnabled(True)
        self.appointment_table.setSortingEnabled(True)

        self.patient_table.setColumnCount(7)
        self.patient_table.setHorizontalHeaderLabels(['ID', 'Телефон', 'Пароль', 'Фамилия', 'Имя', 'Отчество',
                                                      'Дата рождения'])

        self.doctor_table.setColumnCount(10)
        self.doctor_table.setHorizontalHeaderLabels(['ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения',
                                                     'Специализация', 'Стаж', 'Образование', 'Адрес клиники', 'Кабинет']
                                                    )

        self.appointment_table.setColumnCount(7)
        self.appointment_table.setHorizontalHeaderLabels(['ID', 'Пациент', 'Врач', 'Адрес клиники', 'Дата приёма',
                                                          'Время приёма', 'Кабинет'])

        self.tabs.addTab(self.patient_table, "Пациенты")
        self.tabs.addTab(self.doctor_table, "Врачи")
        self.tabs.addTab(self.appointment_table, "Медицинские записи")

        self.delete_patient_button = QPushButton("Удалить пациента")
        self.delete_doctor_button = QPushButton("Удалить врача")
        self.delete_appointment_button = QPushButton("Удалить запись")

        self.delete_patient_button.clicked.connect(self.delete_selected_patient)
        self.delete_doctor_button.clicked.connect(self.delete_selected_doctor)
        self.delete_appointment_button.clicked.connect(self.delete_selected_appointment)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.delete_patient_button)
        layout.addWidget(self.delete_doctor_button)
        layout.addWidget(self.delete_appointment_button)
        self.setLayout(layout)

        self.refresh_tables()

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f8ff;
                color: #003366;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #003366;
                border-radius: 5px;
                padding: 5px;
            }
            QTabWidget::pane {
                background-color: #f0f8ff;
                border: 1px solid #003366;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background-color: #005799;
            }
            QPushButton {
                background-color: #003366;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005799;
            }
        """)

    def refresh_tables(self):
        patients = get_users()
        self.patient_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            for col, value in enumerate(patient):
                self.patient_table.setItem(row, col, QTableWidgetItem(str(value)))
        self.patient_table.resizeColumnsToContents()

        doctors = get_doctors()
        self.doctor_table.setRowCount(len(doctors))
        for row, doctor in enumerate(doctors):
            for col, value in enumerate(doctor):
                self.doctor_table.setItem(row, col, QTableWidgetItem(str(value)))
        self.doctor_table.resizeColumnsToContents()

        appointments = get_appointments()
        self.appointment_table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            for col, value in enumerate(appointment):
                self.appointment_table.setItem(row, col, QTableWidgetItem(str(value)))
        self.appointment_table.resizeColumnsToContents()

    def delete_selected_patient(self):
        selected_items = self.patient_table.selectedItems()
        if selected_items:
            patient_id = selected_items[0].text()
            delete_patient(patient_id)
        self.close()

    def delete_selected_doctor(self):
        selected_items = self.doctor_table.selectedItems()
        if selected_items:
            doctor_id = selected_items[0].text()
            delete_doctor(doctor_id)
        self.close()

    def delete_selected_appointment(self):
        selected_items = self.appointment_table.selectedItems()
        if selected_items:
            appointment_id = selected_items[0].text()
            delete_appointment(appointment_id)
        self.close()


create_tables()
app = QApplication(sys.argv)
window = LoginDialog()
window.show()
sys.exit(app.exec())
