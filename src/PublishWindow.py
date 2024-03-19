import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

class PublishWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Publish Image")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        label1 = Gtk.Label()
        label1.set_label("Select the image repository:")
        label1.set_halign(Gtk.Align.START)
        label1.set_margin_top(10)
        label1.set_margin_bottom(3)
        label1.set_margin_start(12)
        box.append(label1)

        box_horizontal1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal1.set_margin_start(10)
        box_horizontal1.set_margin_end(10)
        box_horizontal1.set_margin_bottom(5)

        self.text_entry = Gtk.Entry()
        self.text_entry.set_placeholder_text("Select a folder")
        self.text_entry.set_hexpand(True)
        box_horizontal1.append(self.text_entry)

        button1 = Gtk.Button(label="Open")
        button1.set_margin_start(5)
        button1.connect("clicked", self.on_button_clicked)
        box_horizontal1.append(button1)

        box.append(box_horizontal1)

        box_horizontal2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal2.set_margin_start(12)
        box_horizontal2.set_margin_end(10)
        box_horizontal2.set_margin_bottom(10)
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

    def on_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select a folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )

        dialog.add_buttons(
            "Select",
            Gtk.ResponseType.OK,
            "Cancel",
            Gtk.ResponseType.CANCEL
        )

        dialog.connect("response", self.on_dialog_response)
        dialog.show()

    def on_dialog_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            selected_folder = dialog.get_file().get_path()
            self.text_entry.set_text(selected_folder)
        dialog.destroy()