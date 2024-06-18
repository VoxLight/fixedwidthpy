import pytest
from fixedwidthpy.fwf_handler import FixedWidthFileHandler
from fixedwidthpy.datarow import DataRow, mark_as_column
from fixedwidthpy.column import ColumnSpec

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

def test_fwf_handler_add_row():
    handler = FixedWidthFileHandler()
    record = _TestRecord("valid", 1000)
    record.fetch_data()
    handler.add_row(record)
    assert len(handler._data) == 1

def test_fwf_handler_export_to_fw_file(tmp_path):
    handler = FixedWidthFileHandler()
    record1 = _TestRecord("valid", 1000)
    record2 = _TestRecord("valid", 2000)
    record1.fetch_data()
    record2.fetch_data()
    handler.add_row(record1)
    handler.add_row(record2)

    file_path = tmp_path / "data.txt"
    handler.export_to_fw_file(file_path)

    with open(file_path, 'r') as file:
        lines = file.readlines()
        assert len(lines) == 2
        assert lines[0].strip() == "000000100000000valid"
        assert lines[1].strip() == "000000200000000valid"
