# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    OpenContainingFolder.py
#
#    Adds an option to open the folder containing the selected track(s)
#    to the right click context menu.
#    Copyright (C) 2012-2016 Donagh Horgan <donagh.horgan@gmail.com>
#
#    Partly based on rb-open-folder by Adolfo González Blázquez.
#    Copyright (C) 2007, 2008 Adolfo González Blázquez <code@infinicode.org>
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

from gi.repository import Gio, GObject, Gtk, Peas, RB
import logging
import subprocess


class OpenContainingFolder(GObject.Object, Peas.Activatable):

    """Adds an option to open the folder containing the selected track(s) to
    the right click context menu."""

    object = GObject.property(type=GObject.Object)

    _action = 'open-containing-folder'
    _locations = locations = ['browser-popup',
                              'playlist-popup',
                              'podcast-episode-popup',
                              'queue-popup']

    def __init__(self):
        super(OpenContainingFolder, self).__init__()
        self._app = Gio.Application.get_default()

    def open_folder(self, *args):
        """Open the given folder.

        Args:
            args: Additional arguments. These are ignored.
        """
        page = self.object.props.selected_page
        try:
            selected = page.get_entry_view().get_selected_entries()
            if selected:
                uri = selected[0].get_playback_uri()
                dirpath = uri.rpartition('/')[0]
                dirpath = '/' if not dirpath else dirpath
                subprocess.check_call(['xdg-open', dirpath])
        except:
            logging.exception('Could not open folder')

    def do_activate(self):
        """Activate the plugin."""
        logging.debug('Activating plugin...')

        action = Gio.SimpleAction(name=OpenContainingFolder._action)
        action.connect('activate', self.open_folder)
        self._app.add_action(action)

        item = Gio.MenuItem()
        item.set_label('Open containing folder')
        item.set_detailed_action('app.%s' % OpenContainingFolder._action)

        for location in OpenContainingFolder._locations:
            self._app.add_plugin_menu_item(location,
                                           OpenContainingFolder._action,
                                           item)

    def do_deactivate(self):
        """Deactivate the plugin."""
        logging.debug('Deactivating plugin...')

        for location in OpenContainingFolder._locations:
            self._app.remove_plugin_menu_item(location,
                                              OpenContainingFolder._action)
