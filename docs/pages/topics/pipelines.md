---
layout: default
title: Pipelines
nav_order: 1
parent: Topics
has_children: true
permalink: /gluepy/topics/pipelines/
---

# Pipelines

One of the core pieces of any data science project -- other than the data itself -- is the construction
of a pipeline that execute the steps that make up your model one by one until you get your final
results.

This document explains how the different pieces that make up a model fit in together, and
how you can create your own pipeline.

A pipeline in Gluepy is also refered to as a [DAG]({% link pages/reference/execution.md %}#dag) 
(directed acyclic graph). Here is a simple example of a preprocess `DAG` that we will
refer to throughout this document.

```python

from gluepy.exec import DAG, Task

class PreprocessDAG(DAG):
    label = "preprocess"
    tasks = (
        ProcessProducts,
        ProcessPrices,
        ProcessTransactions,
    )

class ProcessProducts(Task):
    def run(self):
        """Logic related to prepare product data"""

class ProcessPrices(Task):
    def run(self):
        """Logic related to prepare price data"""

class ProcessTransactions(Task):
    def run(self):
        """Logic related to prepare transaction data"""

```

## Defining a DAG

A [DAG]({% link pages/reference/execution.md %}#dag) is a simple class that is responsible
for grouping a set of [Tasks]({% link pages/reference/execution.md %}#task) together and
define in which order they should be executed.

As you can see from our example `PreprocessDAG`, it groups a set of preprocess `Task` classes
under the `PreprocessDAG.tasks` attribute and give the `DAG` a label. The `label` is the name
of our `DAG` and defines how we will refer to our DAG later when we want to execute it.

```python
class PreprocessDAG(DAG):
    label = "preprocess"
    tasks = (
        ProcessProducts,
        ProcessPrices,
        ProcessTransactions,
    )
```

In our simple example, this defines a `DAG` that executes 3 tasks one by one in the order
from top to bottom.


## Running a DAG

Your `DAG` is automatically loaded to your projects CLI and callable from the `./run.py dag <label>`
command as long as the module that the `DAG` belongs to is included in your projects `INSTALLED_MODULES` 
[setting]({% link pages/reference/settings.md %}#installed_modules).

This means that to run our `PreprocessDAG` defined earlier, we can call it by the `preprocess` label
that we set using the following CLI command:

```bash
$ python run.py dag preprocess
```

As you can see, this makes it very easy to have multiple `DAG` definitions in your project
and call them one by one. For example you might separate your project into `preprocess`,
`test`, `train`, `predict` and so on to make your pipelines shorter and independant from
each other.


## The execution of a DAG

A [DAG]({% link pages/reference/execution.md %}#dag) is simply a definition. It does not
contain any logic related to the actual execution of the defined `Task` classes,
this is instead the job of the [Executor]({% link pages/reference/execution.md %}#executor).

This means that a single `DAG` can be executed in different ways depending on which
`Executor` that is set for the project. For example, you might want to execute things
locally, or on a remote service using message queues, or on a SaaS platform like Databricks.

No matter how you execute things, your code and `DAG` looks the same, its only the settings
relating to the `Executor` of your project that is updated. This makes it very convenient
to switch from local development to production infrastructure.

## Creating a Task

A `Task` is an individual step within your `DAG`. The `Task` is where most of your code
and custom logic will reside, this is where you spend most of your development efforts 
in any project.

The `Task` class is a simple interface that allows the rest of the pieces that make up a
pipeline to understand the entrypoint of your code and how it can be executed, this
entrypoint is the `run()` method.

```python
class ProcessProducts(Task):
    def run(self):
        """Logic related to prepare product data"""
```

What you fill your `Task` with is completely up to you, go ahead and read in your data
as Dataframes and run your models. Feel free to separate your code into multiple files
or classes if it makes sense, what matters is that the `Task` is the entrypoint to your
module -- and it is what is used within your `DAG` definition to make up your pipeline.

Note that the `Task.run()` method do not accept any arguments. This is to force each
task to be independant from each other, and make sure that they do not rely on in-memory
arguments or data to be passed into them.

The benefits of this are:

* Tasks are composable and can be reused across `DAG` defintions no matter what other `Task`
  that is executed right before it.
* Tasks are replayable and you can either retry a failed run, or resume a run from a specific
  `Task` without having to run the full pipeline and depend on in-memory objects being passed
  through from task to task.
* Tasks can be executed across different machines or processes without shared memory.

The way you share data between tasks are through file reads and writes. `TaskA` might save
output to a database or file, and `TaskB` might read in this data if it depend on it.


## Executor

An `Executor` is the class that implements the actual execution of the `Task` classes within
our `DAG`. At first glance you might think that you "just want to run" your code but this
is actually a quite complex topic.

* Do you want to run your code on your local machine or VM?
* Do you want to deploy and run your code on a platform like Databricks?
* Do you want to use message queues and workers to execute your Tasks?
* Do you want to use technologies such as Airflow or Luigi to run your Tasks?

You control how your pipeline is executed by setting the `EXECUTOR_BACKEND`
[setting]({% link pages/reference/settings.md %}#executor_backend) to the implementation
that you want to use. You can use a built-in `Executor` or you are free to implement
your own for your own needs.

```python
# settings.py
EXECUTOR_BACKEND = "gluepy.exec.executors.LocalExecutor"
```

By separating the execution of the Tasks from the business logic itself, you can easily
customize the execution from for example development on your local machine, running your
test suite and deploying your pipeline on a production system -- without having to change
your the code or implementation of your pipeline.

## Building your own Executor

...