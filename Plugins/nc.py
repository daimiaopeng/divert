from PyQt5.QtCore import *

import pydivert

filter = "ip.SrcAddr == 120.77.204.248  or ip.DstAddr == 120.77.204.248 and tcp.DstPort == 8888"



def changesPayload(packet: pydivert.packet.Packet):
    if str(packet.direction) == 'Direction.INBOUND':
        # packet.payload = b""""""
        pass
    elif str(packet.direction) == 'Direction.OUTBOUND':
        pass
        # packet.payload = b""""""
        # a = readData(packet.payload)
    # if  a != None:
    #     temp = a

    return packet


if __name__ == '__main__':
    pass
