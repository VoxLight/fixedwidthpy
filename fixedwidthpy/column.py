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

   /fixedwidthpy/column.py
"""
from typing import Any, Callable
from .exceptions import InvalidColumnSpec, InvalidColumnData

class ColumnSpec:

    def __init__(self, name:str, width: int, fill: str = ' ', align: str = 'left'):
        """
        Initialize a ColumnSpec object.

        - Parameters:
            - name: The name of the column.
            - width: The width of the column.
            - fill: The fill character for the column.
            - align: The alignment of the column ('left' or 'right').
        """
        if not isinstance(name, str):
            raise InvalidColumnSpec("Value for 'name' not a string.")
        if not isinstance(width, int):
            raise InvalidColumnSpec("Value for 'width' not an integer.")
        if not isinstance(fill, str):
            raise InvalidColumnSpec("Value for 'fill' not a string.")
        if not isinstance(align, str):
            raise InvalidColumnSpec("Value for 'align' not a string.")
        if align not in ('left', 'right'):
            raise InvalidColumnSpec("Value for 'align' must be 'left' or 'right'.")
        
        self.name:  str = name
        self.width: int = width
        self.fill:  str = fill
        self.align: str = align

    def __iter__(self):
        return iter((self.name, self.width, self.fill, self.align))

class Column:
    def __init__(self, data: Any, spec: ColumnSpec):
        """
        Initialize a Column object.

        - Parameters:
            - name: The name of the column.
            - data: The data for the column.
            - spec: The specification for the column width, fill character, and alignment.
        """
        if not isinstance(spec, ColumnSpec):
            raise InvalidColumnData("Value for 'spec' not of type 'ColumnSpec'.")
        if len(str(data)) > spec.width:
            raise InvalidColumnData("Data exceeds column width.")
        
        self.data: str = str(data)
        self.spec: ColumnSpec = spec
    
    def get_data_as_fixed_width(self) -> str:
        """
        Justify a string based on this colspec.

        - Parameters:
            - data: The data to justify.

        - Returns:
            - str: The justified string.
        """
        if self.spec.align == 'left':
            return self.data.ljust(self.spec.width, self.spec.fill)
        return self.data.rjust(self.spec.width, self.spec.fill)
    