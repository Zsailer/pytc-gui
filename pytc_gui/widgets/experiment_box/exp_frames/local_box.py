from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect

from .base import Experiments
from .. import slider_popup
from .. import sliders
from .exp_options import ExpOptions

class LocalBox(Experiments):
    """
    hold local parameters/sliders
    """

    def __init__(self, exp, name, parent):

        self._exp = exp
        self._required_fields = {}
        self._experiments = parent._fit.experiments
        self._fit = parent._fit
        self._exp_box = parent._exp_box
        self._update = parent._update
        self._main_box = parent

        super().__init__(name, parent)

    def exp_widgets(self):
        """
        create sliders for experiment
        """
        parameters = self._exp.param_values

        for p, v in parameters.items():
            s = sliders.LocalSliders(p, v, self)
            self._slider_list["Local"][self._exp].append(s)

    def options(self):
        """
        shots layout
        """
        # change shot start
        #self._exp_options = QPushButton("Options", self)
        #self._exp_options.setFixedWidth(200)
        #self._exp_options.clicked.connect(self.update)
        #self._main_layout.addWidget(self._exp_options)
        pass

    def slider_popup(self):
        """
        hide and show slider window
        """
        self._slider_window = slider_popup.LocalPopUp(self)
        self._slider_window.show()

    def options_popup(self):
        """
        change the shot start
        """
        self._options = ExpOptions(self,self._exp)
        self._options.show()
                
    def update_req(self):
        """
        checks if any global connectors are connected and updates to add fields for any required data
        """
        exp_connectors = self._connectors_seen[self._exp]

        for c in exp_connectors:
            required = c.required_data
            for i in required:
                if i not in self._required_fields:
                    label_name = str(i).replace("_", " ") + ": "
                    label = QLabel(label_name.title(), self)
                    field = QLineEdit(self)
                    field.setMinimumWidth(150)
                    field.setPlaceholderText("")
                    self._required_fields[i] = field

                    stretch = QHBoxLayout()
                    stretch.addWidget(label)
                    stretch.addWidget(field)
                    stretch.addStretch(1)

                    self._req_layout.addLayout(stretch)
                else:
                    pass
                    
    def set_attr(self):
        """
        update data from global connector fields
        """
        for n, v in self._required_fields.items():
            if v.text():
                try:
                    val = float(v.text())
                except:
                    val = v.text()

                setattr(self._exp, n, val)
            else:
                error_message = QMessageBox.warning(self, "Fit Unsuccessful!", "Empty required data fields present", QMessageBox.Ok)
                break

    def remove(self):
        """
        """
        self._fitter.remove_experiment(self._exp)
        self._slider_list["Local"].pop(self._exp, None)
        self.close()
