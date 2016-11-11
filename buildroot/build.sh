#!/bin/bash

echo "This is a utility script that may suit some cases."
echo "It's written to fail if the environment isn't correctly"
echo "setup, so try running it and read the failure output."
echo ""
echo "Also, remember installing required packages!"
echo "Read the docs for more info..."
echo ""

# Goto location of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

BUILDROOT_DIR="$DIR/linked-buildroot"

if ! [ -h "$BUILDROOT_DIR" ]
then
	echo "Please unpack buildroot to some place you like and symlink"
	echo "the unpacked directory to $DIR/linked-buildroot"
	exit 123
fi

cd linked-buildroot

if ! [ -f "$BUILDROOT_DIR/.config" ]
then
	echo "Copying buildroot .config"
	cp "$DIR/buildroot-config-dist" "$BUILDROOT_DIR/.config"
fi

if ! diff -q "$DIR/buildroot-config-dist" "$BUILDROOT_DIR/.config"
then
        echo "Warning! Configuration has changed, remember to copy changes to Git (buildroot-config-dist)! The current .config will be used, nothing will be overwritten."
	echo -n "Continue? [y]"
        read yn
	if [[ "$yn" == "y" || "$yn" == "" ]]
	then
		echo "Continuing..."
	else
		exit 1
	fi
fi

if ! [ -f "$BUILDROOT_DIR/linux-config" ]
then
	echo "Copying linux config, linux-config"
	cp "$DIR/linux-config-dist" "$BUILDROOT_DIR/linux-config"
fi

if ! diff -q "$DIR/linux-config-dist" "$BUILDROOT_DIR/linux-config"
then
        echo "Warning! Linux kernel configuration has changed, remember to copy changes to Git (linux-config-dist)! The current linux-config will be used, nothing will be overwritten."
	echo -n "Continue? [y]"
        read yn
	if [[ "$yn" == "y" || "$yn" == "" ]]
	then
		echo "Continuing..."
	else
		exit 1
	fi
fi

cd "$BUILDROOT_DIR"
make

cd "$DIR"

IMAGES_DIR="$DIR/images"

mkdir -p "$IMAGES_DIR"

cp "$BUILDROOT_DIR/output/images/rootfs.iso9660" "$IMAGES_DIR/rootfs-`date +%F-%R`.iso"
