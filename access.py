#!/bin/env/python3
import types


class Access(object):
    """docstring for Access."""
    _addr = None
    _port = None
    _send_buf = []

    def __init__(self,addr = None, port = None):
        super().__init__()
        if type(addr) is int:
            if addr>=0 and addr<256 :
                self._addr = addr
        if type(port) is int:
            if port>=0 and port<8 :
                self._port = port
        _send_buf = []



    def set(self, addr=-1, port=-1 ):
        if addr>=0 and addr<256 :
            self._addr = addr
        if port>=0 and port<8 :
            self._port = port


    def resetData(self, datas = []):
        self._send_buf = list(datas)


    def addDataU8(self,u8):
        if type(u8) is list or type(u8) is tuple :
            for val in u8:
                self.addDataU8(val)
        elif type(u8) is int:
            self._send_buf.append(u8)
        else:
            raise ValueError(
            """Access import data in {} type,
            it shoud be int int list,int tuple""".format(type(u8)),
            u8)

    def addDataU8(self,u8):
        if type(u8) is list or type(u8) is tuple :
            for val in u8:
                self.addDataU8(val)
        elif type(u8) is int:
            self._send_buf.append(toU8(u8))
        else:
            raise ValueError(
            """Access import data in {} type,
            it shoud be int, list or tuple""".format(type(u8)),
            u8)
    def addDataU16(self,u16):
        if type(u16) is list or type(u16) is tuple :
            for val in u16:
                self.addDataU16(val)
        elif type(u16) is int:
            self._send_buf.append(toU8(u16))
            self._send_buf.append(toU8(u16>>8))
        else:
            raise ValueError(
            """Access import data in {} type,
            it shoud be int, list or tuple""".format(type(u16)),
            u16)
    def addDataU32(self,u32):
        if type(u32) is list or type(u32) is tuple :
            for val in u32:
                self.addDataU32(val)
        elif type(u32) is int:
            self._send_buf.append(toU8(u32))
            self._send_buf.append(toU8(u32>>8))
            self._send_buf.append(toU8(u32>>16))
            self._send_buf.append(toU8(u32>>24))
        else:
            raise ValueError(
            """Access import data in {} type,
            it shoud be int, list or tuple""".format(type(u32)),
            u32)
    def addDataString(self,s):
        if type(s) is str:
            for c in s:
                self._send_buf.append(ord(c))
        else:
            raise ValueError(
            """Access import data in {} type,
            it shoud be str""".format(type(s)),
            s)

    send_len_doc = ''' send_len
    get return the length for send buffer, and set to change length
    for send buffer. Change to large buffer will append 0,and
    change to smaller buffer will remove data from end of buffer.
    it is useful in send string.'''
    def sendLen_get(self):
        return len(self._send_buf)

    def sendLen_set(self, l):
        if type(l) is int:
            if 0<=l<=31:
                if l > len(self._send_buf):
                    self._send_buf.extend((0,)*(l-len(self._send_buf)))
                elif l < len(self._send_buf):
                    del self._send_buf[l:]
            else:
                raise ValueError('l _send_buf.len shold be 0 to 32 ',l)
        else:
            raise ValueError('l is length in int for _send_buf ',l)

    send_len = property(fget = sendLen_get,fset = sendLen_set, doc = send_len_doc)

    @property
    def send_bfc(self):
        return len(self._send_buf) + (self._port<<5)

def toU8(val):
    val= val & 0xff
    return val


if __name__ == '__main__':
    a1 = Access()
    a1.resetData(datas = [1,2])
    a1.set(addr = 12,port = 13)
    print("a1._addr = ", a1._addr)
    print("a1._port = ", a1._port)
    print("Init a1._data = ", a1._send_buf)
    a1.addDataU8(1112);
    a1.addDataU8((-13,14));
    a1.addDataU8([-1000,-1000>>8]);
    a1.addDataU16(1000)
    a1.addDataString("Hello")
    a1.addDataU32(0xfefdfcfa)
    print("append datas a1._data = ", a1._send_buf)
    a1.send_len = 5
    print("set length smaller to 5 a1._data = ", a1._send_buf)
    a1.send_len = 10
    print("set length bigger to 10 a1._data = ", a1._send_buf)
    a1.set(addr = 12,port = 3)
    print("a1.bfc = ", a1.send_bfc)
