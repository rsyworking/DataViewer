import os
from dataclasses import dataclass
from os import remove

from PySide6 import  QtCore, QtGui, QtWidgets

CONDITIONS = ['contains', 'starts_with', 'ends_with']


@dataclass
class FilterData:
    condition: int
    keyword: str

    def __init__(self, condition: int, keyword: str):
        self.condition = condition
        self.keyword = keyword

    def __getitem__(self, item):
        if item == 0:
            return self.condition
        elif item == 1:
            return self.keyword

    def __setitem__(self, key, value):
        if key == 0:
            self.condition =value
        elif key == 1:
            self.keyword = value


class MyFilterModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._headers = ['condition', 'keyword']
        self._data = []

    def add_filter(self):
        '''
        get file_data from new_folder
        :param new_folder: str
        '''
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        self._data.append(FilterData(0, ''))
        self.layoutChanged.emit()
        self.endResetModel()

    def remove_filter(self, index):
        '''
        get file_data from new_folder
        :param new_folder: str
        '''
        self.beginResetModel()
        self.layoutAboutToBeChanged.emit()
        del self._data[index]
        self.layoutChanged.emit()
        self.endResetModel()

    def update_filter(self, row, column, value):
        self._data[row][column] = value

    def get_filter_data(self, row, column):
        return self._data[row][column]

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

    def get_reg_data(self):
        result = []
        for filter_data in self._data:
            if not filter_data.keyword:
                continue
            if filter_data.condition == 0:
                # contain
                result.append(r'^.*(' + filter_data.keyword + r').*$')
            elif filter_data.condition == 1:
                # startswith
                result.append(r'^(' + filter_data.keyword + r').*')
            elif filter_data.condition == 2:
                # endswith
                result.append(r'.*(' + filter_data.keyword + r')$')
        return result


class FilterComposer(QtWidgets.QScrollArea):

    '''
    doc about how to make a custom view:
    https://www.informit.com/articles/article.aspx?p=1613548
    '''

    filter_updated = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        # map row index to QRectF
        self.rectForRow = {}
        self.condition_widgets = {}
        self.filter_texts = {}

        self.model = MyFilterModel()

        content_widget = QtWidgets.QWidget()
        self.setWidget(content_widget)
        self.setWidgetResizable(True)

        self.layout = QtWidgets.QVBoxLayout(content_widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        add_remove_widget = QtWidgets.QWidget()
        add_remove_layout = QtWidgets.QHBoxLayout(add_remove_widget)
        self.layout.addWidget(add_remove_widget)
        add_button = QtWidgets.QPushButton('add filter')
        add_button.clicked.connect(self.add_new_filter)
        add_remove_layout.addWidget(add_button)

        grid_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(grid_widget)
        self.layout.addWidget(grid_widget)

        self.set_grid_layout()
        self.setMaximumHeight(200)

    def set_grid_layout(self):
        self.condition_widgets = {}
        self.filter_texts = {}

        for i in range(self.grid_layout.rowCount()):
            row = self.grid_layout.rowCount()  - i - 1
            for j in range(self.model.columnCount() + 1):
                item = self.grid_layout.itemAtPosition(row,j)
                if item:
                    widget = item.widget()
                    if widget:
                        self.grid_layout.removeItem(item)
                        widget.hide()
                        widget.deleteLater()

        for i in range(self.model.rowCount()):
            condition = QtWidgets.QComboBox()
            self.condition_widgets[i] = condition
            condition.addItems(CONDITIONS)
            condition.setCurrentIndex(self.model.get_filter_data(i, 0))
            condition.currentIndexChanged.connect(lambda x, index = i: self.on_update_filter(index, 0))
            self.grid_layout.addWidget(condition, i, 0)

            filter_text = QtWidgets.QLineEdit()
            self.filter_texts[i] = filter_text
            filter_text.setText(self.model.get_filter_data(i, 1))
            filter_text.textChanged.connect(lambda x, index = i: self.on_update_filter(index, 1))
            self.grid_layout.addWidget(filter_text, i, 1)

            remove_button = QtWidgets.QPushButton('-')
            remove_button.clicked.connect(lambda x, index = i: self.remove_filter(index))
            self.grid_layout.addWidget(remove_button, i, 2)

    def on_update_filter(self, row, column):
        if column == 0:
            self.model.update_filter(row, column, self.condition_widgets[row].currentIndex())
        elif column == 1:
            self.model.update_filter(row, column, self.filter_texts[row].text())
        self.filter_updated.emit(self.get_reg_filter())

    def add_new_filter(self, *args):
        self.model.add_filter()
        self.set_grid_layout()
        self.filter_updated.emit(self.get_reg_filter())

    def remove_filter(self, row, *args):
        self.model.remove_filter(row)
        self.set_grid_layout()
        self.filter_updated.emit(self.get_reg_filter())

    def get_reg_filter(self, *args):
        return self.model.get_reg_data()
