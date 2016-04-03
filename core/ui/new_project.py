#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Ui_NewProjectDialog:
    def __init__(self, parent):
        self.dialog = gtk.Dialog(title="New Project", parent=parent)
        self.dialog.set_modal(True)
        self.dialog.set_default_size(320, 160)
        self.notebook = gtk.Notebook()
        self.button = gtk.Button(label="OK")
        self.button.connect("clicked", self.buttonPressed)
        
        self.createNotebookPage(gtk.Label("General"))
        self.createNotebookPage(gtk.Label("Toolchain"))
        self.createNotebookPage(gtk.Label("Misc"))
        self.createNotebookPage(gtk.Label("Debug"))
        
        self.insertNotebookElement(gtk.Label("Project Name"), gtk.Entry(), 0)
        self.insertNotebookElement(gtk.Label("Project Path"), gtk.Entry(), 0)
        self.insertNotebookElement(gtk.Label("Project Type"), gtk.ComboBox(), 0)
        self.insertNotebookElement(gtk.Label("Project Category"), gtk.ComboBox(), 0)
        
        widget_list = {gtk.Label("l1"), gtk.Label("l2")}
        self.insertNotebookElementList(widget_list, 0)

        self.notebook.show()
        self.button.show()
        self.dialog.vbox.pack_start(self.notebook)
        self.dialog.vbox.pack_start(self.button)
        self.dialog.run()

    def createNotebookPage(self, label):
        container = gtk.VBox()
        container.show()
        self.notebook.append_page(container, label)
    
    def insertNotebookElement(self, label, widget, notebookPage):
        hBox = gtk.HBox()
        hBox.pack_start(label)
        hBox.pack_start(widget)
        self.notebook.get_nth_page(notebookPage).add(hBox)
        label.show()
        widget.show()
        hBox.show()

    def insertNotebookElementList(self, widget_list, notebookPage):
        hBox = gtk.HBox()
        for widget in widget_list:
            hBox.pack_start(widget)
            widget.show()
        self.notebook.get_nth_page(notebookPage).add(hBox)
        hBox.show()
    
    def buttonPressed(self, button):
        #self.dialog.response(gtk.RESPONSE_OK)
        self.dialog.hide()

if __name__ == "__main__":
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    ui_newProjectDialog = Ui_NewProjectDialog(window)


# ProjectType   | Action_NewProject | Action_SelectBuildSystem
#  Generic      |         X         |         {N.A.}
#  C            |         X         |    {Makefile, CMake}
#  C++          |         X         |    {Makefile, CMake}     
#  Android      |         -         |         { ? }
#  Python       |         -         |         { ? }
#  Mixed        |         X         |         { ? }
