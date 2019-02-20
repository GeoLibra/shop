from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QComboBox, QMessageBox, QMenu, QAction, QHeaderView, QAbstractItemView
import time
from decimal import Decimal
from string import Template
from shop_sale import ShopSale_UI
from ToDB import ToDB
class MSale(QMainWindow, ShopSale_UI):

    def __init__(self, parent=None):
        super(MSale, self).__init__(parent)
        self.setupUi(self)
        self.db = ToDB()

    # @pyqtSlot(int, int)
    # def on_tableWidget_cellDoubleClicked(self, row, column):
    #     """
    #     双击修改
    #     """
    #     print("双击修改")
    #
    # @pyqtSlot(QTableWidgetItem)
    # def on_tableWidget_itemActivated(self, item):
    #     """
    #     按住Enter键时
    #     """
    #     print("asda")

    @pyqtSlot(int, int, int, int)
    def on_tableWidget_itemChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        """
        当前单元格改变
        """
        print("当前单元格改变")



    # 查找并显示
    def event_lr(self):
        if self.code_radio.isChecked():
            if self.line_code.text() == '':
                replay = QMessageBox.warning(self, "!", "请输入条形码！", QMessageBox.Yes)
                return
            self.line_code.textChanged.connect(self.searchByCode)
            code = self.line_code.text()
            # ["条形码", "名称", "生产厂家", "批号", "有效期", "零售价", "数量", "总计"]
            sql = "select 条形码,名称,生产厂家,批号,有效期,MAX(零售价) as 零售价 from 库存 where 条形码='{0}'".format(code)
        else:
            try:
                self.line_code.textChanged.disconnect()
            except Exception as e:
                print(e)
            if self.line_code.text() == '':
                replay = QMessageBox.warning(self, "!", "请输入药品名称！", QMessageBox.Yes)
                return
            name = self.line_code.text()
            sql = "select 条形码,名称,生产厂家,批号,有效期,零售价 from 库存 where 名称 like '%{0}%'".format(name)
            # 情空表格

        result = self.db.search(sql)
        if not result:
            replay = QMessageBox.warning(self, "!", "未找到！", QMessageBox.Yes)
            return
        try:

            if self.Row==-1:
                self.Row=0
            for cur in result:

                if self.Row == 0:
                    self.tabel_sell.itemChanged.connect(self.handleItemClick)

                items = self.tabel_sell.findItems(cur[0], Qt.MatchExactly)
                # 当前记录是否存在
                if len(items) != 0:
                    row = items[0].row()
                    cur_count = int(self.tabel_sell.item(row, 6).text())
                    cur_count += 1
                    self.tabel_sell.setItem(row, 6, QTableWidgetItem(str(cur_count)))
                    one_sum = cur_count * Decimal(self.tabel_sell.item(row, 5).text())
                    self.tabel_sell.setItem(row, 7, QTableWidgetItem(str(one_sum)))

                else:
                    self.tabel_sell.setRowCount(self.Row + 1)
                    code = QTableWidgetItem(cur[0])
                    name = QTableWidgetItem(cur[1])
                    prducer = QTableWidgetItem(cur[2])
                    batch = QTableWidgetItem(cur[3])
                    valid = QTableWidgetItem(cur[4])
                    cost = QTableWidgetItem(str(cur[5]))
                    num = QTableWidgetItem('1')
                    sum_price = QTableWidgetItem(str(cur[5] * 1))

                    self.tabel_sell.setItem(self.Row, 0, code)
                    self.tabel_sell.setItem(self.Row, 1, name)
                    self.tabel_sell.setItem(self.Row, 2, prducer)
                    self.tabel_sell.setItem(self.Row, 3, batch)
                    self.tabel_sell.setItem(self.Row, 4, valid)
                    # 零售价
                    self.tabel_sell.setItem(self.Row, 5, cost)
                    # 数量
                    self.tabel_sell.setItem(self.Row, 6, num)
                    self.tabel_sell.setItem(self.Row, 7, sum_price)
                    self.tabel_sell.item(self.Row, 0).setFlags(Qt.ItemIsEnabled)
                    self.tabel_sell.item(self.Row, 1).setFlags(Qt.ItemIsEnabled)
                    self.tabel_sell.item(self.Row, 2).setFlags(Qt.ItemIsEnabled)
                    self.tabel_sell.item(self.Row, 3).setFlags(Qt.ItemIsEnabled)
                    self.tabel_sell.item(self.Row, 4).setFlags(Qt.ItemIsEnabled)
                    self.tabel_sell.item(self.Row, 5).setFlags(Qt.ItemIsEnabled)

                    self.Row += 1
            self.updateCost()

        except Exception as e:
            print(e)
    def updateCost(self):
        r_sum = 0
        rows = self.tabel_sell.rowCount()
        for rows_index in range(rows):
            # print items[item_index].text()
            num = self.tabel_sell.item(rows_index, 7)
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
            # self.Row=0
            # self.tabel_sell.clearContents()
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
                width = 35
                price_width = 15
                item_width = width - price_width
                header_format = '%-*s%*s%*s%*s'
                content_format = '%-*s%*s%*s%*s'

                xsjl = open("销售记录.txt", "a+")
                xsjl.write("="*(price_width*4+item_width)+'\n')
                xsjl.write(content_format%(item_width,"名称",price_width,"单价",price_width,"数量",price_width,"总计"))
                xsjl.write("\n")
                xsjl.write("-" * (price_width*4+item_width)+ '\n')
                goods = []
                rows = self.tabel_sell.rowCount()
                for rows_index in range(rows):
                    name = self.tabel_sell.item(rows_index, 0).text()
                    price = self.tabel_sell.item(rows_index, 5).text()
                    count = self.tabel_sell.item(rows_index, 6).text()
                    sum_price = self.tabel_sell.item(rows_index, 7).text()
                    record = content_format % (item_width, name, price_width, price, price_width, count, price_width, sum_price)

                    goods.append(record)
                    sql='''
                    INSERT INTO 销售 (条形码,名称,数量)\
                       VALUES\
                       ('%s','%s','%s')
                    ''' % (self.tabel_sell.item(rows_index, 4).text(),name,count,)
                    self.db.runSql(sql)

                xsjl.write('\n'.join(goods))
                xsjl.write('\n'+"-" * (price_width*4+item_width) + '\n')
                xsjl.write("总计：%.2f 元\n" % float(self.line_sell1.text()))
                xsjl.write("实收：%.2f 元\n" % float(self.line_sell3.text()))
                xsjl.write("找零：%.2f 元\n" % float(self.line_sell4.text()))
                xsjl.write("\n" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                xsjl.write("=" * (price_width*4+item_width) + '\n')
                xsjl.close()

                # 入库
                sql="insert into 收入(总计,实收,找零) values ('%s','%s','%s')" % (self.line_sell1.text(),self.line_sell3.text(),self.line_sell4.text())
                self.db.runSql(sql)

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

        self.tabel_sell.setRowCount(1)
        self.tabel_sell.setColumnCount(8)
        self.tabel_sell.setHorizontalHeaderLabels(["条形码", "名称", "生产厂家", "批号", "有效期", "零售价", "数量", "总计"])
        # 添加背景图片

    def handleItemClick(self):
        try:
            column=self.tabel_sell.currentColumn()
            # print(self.tabel_sell.selectedItems().pop().column())

            if column==6:
                row = self.tabel_sell.currentRow()
                cur=self.tabel_sell.item(row, 6).text()
                price=Decimal(self.tabel_sell.item(row, 5).text())
                result=QTableWidgetItem(str(Decimal(cur)*price))
                self.tabel_sell.itemChanged.disconnect()
                self.tabel_sell.setItem(row, 7, result)
                self.tabel_sell.itemChanged.connect(self.handleItemClick)
                self.updateCost()
        except Exception as e:
            print(e)

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
        rr = QMessageBox.warning(self, "注意", "是否删除该行！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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
            self.Row -=1

    def removeRows(self, rows, isdel_list = 0):
        if isdel_list != 0:
            rows.reverse()
            for i in rows:
                self.tabel_sell.removeRow(i)
        else:
            for i in range(rows-1, -1, -1):
                self.tabel_sell.removeRow(i)
    def searchByCode(self):
        code=self.line_code.text()
        if self.code_radio.isChecked():
            if len(code)==14:
                self.event_lr()
                self.line_code.clear()
            if len(code)>14:
                self.line_code.clear()

