import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

class FilePicker(Gtk.Box):
  def __init__(self, label, action):
    super().__init__(orientation=Gtk.Orientation.VERTICAL)
    self.action = action
    self.set_margin_top(5)
    self.set_margin_start(10)
    self.set_margin_end(10)
    self.set_margin_bottom(5)

    label1 = Gtk.Label()
    label1.set_label(label)
    label1.set_halign(Gtk.Align.START)
    label1.set_margin_bottom(3)
    label1.set_margin_start(2)
    self.append(label1)

    box_horizontal1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

    self.text_entry1 = Gtk.Entry()
    #self.text_entry1.set_placeholder_text("Select a folder")
    self.text_entry1.set_hexpand(True)
    box_horizontal1.append(self.text_entry1)

    button1 = Gtk.Button(label="Open")
    button1.set_margin_start(5)
    button1.connect("clicked", self.on_button_clicked)

    box_horizontal1.append(button1)

    self.append(box_horizontal1)

  def on_button_clicked(self, button):
      dialog = Gtk.FileChooserDialog(
          title="Select a folder",
          parent=self,
          action=self.action
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
          self.text_entry1.set_text(selected_folder)
      dialog.destroy()