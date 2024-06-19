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
from fixedwidthpy.column import ColumnSpec, Column
from fixedwidthpy.exceptions import InvalidColumnSpec, InvalidColumnData

def test_column_spec_initialization():
    spec = ColumnSpec(name="Test Column", width=10, fill='0', align='right')
    assert spec.name == "Test Column"
    assert spec.width == 10
    assert spec.fill == '0'
    assert spec.align == 'right'

def test_column_spec_invalid_initialization():
    with pytest.raises(InvalidColumnSpec):
        ColumnSpec(name="Test Column", width="10", fill='0', align='right')

def test_column_initialization():
    spec = ColumnSpec(name="Test Column", width=10, fill='0', align='right')
    column = Column(data="123", spec=spec)
    assert column.data == "123"
    assert column.spec == spec

def test_column_get_data_as_fixed_width():
    spec = ColumnSpec(name="Test Column", width=10, fill='0', align='right')
    column = Column(data="123", spec=spec)
    assert column.get_data_as_fixed_width() == '0000000123'
