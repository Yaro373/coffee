from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from PyQt5 import uic
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.push_button_action)
        self.select_data()

    def select_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cur = connection.cursor()
        data = cur.execute('SELECT * FROM coffee').fetchall()
        headers = list(map(lambda attr: attr[0], cur.description))
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.itemClicked.connect(self.item_clicked)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def push_button_action(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.fr = AddEditCoffeeForm(self)
        self.fr.show()

    def update_row(self, idf, index):
        if index is None:
            index = self.tableWidget.rowCount() - 1
        connection = sqlite3.connect('coffee.sqlite')
        cur = connection.cursor()
        data = cur.execute('SELECT * FROM coffee WHERE id=?',
                           (idf, )).fetchall()[0]
        for i, elem in enumerate(data):
            self.tableWidget.setItem(index, i, QTableWidgetItem(str(elem)))

    def item_clicked(self, item):
        connection = sqlite3.connect('coffee.sqlite')
        cur = connection.cursor()
        print(self.tableWidget.item(item.row(), 0).text())
        print('_______')
        data = cur.execute('SELECT * FROM coffee WHERE id=?',
                           (self.tableWidget.item(item.row(), 0).text(), )).fetchall()[0]
        self.fr = AddEditCoffeeForm(self, row=item.row(), data=data)
        self.fr.show()


class AddEditCoffeeForm(QWidget):
    def __init__(self, parent, row=None, data=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.set_data(data)

        self.data = data
        print(data)
        self.parent = parent
        self.row = row
        self.lineEdit_3.editingFinished.connect(self.lineEdit_3_editing_finished_action)
        self.lineEdit_4.editingFinished.connect(self.lineEdit_4_editing_finished_action)
        self.pushButton.clicked.connect(self.save_data)
        self.pushButton_2.clicked.connect(self.cancel_action)

    def set_data(self, data):
        if data is None:
            return
        data = list(map(str, data))
        self.lineEdit_2.setText(data[1])
        self.lineEdit_3.setText(data[2])
        self.lineEdit_4.setText(data[3])
        self.lineEdit_5.setText(data[4])
        self.lineEdit_6.setText(data[5])
        self.lineEdit_7.setText(data[6])

    def lineEdit_3_editing_finished_action(self):
        text = self.lineEdit_3.text()
        if text not in map(str, range(1, 16 + 1)) and text != '':
            self.lineEdit_3.setText('1')

    def lineEdit_4_editing_finished_action(self):
        if self.lineEdit_4.text() not in ('1', '2', ''):
            self.lineEdit_4.setText('1')

    def get_data(self):
        return (self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.lineEdit_6.text(),
                self.lineEdit_7.text())

    def save_data(self):
        data = self.get_data()
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if self.data is None:
            cur.execute('''INSERT INTO coffee(name, roasting, ground, taste, price, volume)
                            VALUES (?, ?, ?, ?, ?, ?)''', (*data, ))
            idf = cur.execute('''SELECT MAX(id) FROM coffee''').fetchone()[0]

        else:
            print(data)
            cur.execute('''UPDATE coffee SET 
                            name = ?,
                            roasting = ?, 
                            ground = ?, 
                            taste = ?, 
                            price = ?, 
                            volume = ? WHERE id=?''', (*data, self.data[0]))
            idf = self.data[0]
        con.commit()
        con.close()
        self.parent.update_row(idf, self.row)
        self.close()

    def cancel_action(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
