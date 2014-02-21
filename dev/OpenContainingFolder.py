# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
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

from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from gi.repository import Gtk
from gi.repository import Gio

from subprocess import Popen
import urllib

class OpenContainingFolderPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property (type = GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
    
    def log(self, function_name, message, error=False):
        if error:
            message_type = 'ERROR'
        else:
            message_type = 'DEBUG'
        print(function_name + ': ' + message_type + ': ' + message)

    def open_folder(self, action, *args):
        self.log(self.open_folder.__name__, 'Opening folder...')
        
        shell = self.object
        page = shell.props.selected_page
        if not hasattr(page, 'get_entry_view'):
            self.log(self.open_folder.__name__, 'Page has no entry view.', True)
            return
        
        selected = page.get_entry_view().get_selected_entries()
        if selected != []:
            uri = selected[0].get_playback_uri()
            dirpath = uri.rpartition('/')[0]
            if dirpath == '': dirpath = '/'
            self.log(self.open_folder.__name__, 'Opening ' + urllib.parse.unquote(dirpath))
            Popen(['xdg-open', dirpath])

    def do_activate(self):
        self.log(self.do_activate.__name__, 'Activating plugin...')
        
        self.locations = [
            'browser-popup', 'playlist-popup',
            'podcast-episode-popup', 'queue-popup'
            ]
        
        app = Gio.Application.get_default()
        
        action = Gio.SimpleAction(name='open-containing-folder')
        action.connect('activate', self.open_folder)
        app.add_action(action)
        
        item = Gio.MenuItem()
        item.set_label('Open containing folder')
        item.set_detailed_action('app.open-containing-folder')
        for location in self.locations:
            app.add_plugin_menu_item(
                location, 'open-containing-folder', item
                )

    def do_deactivate(self):
        self.log(self.do_deactivate.__name__, 'Deactivating plugin...')
        
        app = Gio.Application.get_default()
        for location in self.locations:
            app.remove_plugin_menu_item(location, 'open-containing-folder')
