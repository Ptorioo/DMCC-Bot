# Makefile for packaging the project. DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU ARE DOING
# GNU Make 4.4
# Built for x86_64-pc-msys
# Copyright (C) 1988-2022 Free Software Foundation, Inc.
# License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
#===================================================================================

# Allow only one "make -f Makefile2" at a time, but pass parallelism
.NOTPARALLEL:

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE)
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands
$(VERBOSE).SILENT:

#===================================================================================

.DEFAULT_GOAL := help

PYTHON ?= python3.10

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifneq ($(wildcard $(ROOT_DIR)/.venv/.),)
	VENV_PYTHON = $(ROOT_DIR)/.venv/bin/python
else
	VENV_PYTHON = $(PYTHON)
endif

define HELP_BODY
Usage:
  make <command>

Commands:
  reformat                   Reformat all .py files being tracked by git.
  stylecheck                 Check which tracked .py files need reformatting.
  stylediff                  Show the post-reformat diff of the tracked .py files
                             without modifying them.
  newenv                     Create or replace this project's virtual environment.
  syncenv                    Sync this project's virtual environment to the latest
                             dependencies.
endef
export HELP_BODY

reformat:
	$(VENV_PYTHON) -m black $(ROOT_DIR)
.PHONY: reformat

stylecheck:
	$(VENV_PYTHON) -m black --check $(ROOT_DIR)
.PHONY: stylecheck

stylediff:
	$(VENV_PYTHON) -m black --check --diff $(ROOT_DIR)
.PHONY: stylediff

newenv:
	$(PYTHON) -m venv --clear .venv
	.venv/bin/python3.10.exe -m pip install -U pip wheel
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --upgrade setuptools
	.venv/bin/pip install --upgrade setuptools wheel
	$(MAKE) syncenv
.PHONY: newenv

syncenv:
	SETUPTOOLS_USE_DISTUTILS=stdlib .venv/bin/pip install -r ./requirements.txt
	SETUPTOOLS_USE_DISTUTILS=stdlib .venv/bin/pip install -r ./tools/requirements.txt
.PHONY: syncenv

help:
	@echo "$$HELP_BODY"
.PHONY: help