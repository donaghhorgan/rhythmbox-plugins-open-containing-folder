#!/usr/bin/python
# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    install.py
#
#    A generic Rhythmbox plugin installer for users and developers.
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

##############################################################################
# Customisable options
##############################################################################
plugin_name = 'OpenContainingFolder'
install_directory_name = 'OpenContainingFolder'
old_install_locations = [
    'opencontainingfolder'
]
source_file_locations = {
    '2.95': './old/2.99',
    '2.96': './old/2.99',
    '2.97': './old/2.99',
    '2.98': './old/2.99',
    '2.99': './old/2.99',
    '3.0': './old/3.0',
    '3.0.1': './old/3.0',
    'dev': './'
}
glib_schema = ''
files_to_remove_after_install = [
    '.git', '.gitignore', 'old'
]

##############################################################################
# Everything below this line does not need to be edited (unless you want to)
##############################################################################
import argparse
import os
import shutil
from subprocess import call
from gi.repository import RB

plugins_path = os.path.expanduser('~/.local/share/rhythmbox/plugins/')
install_path = plugins_path + install_directory_name + '/'
glib_path = '/usr/share/glib-2.0/schemas/'
if glib_schema:
    files_to_remove_after_install += [glib_schema]

def guess_rb_version():
    '''
    Guesses the version of the plugin to install.
    '''
    if 'default_eject' in dir(RB.DeviceSource):
        version = '3.0.1'
    elif 'ListModel' in dir(RB):
        version = '3.0'
    elif 'Application' in dir(RB):
        version = '2.99'
    elif 'get_processed' in dir(RB.RhythmDBImportJob):
        version = '2.98'
    elif 'RhythmDBQueryResultList' in dir(RB):
        version = '2.97'
    elif 'ChunkLoader' in dir(RB):
        version = '2.96'
    elif 'Player' in dir(RB): # untested
        version = '2.95'
    else:
        version = None
    return version

def install(version):
    '''
    Installs the specified version of the plugin.
    '''
    print('Removing old versions.')
    remove_old_versions()
    uninstall()
    print('Installing ' + plugin_name + ' for Rhythmbox ' + version + '.')
    source_path = source_file_locations[version]
    shutil.copytree(source_path, install_path)
    if glib_schema:
        print('Need sudo to install settings schema.')
        call(['sudo', 'cp', glib_schema, glib_path])
        call(['sudo', 'glib-compile-schemas', glib_path])

def uninstall():
    '''
    Uninstalls the plugin.
    '''
    if os.path.exists(install_path):
        shutil.rmtree(install_path)

def remove_old_versions():
    '''
    Removes old versions of the plugin, if present.
    '''
    for location in old_install_locations:
        if location is not '' and location is not None:
            if os.path.exists(plugins_path + location):
                shutil.rmtree(plugins_path + location)

def manual_install(error=False):
    '''
    Generates the dialog for manual installation. Should be passed 
    error=True if guess_rb_version doesn't find anything. 
    '''
    choice = None
    available_versions = get_available_versions()
    while choice not in available_versions and choice is not 'q':
        os.system('clear')
        if error:
            print('Could not determine Rhythmbox version. Trying manual ' + 
                  'install \ninstead...\n')
        print(
            'Please select the version of Rhythmbox you want to install \n' + 
            plugin_name + ' for, or type q to quit.\n\n'
            'Available versions:\n\n' + '\n'.join(available_versions) + '\n'
            )
        choice = raw_input('Version: ')
    
    if choice is not 'q':
        install(choice)
        cleanup()

def get_available_versions():
    '''
    Does some checks on source_file_locations to make sure the listed 
    locations exist.
    '''
    versions = sorted(source_file_locations.keys())
    available_versions = []
    for v in versions:
        if (
            source_file_locations[v] != '' and 
            source_file_locations[v] is not None and
            os.path.exists(source_file_locations[v]) and
            os.path.isdir(source_file_locations[v])
            ):
            available_versions += [v]
        else:
            if (
                (source_file_locations[v] != '' and 
                 source_file_locations[v] is not None) and
                (not os.path.exists(source_file_locations[v]) or
                 not os.path.isdir(source_file_locations[v]))
                ):
                print('ERROR: The source file location for version ' + v + 
                      ' (' + source_file_locations[v] + ') is not a valid ' + 
                      'directory.\n')
                raise
    return available_versions

def cleanup():
    '''
    Removes the files specified in files_to_remove_after_install.
    '''
    print('Cleaning up...')
    file_list = [install_path + f for f in files_to_remove_after_install]
    for f in file_list:
        if os.path.exists(f):
            if os.path.isdir(f):
                shutil.rmtree(f)
            elif os.path.isfile(f):
                os.remove(f)
            else:
                print('ERROR: The file ' + str(f) + 
                      ' is not a file or a directory.\n')
                raise

def main():
    '''
    Parse command line arguments and call relevant functions.
    '''    
    parser = argparse.ArgumentParser(
        description='Installs the ' + plugin_name + ' plugin for Rhythmbox.'
        )
    parser.add_argument(
        '-d', '--debug', action='store_true', 
        help = 'install the plugin and run Rhythmbox in debug mode'
        )
    parser.add_argument(
        '-l', '--list', action='store_true', 
        help = 'list the available versions of the plugin'
        )
    parser.add_argument(
        '-u', '--uninstall', action='store_true', 
        help = 'uninstall the plugin'
        )
    parser.add_argument(
        '-v', '--version', help = 'install a specific version')

    debug_mode = vars(parser.parse_args())['debug']
    list_mode = vars(parser.parse_args())['list']
    uninstall_mode = vars(parser.parse_args())['uninstall']
    force_version = vars(parser.parse_args())['version']

    if force_version:
        version = force_version
    else:
        version = guess_rb_version()

    if list_mode:
        manual_install()
    elif uninstall_mode:
        remove_old_versions()
        uninstall()
    else:
        if version:
            install(version)
            cleanup()
        else:
            manual_install(error=True)
    
    if debug_mode:
        call(['clear'])
        call(['rhythmbox', '-D', plugin_name])

main()
print('Done.')
