from PyQt5.QtCore import *
import pydivert
from PyQt5.QtWidgets import *


class WdThread(QThread, QMainWindow):
    signalPacket = pyqtSignal(pydivert.packet.Packet, int)

    def __init__(self, parent=None):
        super(WdThread, self).__init__(parent)
        self.working = True
        self.num = 0
        self.parent = parent
        self.parent.signalSendPacket.connect(self.sendPacket)

    def __del__(self):
        self.working = False
        self.wd.close()
        self.wait()

    def run(self):
        while self.working == True:
            try:
                filterStr = self.parent.lineEdit_filter.text()
                if self.parent.checkBox_2.isChecked():
                    filterStr = '(' + filterStr + ') and (tcp.PayloadLength > 0 or udp.PayloadLength > 0)'
                self.wd = pydivert.WinDivert(filterStr)
                self.wd.open()
                for packet in self.wd:
                    self.signalPacket.emit(packet, self.num)
                    self.num = self.num + 1
            except Exception as e:
                print(e)
                QMessageBox.warning(self.parent, "错误", e, QMessageBox.Ok)

    def sendPacket(self, packet):
        self.wd.send(packet)
