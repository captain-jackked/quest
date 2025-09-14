import os

import pandas as pd
from pypdf import PdfReader

from src.data.filer import file_utils

PDF = '.pdf'
SPLIT_THRESHOLD = 50

CONTEXT = 'Context'
TITLE = 'Title'
PAGES = 'Pages'
CHAPTERS = 'Chapters'


def _get_count_validation_msg(files) -> str | None:
    lowest, highest = (f(files.values()) for f in (min, max))
    if len(files) == 1:
        return 'No chapters found'
    elif lowest > SPLIT_THRESHOLD:
        return 'Split full directory'
    # elif lowest * 10 < highest:
    #     return 'Rethink parity'
    return None


def _get_page_counts(tags, pdf_files: list[str], curr_dir: str):
    page_counts = {f: len(PdfReader(os.path.join(curr_dir, f)).pages) for f in pdf_files}
    page_note = _get_count_validation_msg(page_counts)
    if page_note:
        print(f'{page_note} | {tags} | {page_counts}')
    return page_counts


def _get_tags_and_files(trimmed_dir, child_dirs, files):
    pdf_files = [x for x in files if PDF in x]
    if len(pdf_files) * len(child_dirs) != 0:
        print(f'Skipping {trimmed_dir}. Unprocessed folder')
        return [], []
    tags = trimmed_dir.replace('\\', '|').replace('/', '|').split('|')
    return tags, pdf_files


def get_books_report(start_dir: str):
    res = []
    for curr_dir, child_dirs, files in os.walk(start_dir):
        trimmed_dir = curr_dir.replace(start_dir, '')
        tags, pdf_files = _get_tags_and_files(trimmed_dir, child_dirs, files)
        if len(pdf_files) > 0:
            page_counts = _get_page_counts(tags, pdf_files, curr_dir)
            res.append({
                CONTEXT: ' | '.join(tags[0:-1]),
                TITLE: tags[-1],
                CHAPTERS: len(page_counts.values()),
                PAGES: sum(page_counts.values()),
            })
    return pd.DataFrame(res)


if __name__ == '__main__':
    df = get_books_report('D:/Collection/Books/.Casual/')
    file_utils.write_sheet('read_path-casual.xlsx', df)
    print()
