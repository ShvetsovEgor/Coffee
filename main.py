import sqlite3
import sys
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Отображение информации о кофе")
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM price""").fetchall()
        self.tableWidget.setRowCount(len(result))
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
