# Data Management

The data manager provides a high-level interface for reading and writing DataFrames through the configured storage backend.

## `data_manager`

```python
from gluepy.files.data import data_manager
```

### `read(path, root=False, *args, **kwargs)`

Read a DataFrame from a file.

```python
# Read from current run folder
df = data_manager.read("cleaned.csv")

# Read from storage root (absolute within storage)
df = data_manager.read("shared/reference_data.csv", root=True)
```

- `path` (str): Path to the file on the configured storage backend.
- `root` (bool): If `False` (default), path is relative to the current run folder. If `True`, path is relative to `STORAGE_ROOT`.

### `write(path, df, root=False, *args, **kwargs)`

Write a DataFrame to a file.

```python
# Write to current run folder
data_manager.write("output.csv", df)

# Write to storage root
data_manager.write("shared/output.csv", df, root=True)
```

### `read_sql(sql, *args, **kwargs)`

Read a DataFrame from a SQL query.

```python
df = data_manager.read_sql("SELECT * FROM my_table")
```

## Available Backends

### PandasDataManager
Default backend. Uses pandas for reading/writing files.

```python
DATA_BACKEND = "gluepy.files.data.PandasDataManager"
```

### Custom Data Manager
Create a custom backend by subclassing `BaseDataManager`:

```python
from gluepy.files.data.base import BaseDataManager

class MyDataManager(BaseDataManager):
    def read(self, path, root=False, *args, **kwargs):
        # custom read logic
        ...

    def write(self, path, df, root=False, *args, **kwargs):
        # custom write logic
        ...
```

Configure in settings:
```python
DATA_BACKEND = "mymodule.data.MyDataManager"
```
