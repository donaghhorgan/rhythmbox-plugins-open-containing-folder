# -*- coding: utf-8 -*-
#
#    OpenContainingFolder.py
#
#    Adds an option to open the folder containing the selected track(s) 
#    to the right click context menu.
#    Copyright (C) 2012-2013 Donagh Horgan <donagh.horgan@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#    Partly based on rb-open-folder by Adolfo González Blázquez.
#    Copyright (C) 2007, 2008 Adolfo González Blázquez <code@infinicode.org>

from gi.repository import GObject, Gio, Peas
from subprocess import Popen

class OpenContainingFolderPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property (type = GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

    def open_folder(self, action, _):
        shell = self.object
        page = shell.props.selected_page
        if not hasattr(page, 'get_entry_view'):
            return
        selected = page.get_entry_view().get_selected_entries()
        if selected != []:
            uri = selected[0].get_playback_uri()
            dirpath = uri.rpartition('/')[0]
            if dirpath == '': dirpath = '/'
            Popen(['xdg-open', dirpath])

    def do_activate(self):
        print "Activating plugin..."
    
        app = Gio.Application.get_default()

        # Create action
        action = Gio.SimpleAction(name='open-containing-folder')
        action.connect('activate', self.open_folder)
        app.add_action(action)

        # Add plugin menu items
        item = Gio.MenuItem()
        item.set_label('Open containing folder')
        item.set_detailed_action('app.open-containing-folder')
        app.add_plugin_menu_item('browser-popup', 'open-containing-folder', 
            item)
        app.add_plugin_menu_item('playlist-popup', 'open-containing-folder', 
            item)
        app.add_plugin_menu_item('podcast-episode-popup', 
            'open-containing-folder', item)
        app.add_plugin_menu_item('queue-popup', 'open-containing-folder', 
            item)

    def do_deactivate(self):
        print "Deactivating plugin..."
        
        app = Gio.Application.get_default()
        
        app.remove_plugin_menu_item('browser-popup', 'open-containing-folder')
        app.remove_plugin_menu_item('playlist-popup', 
            'open-containing-folder')
        app.remove_plugin_menu_item('podcast-episode-popup', 
            'open-containing-folder')
        app.remove_plugin_menu_item('queue-popup', 'open-containing-folder')
