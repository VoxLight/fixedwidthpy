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
import pytest
from fixedwidthpy import DataRow, mark_as_column
from fixedwidthpy.column import Column, ColumnSpec

class _TestRecord(DataRow):

    def __init__(self, data: str, id_: int):
        super().__init__()
        self.data_value = data
        self.id_ = id_

    @mark_as_column(header="Test Column", width=10, order=1, fill='0', align='right')
    def fetch_test_column(self):
        if self.data_value != "valid":
            self.invalidate("Invalid data_value")
        return self.data_value
    
    @mark_as_column(header="ID", width=10, order=0, fill='0', align='right')
    def fetch_id(self):
        if self.id_ < 1000:
            self.invalidate("Invalid ID")
        return self.id_

def test_data_row_fetch_data():
    record = _TestRecord("valid", 1000)
    columns = record.fetch_data()
    assert record.is_valid
    assert len(columns) == 2
    assert columns[0].get_data_as_fixed_width() == "0000001000"
    assert columns[1].get_data_as_fixed_width() == "00000valid"

def test_data_row_invalidation():
    record = _TestRecord("invalid", 1000)
    columns = record.fetch_data()
    assert not record.is_valid
    assert record.invalid_reason == "Invalid data_value"

    record = _TestRecord("valid", 999)
    columns = record.fetch_data()
    assert not record.is_valid
    assert record.invalid_reason == "Invalid ID"
