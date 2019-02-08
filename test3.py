import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Table(QWidget):
    def __init__(self,parent=None):
        super(Table, self).__init__(parent)
        #设置标题与初始大小
        self.setWindowTitle('购物车')
        self.resize(800,400)

        #设置数据层次结构，4行4列
        self.model=QStandardItemModel()
        #设置水平方向四个头标签文本内容
        # self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])


        # #Todo 优化2 添加数据
        # self.model.appendRow([
        #     QStandardItem(11),
        #     QStandardItem(12),
        #     QStandardItem(14),
        #     QStandardItem(15),
        # ])
        #
        # for row in range(5):
        #     for column in range(4):
        #         item=QStandardItem('row %s,column %s'%(row,column))
        #         #设置每个位置的文本值
        #         self.model.setItem(row,column,item)

        #实例化表格视图，设置模型为自定义的模型
        self.tableView=QTableView()
        self.tableView.setModel(self.model)



        # #todo 优化1 表格填满窗口
        # #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #
        # #TODO 优化3 删除当前选中的数据
        # indexs=self.tableView.selectionModel().selection().indexes()
        # print(indexs)
        # if len(indexs)>0:
        #     index=indexs[0]
        #     self.model.removeRows(index.row(),1)


        #设置布局
        layout=QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    table=Table()
    table.show()
    data={
        '名称':'999感冒灵',
        '单价':10.8,
        '数量':1,
        '总价':10.8
    }
    table.model.setHorizontalHeaderLabels(data.keys())
    tabData=[]
    i=0
    for key in data.keys():
        # if key=="数量":
        #     sb = QSpinBox()
        #     sb.setRange(0, 10000)
        #     sb.setValue(1)  # 设置最开始显示的数字
        #     # sb.setDisplayIntegerBase(10)  # 这个是显示数字的进制，默认是十进制。
        #     # sb.setSuffix("元")  # 设置后辍
        #     # sb.setPrefix("RMB: ")  # 设置前辍
        #     sb.setSingleStep(1)
        #     table.model.setCellWidget(0, 4, sb)
        # else:
        table.model.setItem(0, i, QStandardItem(str(data[key])))
        i+=1

    sys.exit(app.exec_())