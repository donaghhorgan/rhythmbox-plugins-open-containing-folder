#!/usr/bin/python
# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    install.py
#
#    Generic Rhythmbox plugin installer.
#    Copyright (C) 2013 Donagh Horgan <donagh.horgan@gmail.com>
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

import argparse
import os
import shutil
from subprocess import call

plugin_name = 'OpenContainingFolder'
version_locations = {
    '2.95': './old/2.99',
    '2.96': './old/2.99',
    '2.97': './old/2.99',
    '2.98': './old/2.99',
    '2.99': './old/2.99',
    '3.0': './'
}
plugins_directory = os.path.expanduser('~/.local/share/rhythmbox/plugins/')
install_location = plugins_directory + plugin_name + '/'
old_install_locations = [
    'opencontainingfolder'
]
glib_schema = None
glib_path = '/usr/share/glib-2.0/schemas/'

def remove_old_versions():
    for location in old_install_locations:
        if location is not '' and location is not None:
            if os.path.exists(plugins_directory + location):
                shutil.rmtree(plugins_directory + location)

def install(version):
    shutil.copytree(version_locations[version], install_location)
    if glib_schema:
        print('Need sudo to install settings schema.')
        call(['sudo', 'cp', glib_schema, glib_path])
        call(['rm', install_location + glib_schema])
        call(['sudo', 'glib-compile-schemas', glib_path])

def uninstall():
    if os.path.exists(install_location):
        shutil.rmtree(install_location)

parser = argparse.ArgumentParser(
    'Installs the ' + plugin_name + ' plugin for Rhythmbox.'
    )
parser.add_argument(
    '-d', '--debug', action='store_true', 
    help = 'installs the plugin and runs Rhythmbox in debug mode'
    )
parser.add_argument(
    '-u', '--uninstall', action='store_true', 
    help = 'uninstall the plugin'
    )
parser.add_argument(
    '-v', '--version', help = 'install a specific version')

debug_mode = vars(parser.parse_args())['debug']
uninstall_mode = vars(parser.parse_args())['uninstall']
choice = vars(parser.parse_args())['version']

if uninstall_mode:
    remove_old_versions()
    uninstall()
else:
    available_versions = sorted(version_locations.keys())
    while choice not in available_versions and choice is not 'q':
        os.system('clear')
        print(
            'Please select the version of Rhythmbox you want to install \n' + 
            plugin_name + ' for, or type q to quit.\n\n'
            'Available versions:\n\n' + '\n'.join(available_versions) + '\n'
            )
        choice = raw_input('Version: ')
    
    if choice is not 'q':
        print('Removing old versions.')
        remove_old_versions()
        uninstall()
        print('Installing version ' + choice + '.')
        install(choice)
        if debug_mode:
            call(['clear'])
            call(['rhythmbox', '-D', plugin_name])

