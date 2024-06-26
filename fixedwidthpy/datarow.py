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
from typing import List, Any, Dict, Callable
from .column import Column, ColumnSpec
import logging
import json
import os

logger = logging.getLogger(__name__)

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
    
    def __init__(self):
        """
        Initialize the DataRow object.

        - Attributes:
            - columns (List[Column]): The list of columns in the row.
            - is_valid (bool): A flag indicating if the row is valid.
            - invalid_reason (str): The reason the row is invalid.
        """
        self.columns: List[Column] = []
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
        
        # Return the list of column specifications
        return [method for _, method in methods]

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
        logger.info(f"Row invalidated: {reason}")

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
    
    def get_config(self, filename: str = None) -> List[Dict[str, Any]]:
        """
        Get the configuration for the row as a Dict where the key is the column name,
        and the value is a dictionary with the ColumnSpec attributes. This config can
        be imported into a data row class to recreate the column specifications. This
        way, you just mark each column with the header name, and the rest of the con-
        fig is imported from the file.

        Example Config:
        {
            {'name':'name','width': '10', 'fill': ' ', 'align': 'left', 'order': '0'},
            {'name':'age','width': '3', 'fill': '0', 'align': 'right', 'order': '1'},
            {'name':'city','width': '15', 'fill': ' ', 'align': 'left', 'order': '2'},
        }

        Args:
            filename (str): The name of the file to write the config to. Defaults to None. 
            If None, the configuration is only returned as a dictionary.

        Returns:
            List[Dict[str, Any]]: The list of column specifications.
        """
        # We are going to require you to make sure the file exists when writing.
        if filename and not os.path.exists(filename):
            logger.error(f"Provided file does not exist: {filename}")
            raise FileNotFoundError(f"File not found: {filename}.")

        # Create a list to hold the column specifications
        config = [method._column_spec.as_dict() for method in self._fetch_decorated_methods()]

        # Write the configuration to a file if a filename is provided
        if filename:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
                logger.info(f"Configuration for {self.__class__.__name__} written to {filename}")
        
        return config

    def get_data_row(self) -> List[str]:
        """
        Get the data row as a list of fixed-width strings.

        - Returns:
            - List[str]: The list of fixed-width strings for each column.
        """
        return [col.get_data_as_fixed_width() for col in self.columns]
    
    def get_header_row(self) -> List[str]:
        """
        Get the header row as a list of column names.

        - Returns:
            - List[str]: The list of column names.
        """
        return [col.spec.name for col in self.columns]

    def __repr__(self):
        return f"DataRow({self.columns})"
