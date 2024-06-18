# fixedwidthpy

![GitHub stars](https://img.shields.io/github/stars/VoxLight/fixedwidthpy)
![GitHub forks](https://img.shields.io/github/forks/VoxLight/fixedwidthpy)
![GitHub issues](https://img.shields.io/github/issues/VoxLight/fixedwidthpy)
![GitHub watchers](https://img.shields.io/github/watchers/VoxLight/fixedwidthpy)

Fixed Width Files are a NIGHTMARE!! So, I took my time to make the BEST library for dealing with them!

## Installation

You can install the package using pip:

```bash
pip install git+https://github.com/VoxLight/fixedwidthpy
```

## Usage

### Basic Usage

Here is a basic example of how to use `fixedwidthpy` to define and use columns, data rows, and the file handler.

```python
from fixedwidthpy.datarow import DataRow, mark_as_column
from fixedwidthpy.fwf_handler import FixedWidthFileHandler

# Define a simple record with some data and column specifications
class SimpleRecord(DataRow):

    @mark_as_column(header="Name", width=20, order=1, fill=' ', align='left')
    def fetch_name(self):
        return "Alice"

    @mark_as_column(header="Age", width=3, order=2, fill='0', align='right')
    def fetch_age(self):
        return 30

# Create an instance of the record
record = SimpleRecord()
record.fetch_data()

# Create a file handler and add the record
handler = FixedWidthFileHandler()
handler.add_row(record)
handler.export_to_fw_file('simple_data.txt')
```

### Advanced Usage with Business Logic

The `fixedwidthpy` library was createdout of frustration with the clashing of business logic and formatting and adadada... I wasn't alone, however, This often arises when working with fixed-width files. However, take a look. This example shows how you can define business logic within your data rows and invalidate rows based on specific conditions. This helps us parse data and get so much more hands on with the data (like we have always wanted) without a messy codebase.

You can call `invalidate()` on the instance of your record in the event that you no longer want to process the record. This will prevent the record from being written to the file, but save the rest of the data. This is useful when you want to skip invalid records but still process the rest of the data.

```python
from fixedwidthpy.column import ColumnSpec, Column
from fixedwidthpy.datarow import DataRow, mark_as_column
from fixedwidthpy.fwf_handler import FixedWidthFileHandler

class AdvancedRecord(DataRow):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age

    @mark_as_column(header="Name", width=20, order=1, fill=' ', align='left')
    def fetch_name(self):
        if not self.name:
            self.invalidate("Name cannot be empty")
        return self.name

    @mark_as_column(header="Age", width=3, order=2, fill='0', align='right')
    def fetch_age(self):
        if not (0 <= self.age <= 120):
            self.invalidate("Age must be between 0 and 120")
        return self.age

# Create an instance of the record
records = [
    AdvancedRecord("Alice", 30),
    AdvancedRecord("", 25),         # This record will be invalidated
    AdvancedRecord("Bob", 200)      # This record will be invalidated
]

# Create a file handler and add the valid records
handler = FixedWidthFileHandler()
for record in records:
    record.fetch_data()
    if record.is_valid:
        handler.add_row(record)
    else:
        print(f"Invalid record: {record.invalid_reason}")

handler.export_to_fw_file('advanced_data.txt')
```

## Why fixedwidthpy?

When working with fixed-width files, there is often a complex interaction between business logic and the formatting of the data. Many existing libraries either focus on the formatting aspect or the data validation aspect but not both. `fixedwidthpy` was created to address this gap.

By using `fixedwidthpy`, you can:

- Define columns with specific formatting rules.
- Embed business logic within your data-fetching methods.
- Invalidate rows based on custom business rules, ensuring only valid data is written to your fixed-width files.

This approach not only simplifies the handling of fixed-width files but also ensures that your data processing logic remains clean and maintainable.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
