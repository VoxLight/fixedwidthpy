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
from typing import List, Literal
from .column import ColumnSpec, Column
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

    def import_from_fw_file(
            self, 
            fw_file_path: str, 
            config_path: str
            ) -> List[DataRow]:
        """
        Import data from a fixed-width file given the filepath for the data file and the config file.

        Args:
            fw_file_path (str): The path to the fixed-width file.
            config_path (str): The path to the configuration file.

        Returns:
            List[DataRow]: The list of DataRow objects created from the fixed-width file.

        Raises:
            FileNotFoundError: If either of the file paths are invalid.
        """
        try:
            with open(config_path, 'r') as f:
                config: List[dict] = f.read()
            with open(fw_file_path, 'r') as f:
                data: List[str] = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file path {config_path} is invalid.")
        
        rows = []
        for line in data:
            row = DataRow()
            specs = [ColumnSpec(**spec) for spec in config]
            start = 0
            end = 0
            for spec in specs:
                start = end
                end += spec.width
                # Try to strip the fill character from the line.
                # I.e. if the fill character is '0' and the line is '000123', the column should be '123'
                # If the fill character is ' ' and the line is 'John Doe                      ', the column should be 'John Doe'
                row.add_column(Column(line[start:end].strip(spec.fill), spec))
            rows.append(row)

        return rows

