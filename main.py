import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from shop_stock import *
from msale import *
class Shopmain(QWidget):
    def __init__(self, parent=None):
        super(Shopmain, self).__init__(parent)
        self.initUI()
        #UI窗口设计
    def initUI(self):
        self.resize(1366,768)
        #self.setGeometry(50, 50, 800, 600)
        #标题
        self.setWindowTitle("药店信息管理系统")
        #三个子系统选择按钮，绑定信号事件

        btn_main_sale= QPushButton("销售")
        btn_main_sale.setFixedSize(200, 45)
        btn_main_sale.setStyleSheet("background-color :rgb(253,216,174)")
        btn_main_sale.clicked.connect(self.sale)

        btn_main_stock = QPushButton("录入")
        btn_main_stock.setStyleSheet("background-color :rgb(253,216,174)")
        btn_main_stock.setFixedSize(200, 45)
        btn_main_stock.clicked.connect(self.stock)

        #title
        label_main_title = QLabel("药店信息管理系统")
        label_main_title.setFont(QFont("华文行楷", 25))
        label_main_title.setStyleSheet('''color: rgb(200,10,100);''')
        label_main_explain = QLabel(self)
        label_main_explain.setText("<a href = '#'>关于本系统</a>")
        label_main_explain.linkActivated.connect(self.explain)
        labe_null1 = QLabel()
        labe_null2 = QLabel()
        #布局设计
        layout = QVBoxLayout(self)
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        g1 = QGridLayout()
        g2 = QGridLayout()
        g3 = QGridLayout()
        h1.addWidget(label_main_title, 0, Qt.AlignCenter)
        g1.addWidget(labe_null1)
        g2.addWidget(btn_main_sale, 1, 0)
        g2.addWidget(btn_main_stock, 2, 0)
        g3.addWidget(labe_null2)
        h2.addLayout(g1)
        h2.addLayout(g2)
        h2.addLayout(g3)
        h3.addWidget(label_main_explain, 0, Qt.AlignLeft|Qt.AlignBottom)
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)
    def explain(self):
        pass
    #Stock实例化
    def stock(self):
        self.stock = Shopstock()
        self.stock.show()
    #Sell实例化
    def sale(self):
        self.sell = MSale()
        self.sell.show()
    #设置背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("main.jpg")
        painter.drawPixmap(self.rect(), pixmap)
if __name__ == "__main__":
    app =QApplication(sys.argv)
    shop = Shopmain()
    shop.show()
    sys.exit(app.exec())
