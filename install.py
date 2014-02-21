#!/usr/bin/python
# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    install.py
#
#    An RBPluginInstaller for <plugin_name>.
#    Copyright (C) <year> <plugin_author_name> <plugin_author_email>
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
#
from rbpi import RBPluginInstaller

plugin_files_path = {
    '2.95': './release/2.99',
    '2.96': './release/2.99',
    '2.97': './release/2.99',
    '2.98': './release/2.99',
    '2.99': './release/2.99',
    '3.0': './release/3.0',
    '3.0.1': './release/3.0',
    'dev': './dev'
}
cleanup_files = [
    '.git', '.gitignore', 'old'
]

if __name__ == "__main__":
    RBPluginInstaller('OpenContainingFolder', plugin_files_path,
                      install_folder='OpenContainingFolder',
                      cleanup_files=cleanup_files,
                      old_install_folders=['opencontainingfolder'])
