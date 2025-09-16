from src.common import file_utils
from test import testing_utils


@testing_utils.setup_test_files({'xyz.xlsx': testing_utils.generate_random_df})
def test_read_and_write():
    file_utils.read_sheet('xyz.xlsx')
    assert True
