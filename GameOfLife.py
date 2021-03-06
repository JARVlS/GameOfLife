from email.charset import QP
from uiFiles.GameOfLifeWindow import Ui_MainWindow
from PySide6 import QtSql, QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QThread, Signal
import random, time

ADJACENTS:set = {(-1, 1), (0, 1), (1, 1), (-1, 0),
             (1, 0), (-1, -1), (0,-1), (1,-1)}

class ContainingFrame(QFrame):
    def __init__(self):
        super().__init__()

class GameOfLife(QMainWindow, Ui_MainWindow):
    def __init__(self, population:list):
        super().__init__()
        self.setupUi(self)
        self.verticalLayout.setSpacing(0)
        self.population:list = population
        self.calculating = False
        self.btn_startCalc.clicked.connect(self.startCalc)
        self.btn_stopCalc.clicked.connect(self.stopCalc)
        
        self.thread = {}
    
    def calc_next_gen(self):
        new_pop = []
        for line_number, line in enumerate(self.population):
            new_line = []
            for subject_number, subject in enumerate(line):
                new_subject = 0
                living_counter = 0
                for dy, dx in ADJACENTS:
                    try:
                        deltay = line_number+dy
                        deltax = subject_number+dx
                        if deltax < 0 or deltay < 0:
                            raise IndexError
                        living_counter += self.population[deltay][deltax] 
                    except IndexError:
                        # print(f'at the edge: line:{line_number} - subject {subject_number} - deltaX: {deltax} - deltaY: {deltay}')
                        pass
                if subject:
                    if living_counter < 2 or living_counter > 3:
                        new_subject = 0
                    else:
                        new_subject = 1
                elif living_counter  == 3:
                    new_subject = 1
                new_line.append(new_subject)
            new_pop.append(new_line)
        self.population = new_pop
        
        self.update_canvas()

    
    ##################################################
    
    def update_canvas(self):
        try:
            for line_index, line in enumerate(self.population):
                canvas_line:list[QPushButton] = self.wdgt_gameOfLife.findChildren(ContainingFrame)[line_index].findChildren(QPushButton)
                for subject_index, subject in enumerate(line):
                    canvas_subject:QPushButton = canvas_line[subject_index]
                    if subject:
                        canvas_subject.setStyleSheet(f"background: #ddd; width: {window_size/field_size}px; height: {window_size/field_size}px; border:none;")
                    else:
                        canvas_subject.setStyleSheet(f"background: #000; width: {window_size/field_size}px; height: {window_size/field_size}px; border:none;")
        except Exception:
            print('pass')
    
    def change_state(self, Xindex, Yindex):
        print(f"change state {self.population[Yindex][Xindex]}, {Yindex}, {Xindex}")
        self.population[Yindex][Xindex] = 0 if self.population[Yindex][Xindex] == 1 else 1
        self.update_canvas()
    
    def draw(self):
        print('drawing')
        while self.verticalLayout_3.takeAt(0):
            item = self.verticalLayout_3.takeAt(0)
            if item:
                w = item.widget()
                if w:
                   w.deleteLater()
        # policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # policy.setHeightForWidth(True)
        # containingFrame_H.setSizePolicy(policy)
        for Yindex, line in enumerate(self.population):
            containingFrame_H = ContainingFrame()
            
            horizontalLayout = QHBoxLayout(containingFrame_H)
            horizontalLayout.setSpacing(0)
            horizontalLayout.setContentsMargins(0, 0, 0, 0)
            
            for Xindex, subject in enumerate(line):
                new_subject:QPushButton = QPushButton(containingFrame_H)
                if subject == 1:
                    new_subject.setStyleSheet(f"background: #ddd; width: {window_size/field_size}px; height: {window_size/field_size}px; border:none;")
                    # new_subject.setStyleSheet("background: #ddd; border:1px solid black;")
                else:
                    new_subject.setStyleSheet(f"background:black; width: {window_size/field_size}px; height: {window_size/field_size}px; border:none;")
                new_subject.clicked.connect(lambda x=Xindex, y=Yindex: self.change_state(x, y))
                horizontalLayout.addWidget(new_subject)
        
            self.verticalLayout_3.addWidget(containingFrame_H)
    ##################################################
            
    def startCalc(self):
        self.calculating = True
        print('start calculating')
        self.thread[1] = ThreadClass(parent=None, index = 1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.calc_next_gen)
        self.btn_startCalc.setEnabled(False)
    
    def stopCalc(self):
        self.calculating = False
        print('stop calculating')
        self.btn_startCalc.setEnabled(True)
        self.thread[1].stop()
        

class ThreadClass(QThread):
    any_signal = Signal()
    def __init__(self, parent = None, index = 0):
        super().__init__(parent)
        self.index = index
        self.is_running = True
        
    def run(self):
        print('Starting Thread...', self.index)
        while self.is_running:
            time.sleep(.01*field_size)
            self.any_signal.emit()
            
    def stop(self):
        self.is_running = False
        print('Stopping Thread...', self.index)
    
    

field_size = 50 #random.randint(10, 30)
liste = [[0 for x in range(field_size)] for y in range(field_size)]
print(len(liste), len(liste[0]))

# liste = [[1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# liste = [[1,0,0,0],[0,1,1,0],[1,1,0,0], [0,0,0,0]]



app = QApplication()
MainWindow = GameOfLife(liste)
MainWindow.setStyleSheet(open('./styleMain.css', encoding='utf-8').read())
window_size = MainWindow.width()
MainWindow.show()
MainWindow.draw()
app.exec()
