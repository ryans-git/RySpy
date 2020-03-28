#!/usr/bin/env python
#############################################################################
##
#############################################################################


import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        #self.setLayout(grid)

        box = QGroupBox("title here")
        

        pan_slider = QSlider(Qt.Horizontal)
        pan_dial = QDial()
        grid.addWidget(pan_dial, 0,0)
        grid.addWidget(pan_slider, 1,0)

        tilt_slider = QSlider(Qt.Vertical)
        tilt_dial = QDial()
        grid.addWidget(tilt_slider, 0,1)
        grid.addWidget(tilt_dial,0,2)

        # Set strect priority 1 so all scale evenly
        for row in range(0, 2, 1):
            grid.setRowStretch(row,1)
        
        for col in range(0, 3, 1):
            grid.setColumnStretch(col,1)
           
        box.setLayout(grid)

        self.move(500, 250)
        self.setWindowTitle('Calculator')
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())