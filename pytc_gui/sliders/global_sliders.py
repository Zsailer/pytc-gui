from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import pytc
import inspect, math

from .base import Sliders

class GlobalSliders(Sliders):
    """
    create sliders for a global exp object
    """

    def __init__(self, param_name, parent):
        """
        """
        super().__init__(param_name, parent)

    def bounds(self):
        """
        update min/max for slider
        """
        exp_range = self._fitter.param_ranges[0][self._param_name]

        min_range = exp_range[0]
        max_range = exp_range[1]

        self._min = min_range
        self._max = max_range

        # transform values based on parameter to allow floats to pass to fitter and 
        # make sliders easier to use, QtSlider only allows integers
        self._range_diff = self._max - self._min

        if self._range_diff < 10:
            min_range *= 10
            max_range *= 10
        elif self._range_diff < 100000:
            min_range /= 100
            max_range /= 100
        elif self._range_diff < 100000000.0:
            min_range = math.log10(self._min)
            max_range = math.log10(self._max)

    def update_bounds(self):
        """
        update min/max bounds and check if range needs to be updated as well
        """
        bounds = [self._min, self._max]
        self._fitter.update_bounds(self._param_name, bounds, self._exp)

        # check if bounds are smaller than range, then update.
        curr_range = self._exp.model.param_guess_ranges[self._param_name]
        curr_bounds = self._exp.model.bounds[self._param_name]

        if curr_range[0] < curr_bounds[0] or curr_range[1] > curr_bounds[1]:
            self._fitter.update_range(self._param_name, bounds, self._exp)
