import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from ServerWindow import ServerWindow
from PublishWindow import PublishWindow

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Main Menu")

        # Create a box to hold the buttons
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        button1 = self.create_button_content(
            "drive-harddisk",
            "Creates Block Device/Partition Image",
            "Mirror an block device or an partition into an image file.")
        box.append(button1)
        
        button2 = self.create_button_content(
            "drive-removable-media",
            "Publish Image",
            "Writes an image into an block device or partition.")
        button2.connect("clicked", self.open_publish_window)
        box.append(button2)

        button3 = self.create_button_content(
            "network-wireless",
            "Image Server",
            "Creates an simple http server to share images alongside the network.")
        button3.connect("clicked", self.open_server_window)
        box.append(button3)

        self.set_child(box)

    def open_publish_window(self, button):
        publish_window = PublishWindow(self.get_application())
        publish_window.show()
        self.close()

    def open_server_window(self, button):
        server_window = ServerWindow(self.get_application())
        server_window.show()
        self.close()

    def create_button_content(self, icon_name, label_text, description_text):
        button = Gtk.Button()

        # Define margins
        margin = 15
        button.set_margin_start(margin)
        button.set_margin_end(margin)
        button.set_margin_top(margin)
        button.set_margin_bottom(margin)

        # Create a box to hold icon and label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        button.set_child(box)

        # Create an image for the icon
        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon)
        image.set_pixel_size(64)
        box.append(image)

        # Create a label for the button name
        label = Gtk.Label()
        label.set_label(label_text)
        box.append(label)

        # Create a label for the description
        description = Gtk.Label()
        description.set_label(description_text)
        box.append(description)

        return button