import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.button_make.clicked.connect(self.make_coffee)
        self.button_remake.clicked.connect(self.remake_coffee)
        self.button_find.clicked.connect(self.find_coffee)

    def make_coffee(self):
        try:
            coffee, roasting = self.line_make_coffee.text(), self.line_make_roasting.text()
            grains, description = self.line_make_grains.text(), self.line_make_description.text()
            price, V = self.line_make_price.text(), self.line_make_V.text()

            if not all([coffee, roasting, grains, description, price, V]):
                raise Exception("!!!ОШИБКА!!! Некоторые поля пусты")

            ex.cur.execute("""INSERT INTO Кофе (
            title,
            roasting,
            grains,
            description,
            price,
            V)
            VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?)""", (coffee, roasting, grains, description, float(price), float(V),))
            ex.con.commit()
            ex.show_coffee()

        except Exception as obj:
            self.label_error.setText(str(obj))

    def find_coffee(self):
        try:
            if not self.line_find_id.text():
                raise Exception("!!!ОШИБКА!!! Не введен id кофе")

            id = int(self.line_find_id.text())

            result = ex.cur.execute("""SELECT title, roasting, grains, description, price, V FROM Кофе
                WHERE id = ?""", (id,)).fetchone()

            self.line_remake_coffee.setText(result[0]), self.line_remake_roasting.setText(result[1])
            self.line_remake_grains.setText(result[2]), self.line_remake_description.setText(result[3])
            self.line_remake_price.setText(str(result[4])), self.line_remale_V.setText(str(result[5]))

        except Exception as obj:
            self.label_error.setText(str(obj))

    def remake_coffee(self):
        try:
            coffee, roasting = self.line_remake_coffee.text(), self.line_remake_roasting.text()
            grains, description = self.line_remake_grains.text(), self.line_remake_description.text()
            price, V = self.line_remake_price.text(), self.line_remale_V.text()
            id = self.line_find_id.text()

            if not all([coffee, roasting, grains, description, price, V, id]):
                raise Exception("!!!ОШИБКА!!! какое-то поле пустое")

            ex.cur.execute("""REPLACE INTO Кофе (
            id,
            title,
            roasting,
            grains,
            description,
            price,
            V)
            VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?)
            """, (int(id), coffee, roasting, grains, description, float(price), float(V),))
            ex.con.commit()

            ex.show_coffee()

        except Exception as obj:
            self.label_error.setText(str(obj))


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.button_open_form.clicked.connect(self.open_form)
        self.show_coffee()

    def show_coffee(self):
        result = self.cur.execute("""SELECT * FROM Кофе""").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))

    def open_form(self):
        self.coffee_form = Form()
        self.coffee_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
