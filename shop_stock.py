import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from decimal import Decimal
import xlrd
from ToDB import ToDB
class Shopstock(QWidget):
    def __init__(self):
        super(Shopstock, self).__init__()
        self.initUI()
        self.db = ToDB()

    # UI设计实现
    def initUI(self):
        self.setGeometry(100, 100, 1000, 600)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        label_sell_title = QLabel("录入")
        label_sell_title.setFont(QFont("华文行楷", 20))
        # 定义条形码输入框，并设置只允许输入整数
        self.line_code = QLineEdit()
        self.line_code.setMaxLength(14)

        self.line_code.textChanged.connect(self.coudesearch)

        # 设置输入框的大小
        self.line_code.setFixedSize(450, 30)

        # 录入按钮，绑定事件
        btn_sell_lr = QPushButton("录入")
        btn_sell_lr.clicked.connect(self.event_lr)

        btn_excel = QPushButton("打开Excel")
        btn_excel.clicked.connect(self.event_excel)

        self.tabel_sell = QTableWidget()
        self.tabel_sell.setRowCount(1)
        self.tabel_sell.setColumnCount(8)
        self.tabel_sell.setHorizontalHeaderLabels(["条形码", "名称", "生产厂家", "批号", "有效期", "进价", "零售价", "数量"])

        self.tabel_sell.setColumnWidth(5, 200)

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
        h3 = QHBoxLayout()

        w_title = QWidget()
        w_21 = QWidget()
        w_22 = QWidget()
        w_31 = QWidget()


        v1.addWidget(label_sell_title, 0, Qt.AlignCenter)

        h1.addWidget(self.line_code)
        # h1.addWidget(label_name)
        h2.addWidget(btn_excel)
        h2.addWidget(btn_sell_lr)


        h3.addWidget(self.tabel_sell)

        w_title.setLayout(v1)
        w_21.setLayout(h1)
        w_22.setLayout(h2)
        w_31.setLayout(h3)

        splitter_sell1 = QSplitter(Qt.Horizontal)
        splitter_sell1.setSizes([800, 80])
        splitter_sell1.addWidget(w_title)
        splitter_sell2 = QSplitter(Qt.Horizontal)
        splitter_sell2.setSizes([150, 60])
        splitter_sell2.addWidget(w_22)
        splitter_sell3 = QSplitter(Qt.Horizontal)
        splitter_sell3.addWidget(w_21)
        splitter_sell3.addWidget(splitter_sell2)
        splitter_sell4 = QSplitter(Qt.Vertical)
        splitter_sell4.setSizes([800, 140])
        splitter_sell4.addWidget(splitter_sell1)
        splitter_sell4.addWidget(splitter_sell3)


        splitter_sell7 = QSplitter(Qt.Horizontal)
        splitter_sell7.setSizes([700, 390])
        splitter_sell7.addWidget(self.tabel_sell)
        splitter_sell8 = QSplitter(Qt.Horizontal)
        splitter_sell8.addWidget(splitter_sell7)

        splitter_sell9 = QSplitter(Qt.Vertical)
        splitter_sell9.addWidget(splitter_sell4)
        splitter_sell9.addWidget(splitter_sell8)
        # splitter_sell9.addWidget(w_low)
        layout.addWidget(splitter_sell9)
        self.setLayout(layout)
        # 临时变量
        self.Row = 0

    # 录入数据库
    def event_lr(self):
        data=[]
        delRows=[]
        try:

            for row in range(0,self.tabel_sell.rowCount()):
                flag = False  # 一行是否有空值
                for j in range(0,self.tabel_sell.columnCount()):

                    if not self.tabel_sell.item(row,j) or self.tabel_sell.item(row,j).text()=="":
                        flag=True
                        break
                if not flag:
                    code = self.tabel_sell.item(row,0).text()

                    name=self.tabel_sell.item(row,1).text()
                    # 生产商
                    producer=self.tabel_sell.item(row,2).text()
                    batch=self.tabel_sell.item(row,3).text()
                    validity=self.tabel_sell.item(row,4).text()

                    price=self.tabel_sell.item(row,5).text()
                    cost=self.tabel_sell.item(row,6).text()
                    count=self.tabel_sell.item(row,7).text()

                    data.append((code,name,producer,batch,validity,price,cost,count))
                    delRows.append(row)

            self.removeRows(delRows, isdel_list=1)

        except Exception as e:
            print(e)
        # "条形码", "名称", "生产厂家", "批号", "有效期", "进价", "零售价", "数量"
        sql="INSERT INTO 库存(条形码,名称,生产厂家,批号,有效期,进价,零售价,数量) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        self.db.insertMany(sql,data)
    def event_excel(self):
        if not self.isNullTab():
            replay = QMessageBox.question (self, "!", "当前还有数据为入库，是否继续？", QMessageBox.Yes | QMessageBox.No)
            if replay==QMessageBox.Yes:
                # 重新初始化表格
                self.tabel_sell.clear()
                self.tabel_sell.setRowCount(1)
                self.tabel_sell.setColumnCount(8)
                self.tabel_sell.setHorizontalHeaderLabels(["条形码", "名称", "生产厂家","批号","有效期","进价", "零售价", "数量"])
            else:
                return
        openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        if openfile_name[0]=="":
            return

        input_table=xlrd.open_workbook(openfile_name[0]) # 打开一个excel
        sheet=input_table.sheet_by_index(0) # 根据顺序获取sheet

        input_table_rows = sheet.nrows # 行

        input_table_colunms = sheet.ncols # 列

        input_table_header = sheet.row_values(0)
        self.tabel_sell.setRowCount(input_table_rows)
        # self.tabel_sell.setColumnCount(input_table_colunms)

        # self.tabel_sell.setHorizontalHeaderLabels(input_table_header)

        if "条形码" in input_table_header:

            for i in range(1,input_table_rows):
                input_table_rows_values = sheet.row_values(i)
                for j in range(input_table_colunms):
                    rc_value=sheet.cell(i,j).value

                    input_table_items = str(rc_value)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tabel_sell.setItem(i, j, newItem)
        else:
            for i in range(1,input_table_rows):
                input_table_rows_values = sheet.row_values(i)
                for j in range(input_table_colunms):
                    rc_value=sheet.cell(i,j).value
                    if j==0:

                        results = self.db.searchCode('select 条形码 from 库存 where 名称="%s"' % rc_value)

                        if results:
                            input_table_items = str(results[0])
                            self.tabel_sell.setItem(i,0, QTableWidgetItem(input_table_items))
                    input_table_items = str(rc_value)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tabel_sell.setItem(i, j+1, newItem)


    def contextMenuEvent(self, event):
        try:
            pmenu = QMenu(self)
            pDeleteAct = QAction('删除行', self.tabel_sell)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleterows)
            pmenu.popup(self.mapToGlobal(event.pos()))

            pAddAct = QAction('增加行', self.tabel_sell)
            pmenu.addAction(pAddAct)
            pAddAct.triggered.connect(self.addrows)
            pmenu.popup(self.mapToGlobal(event.pos()))
        except Exception as e:
            print(e)

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



    def removeRows(self, rows, isdel_list = 0):
        if isdel_list != 0:
            rows.reverse()
            for i in rows:
                self.tabel_sell.removeRow(i)
        else:
            for i in range(rows-1, -1, -1):
                self.tabel_sell.removeRow(i)

    def addrows(self):
        self.tabel_sell.setRowCount(self.tabel_sell.rowCount()+1)

    def closeEvent(self, event):
        """
        重写closeEvent方法
        :param event: close()触发的事件
        :return: None
        """
        if self.tabel_sell.item(0, 1) is not None:
            reply =QMessageBox.question(self,
                                                   '提示',
                                                   "还有数据未入库，是否要退出程序？",
                                                   QMessageBox.Yes | QMessageBox.No,
                                                   QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
    def coudesearch(self):
        code=self.line_code.text()
        if len(code)==14:
            try:
                sql = 'select 名称,进价,零售价 from 库存 where 条形码="%s"' % code
                result = self.db.searchCode(sql)
                # 是否已经在表格中
                items = self.tabel_sell.findItems(code, Qt.MatchExactly)
                if len(items) != 0:
                    curRow = items[0].row()
                else:
                    if not self.isNullTab():
                        self.tabel_sell.setRowCount(self.tabel_sell.rowCount() + 1)
                    # 是空表且没有一行
                    if self.isNullTab() and self.tabel_sell.rowCount() == 0:
                        self.tabel_sell.setRowCount(self.tabel_sell.rowCount() + 1)
                    curRow = self.tabel_sell.rowCount()-1

                self.tabel_sell.setItem(curRow, 0, QTableWidgetItem(code))
                if result:
                    name=QTableWidgetItem(result[0])
                    name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tabel_sell.setItem(curRow, 1,name)

                    bid=QTableWidgetItem(str(result[1]))
                    bid.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tabel_sell.setItem(curRow, 2, bid)

                    retail=QTableWidgetItem(str(result[2]))
                    retail.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tabel_sell.setItem(curRow, 3, retail)
                # 数量
                if self.tabel_sell.item(curRow,4):
                    curCount=self.tabel_sell.item(curRow,4).text()
                    count=QTableWidgetItem(str(int(curCount)+1))
                else:
                    count = QTableWidgetItem(str(0 + 1))
                count.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tabel_sell.setItem(curRow, 4, count)
            except Exception as e:
                print(e)
            finally:
                self.line_code.clear()
    def isNullTab(self):
        rows=self.tabel_sell.rowCount()
        column=self.tabel_sell.columnCount()

        for i in range(0,rows):
            for j in range(0,column):
                if self.tabel_sell.item(i,j):
                    return False

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sell = Shopstock()
    sell.show()
    sys.exit(app.exec())
