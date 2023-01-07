#!/bin/sh

set -xe

nasm -felf64 ./output.asm
ld -o output output.o