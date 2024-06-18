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

   /fwf/datarow.py
"""
from collections import OrderedDict as OD

from typing import Dict, Any, List, Callable, Tuple

from .exceptions import InvalidDataRow
from .column import Column, ColumnSpec

import json

def mark_as_column(header: str, width: int, order: int = -1, fill: str = ' ', align: str = 'left'):
    def decorator(func: Callable[[], Any]):
        func._column_spec = {
            'spec': ColumnSpec(name=header,width=width,fill=fill,align=align),
            'order': order
        }
        
        return func
    return decorator

class DataRow:
    
    def __init__(self):
        self.columns: List[Column] = []
        self.is_valid: bool = True

    def invalidate(self):
        self.is_valid = False

    def fetch_data(self) -> List[Column]:
        """
        Fetch the data by calling decorated methods in the specified order.
        """
        # Collect methods decorated with @column_spec
        methods = [
            (name, method)
            for name, method in vars(self.__class__).items()
            if callable(method) and hasattr(method, '_column_spec')
        ]
        
        # Sort methods by their specified order (in place)
        methods.sort(key=lambda item: item[1]._column_spec['order'])
        
        # Call each method and store the result in the data dictionary
        for name, method in methods:
            spec: ColumnSpec = method._column_spec['spec']
            column = Column(method(self), spec)
            if not self.is_valid:
                break
            self.data[spec.name] = column

        if not self.is_valid:
            return {}
        return self.data
    


    def __repr__(self):
        return f"DataRow({json.dumps(self.data)})"
    


class ExampleRecord(DataRow):

    def __init__(self, eluc: str, id_: int):
        super().__init__()
        self.eluc = eluc
        self.id_ = id_

    @mark_as_column('example', 10, order=1)
    def fetch_example_data(self):
        return self.eluc
    
    @mark_as_column('id', 10, order=0)
    def fetch_id_data(self):
        return self.id_

def main():
    eluc = 'example'
    ids = [100000, 2000000, 3000000, 4000000, 500000, 60000]
    for id_ in ids:
        data = ExampleRecord(eluc, id_).fetch_data()
        print(data)

if __name__ == "__main__":
    main()


