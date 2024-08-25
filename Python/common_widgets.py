from PySide6 import  QtCore, QtGui, QtWidgets


class FileSelector(QtWidgets.QWidget):

    file_path_updated = QtCore.Signal(str)

    def __init__(self, title='', parent=None):
        super(FileSelector, self).__init__(parent=parent)
        self.title = title
        self.build_ui()
        self.show()

    def build_ui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)

        label = QtWidgets.QLabel(self.title)
        layout.addWidget(label)
        self.file_path_edit = QtWidgets.QLineEdit()
        self.file_path_edit.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(self.file_path_edit)
        self.button = QtWidgets.QPushButton('Select')
        self.button.clicked.connect(self.find_file)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.setMinimumWidth(600)

    def find_file(self, *args):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        filenames = []
        if dlg.exec_():
            filenames = dlg.selectedFiles()
        if filenames:
            self.file_path_edit.setText(filenames[0])
            self.file_path_updated.emit(self.file_path_edit.text())


class SortOptions(QtWidgets.QWidget):
    sort_option_updated = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(SortOptions, self).__init__(parent=parent)
        self.build_ui()
        self.show()

    def build_ui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)

        label = QtWidgets.QLabel('Sort Options:')
        layout.addWidget(label)
        self.sort_options = QtWidgets.QComboBox()
        self.sort_options.currentIndexChanged.connect(self.on_sort_option_updated)
        layout.addWidget(self.sort_options)
        self.setLayout(layout)

    def on_sort_option_updated(self, *args):
        self.sort_option_updated.emit(self.sort_options.currentIndex())


class FilterOptions(QtWidgets.QWidget):
    filter_option_updated = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(FilterOptions, self).__init__(parent=parent)
        self.build_ui()
        self.show()

    def build_ui(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)

        label = QtWidgets.QLabel('Filters:')
        layout.addWidget(label)
        self.filter_options = QtWidgets.QLineEdit()
        self.filter_options.textChanged.connect(self.on_filter_option_updated)
        layout.addWidget(self.filter_options)
        self.setLayout(layout)

    def on_filter_option_updated(self, *args):
        self.filter_option_updated.emit(self.sort_options.currentIndex())