---
title: Arch Linux Installation
date: 2025-01-06
tags:
  - Linux
  - Kernel
Description: Some targets that should be installed when installing arch linux on the host
cover:
---
# Arch Linux Installation

##### install targets

- base
- linux
- linux-firmware
- vim (for editing files)
- man-db (for man pages)
- man-pages
- dhcpcd
- amd-ucode / intel-ucode ([[microcode]])
- lvm2 (for lvm partitions)

##### optional
- git
- base-devel

> if `dhcpcd` is not installed, and arch is installed in an emulated environment
> the newly installed operating system would not have network access
> to get the network access back, the iso file that installed the operating system is needed

- use `fdisk -l` to identify the `root partition`
- use `mount /dev/sda3 /mnt` to mount the `root partition`
	- (assuming the root partition is in `/dev/sda3`)
- use mount `/dev/sda1 /mnt/boot` to mount the `boot partition`
	- (assuming the boot partition is int `/dev/sda1)
- swap on any swap partition if any exist using `swapon /dev/sda2`
- use `arch-chroot /mnt` into the system
- install the missing services using `pacman -S <target>`

### References
