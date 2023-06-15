import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction
from PyQt5 import uic
from connect_db import Сonnect_DB_users, Сonnect_DB_data
from pyperclip import copy


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MainClass(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('data/ui/main.ui', self)

        self.user_active_id = None
        self.update_list()

        self.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))

        self.btn_page_1.clicked.connect(self.update_list)
        self.btn_new_entry.clicked.connect(self.new_entry)
        self.listWidget.itemClicked.connect(self.lw_clicked)

        self.copy_note_name.clicked.connect(lambda x: copy(self.note_name_out.toPlainText()))
        self.copy_login.clicked.connect(lambda x: copy(self.login_out.toPlainText()))
        self.copy_password.clicked.connect(lambda x: copy(self.password_out.toPlainText()))

    def lw_clicked(self, event):
        title = event.text()
        login, password = db_data.get_data(self.user_active_id, title)[0]
        self.note_name_out.setText(title)
        self.login_out.setText(login)
        self.password_out.setText(password)

    def update_list(self):
        self.listWidget.clear()
        data = db_data.get_titles(self.user_active_id)
        for el in data:
            self.listWidget.addItem(el[0])

    def new_entry(self):
        title = self.note_name_text.toPlainText()
        login = self.login_text.toPlainText()
        password = self.password_text.toPlainText()

        result = db_data.new_entry(self.user_active_id, title, login, password)

        if result == 1:
            self.message(f'Title: <{title}> is already taken.')
        else:
            self.message(f'All OK!', typee=0)

    def user_info(self):
        print(db_users.user_info(self.user_active_id))

    def message(self, text, typee=1):
        msg = QMessageBox()
        if typee:
            msg.setInformativeText(text)
            msg.setWindowTitle("Error")
        elif typee == 0:
            msg.setInformativeText(text)
            msg.setWindowTitle("Notice")
        msg.exec_()



class WinSingUp(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('data/ui/sign_up.ui', self)

        self.create_new_acc.clicked.connect(self.new_user)

    def closeEvent(self, event):
        win_sing_in.show()

    def new_user(self):
        print('Start add new user.')
        login = self.login_text_new.toPlainText()
        password = self.password_text_new.toPlainText()

        if login == '' or password == '':
            self.message('Fields should not be empty.')
            print('Error')
            return 0


        print(f'Login: {login};\nPassword: {password}.')

        result = db_users.new_user(login, password)

        print(f'Result: {result}')

        if result == 0:
            self.close()
            self.message(f'New user <{login}> is registered!', 0)
        elif result == 1:
            self.message('User already exists.')
        elif result == 3 or result == 4:
            if result == 3:
                self.message('Forbidden character in the login - (&=+<>,-.).')
            elif result == 4:
                self.message('Forbidden character in the password - (&=+<>,-.).')
        elif result == 6:
            self.message('Password length must be between 6 <= x <= 30')
        else:
            self.message('Unknown error :(')

        print('End add new user.')

    def message(self, text, type=1):
        msg = QMessageBox()
        if type:
            msg.setInformativeText(text)
            msg.setWindowTitle("Error")
        elif type == 0:
            msg.setInformativeText(text)
            msg.setWindowTitle("Notice")
        msg.exec_()


class WinSingIn(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('data/ui/sign_in.ui', self)

        self.user_active = None

        self.login_text.setText('')
        self.password_text.setText('')

        self.sign_up.clicked.connect(self.sign_up_win)
        self.sign_in.clicked.connect(self.sign_in_user)

    def sign_up_win(self):
        self.close()
        win_sing_up.login_text_new.setText('')
        win_sing_up.password_text_new.setText('')
        win_sing_up.show()

    def sign_in_user(self):
        login = self.login_text.toPlainText()
        password = self.password_text.toPlainText()

        if login == '' or password == '':
            self.message('Fields should not be empty.')
            return 0

        result = db_users.check_user(login, password)

        if result == 0:
            self.start_app(login)
        elif result == 1:
            self.message('Incorrect login.')
        elif result == 2:
            self.message('Incorrect password.')

    def start_app(self, login):
        user_id = db_users.take_id(login)
        mainWin.user_active_id = user_id
        db_users.con.close() # break connection with database
        self.close()
        mainWin.show()

    def message(self, text, typee=1):
        msg = QMessageBox()
        if typee:
            msg.setInformativeText(text)
            msg.setWindowTitle("Error")
        elif typee == 0:
            msg.setInformativeText(text)
            msg.setWindowTitle("Notice")
        msg.exec_()




if __name__ == '__main__':
    db_users = Сonnect_DB_users()
    db_data = Сonnect_DB_data()

    app = QApplication(sys.argv)

    mainWin = MainClass()
    win_sing_in = WinSingIn()
    win_sing_up = WinSingUp()

    win_sing_in.show()

    sys.excepthook = except_hook
    sys.exit(app.exec_())