---
layout: default
title: Commands
parent: Reference
permalink: /gluepy/ref/commands
nav_order: 3
---

# Commands

The entrypoint to run any code of a gluepy project is the `run.py` commandline interface
that is generated when you start a new project. By executing your code through this 
CLI instead of creating your own scripts, you can take advantage of bootstrapping such
as:

* Preload modules.
* Load settings and set log configuration.
* Have a single execution root to simplify import paths.

The command line interface (CLI) is the entrypoint of your 