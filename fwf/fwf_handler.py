from collections import OrderedDict as OD
from typing import List, Dict, Any, Tuple, Union, Literal
import datetime

class FixedWidthFileHandler:
    def __init__(self):
        self._data: List[Dict[str, Any]] = []
        self._colnames: List[str] = []

    @property
    def colnames(self) -> List[str]:
        if self._data:
            self._colnames = list(self._data[0].keys())
        return self._colnames

    def add_row(self, row: Dict[str, Any]) -> None:
        """Add a row to the data."""
        self._data.append(row)

    def export_to_fw_file(
            self, 
            file_path: str, 
            col_specs: Dict[str, Union[int, Tuple[int, str, str]]], 
            include_header=False, 
            mode: Literal['w', 'a', 'x'] = 'x'
            ) -> None:
        """
        Export data to a fixed-width file.

        - Parameters:
            - file_path: The path to the file to write to.
            - col_specs: A dictionary of column specifications. The keys are column names and the values are either integers (for fixed-width columns) or tuples of integers and strings (for columns with fill characters).
            - include_header: Whether to include a header line in the file.
            - mode: The file mode to use for writing. Default is 'x' (exclusive creation).
        """
        if not self._data:
            raise ValueError("No data to export.")
        
        if not all(col in col_specs for col in self.colnames):
            raise ValueError(f"Column specifications do not match the columns in the data.\n    Extra Specs: {set(col_specs.keys()) - set(self.colnames)}\n    Missing Data: {set(self.colnames) - set(col_specs.keys())}")
        
        columns = [ColumnSpec(col, col_specs[col]) for col in self.colnames]
        self._validate_column_widths(columns)
        
        try:
            with open(file_path, mode) as f:
                if include_header:
                    header_line = ''.join([col.justify_string(col.name) for col in columns])
                    f.write(header_line + '\n')
                for row in self._data:
                    row_line = ''.join([col.justify_string(row[col.name]) for col in columns])
                    f.write(row_line + '\n')
        except FileNotFoundError:
            raise FileNotFoundError(f"The file path {file_path} is invalid.")
        except ValueError as ve:
            raise ValueError(f"Error exporting data to fixed-width file: {ve}")

    def import_from_fw_file(self, file_path: str, col_specs: Dict[str, Union[int, Tuple[int, str, str]]]) -> None:
        """
        Import data from a fixed-width file.

        - Parameters:
            - file_path: The path to the file to read from.
            - col_specs: A dictionary of column specifications. The keys are column names and the values are either integers (for fixed-width columns) or tuples of integers and strings (for columns with fill characters).
        """
        raise NotImplementedError("Importing data from fixed-width file is not implemented yet.")
    
    def _validate_column_widths(self, columns: List[ColumnSpec]) -> None:
        """Validate that all data fits within the specified column widths."""
        for row in self._data:
            for col in columns:
                if not col.validate_data(str(row[col.name])):
                    raise ValueError(f"Data in column '{col.name}' exceeds the specified width of {col.width}.")


# Example usage
def main():
    # Write the first record to the file
    handler1 = FixedWidthFileHandler()
    handler1.add_row(OD({"name": "Alice", "age": 25, "zip": "12345"}))
    handler1.add_row(OD({"name": "Bob", "age": 30, "zip": "54321"}))
    handler1.add_row(OD({"name": "Charlie", "age": 35, "zip": "67890"}))
    handler1.add_row(OD({"name": "David", "age": 40, "zip": "09876"}))

    handler1.export_to_fw_file(
        "data.txt",                     # Name of the file
        {                               # Column specifications
            "name": 20,                 # Fixed width of 20
            "age": (3, '0', 'right'),   # Fixed width of 3, fill with '0', right align
            "zip": (15, '0', 'right')   # Fixed width of 15, fill with '0', right align
        }, 
        include_header=False,           # Do not include header
        mode='w'                        # Write mode
    )
    
    # Import records from the file
    handler2 = FixedWidthFileHandler()
    handler2.add_row(OD({"records": 4, "timestamp": datetime.datetime.now()}))
    handler2.export_to_fw_file("data.txt", {"records": (3, '0', 'right'), "timestamp": 30}, include_header=False, mode='a')


if __name__ == "__main__":
    main()
