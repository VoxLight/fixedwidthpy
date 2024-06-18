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
