import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from FilePicker import FilePicker

class ServerWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Image Server")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        fp = FilePicker("Select the image repository:", Gtk.FileChooserAction.SELECT_FOLDER)
        box.append(fp)

        box_horizontal2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal2.set_margin_start(12)
        box_horizontal2.set_margin_end(10)
        box_horizontal2.set_margin_bottom(5)
        box_horizontal2.set_hexpand(True)

        label2 = Gtk.Label()
        label2.set_label("Server Status: Stopped!")
        label2.set_halign(Gtk.Align.START)
        label2.set_hexpand(True)
        box_horizontal2.append(label2)

        button2 = Gtk.Button(label="Start")
        box_horizontal2.append(button2)

        box.append(box_horizontal2)

        self.set_child(box)