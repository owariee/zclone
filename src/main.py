import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

from MainWindow import MainWindow

class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="io.github.glclearcolor", flags=Gio.ApplicationFlags.FLAGS_NONE)
    
    def do_activate(self):
        win = MainWindow(application=self)
        win.present()

app = MyApplication()
exit_status = app.run([])
