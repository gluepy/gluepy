---
layout: default
title: Commands
nav_order: 3
parent: Topics
permalink: /gluepy/topics/commands/
---

# Commands

The entrypoint to run any code of a gluepy project is the `run.py` commandline interface
that is generated when you start a new project. By executing your code through this 
CLI instead of creating your own scripts, you can take advantage of bootstrapping such
as:

* Preloading modules.
* Loading settings and set log configuration.
* Have a single execution root to simplify import paths.
* Simplify onboarding of your project with a clear way of how to run your code.


## Start a project with gluepy-cli.py

As you [install gluepy]({% link pages/introduction/install.md %}), you automatically get
access to a global commandline interface that is available from anywhere on your system.
This CLI gives you access to all built-in commands that come with gluepy, including 
the ones used to start a new project.

```bash
$ gluepy-cli.py startproject demo
$ cd demo/
```

## Manage your project using run.py


## Built-in commands


## Extend CLI with your own commands
