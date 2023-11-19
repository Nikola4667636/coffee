import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        result = self.cur.execute("""SELECT * FROM Кофе""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
