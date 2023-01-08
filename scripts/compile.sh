#!/bin/sh

set -xe

nasm -felf64 ./output/output.asm
ld -o ./output/output ./output/output.o