from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class ShopSale_UI(object):
    # def __init__(self):
    #     super(ShopSale_UI, self).__init__()
    #     self.setupUi()
    def setupUi(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000,600)

        self.widget = QWidget(MainWindow)
        self.widget.setGeometry(10, 10, 1000, 600)
        self.widget.setObjectName("widget")

        # self.setWindowFlags(Qt.FramelessWindowHint)
        label_sell_title = QLabel("销售")
        label_sell_title.setFont(QFont("华文行楷", 20))
        # label_code = QLabel("条码:")
        # label_name = QLabel("名称:")
        self.code_radio = QRadioButton("条码")
        self.name_radio = QRadioButton("名称")

        self.code_radio.setChecked(True)


        label_sum = QLabel("总计")
        label_sale = QLabel("应收")
        label_cost = QLabel("实收")
        label_change = QLabel("找零")
        # 定义条形码输入框，并设置只允许输入整数
        self.line_code = QLineEdit()
        # 设置输入框的大小
        self.line_code.setFixedSize(350, 30)
        self.line_code.textChanged.connect(self.searchByCode)
        self.line_code.setFocus()
        # self.line_txm.setValidator(QIntValidator())
        # self.line_name = QLineEdit()
        # self.line_name.setFixedSize(150, 30)
        # self.line_xssl.setValidator(QIntValidator())

        # 定义多个list用来暂存预售货信息
        self.name = []  # 名称
        self.price = []  # 单价
        self.count = []  # 数量
        self.sum = []  # 总计

        # 结算窗口
        self.line_sell1 = QLineEdit()
        self.line_sell2 = QLineEdit()
        self.line_sell3 = QLineEdit()
        self.line_sell4 = QLineEdit()
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        # 实收框发生改变时
        self.line_sell3.textChanged.connect(self.jiesuan)
        self.line_sell3.selectionChanged.connect(self.jiesuan0)
        self.line_sell4.setText("0.0")
        self.line_sell1.setReadOnly(True)
        self.line_sell2.setReadOnly(True)
        self.line_sell4.setReadOnly(True)

        self.line_sell1.setFixedSize(150, 30)
        self.line_sell2.setFixedSize(150, 30)
        self.line_sell3.setFixedSize(150, 30)
        self.line_sell4.setFixedSize(150, 30)
        # 录入按钮，绑定事件
        btn_sell_lr = QPushButton("查找")
        btn_sell_lr.clicked.connect(self.event_lr)
        # 确认按钮，绑定事件
        btn_sell_qr = QPushButton("确认")
        btn_sell_qr.clicked.connect(self.event_qr)
        # 清零按钮，绑定事件
        btn_sell_ql = QPushButton("清零")
        btn_sell_ql.clicked.connect(self.event_ql)
        btn_sell_qr.setFixedSize(150, 30)
        btn_sell_ql.setFixedSize(150, 30)

        self.tabel_sell = QTableWidget()
        self.tabel_sell.setObjectName("tableWidget")
        self.tabel_sell.setRowCount(1)
        self.tabel_sell.setColumnCount(4)
        self.tabel_sell.setHorizontalHeaderLabels(["名称", "零售价", "数量", "总计"])

        self.tabel_sell.setColumnWidth(4, 200)
        # 不可编辑
        self.tabel_sell.setEditTriggers(QAbstractItemView.DoubleClicked)
        # 隔行改变颜色
        self.tabel_sell.setAlternatingRowColors(True)

        self.tabel_sell.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tabel_sell.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 布局
        layout = QVBoxLayout(self.widget)
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        # 控制台
        v2 = QVBoxLayout()
        h4 = QHBoxLayout()

        f = QFormLayout()
        w_title = QWidget()
        w_21 = QWidget()
        w_22 = QWidget()
        w_31 = QWidget()
        w_321 = QWidget()
        w_321.setFixedSize(235, 330)
        w_322 = QWidget()

        w_console = QWidget()


        v1.addWidget(label_sell_title, 0, Qt.AlignCenter)
        h1.addWidget(self.code_radio, 0, Qt.AlignLeft)
        h1.addWidget(self.name_radio, 0, Qt.AlignLeft)
        h1.addWidget(self.line_code, 0, Qt.AlignLeft)

        # h1.addWidget(label_name)
        # h1.addWidget(self.line_name)
        h2.addWidget(btn_sell_lr)

        h3.addWidget(self.tabel_sell)
        self.textEdit =QTextEdit()
        self.textEdit.setGeometry(QRect(0, 0, 200, 200))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        # self.textEdit.setText("sadddddddddddddddddddddddddddddd")
        h4.addWidget(self.textEdit, 0, Qt.AlignBottom)

        f.addRow(label_sum, self.line_sell1)
        f.addRow(label_sale, self.line_sell2)
        f.addRow(label_cost, self.line_sell3)
        f.addRow(label_change, self.line_sell4)
        v2.addWidget(btn_sell_qr, Qt.AlignCenter | Qt.AlignVCenter)
        v2.addWidget(btn_sell_ql, Qt.AlignCenter | Qt.AlignVCenter)
        w_title.setLayout(v1)
        w_21.setLayout(h1)
        w_22.setLayout(h2)
        w_31.setLayout(h3)
        w_321.setLayout(f)
        w_322.setLayout(v2)

        w_console.setLayout(h4)

        splitter_sell1 = QSplitter(Qt.Horizontal)
        splitter_sell1.setSizes([800, 60])
        splitter_sell1.addWidget(w_title)

        splitter_sell2 = QSplitter(Qt.Horizontal)
        splitter_sell2.setSizes([150, 60])
        splitter_sell2.addWidget(w_22)
        splitter_sell3 = QSplitter(Qt.Horizontal)
        # splitter3.setSizes([800, 60])
        splitter_sell3.addWidget(w_21)
        splitter_sell3.addWidget(splitter_sell2)
        splitter_sell4 = QSplitter(Qt.Vertical)
        splitter_sell4.setSizes([800, 140])
        splitter_sell4.addWidget(splitter_sell1)
        splitter_sell4.addWidget(splitter_sell3)
        splitter_sell5 = QSplitter(Qt.Horizontal)
        splitter_sell5.setSizes([150, 60])
        splitter_sell5.addWidget(w_322)
        splitter_sell6 = QSplitter(Qt.Vertical)
        splitter_sell6.addWidget(w_321)
        splitter_sell6.addWidget(splitter_sell5)
        splitter_sell7 = QSplitter(Qt.Horizontal)
        splitter_sell7.setSizes([700, 390])
        splitter_sell7.addWidget(self.tabel_sell)
        splitter_sell8 = QSplitter(Qt.Horizontal)
        splitter_sell8.addWidget(splitter_sell7)
        splitter_sell8.addWidget(splitter_sell6)


        # splitter_sell10 = QSplitter(Qt.Horizontal)
        # splitter_sell10.addWidget(w_console)

        splitter_sell9 = QSplitter(Qt.Vertical)
        splitter_sell9.addWidget(splitter_sell4)
        splitter_sell9.addWidget(splitter_sell8)
        # splitter_sell9.addWidget(splitter_sell10)
        # splitter_sell9.addWidget(w_low)

        layout.addWidget(splitter_sell9)
        self.setLayout(layout)
        # 临时变量
        self.Row = 0
        QMetaObject.connectSlotsByName(MainWindow)
