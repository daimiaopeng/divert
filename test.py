a = b"""HTTP/1.1 200 OK\r\nServer: JSP3/2.0.14\r\nDate: Sun, 07 Jun 2020 01:49:28 GMT\r\nContent-Type: image/x-icon\r\nContent-Length: 5430\r\nConnection: keep-alive\r\nETag: "76ddd763ff7d01:0"\r\nLast-Modified: Fri, 25 Sep 2015 03:08:34 GMT\r\nAge: 138649\r\nAccept-Ranges: bytes\r\nCache-Control: no-cache\r\nX-Powered-By: ASP.NET\r\nOhc-File-Size: 543"""
print(a[:4]==b"HTTP")

def test():
    print("ok")