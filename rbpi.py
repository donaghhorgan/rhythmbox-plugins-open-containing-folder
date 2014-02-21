#!/usr/bin/python
# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    rbpi.py
#
#    A generic Rhythmbox plugin installer for users and developers.
#    Copyright (C) 2013-2014 Donagh Horgan <donagh.horgan@gmail.com>
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
from argparse import ArgumentParser
import logging
import os
import shutil
from subprocess import call
from gi.repository import RB

class RBPluginInstaller():
    
    """
    A generic plugin installer for Rhythmbox.
    """
    
    PLUGINS_PATH = '~/.local/share/rhythmbox/plugins/'
    GLIB_PATH = '/usr/share/glib-2.0/schemas/'
    
    def __init__(self, plugin_name, plugin_files_path, install_folder=None, 
                 glib_schema=None, cleanup_files=[], old_install_folders=[]):
        """
        Parse command line options and set paths.
        """
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s %(levelname)-8s %(message)s', 
                            datefmt='%H:%M:%S')
        
        self.plugin_name = plugin_name
        self.plugin_files_path = plugin_files_path
        self.install_folder = install_folder if install_folder else plugin_name
        self.glib_schema = glib_schema
        self.cleanup_files = cleanup_files
        self.old_install_folders = old_install_folders
        
        parser = ArgumentParser(
            description='Installs the ' + plugin_name + \
                        ' plugin for Rhythmbox.')
        parser.add_argument(
            '-u', '--uninstall', action='store_true', 
            help = 'uninstall the plugin')
        parser.add_argument(
            '-d', '--debug', action='store_true', 
            help = 'run Rhythmbox in debug mode after installation')
        parser.add_argument(
            '-m', '--manual', action='store_true', 
            help = 'choose which version of the plugin to install')
        parser.add_argument(
            '-v', '--version', 
            help = 'force the installation of a specific plugin version')
        args = parser.parse_args()
        
        if args.uninstall:
            self.uninstall()
        elif args.manual:
            self.manual_install()
        elif args.version:
            try:
                self.install(args.version)
            except:
                self.manual_install(error=True)
        else:
            version = self.guess_rb_version()
            try:
                self.install(version)
            except:
                self.manual_install(error=True)
        
        logging.debug("Complete")
        
        if args.debug:
            os.system('clear')
            call(['rhythmbox', '-D', plugin_name])
    
    def uninstall(self):
        """
        Uninstall the plugin.
        """
        logging.debug("Uninstalling %s..." % self.plugin_name)
        self.old_install_folders.append(self.install_folder)
        self.remove_old_versions()
    
    def remove_old_versions(self):
        """
        Remove old versions of the plugin, if present.
        """
        logging.debug("Removing old files...")
        for folder in self.old_install_folders:
            path = os.path.expanduser(os.path.join(self.PLUGINS_PATH, folder))
            if os.path.exists(path):
                shutil.rmtree(path)
    
    def install(self, version):
        """
        Install the specified version of the plugin.
        """
        self.uninstall()
        
        logging.debug('Installing %s for Rhythmbox %s...' % \
                      (self.plugin_name, version))
        
        source_path = self.plugin_files_path[version]
        install_path = os.path.expanduser(os.path.join(self.PLUGINS_PATH,
                                                       self.install_folder))
        shutil.copytree(source_path, install_path)
        if self.glib_schema:
            logging.info('Need sudo permissions to install ' \
                         'the settings schema.')
            call(['sudo', 'cp', self.glib_schema, self.GLIB_PATH])
            call(['sudo', 'glib-compile-schemas', self.GLIB_PATH])
        
        self.cleanup()
    
    def guess_rb_version(self):
        """
        Return the installed version of Rhythmbox.
        """
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

    def manual_install(self, error=False):
        """
        Display available plugin versions and install the first 
        valid selection.
        """
        if error:
            logging.warning('Could not determine Rhythmbox version. ' \
                            'Trying manual install \ninstead...')
        
        version = ''
        versions = self.get_available_versions()
        while version not in versions:
            os.system('clear')
            print('Please enter the version of Rhythmbox you want to install' \
                  '\n' +  self.plugin_name + ' for, or type "q" to quit:' \
                  '\n\n' + '\n'.join(versions) + '\n')
            version = raw_input('Version: ')
            if version.lower() in ['q', 'quit', 'exit']:
                exit()
        self.install(version)

    def get_available_versions(self):
        """
        Return a list of the available plugin versions.
        """
        versions = sorted(self.plugin_files_path.keys())
        available_versions = []
        for version in versions:
            path = self.plugin_files_path[version]
            abspath = os.path.abspath(path)
            if path and os.path.exists(abspath) and os.path.isdir(abspath):
                available_versions.append(version)
            else:
                logging.error('The plugin files path for version ' + \
                              version + ' (' + path + ') is not valid.')
                exit()
        return available_versions

    def cleanup(self):
        """
        Remove unnecessary files.
        """
        logging.debug('Cleaning up...')
        for f in self.cleanup_files:
            path = os.path.join(self.PLUGINS_PATH, self.install_folder, f)
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                elif os.path.isfile(path):
                    os.remove(path)
                else:
                    logging.warning(path + ' is not a valid file or ' \
                                    'directory and cannot be removed')
