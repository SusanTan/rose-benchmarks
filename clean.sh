#!/bin/bash


for dir in */ ; do cd $dir ; make clean > /dev/null 2>&1 ; cd ../ ; done
