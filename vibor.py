import sys
import random
import math

from PyQt5.QtCore import Qt
import PyQt5.QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QLabel
from project_b import Ui_MainWindow
from project_b2 import Ui_MainWindow2
import time
import sqlite3


def compare(r1, r2, reverse=False):
    return r1 > r2 if not reverse else r1 < r2


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.rev2 = False
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.random_spis)
        self.next.clicked.connect(self.next_)
        self.label.setStyleSheet("""
                            font: bold italic;
                            color: black;
                            font-size: 17px;
                            """)
        self.checkBox.stateChanged.connect(self.change)

    def change(self, state):
        self.rev2 = (state == Qt.Checked)

    def run(self):
        self.list = self.textEdit.toPlainText()
        self.list = list(map(int, self.list.split()))
        self.label.setText(str(self.list))

    def random_spis(self):
        self.list = [random.randint(0, 100) for i in range(10)]
        self.label.setText(str(self.list))

    def next_(self):
        self.second_form = SecondForm(self, self.list, self.rev2)
        self.second_form.show()


class SecondForm(QMainWindow, Ui_MainWindow2):
    def __init__(self, *args):
        super().__init__()
        self.con = sqlite3.connect("sortirovki.db")
        self.setupUi(self)
        self.rev = args[-1]
        self.list = args[-2]
        self.stupid.clicked.connect(self.stup_sort)
        self.bubble.clicked.connect(self.bubble_)
        self.ba_ma_shegi_ba.clicked.connect(self.ba_ma_shegi_ba_)
        self.gnom.clicked.connect(self.gnom_)
        self.chet_nechet.clicked.connect(self.even_odd_)
        self.comb.clicked.connect(self.comb_)
        self.insertion.clicked.connect(self.insertion_)
        self.pair_insertion.clicked.connect(self.pair_insertion_)
        self.selection.clicked.connect(self.selection_)
        self.shell.clicked.connect(self.shell_)
        self.quick.clicked.connect(self.quick_)
        self.label.setStyleSheet("""
                    font: bold italic;
                    color: black;
                    font-size: 17px;
                    """)
        self.label3.setStyleSheet("""
                                font: bold italic;
                                color: black;
                                font-size: 13px;
                                """)
        self.setUpdatesEnabled = True
        if len(self.list) <= 13:
            self.label2 = [(QLabel(self), self.list[i]) for i in range(len(self.list))]
            for i in range(len(self.list)):
                self.label2[i][0].resize(300, 100)
                self.label2[i][0].setStyleSheet("""
                                        font: bold italic;
                                        color: black;
                                        font-size: 13px;
                                        """)
                self.label2[i][0].setText(str(self.label2[i][1]))
                self.label2[i][0].move(30, 120 + i * 20)

    def highlight(self, args, color, timer=0.6):
        for index in args:
            self.label2[index][0].setStyleSheet(f"""
                                    font: bold italic;
                                    color: {color};
                                    font-size: 13px;
                                    """)
        self.repaint()
        time.sleep(timer)

    def stup_sort(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 1""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText(self.list_info)
        reverse = self.rev
        new_list = self.list[:]
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        i = 1
        while i < len(self.list):
            '''проходим по списку'''
            self.highlight([i - 1, i], "green")
            if compare(new_list[i - 1], new_list[i]):
                self.highlight([i - 1, i], "red")
                new_list[i - 1], new_list[i] = new_list[i], new_list[i - 1]
                self.label2[i - 1][0].setText(str(new_list[i - 1]))
                self.label2[i][0].setText(str(new_list[i]))
                self.repaint()
                time.sleep(0.6)
                self.highlight([i - 1, i], "black")
                i = 1
                '''когда доходим до неотсортированной пары, сортируем её и возвращемся к НУЛЕВОМУ
                ЭЛЕМЕНТУ'''
            else:
                self.highlight([i - 1, i], "black")
                i += 1

    def bubble_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 2""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        for i in range(len(new_list) - 1):
            for j in range(i + 1, len(new_list)):
                self.highlight([i, j], "green")
                if compare(new_list[i], new_list[j], reverse):
                    new_list[i], new_list[j] = new_list[j], new_list[i]
                    self.highlight([i, j], "red")
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[j][0].setText(str(new_list[j]))
                    time.sleep(0.6)
                self.highlight([i, j], "black")

    def ba_ma_shegi_ba_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 3""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        l, r = 0, len(new_list) - 1
        while l < r:
            for i in range(l, r):
                self.highlight([i, i + 1], "green")
                if compare(new_list[i], new_list[i + 1], reverse):
                    self.highlight([i, i + 1], "red")
                    new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[i + 1][0].setText(str(new_list[i + 1]))
                    time.sleep(0.6)
                self.highlight([i, i + 1], "black")
            r -= 1
            for i in range(r, l, -1):
                self.highlight([i, i - 1], "green")
                if compare(new_list[i - 1], new_list[i], reverse):
                    self.highlight([i, i - 1], "red")
                    new_list[i], new_list[i - 1] = new_list[i - 1], new_list[i]
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[i - 1][0].setText(str(new_list[i - 1]))
                    time.sleep(0.6)
                self.highlight([i, i - 1], "black")
            l += 1

    def gnom_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 4""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        i = 0
        while i < len(new_list) - 1:
            '''проходим по списку'''
            self.highlight([i, i + 1], "green")
            if compare(new_list[i], new_list[i + 1], reverse):
                '''если натыкаемся на неотсортированную пару, то сортируем её и идём обратно
                пока не достигнем отсортированной пары'''
                self.highlight([i, i + 1], "red")
                new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                self.label2[i][0].setText(str(new_list[i]))
                self.label2[i + 1][0].setText(str(new_list[i + 1]))
                time.sleep(0.6)
                self.highlight([i, i + 1], "black")
                i -= 2 if i != 0 else 1
            else:
                self.highlight([i, i + 1], "black")
            i += 1

    def even_odd_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 5""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        _sorted = sorted(new_list)
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        r_temp = 1 #счётчик перестановок
        while r_temp != 0:
            '''
            сортируем каждую пару, если понадобится.
            прекращаем, когда количество сортировок за итерацию будет равно нулю
            '''
            r_temp = 0
            for i in range(0, len(new_list) - 1, 2):
                self.highlight([i, i + 1], "green")
                if compare(new_list[i], new_list[i + 1], reverse):
                    self.highlight([i, i + 1], "red")
                    new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[i + 1][0].setText(str(new_list[i + 1]))
                    self.repaint()
                    time.sleep(0.6)
                    r_temp += 1
                self.highlight([i, i + 1], "black")
            for i in range(1, len(new_list) - 1, 2):
                self.highlight([i, i + 1], "green")
                if compare(new_list[i], new_list[i + 1], reverse):
                    self.highlight([i, i + 1], "red")
                    new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[i + 1][0].setText(str(new_list[i + 1]))
                    self.repaint()
                    time.sleep(0.6)
                    r_temp += 1
                self.highlight([i, i + 1], "black")

    def comb_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 6""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        reverse = self.rev
        r = len(new_list) - 1
        j = r
        '''выбираем некий шаг'''
        i = 0
        while i < i + j:
            '''идём по списку и сравниваем элементы, которые
            различаются на выбранный нами шаг'''
            i = 0
            while i + j < len(new_list):
                self.highlight([i, i + j], "green")
                if compare(new_list[i], new_list[i + j], reverse):
                    self.highlight([i, i + j], "red")
                    new_list[i], new_list[i + j] = new_list[i + j], new_list[i]
                    self.label2[i][0].setText(str(new_list[i]))
                    self.label2[i + j][0].setText(str(new_list[i + j]))
                    self.repaint()
                    time.sleep(0.6)
                self.highlight([i, i + j], "black")
                i += 1
            r = j
            '''
            считаем новый шаг
            оптимальный коеффициент = 1 / 1.247
            '''
            j = math.ceil(r / 1.247) if math.ceil(r / 1.247) != r else int(r / 1.247)

    def ins_sort(self, arr, reverse, it=0, c=1):
        for i in range(len(arr)):
            temp = arr[i]
            '''
            берём элемент, идущий сразу после отсортированной области,
            и ищем для него подходящее место в отсортированной области
            '''
            self.label2[i * c + it][0].setText(str(temp) + '   ' + '<--')
            self.highlight([i * c + it], "blue")
            j = i - 1
            while j >= 0 and compare(arr[j], temp, reverse):
                self.highlight([j * c + it, j * c + it + c], "red")
                arr[j + 1], arr[j] = arr[j], arr[j + 1]
                self.label2[j * c + it][0].setText(str(arr[j]))
                self.label2[c + j * c + it][0].setText(str(arr[1 + j]) + '   ' + '<--'
                                                       if j == i - 1 else str(arr[j + 1]))
                self.repaint()
                time.sleep(0.6)
                self.highlight([j * c + it, j * c + it + c], "black")
                j -= 1
            self.label2[i * c + it][0].setStyleSheet("""
                                        font: bold italic;
                                        color: black;
                                        font-size: 13px;
                                                """)
            self.label2[i * c + it][0].setText(str(arr[i]))
            self.repaint()
            time.sleep(0.3)
        return arr

    def insertion_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 7""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        new_list = self.ins_sort(new_list, reverse)

    def pair_insertion_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 8""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        self.highlight([0, 1], "red")
        if compare(new_list[0], new_list[1], reverse):
            new_list[0], new_list[1] = new_list[1], new_list[0]
            self.label2[0][0].setText(str(new_list[0]))
            self.label2[1][0].setText(str(new_list[1]))
            self.repaint()
            time.sleep(0.6)
        self.label2[1][0].setText(str(new_list[1]) + '   <--')
        self.highlight([0, 1], "black")
        for i in range(2, len(new_list), 2):
            temp = [new_list[i]]
            self.highlight([i], "green", 0 if i + 1 < len(new_list) else 0.6)
            if i + 1 < len(new_list):
                temp.append(new_list[i + 1])
                self.highlight([i + 1], "green", 0.6)
                if not reverse:
                    temp.sort(reverse=True)
                else:
                    temp.sort()
            if i + 1 < len(new_list) and compare(new_list[i + 1], new_list[i], reverse):
                new_list[i], new_list[i + 1] = new_list[i + 1], new_list[i]
                self.highlight([i, i + 1], "red")
                self.label2[i][0].setText(str(new_list[i]))
                self.label2[i + 1][0].setText(str(new_list[i + 1]))
                self.repaint()
                time.sleep(0.6)
            j = i - 1
            while j >= 0 and compare(new_list[j], temp[0], reverse):
                self.highlight([j, j + 1, j + 2], "red")
                new_list[j + 1], new_list[j] = new_list[j], new_list[j + 1]
                self.label2[j][0].setText(str(new_list[j]))
                self.label2[j + 1][0].setText(str(new_list[j + 1]) + '   <--' if j == i - 1
                                              else str(new_list[j + 1]))
                self.repaint()
                time.sleep(0.6)
                new_list[j + 1], new_list[j + 2] = new_list[j + 2], new_list[j + 1]
                self.label2[j + 1][0].setText(str(new_list[j + 1]))
                self.label2[j + 2][0].setText(str(new_list[j + 2]) + '   <--' if j == i - 1
                                              else str(new_list[j + 2]))
                self.repaint()
                time.sleep(0.6)
                self.highlight([j + 2], "black", 0)
                j -= 1
            self.highlight([j + 2], "black", 0)
            if i + 1 < len(new_list):
                j += 1
                del temp[0]
            if temp:
                while j >= 0 and compare(new_list[j], temp[0], reverse):
                    self.highlight([j, j + 1], "red")
                    new_list[j + 1], new_list[j] = new_list[j], new_list[j + 1]
                    self.label2[j + 1][0].setText(str(new_list[j + 1]) + '   <--' if '<' in
                                                                                     self.label2[j][0].text() else str(
                        new_list[j + 1]))
                    self.label2[j][0].setText(str(new_list[j]))
                    self.repaint()
                    time.sleep(0.6)
                    self.highlight([j + 1], "black", 0)
                    j -= 1
            self.highlight([j + 1], "black", 0)
            if '<' not in self.label2[i + 1][0].text() and i + 1 < len(new_list):
                self.label2[i - 1][0].setText(str(new_list[i - 1]))
                self.label2[i][0].setText(str(new_list[i]))
                self.label2[i + 1][0].setText(str(new_list[i + 1]) + '   <--')
                self.repaint()
                time.sleep(0.2)
            if '<' not in self.label2[i][0].text() and i + 1 == len(new_list):
                self.label2[i - 1][0].setText(str(new_list[i - 1]))
                self.label2[i][0].setText(str(new_list[i]) + '   <--')
                self.repaint()
                time.sleep(0.2)

    def selection_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 9""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        i = len(new_list)
        while i > 1:
            '''
            ищем максимальный элемент в неотсортированной области и меняем его местами с 0-м 
            элементом неотсортированной области
            '''
            m = 0
            '''может быть как и max, так и min'''
            self.label2[i - 1][0].setText(str(new_list[i - 1]) + '   <--')
            self.highlight([i - 1], "blue")
            for j in range(i):
                self.highlight([j], "green")
                if compare(new_list[j], new_list[m], reverse):
                    self.label2[m][0].setText(str(new_list[m]))
                    self.highlight([m], "black")
                    m = j
                    self.label2[m][0].setText(str(new_list[m]) + '   <--')
                    self.highlight([m], "purple")
                else:
                    self.highlight([j], "black")
            self.highlight([i - 1, m], "red")
            new_list[i - 1], new_list[m] = new_list[m], new_list[i - 1]
            self.label2[m][0].setText(str(new_list[m]))
            self.highlight([m], "black")
            self.label2[i - 1][0].setText(str(new_list[i - 1]))
            self.highlight([i - 1], "blue")
            i -= 1
        '''уменьшаем размер неотсортированной области на 1'''

    def shell_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 10""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        step = len(new_list) // 2
        while step > 0:
            for i1 in range(step):
                arr_temp = new_list[i1::step]
                '''
                разбиваем изначальный список на списки, состоящие из элементов,
                отстоящих друг от друга на step
                '''
                self.highlight([ih for ih in range(i1, len(new_list), step)], "red", 1)
                self.highlight([ih for ih in range(i1, len(new_list), step)], "black", 0)
                arr_temp = self.ins_sort(arr_temp, reverse, i1, step)
                for j1 in range(i1, len(new_list), step):
                    new_list[j1] = arr_temp[j1 // step]
                '''
                сортируем получившиеся списки сортировкой вставками
                '''
            step //= 2

    def display_qsort(self, arr, beg_index):
        reverse = self.rev
        bef, aft = [], []
        wall = None if len(arr) == 0 else arr[-1]
        wall_index = 0
        end_index = len(arr) - 1
        for i in range(len(arr)):
            self.highlight([i + beg_index], "black", 0)
        self.highlight([len(arr) + beg_index - 1], "blue")
        if len(arr) > 1:
            for i in range(len(arr) - 2, -1, -1):
                if compare(wall, arr[i], reverse):
                    bef.insert(0, arr[i])
                    self.highlight([i + beg_index], "green")
                    wall_index += 1
                else:
                    aft.insert(0, arr[i])
                    self.highlight([i + beg_index], "red")
                    j = end_index - 2
                    for j in range(i, end_index - 1):
                        self.label2[j + beg_index][0].setText(str(arr[j + 1]))
                        self.label2[j + beg_index + 1][0].setText(str(arr[j]))
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        self.highlight([j + beg_index], "black", 0)
                        self.highlight([j + 1 + beg_index], "red")
                    self.label2[j + beg_index + 1][0].setText(str(arr[j + 2]))
                    self.label2[j + beg_index + 2][0].setText(str(arr[j + 1]))
                    arr[j + 2], arr[j + 1] = arr[j + 1], arr[j + 2]
                    self.highlight([j + 1 + beg_index], "blue", 0)
                    self.highlight([j + 2 + beg_index], "red")
                    end_index -= 1
        if len(bef) > 1:
            bef = self.display_qsort(bef, beg_index)
        if len(aft) > 1:
            aft = self.display_qsort(aft, beg_index + len(bef) + 1)
        if wall is not None:
            bef.append(wall)
        bef.extend(aft)
        return bef

    def quick_(self):
        self.list_info = self.con.execute(f"""SELECT alg from sort WHERE id = 11""").fetchall()
        self.list_info = self.list_info[0][0]
        self.label4.setText('\n'.join(self.list_info.split(' \\n ')))
        new_list = self.list[:]
        reverse = self.rev
        _sorted = sorted(new_list, reverse=reverse)
        self.label.setText(str(_sorted))
        new_list = self.display_qsort(new_list, 0)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
