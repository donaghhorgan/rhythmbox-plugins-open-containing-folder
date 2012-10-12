# -*- coding: utf-8 -*-
#
#    OpenContainingFolder.py
#
#    Adds an option to open the folder containing the selected track(s) 
#    to the right click context menu.
#    Copyright (C) 2012 Donagh Horgan <donaghhorgan@gmail.com>
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

from gi.repository import GObject, RB, Peas, Gtk
from subprocess import Popen

ui_str = """
<ui>
  <popup name="BrowserSourceViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="OpenContainingFolderPopup" action="OpenContainingFolder"/>
    </placeholder>
  </popup>

  <popup name="PlaylistViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="OpenContainingFolderPopup" action="OpenContainingFolder"/>
    </placeholder>
  </popup>

  <popup name="QueuePlaylistViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="OpenContainingFolderPopup" action="OpenContainingFolder"/>
    </placeholder>
  </popup>

  <popup name="PodcastViewPopup">
    <placeholder name="PluginPlaceholder">
      <menuitem name="OpenContainingFolderPopup" action="OpenContainingFolder"/>
    </placeholder>
  </popup>
</ui>
"""

class TestPlugin (GObject.Object, Peas.Activatable):
	object = GObject.property (type = GObject.Object)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		data = dict()
		shell = self.object
		manager = shell.props.ui_manager
		
		data['action_group'] = Gtk.ActionGroup(name='OpenContainingFolderActions')

		action = Gtk.Action(name='OpenContainingFolder', label=_("_Open containing folder"),
		                    tooltip=_("Open the folder containing the selected track(s)"),
		                    stock_id='gnome-mime-text-x-python')
		action.connect('activate', self.open_folder, shell)
		data['action_group'].add_action(action)		
				
		manager.insert_action_group(data['action_group'], 0)
		data['ui_id'] = manager.add_ui_from_string(ui_str)
		manager.ensure_update()
		
		shell.set_data('OpenContainingFolderInfo', data)
	
	def do_deactivate(self):
		shell = self.object
		data = shell.get_data('OpenContainingFolderInfo')

		manager = shell.props.ui_manager
		manager.remove_ui(data['ui_id'])
		manager.remove_action_group(data['action_group'])
		manager.ensure_update()

		shell.set_data('OpenContainingFolderInfo', None)

	def open_folder (self, action, shell):
		page = shell.props.selected_page
		if not hasattr(page, "get_entry_view"):
			return
		selected = page.get_entry_view().get_selected_entries()
		if selected != []:
			uri = selected[0].get_playback_uri()
			dirpath = uri.rpartition('/')[0]
			if dirpath == "": dirpath = "/"
			Popen(["xdg-open", dirpath])

