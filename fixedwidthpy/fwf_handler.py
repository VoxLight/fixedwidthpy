"""
Copyright 2024 VoxLight

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   /fwf/fwf_handler.py
"""
from collections import OrderedDict as OD
from typing import List, Dict, Any, Tuple, Union, Literal
import datetime

from .datarow import DataRow

from collections import OrderedDict as OD
from typing import List, Dict, Union, Literal
import datetime

class FixedWidthFileHandler:
    def __init__(self):
        self._data: List[DataRow] = []

    def add_row(self, row: DataRow) -> None:
        """Add a DataRow to the data."""
        if not isinstance(row, DataRow):
            raise ValueError("Only DataRow objects can be added.")
        self._data.append(row)

    def export_to_fw_file(
            self, 
            file_path: str, 
            include_header: bool = False, 
            mode: Literal['w', 'a', 'x'] = 'x'
            ) -> None:
        """
        Export data to a fixed-width file.

        - Parameters:
            - file_path: The path to the file to write to.
            - include_header: Whether to include a header line in the file.
            - mode: The file mode to use for writing. Default is 'x' (exclusive creation).
        """
        if not self._data:
            raise ValueError("No data to export.")
        
        try:
            with open(file_path, mode) as f:
                for data_row in self._data:
                    if not data_row.is_valid:
                        continue
                    row_line = ''.join(data_row.get_data_row())
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
