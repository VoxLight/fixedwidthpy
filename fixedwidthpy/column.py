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
from typing import Any, Dict, Literal

from .exceptions import InvalidColumnSpec, InvalidColumnData

class ColumnSpec:

    def __init__(self, 
                 name:str, 
                 width: int, 
                 fill: str = ' ', 
                 align: str = Literal['left', 'right'],
                 order: int = -1
                 ):
        """
        Initialize a ColumnSpec object.

        - Parameters:
            - name: The name of the column.
            - width: The width of the column.
            - fill: The fill character for the column.
            - align: The alignment of the column ('left' or 'right').
        """
        if align not in ('left', 'right'):
            raise InvalidColumnSpec("Value for 'align' must be 'left' or 'right'.")
        if len(fill) != 1:
            raise InvalidColumnSpec("Fill character must be a single character.")
        if width < 1:
            raise InvalidColumnSpec("Column width must be greater than zero.")
        if not isinstance(order, int) or order < -1:
            raise InvalidColumnSpec("Order must be an integer greater than or equal to -1.")
        
        self.name:  str = name
        self.width: int = width
        self.fill:  str = fill
        self.align: str = align
        self.order: int = order

    def as_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'width': self.width,
            'fill': self.fill,
            'align': self.align,
            'order': self.order
        }

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
        if len(str(data)) > spec.width:
            # logger.warning(f"Data for column '{spec.name}' exceeds width of {spec.width}. Data will be truncated in final output.")
            data = str(data)[:spec.width]
        
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
    