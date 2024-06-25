"""
Copyright 2024 https://github.com/VoxLight

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   /fixedwidthpy/fwf_handler.py
"""
from typing import List, Dict, Union, Tuple, Literal

from collections import OrderedDict as OD
import datetime

from .datarow import DataRow
from .exceptions import InvalidDataRow


class FixedWidthFileHandler:
    def __init__(self):
        self._data: List[DataRow] = []

    def add_row(self, row: DataRow) -> None:
        """
        Add a DataRow for export into the fixed-width file.

        - Parameters:
            - row: The DataRow object to add.

        - Raises:
            - InvalidDataRow: If the value passed for 'row' is not a DataRow.
        """
        if not isinstance(row, DataRow):
            raise InvalidDataRow(f"Only DataRow objects can be added. {row} is of type {type(row).__name__}.")
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
                    if not data_row._is_data_fetched:
                        data_row.fetch_data()
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
