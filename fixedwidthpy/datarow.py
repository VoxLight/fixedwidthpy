from typing import List, Any
from .column import Column, ColumnSpec
import logging

logger = logging.getLogger(__name__)

def mark_as_column(header: str, width: int, order: int = -1, fill: str = ' ', align: str = 'left'):
    def decorator(func):
        func._column_spec = {
            'spec': ColumnSpec(name=header, width=width, fill=fill, align=align),
            'order': order
        }
        return func
    return decorator

class DataRow:
    
    def __init__(self):
        self.columns: List[Column] = []
        self.is_valid: bool = True
        self.invalid_reason: str = ""

    def invalidate(self, reason: str):
        self.is_valid = False
        self.invalid_reason = reason
        logger.info(f"Row invalidated: {reason}")

    def fetch_data(self) -> List[Column]:
        """
        Fetch the data by calling decorated methods in the specified order.
        """
        # Collect methods decorated with @mark_as_column
        methods = [
            (name, method)
            for name, method in vars(self.__class__).items()
            if callable(method) and hasattr(method, '_column_spec')
        ]
        
        # Sort methods by their specified order
        methods.sort(key=lambda item: item[1]._column_spec['order'])
        
        # Call each method and store the result in the columns list
        for name, method in methods:
            spec: ColumnSpec = method._column_spec['spec']
            value = method(self)
            column = Column(value, spec)
            if not self.is_valid:
                break
            self.columns.append(column)

        if not self.is_valid:
            logger.info(f"Invalid DataRow: {self.invalid_reason}")
            return []
        return self.columns

    def get_data_row(self) -> List[str]:
        """
        Get the data row as a list of fixed-width strings.

        - Returns:
            - List[str]: The list of fixed-width strings for each column.
        """
        return [col.get_data_as_fixed_width() for col in self.columns]

    def __repr__(self):
        return f"DataRow({self.columns})"
