#!/usr/bin/env python2

import sys
import platform
import threading
import socket
import time
if platform.system() == 'Linux':
    import gtk
elif platform.system() == 'Darwin':
    import AppKit
    import Foundation

PORT = 28752


class Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.sock.bind(('', PORT))
        self.sock.listen(1)
        while 1:
            self.conn, self.addr = self.sock.accept()
            e.set()
            while 1:
                try:
                    while 1:
                        n = self.conn.recv(1024)
                        if n != '\0':
                            break
                    data = self.conn.recv(int(n))
                except:
                    break
                c.set(data)
            self.conn.close()
        self.sock.close()


class Transmitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.host = sys.argv[1]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            self.sock.connect((self.host, PORT))
            while 1:
                while 1:
                    data = c.get()
                    if data == None:
                        self.sock.sendall('\0')
                        time.sleep(1)
                    else:
                        break
                self.sock.sendall(str(len(data)))
                self.sock.sendall(data)
        except:
            pass
        finally:
            self.sock.close()


class GTKClipboard():
    def __init__(self):
        self.clip = gtk.Clipboard()
        self.data = self.clip.wait_for_text()
        self.sig1 = False
        self.sig2 = False

    def get(self):
        if self.data == self.clip.wait_for_text():
            return None
        if self.sig1:
            if self.sig2:
                self.data = self.clip.wait_for_text()
                self.sig1 = False
                self.sig2 = False
            return None
        self.data = self.clip.wait_for_text()
        return self.data

    def set(self, data):
        self.sig1 = True
        self.clip.set_text(data)
        self.clip.store()
        self.sig2 = True


class OSXClipboard():
    def __init__(self):
        self.clip = AppKit.NSPasteboard.generalPasteboard()
        self.data = self.clip.stringForType_(AppKit.NSStringPboardType)
        self.sig1 = False
        self.sig2 = False

    def get(self):
        if self.data == self.clip.stringForType_(AppKit.NSStringPboardType):
            return None
        if self.sig1:
            if self.sig2:
                self.data = self.clip.stringForType_(AppKit.NSStringPboardType)
                self.sig1 = False
                self.sig2 = False
            return None
        self.data = self.clip.stringForType_(AppKit.NSStringPboardType)
        return self.data

    def set(self, data):
        self.sig1 = True
        self.clip.declareTypes_owner_([AppKit.NSStringPboardType], None)
        self.clip.setData_forType_(
                Foundation.NSString.stringWithString_(data).nsstring().dataUsingEncoding_(Foundation.NSUTF8StringEncoding),
                AppKit.NSStringPboardType)
        self.sig2 = True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <HOST>"
        sys.exit(2)
    if platform.system() == 'Linux':
        c = GTKClipboard()
    elif platform.system() == 'Darwin':
        c = OSXClipboard()
    else:
        print 'Error: OS not supported (' + self.syst + ')'
        sys.exit(1)
    e = threading.Event()
    r = Receiver()
    r.start()
    while 1:
        t = Transmitter()
        t.start()
        t.join()
        e.wait(60)
        e.clear()
