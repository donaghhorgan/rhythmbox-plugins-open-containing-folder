#!/usr/bin/env bash
# Installs the OpenContainingFolder plugin for Rhythmbox
# Copyright (C) 2016 Donagh Horgan <donagh.horgan@gmail.com>

name=OpenContainingFolder
path=~/.local/share/rhythmbox/plugins/$name
files=( LICENSE $name.plugin $name.py README.md )

SCRIPT_PATH=${0%`basename "$0"`}

if [ -d "$path" ]; then
  rm -rf $path
fi

mkdir -p $path

for file in "${files[@]}"
do
  cp "$SCRIPT_PATH"/$file $path
done

