import sqlite3
import sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class Dialog(QDialog):
    def __init__(self, parent, selected=""):
        super().__init__()
        self.selected = selected
        self.parent = parent
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.setWindowTitle("Изменение данных")
        self.pushButton.clicked.connect(self.submit)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        if self.selected:
            res = cur.execute(f"""SELECT * FROM price WHERE id = {int(self.selected)}""").fetchone()
        else:
            res = ["", "", "", "", "", ""]
        id, title, fried, description, price, weight = res
        self.lineEdit.setText(title)
        self.lineEdit_2.setText(fried)
        self.textEdit.setText(description)
        self.lineEdit_3.setText(str(price))
        self.lineEdit_4.setText(str(weight))

    def submit(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        # получение данных
        try:
            title = self.lineEdit.text()
            fried = self.lineEdit_2.text()
            description = self.textEdit.toPlainText()
            price = int(self.lineEdit_3.text())
            weight = int(self.lineEdit_4.text())
            if self.selected != "":
                cur.execute(
                    f"""UPDATE price SET title='{title}', fried='{fried}', description='{description}', price={price}, 
                    weight={weight} WHERE id={int(self.selected)}""").fetchall()
            else:
                cur.execute(
                    f"""INSERT INTO price (title, fried, description, price, weight) VALUES ('{title}', '{fried}', '{description}', {price}, {weight})""").fetchall()
            con.commit()
            self.parent.fill()
        except Exception as e:
            self.parent.statusBar().showMessage(f"Ошибка {e}")


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Отображение информации о кофе")
        self.tableWidget.cellDoubleClicked.connect(self.change)
        self.fill()

    def change(self, row, col):
        if self.tableWidget.item(row, col) is not None:
            self.d = Dialog(self, self.tableWidget.item(row, col).text())
            self.d.show()
        else:
            self.d = Dialog(self, '')
            self.d.show()

    def fill(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM price""").fetchall()
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ИД", "Название сорта", "Cтепень обжарки", "Описание вкуса", "Цена", "Масса"])
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Oбнаружена ошибка !:", tb)

        #    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось

    sys.excepthook = excepthook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
