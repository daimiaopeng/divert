from PyQt5.QtCore import *

import pydivert
from .mytemp import server as code

filter = "ip.SrcAddr ==  118.178.182.52 or ip.DstAddr == 118.178.182.52"

all_code = {}
for i in dir(code):
    all_code[str(getattr(code, i))] = i


def getChatMessage(data):
    chat_mod = {
        1: '私聊',
        2: '近聊',
        8: '帮会',
        32: '世界',
    }
    cmd = data.readInt32()
    if cmd == 1:
        pass
    else:
        id = data.readInt32()
        nameLen = data.readInt16()
        name = data.readRawData(nameLen).decode('utf-8')
        none = data.readRawData(6)
        messageLen = data.readInt16()
        message = data.readRawData(messageLen).decode('utf-8')
        weiz = data.readInt32()
        rank = data.readInt32()

        str = "id：%s 【%s】%s[%s]级说：%s" % (id, chat_mod[cmd], name, rank, message)
        print(str)


def readData(rxData):
    data = QDataStream(QByteArray(rxData), QIODevice.ReadOnly)
    size = data.readInt16()
    cmd = data.readInt16()
    if cmd == 40:
        getChatMessage(data)
    elif cmd == 29:
        print("移动物品")
        return b'\x00\x12\x00\x1d\x00\x01\x00\x06\x00\x01\x00\x01\x00\x00\x00\x00\x00\xe3'
    else:
        print("解析数据，总包长：%s 长度：%s cmd: %s" % (len(rxData), size, all_code[str(cmd)].lower()))
        return None


def changesPayload(packet: pydivert.packet.Packet):
    temp = packet
    a = b''
    if str(packet.direction) == 'Direction.INBOUND':
        a = readData(packet.payload)
    elif str(packet.direction) == 'Direction.OUTBOUND':
        a = readData(packet.payload)
    # if  a != None:
    #     temp = a

    return temp


if __name__ == '__main__':
    print(all_code['24'])
