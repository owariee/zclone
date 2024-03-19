import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GLib

import re
import requests
import subprocess
import threading

from FilePicker import FilePicker

class PublishWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application, title="zclone: Publish Image")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_margin_bottom(5)

        self.fp1 = FilePicker("Select image souce:", Gtk.FileChooserAction.OPEN)
        box.append(self.fp1)

        self.fp2 = FilePicker("Select the block device or partition:", Gtk.FileChooserAction.OPEN)
        box.append(self.fp2)

        box_horizontal1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_horizontal1.set_margin_start(12)
        box_horizontal1.set_margin_end(10)
        box_horizontal1.set_margin_bottom(5)
        self.label1 = Gtk.Label()
        self.label1.set_label("Progress: Not Started!")
        self.label1.set_halign(Gtk.Align.START)
        self.label1.set_hexpand(True)
        box_horizontal1.append(self.label1)

        self.button1 = Gtk.Button(label="Publish Image")
        self.button1.set_margin_start(5)
        self.button1.connect("clicked", self.create_image)
        box_horizontal1.append(self.button1)
        box.append(box_horizontal1)

        self.set_child(box)
 
    def is_link(self, string):
        # Regular expression pattern to match a link
        link_pattern = r'^https?://(?:www\.)?\S+\.\S+'
        # Check if the string matches the link pattern
        return re.match(link_pattern, string) is not None

    def create_image(self, button):
        # Function to update the label with the last line of the dd output
        def update_label(line, reenable=False):
            GLib.idle_add(lambda: self.label1.set_text(line.strip()))
            if reenable:
              GLib.idle_add(lambda: self.button1.set_sensitive(True))
            #self.label1.set_text(line.strip())

        iffile = self.fp1.text_entry1.get_text()
        offile = self.fp2.text_entry1.get_text()
        self.button1.set_sensitive(False)

        # Function to run dd command in a separate thread
        def run_dd_web():
            # Send GET request to download the file
            response = requests.get(iffile, stream=True)
            response.raise_for_status()  # Check for any errors in response

            # Use subprocess to call dd command and pipe response content to it
            dd_process = subprocess.Popen(
                ['dd', 'of=' + offile, "status=progress"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True)

            # Write response content to dd's stdin byte by byte
            for chunk in response.iter_content(chunk_size=1024):
                dd_process.stdin.write(chunk)
                # Read and process the output of dd in real-time
                for line in dd_process.stdout:
                    # Update the label with the last line of output
                    update_label(line)

            # Close stdin to signal end of input
            dd_process.stdin.close()          

            # Wait for the dd process to finish
            dd_process.wait()

            # Update the label with the exit status of dd process
            exit_status = dd_process.returncode
            Gtk.main_iteration_do(False, lambda: update_label(f"DD process exited with status {exit_status}", True))

        # Function to run dd command in a separate thread
        def run_dd():
            # Run the dd command in a subprocess
            dd_process = subprocess.Popen(
                ["dd", f"if={iffile}", f"of={offile}", "bs=4M", "status=progress"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            # Read and process the output of dd in real-time
            for line in dd_process.stdout:
                # Update the label with the last line of output
                update_label(line)

            # Wait for the dd process to finish
            dd_process.wait()

            # Update the label with the exit status of dd process
            exit_status = dd_process.returncode
            Gtk.main_iteration_do(False, lambda: update_label(f"DD process exited with status {exit_status}", True))
        
        func = run_dd
        # verify if iffile is link, if it is run_dd_web will run
        if self.is_link(iffile):
            func = run_dd_web

        # Start the dd process in a separate thread
        threading.Thread(target=run_dd, daemon=True).start()