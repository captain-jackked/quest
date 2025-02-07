import pandas as pd

from src.data.filer import file_utils


def test_read_and_write():
    sample_df, file_name = pd.DataFrame([[1, 2], [3, 4]], index=['a', 'b'], columns=['c', 'd']), 'xyz.xlsx'
    file_utils.write_sheet(sample_df, file_name)
    read_df = file_utils.read_sheet(file_name)
    assert sample_df.equals(read_df)
