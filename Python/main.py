from PySide6 import  QtCore, QtGui, QtWidgets
from data_view_table import DataViewTable
from common_widgets import FileSelector, SortOptions
from utilities.utilities import time_delta, inspect_func
from utilities.theme import set_theme
from filter_composer import FilterComposer

import sys
import os

class DataViewer(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Viewer')
        self.view_table = DataViewTable()
        self.filter_view = FilterComposer()
        self.filter_view.filter_updated.connect(self.view_table.set_reg_filter)
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addSpacing(15)

        # add file selector
        file_selector = FileSelector('Folder To Process:')
        # add sort & filter
        sort_options = SortOptions()
        sort_options.sort_options.addItems(self.view_table.get_headers_text())
        sort_options.sort_option_updated.connect(self.view_table.on_sort_by_column_updated)

        layout.addWidget(file_selector)
        layout.addWidget(sort_options)
        layout.addWidget(self.view_table)
        layout.addWidget(self.filter_view)

        file_selector.file_path_updated.connect(self.update_folder)
        self.setLayout(layout)
        self.resize(400, 600)

    @time_delta
    def update_folder(self, new_folder, *args):
        self.view_table.update_folder(new_folder)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    set_theme(app, 'dark')
    # create the instance of our Window
    window = DataViewer()
    window.show()

    # start the app
    sys.exit(app.exec())