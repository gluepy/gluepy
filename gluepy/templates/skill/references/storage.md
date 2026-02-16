# Storage System

The storage system abstracts file operations across different backends.

## `default_storage`

Access the configured storage backend:

```python
from gluepy.files.storages import default_storage
from io import StringIO

# Write a file
default_storage.touch("output/results.txt", StringIO("hello world"))

# Read a file
content = default_storage.open("output/results.txt")

# Write to the current run folder
default_storage.touch(default_storage.runpath("results.txt"), StringIO("data"))

# Check existence
if default_storage.exists("some/path.csv"):
    ...

# List files and directories
files, dirs = default_storage.ls("some/directory")

# Copy files
default_storage.cp("src/file.txt", "dest/file.txt")

# Delete files
default_storage.rm("old/file.txt")

# Create directories
default_storage.mkdir("new/directory", make_parents=True)

# Check type
default_storage.isdir("some/path")
default_storage.isfile("some/path")
```

## Path Helpers

- `abspath(path)` - Absolute path including `STORAGE_ROOT`
- `relpath(path)` - Relative path from `STORAGE_ROOT`
- `runpath(path)` - Path relative to current run folder (`gluepy.run_folder`)

## Available Backends

### LocalStorage
Default backend. Stores files on the local filesystem.

```python
STORAGE_BACKEND = "gluepy.files.storages.local.LocalStorage"
STORAGE_ROOT = os.path.join(BASE_DIR, "data")
```

### GoogleStorage
Google Cloud Storage backend. Requires `gluepy[gcp]`.

```python
STORAGE_BACKEND = "gluepy.files.storages.google.GoogleStorage"
STORAGE_ROOT = "gs://my-bucket/prefix"
```

### S3Storage
Amazon S3 / DigitalOcean Spaces backend. Requires `gluepy[digitalocean]`.

```python
STORAGE_BACKEND = "gluepy.files.storages.s3.S3Storage"
STORAGE_ROOT = "s3://my-bucket/prefix"
```

### MemoryStorage
In-memory storage for testing.

```python
STORAGE_BACKEND = "gluepy.files.storages.memory.MemoryStorage"
```

## Configuration

Set in your settings module:

```python
STORAGE_BACKEND = "gluepy.files.storages.local.LocalStorage"
STORAGE_ROOT = os.path.join(BASE_DIR, "data")
```
