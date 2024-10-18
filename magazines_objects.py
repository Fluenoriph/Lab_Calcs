from PyQt6 import QtWidgets, QtCore, QtGui, QtSql
import constants


class MagazineAllFactors(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.connect_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.connect_db.setDatabaseName('magazine.sqlite')
        self.connect_db.open()

        self.model_type = QtSql.QSqlTableModel(parent=self)
        self.model_type.setTable('objects')
        self.model_type.setSort(1, QtCore.Qt.SortOrder.AscendingOrder)
        #self.model_type.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnRowChange)
        self.model_type.select()

        self.rec = self.connect_db.record('objects')
        self.rec.setValue('fff', 'iii')
        self.rec.setValue('hhh', 'gggg')
        self.model_type.insertRecord(-1, self.rec)


        self.model_type.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, constants.MAGAZINE_HEADER_NAMES[0])


        self.box = QtWidgets.QVBoxLayout(self)
        self.table_type = QtWidgets.QTableView(self)
        self.table_type.setModel(self.model_type)
        self.table_type.hideColumn(0)
        self.table_type.setColumnWidth(1, 90)
        self.table_type.setColumnWidth(2, 150)
        self.table_type.setColumnWidth(3, 150)
        self.table_type.setColumnWidth(4, 200)
        self.table_type.setColumnWidth(5, 80)
        self.box.addWidget(self.table_type)
        '''self.button_add = QtWidgets.QPushButton("Добавить запись")
        self.button_add.clicked.connect(self.add_record)
        self.button_delete = QtWidgets.QPushButton("Удалить запись")
        self.button_delete.clicked.connect(self.delete_record)'''
        self.resize(600, 500)

        self.show()

    @QtCore.pyqtSlot()
    def add_record(self):
        self.model_type.insertRow(self.model_type.rowCount())

    @QtCore.pyqtSlot()
    def delete_record(self):
        self.model_type.removeRow(self.table_type.currentIndex().row())
        self.model_type.select()




















if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table = MagazineAllFactors()
    sys.exit(app.exec())
