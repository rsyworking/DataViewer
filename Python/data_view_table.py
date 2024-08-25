import os
import re
from PySide6 import  QtCore, QtGui, QtWidgets
from file_data import FileData

class MySortFilterProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self):
        super().__init__()
        look_for_body = [r'^.*(body).*$']
        self.reg_patterns = [['.'],['.'], ['.']]

    # def lessThan(self, left, right):
    #     '''
    #     :param left: QModelIndex
    #     :param right: QModelIndex
    #     :return: bool
    #     '''
    #     return super().lessThan(left, right)

    def filterAcceptsRow(self,sourceRow, sourceParent):
        model = self.sourceModel()
        for i in range(model.columnCount()):
            index0 = model.index(sourceRow, 0, sourceParent)
            value = model.data(index0)
            for pattern in self.reg_patterns[i]:
                match = re.match(pattern, value, re.IGNORECASE)
                # don't include the row if any of the column doesn't match corresponding pattern
                if not match:
                    return False
        return True


class MyFileModel(QtCore.QAbstractTableModel):

    def __init__(self, folder):
        super().__init__()
        self._headers = ['file_name', 'file_type', 'date modified']
        self.folder = folder
        self._data = []
        self.refresh_data()

    @QtCore.Slot()
    def refresh_data(self):
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        self._data = []
        for root, dirs, files in os.walk(self.folder):
            for name in files:
                file_path = os.path.join(root, name)
                self._data.append(FileData(file_path))
        self.layoutChanged.emit()
        self.endResetModel()

    def update_folder(self, new_folder):
        '''
        get file_data from new_folder
        :param new_folder: str
        '''
        self.folder = new_folder
        self.refresh_data()

    def rowCount(self, parent=''):
        return len(self._data)

    def columnCount(self, parent=''):
        return len(self._headers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value
        if role == QtCore.Qt.BackgroundRole and index.column() == 0:
            # See below for the data structure.
            return QtGui.QColor('blue')
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        # row and column headers
        if orientation == QtCore.Qt.Horizontal:
            return self._headers[section]
        else:
            return None


class DataViewTable(QtWidgets.QTableView):

    def __init__(self, folder_path=''):
        super().__init__()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.model = MyFileModel(folder_path)
        self.model.refresh_data()
        self.proxy_model =MySortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        # autoscroll when drag select items in view
        self.setAutoScroll(True)

    def get_headers_text(self):
        count = self.horizontalHeader().count()
        all_headers_text = [self.horizontalHeader().model().headerData(i, QtCore.Qt.Horizontal) for i in range(0, count)]
        print(all_headers_text)
        return all_headers_text

    def update_folder(self, new_folder, *args):
        self.model.update_folder(new_folder)

    def on_sort_by_column_updated(self, index, *args):
        self.sortByColumn(index, QtCore.Qt.AscendingOrder)

    def set_reg_filter(self, reg_data, *args):
        self.model.layoutAboutToBeChanged.emit()
        self.proxy_model.reg_patterns[0] = reg_data
        self.model.layoutChanged.emit()

