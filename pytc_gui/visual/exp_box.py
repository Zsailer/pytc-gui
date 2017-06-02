from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import seaborn
from io import StringIO

from ..exp_frames import LocalBox, GlobalBox, ConnectorsBox
import pytc


class ParamTable(QTableWidget):
    """
    take csv style param string and put into table widget
    """

    def __init__(self, fitter):
        super().__init__()

        self._fitter = fitter
        self._header = []
        self._col_name = []
        self._data = []

        self.setAlternatingRowColors(True)

    def load_table(self):
        """
        load fit data into the table
        """
        for i, row in enumerate(self._data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.setItem(i, j, item)

    def csv_to_table(self):
        """
        convert csv data file to lists to be read by qtablewidget
        """
        self._header = []
        self._col_name = []
        self._data = []

        file_data = self._fitter.fit_as_csv
        string_file = StringIO(file_data)

        # break up the file data
        for i in string_file:
            if i.startswith("#"):
                self._header.append(i.rstrip())
            elif i.startswith("type"):
                i = i.rstrip().split(',')
                self._col_name = i
            else:
                i = i.rstrip().split(',')
                self._data.append(i)

        for l in self._header:
            print(l)
        print("\n")

    def update(self):
        """
        update the table with updated fit parameters
        """
        self.csv_to_table()

        self.setRowCount(len(self._data))
        self.setColumnCount(len(self._data[0]))
        self.setHorizontalHeaderLabels(self._col_name)

        self.load_table()

    def clear(self):
        """
        """
        super().clear()
        self._header = []
        self._col_name = []
        self._data = []

class ExperimentBox(QWidget):
    """
    Experiment box widget.  This will have all experiments and a parameter
    table.
    """

    fit_signal = pyqtSignal()

    def __init__(self, parent):
        """
        """
        super().__init__()

        self._parent = parent

        self._slider_list = {"Global" : {}, "Local" : {}}
        self._global_var = []
        self._global_tracker = {}
        self._global_connectors = {}
        self._connectors_seen = {}
        self._plot_box = parent._plot_box
        self._update = parent.do_fit_callback

        self.layout()

    def layout(self):
        """
        Create layout.
        """
        self._main_layout = QVBoxLayout(self)

        # scroll box for experiments
        self._scroll = QScrollArea(self)
        self._exp_content = QWidget()
        self._exp_box = QVBoxLayout(self._exp_content)
        self._scroll.setWidget(self._exp_content)
        self._scroll.setWidgetResizable(True)
        self._exp_box.setAlignment(Qt.AlignTop)

        # paramater table
        self._param_box = ParamTable(self._parent.fitter)

        # splitter for experiments and parameter widgets
        self._splitter = QSplitter(Qt.Vertical)
        self._splitter.addWidget(self._scroll)
        self._splitter.addWidget(self._param_box)
        self._splitter.setSizes([200, 200])

        self._main_layout.addWidget(self._splitter)

    def update_exp(self):
        """
        Update fit and parameters, update experiments added to fitter
        """
        self._experiments = self._parent.fitter.experiments

        if len(self._experiments) != 0:
            # create local holder if doesn't exist
            for e in self._experiments:
                if e in self._slider_list["Local"]:
                    continue

                self._slider_list["Local"][e] = []
                self._connectors_seen[e] = []

                file_name = e.dh_file
                exp_name = file_name.split("/")[-1]

                exp = LocalBox(e, exp_name, self)
                self._exp_box.addWidget(exp)
        else:
            # clear anything that might be in parameter box
            self._param_box.clear()

    def perform_fit(self, options):
        """
        perform complete fit, update all
        """
        self.update_exp()

        # check for instances of LocalBox and set any attributes
        for loc_obj in self._exp_box.parentWidget().findChildren(LocalBox):
            loc_obj.set_attr()

        try:
            # after doing fit, emit signal to sliders and update parameter table
            self._parent.fitter.fit(**options)
            self.fit_signal.emit()
            self._param_box.update()
        except:
            pass

    def clear(self):
        """
        for clearing the application
        """
        try:
            # check for any global/connector vars, remove them first
            for i in range(self._exp_box.count()): 
                widget = self._exp_box.itemAt(i).widget()
                if isinstance(widget, LocalBox):
                    continue

                widget.remove()

            # finally, remove local objects
            for loc_obj in self._exp_box.parentWidget().findChildren(LocalBox):
                self._parent.fitter.remove_experiment(loc_obj._exp)
                loc_obj.deleteLater()
        except:
            pass

        # reset all lists/dictionaries
        self._slider_list = {"Global" : {}, "Local" : {}}
        self._global_var = []
        self._connectors_seen = {}
        self._global_connectors = {}
        self._global_tracker = {}

        self._param_box.clear()