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

   /fixedwidthpy/datarow.py
"""
from typing import List, Any, Callable
from .column import Column, ColumnSpec


FixedWidthConfig = List[ColumnSpec]
"""
Represents the configuration for a DataRow object. This is a list of dictionaries or a filename.

- List[ColumnSpec]: The list of column specifications.

Example Config:
[
    {'name':'name','width': 10, 'fill': ' ', 'align': 'left',  'order': '0'},
    {'name':'age', 'width': 3,  'fill': '0', 'align': 'right', 'order': '1'},
    {'name':'city','width': 15, 'fill': ' ', 'align': 'left',  'order': '2'},
]
"""

def mark_as_column(header: str, width: int, order: int = -1, fill: str = ' ', align: str = 'left'):
    def decorator(func):
        func._column_spec = ColumnSpec(
            name=header,
              width=width, 
            fill=fill, 
              align=align,
            order=order,
        )
        return func
    return decorator

class DataRow:
    def __init__(self, columns: List[Column] = None):
        """
        Initialize the DataRow object.

        - Attributes:
            - columns (List[Column]): The list of columns in the row.
            - is_valid (bool): A flag indicating if the row is valid.
            - invalid_reason (str): The reason the row is invalid.
        """
        self.columns: List[Column] = columns if columns is not None else []
        self._is_data_fetched: bool = False
        self.is_valid: bool = True
        self.invalid_reason: str = ""

    @property
    def number_of_columns(self) -> int:
        """
        Get the number of columns in the row.

        - Returns:
            - int: The number of columns in the row.
        """
        return len(self.columns)
    
    @property
    def total_width(self) -> int:
        """
        Get the total width of the row.

        - Returns:
            - int: The total width of the row.
        """
        return sum([col.spec.width for col in self.columns])
    
    def _fetch_decorated_methods(self) -> List[Callable]:
        """
        Fetch all methods on this DataRow instance that are marked as columns.

        - Returns:
            - List[Callable]: The list of instance methods marked as columns.
        """
        # Collect methods decorated with @mark_as_column
        methods = [
            method for _, method in vars(self.__class__).items()
            if callable(method) and 
            hasattr(method, '_column_spec') and 
            isinstance(method._column_spec, ColumnSpec)
        ]

        methods.sort(key=lambda item: item._column_spec.order)
        
        return methods

    def add_column(self, column: Column):
        """
        Add a column to the row.

        - Parameters:
            - data (Any): The data for the column.
            - spec (ColumnSpec): The specification for the column.
        """
        self.columns.append(column)

    def add_columns(self, columns: List[Column]):
        """
        Add a list of columns to the row.

        - Parameters:
            - columns (List[Column]): The list of columns to add.
        """
        self.columns.extend(columns)

    def add_column_from_data(self, data: Any, spec: ColumnSpec):
        """
        Add a column to the row from data and a spec.

        - Parameters:
            - data (Any): The data for the column.
            - spec (ColumnSpec): The specification for the column.
        """
        self.columns.append(Column(data, spec))

    def add_columns_from_data(self, data: List[Any], specs: List[ColumnSpec]):
        """
        Add a list of columns to the row from a list of data and a list of specs.

        - Parameters:
            - data (List[Any]): The list of data for the columns.
            - specs (List[ColumnSpec]): The list of specifications for the columns.
        """
        self.columns.extend([Column(d, s) for d, s in zip(data, specs)])

    def is_empty(self) -> bool:
        """
        Check if the row is empty.

        - Returns:
            - bool: True if the row is empty, False otherwise.
        """
        return self.number_of_columns == 0

    def invalidate(self, reason: str):
        """
        Invalidate the row with the specified reason.

        - Parameters:
            - reason (str): The reason the row is invalid.
        """
        self.is_valid = False
        self.invalid_reason = reason
        # logger.info(f"Row invalidated: {reason}")

    def fetch_data(self) -> List[Column]:
        """
        Fetch the data by calling decorated methods in the specified order.

        - Returns:
            - List[Column]: The list of columns in the row.
        """
        self._is_data_fetched = True

        # Collect methods decorated with @mark_as_column
        methods = self._fetch_decorated_methods()

        for method in methods:
            try:
                # Call the method and get the data
                data = method(self)
                if self.is_valid is False:
                    break
                # Create a column object
                col = Column(data, method._column_spec)
                # Append the column to the list
                self.columns.append(col)
            except Exception as e:
                self.invalidate(f"Error fetching data: {e}")
                break
        
        return self.columns

    def get_data(self) -> List[str]:
        """
        Get the data row as a list of fixed-width strings.

        - Returns:
            - List[str]: The list of fixed-width strings for each column.
        """
        return [col.get_data_as_fixed_width() for col in self.columns]
    
    def save_config(self) -> FixedWidthConfig:
        """
        Get the configuration for the row as a FixedWidthConfig.

        Returns:
            List[Dict[str, Any]]: The list of column specifications.
        """
        return [method._column_spec for method in self._fetch_decorated_methods()]
    
    def get_header(self) -> List[str]:
        """
        Get the header row as a list of column names.

        - Returns:
            - List[str]: The list of column names.
        """
        return [col.spec.name for col in self.columns]
    
    def __str__(self):
        return f"DataRow({self.columns})"

    def __repr__(self):
        return f"DataRow({self.columns})"
