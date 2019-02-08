import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtCore
from ToDB import ToDB
from decimal import Decimal


class Shopsell(QWidget):
    def __init__(self):
        super(Shopsell, self).__init__()
        self.initUI()
        self.db = ToDB()

    # UI设计实现
    def initUI(self):
        self.setGeometry(60, 60, 1000, 600)
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
        self.tabel_sell.setRowCount(1)
        self.tabel_sell.setColumnCount(4)
        self.tabel_sell.setHorizontalHeaderLabels(["药品名称", "单价", "数量", "总计"])

        self.tabel_sell.setColumnWidth(4, 200)
        # 不可编辑
        self.tabel_sell.setEditTriggers(QAbstractItemView.DoubleClicked)
        # 隔行改变颜色
        self.tabel_sell.setAlternatingRowColors(True)

        self.tabel_sell.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        self.tabel_sell.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 布局
        layout = QVBoxLayout(self)
        v1 = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        v2 = QVBoxLayout()
        h5 = QHBoxLayout()
        f = QFormLayout()
        w_title = QWidget()
        w_21 = QWidget()
        w_22 = QWidget()
        w_31 = QWidget()
        w_321 = QWidget()
        w_321.setFixedSize(235, 330)
        w_322 = QWidget()
        w_low = QWidget()
        v1.addWidget(label_sell_title, 0, Qt.AlignCenter)
        h1.addWidget(self.code_radio)
        h1.addWidget(self.name_radio)
        h1.addWidget(self.line_code)
        # h1.addWidget(label_name)
        # h1.addWidget(self.line_name)
        h2.addWidget(btn_sell_lr)
        h3.addWidget(self.tabel_sell)
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
        w_low.setLayout(h5)
        splitter_sell1 = QSplitter(Qt.Horizontal)
        splitter_sell1.setSizes([800, 80])
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
        splitter_sell9 = QSplitter(Qt.Vertical)
        splitter_sell9.addWidget(splitter_sell4)
        splitter_sell9.addWidget(splitter_sell8)
        # splitter_sell9.addWidget(w_low)
        layout.addWidget(splitter_sell9)
        self.setLayout(layout)
        # 临时变量
        self.Row = 0

    # 查找并显示
    def event_lr(self):
        if self.code_radio.isChecked():
            if self.line_code.text() == '':
                replay = QMessageBox.warning(self, "!", "请输入条形码！", QMessageBox.Yes)
                return
            code = self.line_code.text()
            sql = "select 名称,售价 from 库存 where 条码='{0}'".format(code)
        else:
            if self.line_code.text() == '':
                replay = QMessageBox.warning(self, "!", "请输入药品名称！", QMessageBox.Yes)
                return
            name = self.line_code.text()
            sql = "select 名称,售价 from 库存 where 名称 like '{0}'".format(name)
        result = self.db.search(sql)
        if not result:
            replay = QMessageBox.warning(self, "!", "未找到！", QMessageBox.Yes)
            return
        try:
            if self.Row == 0:
                self.tabel_sell.currentCellChanged.connect(self.handleItemClick)

            name = QTableWidgetItem(result['name'])

            items = self.tabel_sell.findItems(result['name'], Qt.MatchExactly)

            if len(items) != 0:
                row = items[0].row()
                cur_count = int(self.tabel_sell.item(row, 2).text())
                cur_count += 1
                self.tabel_sell.setItem(row, 2, QTableWidgetItem(str(cur_count)))
                one_sum = cur_count * Decimal(self.tabel_sell.item(row, 1).text())
                self.tabel_sell.setItem(row, 3, QTableWidgetItem(str(one_sum)))
            else:
                self.tabel_sell.setRowCount(self.Row + 1)
                price = QTableWidgetItem(str(result['price']))
                count = QTableWidgetItem('1')
                sum_price = QTableWidgetItem(str(result['price'] * 1))

                self.tabel_sell.setItem(self.Row, 0, name)
                self.tabel_sell.setItem(self.Row, 1, price)
                self.tabel_sell.setItem(self.Row, 2, count)
                # self.tabel_sell.item(self.Row, 2).setFlags(Qt.ItemIsEnabled)
                # self.tabel_sell.item(self.Row, 2).setFlags(Qt.NoItemFlags)


                self.tabel_sell.setItem(self.Row, 3, sum_price)

                self.tabel_sell.item(self.Row, 0).setFlags(Qt.ItemIsEnabled)
                self.tabel_sell.item(self.Row, 1).setFlags(Qt.ItemIsEnabled)
                # self.tabel_sell.item(self.Row, 3).setFlags(Qt.ItemIsEnabled)

                self.Row += 1
            self.updateCost()

        except Exception as e:
            print(e)
    def updateCost(self):
        r_sum = 0
        rows = self.tabel_sell.rowCount()
        for rows_index in range(rows):
            # print items[item_index].text()
            num = self.tabel_sell.item(rows_index, 3)
            if num:
                r_sum += Decimal(num.text())
        # 计算总价
        self.line_sell1.setText(str(r_sum))
        self.line_sell2.setText(self.line_sell1.text())

        cur = Decimal(self.line_sell3.text())
        if cur != 0.0:
            self.line_sell4.setText(str(cur - r_sum))
    def jiesuan(self):
        if self.line_sell3.text()!='':
            try:
                self.line_sell4.setText(str((Decimal(self.line_sell3.text())-Decimal(self.line_sell2.text()))))
            except Exception as e:
                print("ddd",e)

    def jiesuan0(self):
        try:
            self.line_sell3.setText("")
        except Exception as e:
            print("www", e)

    # 确认录入存表
    def event_qr(self):
        # 确定是否添加有商品
        if self.line_sell1.text() == "0.0":
            replay = QMessageBox.warning(self, "!", "未添加商品！", QMessageBox.Yes)
        else:
            # 录入数据库的同时将收货信息存入txt文件中，模仿打印小票
            try:
                xsjl = open("销售记录.txt", "a+")
                xsjl.write("*******************************************************************\n")
                xsjl.write("商品名称\t\t\t\t单价\t\t\t\t数量\t\t\t\t总计\n")
                xsjl.write("\n")

                goods = []
                rows = self.tabel_sell.rowCount()
                for rows_index in range(rows):
                    name = self.tabel_sell.item(rows_index, 0).text()
                    price = self.tabel_sell.item(rows_index, 1).text()
                    count = self.tabel_sell.item(rows_index, 2).text()
                    sum_price = self.tabel_sell.item(rows_index, 3).text()
                    record = name + '\t\t\t\t' + price +'\t\t\t\t'+ count +'\t\t\t\t'+ sum_price + '\n'
                    goods.append(record)
                    sql='''
                    INSERT INTO 销售 (名称,数量)\
                       VALUES\
                       ('%s','%s')
                    ''' % (name,count)
                    self.db.runSql(sql)
                xsjl.write(''.join(goods))
                xsjl.write("___________________________________________________________________\n")
                xsjl.write("总计：%.1f\n" % float(self.line_sell1.text()))
                xsjl.write("实收：%.1f\n" % float(self.line_sell3.text()))
                xsjl.write("找零：%.1f\n" % float(self.line_sell4.text()))
                xsjl.write("\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                xsjl.write("····································································\n")
                xsjl.close()
                self.event_ql()

            except Exception as e:
                print(e)
            # 清空表格

    def event_ql(self):
        # 清空输入框，清除显示列表，清空暂存信息的列表
        self.line_sell1.setText("0.0")
        self.line_sell2.setText("0.0")
        self.line_sell3.setText("0.0")
        self.line_sell4.setText("0.0")
        self.Row = 0
        self.line_code.clear()
        self.tabel_sell.clear()

        # 添加背景图片

    def handleItemClick(self,event):
        print(self.tabel_sell.selectedItems())
        # currentQTableWidgetItem=self.tabel_sell.selectedItems().pop()
        for currentQTableWidgetItem in self.tabel_sell.:
            if currentQTableWidgetItem.column()==2:
                # print(currentQTableWidgetItem.row())
                # try:
                price = self.tabel_sell.item(currentQTableWidgetItem.row(),
                                             currentQTableWidgetItem.column() - 1).text()
                count = self.tabel_sell.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column()).text()

                sum_price = Decimal(price) * int(count)
                #
                self.tabel_sell.setItem(currentQTableWidgetItem.row(), currentQTableWidgetItem.column() + 1,
                                        QTableWidgetItem(str(sum_price)))

    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pDeleteAct = QAction('删除行', self.tabel_sell)
        pmenu.addAction(pDeleteAct)
        pDeleteAct.triggered.connect(self.deleterows)
        pmenu.popup(self.mapToGlobal(event.pos()))

    def deleterows(self):
        """
        删除行
        """
        rr = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if rr == QMessageBox.Yes:
            curow = self.tabel_sell.currentRow()
            selections = self.tabel_sell.selectionModel()
            selectedsList = selections.selectedRows()
            rows = []
            for r in selectedsList:
                rows.append(r.row())
            if len(rows) == 0:
                rows.append(curow)
                self.removeRows(rows, isdel_list = 1)
            else:
                self.removeRows(rows, isdel_list = 1)

            self.updateCost()

    def removeRows(self, rows, isdel_list = 0):
        if isdel_list != 0:
            rows.reverse()
            for i in rows:
                self.tabel_sell.removeRow(i)
        else:
            for i in range(rows-1, -1, -1):
                self.tabel_sell.removeRow(i)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopsell()
    sell.show()
    sys.exit(app.exec())

