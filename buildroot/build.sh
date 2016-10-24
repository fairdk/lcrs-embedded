#!/bin/bash

echo "This is a utility script that may suit some cases."
echo "It's written to fail if the environment isn't correctly"
echo "setup, so try running it and read the failure output."
echo ""
echo "Also, remember installing required packages!"
echo "Read the docs for more info..."

# Goto location of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

if ! [ -h "./linked-buildroot" ]
then
	echo "Please unpack buildroot to some place you like and symlink"
	echo "the unpacked directory to $DIR/linked-buildroot"
	exit 123
fi
