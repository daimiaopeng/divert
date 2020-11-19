from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui import *
import sys
from WdThread import *
import pydivert
import plugin
import importlib


# https://reqrypt.org/windivert-doc-1.4.html#filter_language

class MyWindow(QMainWindow, Ui_MainWindow):
    signalSendPacket = pyqtSignal(pydivert.packet.Packet)

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('pydivert')
        self.Button_start.clicked.connect(self.startButton)
        self.pushButton.clicked.connect(self.initPlugin)
        self.pushButton_2.clicked.connect(self.usePlugin)
        self.initTable()
        self.initPlugin()
        self.checkBox_1.stateChanged.connect(self.checkBox_1_change)
        self.checkBox_1.setChecked(True)
        self.checkBox_2.setChecked(True)

    def startButton(self):
        if self.lineEdit_filter.text() == "":
            QMessageBox.warning(self, "警告", "请输入过滤器", QMessageBox.Ok)
            return
        self.Button_start.setText("重新开始")
        self.wdThread = WdThread(parent=self)
        self.wdThread.signalPacket.connect(self._getPacket)
        self.wdThread.start()

    def _getPacket(self, packet: pydivert.packet.Packet, num: int):
        self.model.setItem(num, 0, QStandardItem(str(num + 1)))
        self.model.setItem(num, 1, QStandardItem(packet.src_addr))
        self.model.setItem(num, 2, QStandardItem(str(packet.src_port)))
        self.model.setItem(num, 3, QStandardItem(packet.dst_addr))
        self.model.setItem(num, 4, QStandardItem(str(packet.dst_port)))
        self.model.setItem(num, 5, QStandardItem("none"))
        self.model.setItem(num, 6, QStandardItem(str(packet.ip.packet_len)))
        self.model.setItem(num, 7, QStandardItem(str(packet.payload)))
        self.model.setItem(num, 7, QStandardItem(str(packet.payload)))
        self.tableView.setModel(self.model)
        # self.dockWidget.textBrowser: QTextBrowser.setText(str(packet.payload))
        try:
            if self.isUsePlugin:
                packet = self.module.changesPayload(packet)
        except Exception as e:
            QMessageBox.critical(self, "插件运行错误，即将退出", str(e), QMessageBox.Ok)
            self.close()
        finally:  # 发送包的信号
            self.signalSendPacket.emit(packet)
            if self.state:
                self.tableView.scrollToBottom()
        # ip.SrcAddr ==  124.250.115.37 or ip.DstAddr == 124.250.115.37

    def initPlugin(self):
        self.isUsePlugin = False
        self.comboBox.clear()
        self.pluginsName = plugin.findAllPluginsName()
        self.comboBox.addItems(self.pluginsName)

    def usePlugin(self):
        self.module = importlib.import_module('.' + self.comboBox.currentText().replace('.py', ''), 'Plugins')
        # tcp.PayloadLength > 0 and tcp.DstPort == 443
        self.isUsePlugin = True
        self.lineEdit_filter.setText(self.module.filter)
        # self.pushButton_2.setText('点击取消使用')

    def initTable(self):
        self.tableHead = ['No.', 'Source', 'src_port', 'Destination', 'dst_port', 'Protocol', 'Length', 'Payload']
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model = QStandardItemModel()
        # 设置横坐标每项的属性名
        self.model.setHorizontalHeaderLabels(self.tableHead)
        # 配置数据，注意！！！需要使用QStandardItem格式的文本
        # 滚动条的打开关闭
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setStyleSheet("selection-background-color:#0000FF;")

        self.state = False

    def checkBox_1_change(self, state):
        if state == Qt.Unchecked:
            self.state = False
        elif state == QtCore.Qt.Checked:
            self.state = True

    def __del__(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    app.exec_()