from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QComboBox, QMessageBox, QMenu, QAction, QHeaderView, QAbstractItemView
import time
from decimal import Decimal
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
                self.tabel_sell.itemChanged.connect(self.handleItemClick)

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
                self.tabel_sell.setItem(self.Row, 3, sum_price)
                self.tabel_sell.setItem(self.Row, 2, count)
                # qsb=QSpinBox()
                #
                # qsb.setMinimum(0)
                # qsb.setValue(1)

                # h = QHBoxLayout()
                # h.setAlignment(Qt.AlignCenter)
                # h.addWidget(qsb)
                # w = QWidget()
                # w.setLayout(h)
                # self.tabel_sell.item(self.Row, 2).setFlags(Qt.ItemIsEnabled)
                # self.tabel_sell.setCellWidget(self.Row, 2, qsb)

                self.tabel_sell.item(self.Row, 0).setFlags(Qt.ItemIsEnabled)
                self.tabel_sell.item(self.Row, 1).setFlags(Qt.ItemIsEnabled)
                self.tabel_sell.item(self.Row, 3).setFlags(Qt.ItemIsEnabled)

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
            self.Row=0
            self.tabel_sell.clearContents()
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
                xsjl.write("*******************************************************************\n")
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

    def handleItemClick(self):
        try:
            column=self.tabel_sell.currentColumn()
            # print(self.tabel_sell.selectedItems().pop().column())

            if column==2:
                row = self.tabel_sell.currentRow()
                cur=self.tabel_sell.item(row, 2).text()
                price=Decimal(self.tabel_sell.item(row, 1).text())
                result=QTableWidgetItem(str(Decimal(cur)*price))

                self.tabel_sell.setItem(row, 3, result)
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
            self.Row -=1

    def removeRows(self, rows, isdel_list = 0):
        if isdel_list != 0:
            rows.reverse()
            for i in rows:
                self.tabel_sell.removeRow(i)
        else:
            for i in range(rows-1, -1, -1):
                self.tabel_sell.removeRow(i)
