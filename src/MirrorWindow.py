import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from FilePicker import FilePicker

class MirrorWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Create Image")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_bottom(5)

        fp1 = FilePicker("Select the block device or partition:", Gtk.FileChooserAction.OPEN)
        box.append(fp1)

        fp2 = FilePicker("Select image destination:", Gtk.FileChooserAction.SAVE)
        box.append(fp2)

        box_horizontal1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal1.set_margin_start(12)
        box_horizontal1.set_margin_end(10)
        box_horizontal1.set_margin_bottom(5)
        label1 = Gtk.Label()
        label1.set_label("Progress: Not Started!")
        label1.set_halign(Gtk.Align.START)
        label1.set_hexpand(True)
        box_horizontal1.append(label1)

        button1 = Gtk.Button(label="Create Image")
        button1.set_margin_start(5)
        box_horizontal1.append(button1)
        box.append(box_horizontal1)

        self.set_child(box)