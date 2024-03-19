import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

import sys
import os
import threading

from http.server import HTTPServer

from FilePicker import FilePicker

from FileListHTTP import FileListHTTP

class ServerWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Image Server")

        self.httpd = None
        self.server_thread = None

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.fp = FilePicker("Select the image repository:", Gtk.FileChooserAction.SELECT_FOLDER)
        box.append(self.fp)

        box_horizontal2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal2.set_margin_start(12)
        box_horizontal2.set_margin_end(10)
        box_horizontal2.set_margin_bottom(5)
        box_horizontal2.set_hexpand(True)

        self.label1 = Gtk.Label()
        self.label1.set_label("Server Status: Stopped!")
        self.label1.set_halign(Gtk.Align.START)
        self.label1.set_hexpand(True)
        box_horizontal2.append(self.label1)

        button2 = Gtk.Button(label="Start")
        button2.set_margin_start(5)
        button2.connect("clicked", self.start_server)
        box_horizontal2.append(button2)

        box.append(box_horizontal2)

        self.set_child(box)

    def start_server(self, button):
        self.httpd = HTTPServer(('', 8000), FileListHTTP)
        path = self.fp.text_entry1.get_text()
        if not path:
            path = '~/'
        os.chdir(os.path.expanduser(path))
        button.set_label("Stop")
        button.disconnect_by_func(self.start_server)
        button.connect("clicked", self.stop_server)
        self.label1.set_label("Server Status: Running on :8000")
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop_server(self, button):
        #if self.server_thread and self.httpd:
            #self.httpd.socket.close()
            #self.server_thread.join()

        button.set_label("Start")
        button.connect("clicked", self.start_server)
        self.label1.set_label("Server Status: Stopped!")
        self.close()
        return
