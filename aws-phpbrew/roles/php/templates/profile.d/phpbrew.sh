#!/bin/sh

PHPBREW_ROOT={{ phpbrew_root }}
PHPBREW_HOME={{ phpbrew_home }}

[[ -e ${PHPBREW_HOME}/bashrc ]] && source ${PHPBREW_HOME}/bashrc
