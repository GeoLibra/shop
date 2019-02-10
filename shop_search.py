import sys
import pyodbc
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class MSearch(QWidget):
    def __init__(self):
        super(MSearch, self).__init__()
        self.initUI()
    #UI窗口设计
    def initUI(self):
        self.resize(1366, 768)
        #self.setGeometry(50, 50, 800, 600)
        label_select_title = QLabel()
        label_select_title.setText("信息查询")
        label_select_title.setFont(QFont("华文行楷", 25))
        self.tabel_main = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabel_main.addTab(self.tab1, "Tab 1")
        self.tabel_main.addTab(self.tab2, "Tab 2")
        self.tabel_main.addTab(self.tab3, "Tab 3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
    #布局设计
        layout = QVBoxLayout(self)
        v = QVBoxLayout()
        s_title = QWidget()
        s_title.setFixedSize(800, 80)
        s_title.setLayout(v)
        v.addWidget(label_select_title,0,  Qt.AlignCenter)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(s_title)
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.tabel_main)
        layout.addWidget(splitter2)
        #tab1的UI
    def tab1UI(self):
        #窗口1的标题
        self.tabel_main.setTabText(0, "库存查询")
        #创建一个下拉列表框，并设置信号槽绑定事件
        self.tab1.cb = QComboBox()
        self.tab1.cb.addItems(["名称", "条形码"])
        self.tab1.cb.activated.connect(self.event_cb1)
        self.tab1.lineEdit = QLineEdit()
        #定义查询按钮，绑定事件
        self.tab1.btn_select = QPushButton("查询")
        self.tab1.btn_select.clicked.connect(self.event_select1)
        layout_tab1 = QHBoxLayout()
        tab1_11 = QWidget()
        tab1_12 = QWidget()
        self.tab1_2 = QTableWidget()
        self.tab1_2.setRowCount(25)
        self.tab1_2.setColumnCount(4)
        self.tab1_2.setHorizontalHeaderLabels(["条形码", "名称","零售价", "库存量"])

        self.tab1_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab1.cb)
        h1.addWidget(self.tab1.lineEdit)
        h2.addWidget(self.tab1.btn_select)
        tab1_11.setLayout(h1)
        tab1_12.setLayout(h2)
        splitter_select_Tab1_1 = QSplitter(Qt.Horizontal)
        splitter_select_Tab1_1.addWidget(tab1_12)
        splitter_select_Tab1_1.setSizes([150, 80])
        splitter_select_Tab1_2 = QSplitter(Qt.Horizontal)
        splitter_select_Tab1_2.addWidget(tab1_11)
        splitter_select_Tab1_2.addWidget(splitter_select_Tab1_1)
        splitter_select_Tab1_3 = QSplitter(Qt.Vertical)
        splitter_select_Tab1_3.addWidget(splitter_select_Tab1_2)
        splitter_select_Tab1_3.addWidget(self.tab1_2)
        layout_tab1.addWidget(splitter_select_Tab1_3)
        self.tab1.setLayout(layout_tab1)
        #tab2的UI
    def tab2UI(self):
        self.tabel_main.setTabText(1, "进货查询")
        self.tab2.cb = QComboBox()
        self.tab2.cb.addItems(["名称", "条形码"])
        self.tab2.cb.activated.connect(self.event_cb2)
        self.tab2.label = QLabel("采购时间")
        self.tab2.labelnull = QLabel("——")
        self.tab2.lineEdit = QLineEdit()
        self.tab2.dateEdit1 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab2)
        self.tab2.dateEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab2)
        self.tab2.dateEdit1.setDisplayFormat("yyyy-MM-dd")
        self.tab2.dateEdit2.setDisplayFormat("yyyy-MM-dd")
        self.tab2.dateEdit1.setCalendarPopup(True)
        self.tab2.dateEdit2.setCalendarPopup(True)
        self.tab2.btn_select = QPushButton("查询")
        self.tab2.btn_select.clicked.connect(self.event_select2)
        layout_tab2 = QHBoxLayout()
        tab2_11 = QWidget()
        tab2_12 = QWidget()
        self.tab2_2 = QTableWidget()
        self.tab2_2.setRowCount(500)
        self.tab2_2.setColumnCount(4)
        self.tab2_2.setHorizontalHeaderLabels(["条形码", "名称","零售价", "库存量"])

        self.tab2_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab2.cb)
        h1.addWidget(self.tab2.lineEdit)
        h1.addWidget(self.tab2.label)
        h1.addWidget(self.tab2.dateEdit1)
        h1.addWidget(self.tab2.labelnull)
        h1.addWidget(self.tab2.dateEdit2)
        h2.addWidget(self.tab2.btn_select)
        tab2_11.setLayout(h1)
        tab2_12.setLayout(h2)
        splitter_select_tab2_1 = QSplitter(Qt.Horizontal)
        splitter_select_tab2_1.addWidget(tab2_12)
        splitter_select_tab2_1.setSizes([150, 80])
        splitter_select_tab2_2 = QSplitter(Qt.Horizontal)
        splitter_select_tab2_2.addWidget(tab2_11)
        splitter_select_tab2_2.addWidget(splitter_select_tab2_1)
        splitter_select_tab2_3 = QSplitter(Qt.Vertical)
        splitter_select_tab2_3.addWidget(splitter_select_tab2_2)
        splitter_select_tab2_3.addWidget(self.tab2_2)
        layout_tab2.addWidget(splitter_select_tab2_3)
        self.tab2.setLayout(layout_tab2)
        #tab3的UI
    def tab3UI(self):
        self.tabel_main.setTabText(2, "售货查询")
        self.tab3.cb = QComboBox()
        self.tab3.cb.addItems(["商品名称", "条形码"])
        self.tab3.cb.activated.connect(self.event_cb3)
        self.tab3.label = QLabel("销售时间")
        self.tab3.labelnull = QLabel("——")
        self.tab3.lineEdit = QLineEdit()
        self.tab3.dateEdit1 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab3)
        self.tab3.dateEdit2 = QDateTimeEdit(QDateTime.currentDateTime(), self.tab3)
        self.tab3.dateEdit1.setDisplayFormat("yyyy-MM-dd")
        self.tab3.dateEdit2.setDisplayFormat("yyyy-MM-dd")
        self.tab3.dateEdit1.setCalendarPopup(True)
        self.tab3.dateEdit2.setCalendarPopup(True)
        self.tab3.btn_select = QPushButton("查询")
        self.tab3.btn_select.clicked.connect(self.event_select3)
        layout_tab3 = QHBoxLayout()
        tab3_11 = QWidget()
        tab3_12 = QWidget()
        self.tab3_2 = QTableWidget()
        self.tab3_2.setRowCount(500)
        self.tab3_2.setColumnCount(5)
        self.tab3_2.setHorizontalHeaderLabels(["条形码", "名称", "零售价", "销售数量", "售出时间"])

        self.tab3_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h1.addWidget(self.tab3.cb)
        h1.addWidget(self.tab3.lineEdit)
        h1.addWidget(self.tab3.label)
        h1.addWidget(self.tab3.dateEdit1)
        h1.addWidget(self.tab3.labelnull)
        h1.addWidget(self.tab3.dateEdit2)
        h2.addWidget(self.tab3.btn_select)
        tab3_11.setLayout(h1)
        tab3_12.setLayout(h2)
        splitter_select_tab3_1 = QSplitter(Qt.Horizontal)
        splitter_select_tab3_1.addWidget(tab3_12)
        splitter_select_tab3_1.setSizes([150, 80])
        splitter_select_tab3_2 = QSplitter(Qt.Horizontal)
        splitter_select_tab3_2.addWidget(tab3_11)
        splitter_select_tab3_2.addWidget(splitter_select_tab3_1)
        splitter_select_tab3_3 = QSplitter(Qt.Vertical)
        splitter_select_tab3_3.addWidget(splitter_select_tab3_2)
        splitter_select_tab3_3.addWidget(self.tab3_2)
        layout_tab3.addWidget(splitter_select_tab3_3)
        self.tab3.setLayout(layout_tab3)
        
        #下拉选框出现变化时输入框清零
    def event_cb1(self):
        self.tab1.lineEdit.setText("")
    def event_cb2(self):
        self.tab2.lineEdit.setText("")
    def event_cb3(self):
        self.tab3.lineEdit.setText("")
        
    #库存查询
    def event_select1(self):
        #每次查询前都应该先清除表中内容

        #获取输入框中的内容
        text = self.tab1.lineEdit.text()
        if self.tab1.cb.currentText() == "条形码":
            if text == "":
                pass
            else:
                pass
        else:
            if text == "":
                pass
            else:
                pass
        #进货查询
    def event_select2(self):
        #清空显示table

        #获取输入框内容
        text = self.tab2.lineEdit.text()
        #获取两个时间，组成时间段
        time1 = self.tab2.dateEdit1.dateTime().toString("yyyy-MM-dd")
        time2 = self.tab2.dateEdit2.dateTime().toString("yyyy-MM-dd")
        if self.tab2.cb.currentText() == "条形码":
            if text == "":
                pass
            else:
                pass
        else:
            if text == "":
                #如果输入框中并未填写任何内容，应该将数据库表中时间段内所有数据全部显示出来
                pass
            else:
                pass
    #售货查询
    def event_select3(self):
        #清空

        #获取输入框内容及时间
        text = self.tab3.lineEdit.text()
        time1 = self.tab3.dateEdit1.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        time2 = self.tab3.dateEdit2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.tab3.cb.currentText() == "条形码":
            if text == "":
                pass
            else:
                pass
        else:
            if text == "":
                pass
            else:
                pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopselect()
    sell.show()
    sys.exit(app.exec())
        
