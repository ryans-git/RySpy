#!/usr/bin/env python

import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QBoxLayout, QCheckBox, QComboBox,
        QDial, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QScrollBar,
        QSlider, QSpinBox, QStackedWidget, QWidget, QLCDNumber)


class ServoControls(QGroupBox):

    valueChanged = pyqtSignal(int)

    def __init__(self, title, parent=None):
        super(ServoControls, self).__init__(title, parent)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)

        self.dial = QDial()
        self.dial.setFocusPolicy(Qt.StrongFocus)
        self.dial.setNotchesVisible(True)

        self.lcd_display = QLCDNumber()
        self.lcd_display.display(22)

        self.slider.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.lcd_display.display)
        self.dial.valueChanged.connect(self.slider.setValue)
        self.dial.valueChanged.connect(self.valueChanged)

        boxLayout = QBoxLayout(QBoxLayout.TopToBottom)
        boxLayout.addWidget(self.slider)
        boxLayout.addWidget(self.dial)
        boxLayout.addWidget(self.lcd_display)
        boxLayout.setStretchFactor(self.dial, 20)
        self.setLayout(boxLayout)    

        self.setMinimum(0)
        self.setMaximum(100)
        self.dial.setWrapping(True)

    # This shit isnt even getting called
    def setValue(self, value):    
        print("Slider Value: " + str(value))
        self.slider.setValue(value)    
        self.dial.setValue(value)
        self.lcd_display.display(value)

    def setMinimum(self, value):    
        self.slider.setMinimum(value)
        self.dial.setMinimum(value)    

    def setMaximum(self, value):    
        self.slider.setMaximum(value)
        self.dial.setMaximum(value)    



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.pan = ServoControls("Pan")
        self.tilt = ServoControls("Tilt")
        layout = QHBoxLayout()
        layout.addWidget(self.pan)
        layout.addWidget(self.tilt)
        self.setLayout(layout)

        self.setWindowTitle("Sliders")
        self.setMinimumSize(500,300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
