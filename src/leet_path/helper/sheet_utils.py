import pandas as pd

from src.leet_path.helper import consts

MARKDOWN = 'markdown'
EXCEL = 'excel'


def _get_hyperlink(title: str, link: str, style: str | None) -> str:
    if style == MARKDOWN:
        return f'[{title}]({link})'
    elif style == EXCEL:
        return f'=HYPERLINK("{link}", "{title}")'
    return title


def _overload_title(df: pd.DataFrame, title_col: str, link_col: str, style: str | None) -> pd.DataFrame:
    df[title_col] = [_get_hyperlink(title, link, style) for title, link in zip(df[title_col], df[link_col])]
    return df.drop(columns=[link_col])


def beautify(df: pd.DataFrame, style: str) -> pd.DataFrame:
    df = df.copy(deep=True)
    df = _overload_title(df, consts.TITLE, consts.LINK, style=style)
    return df[[x for x in consts.OUTPUT_COLS if x in df.columns]]


def print_progress_summary(df: pd.DataFrame):
    def _get_count(raw: pd.DataFrame, flt):
        return len(raw[flt])

    def _get_scores(raw: pd.DataFrame, flt):
        return sum(raw[flt][consts.SCORE])

    solved_flt, premium_flt = df[consts.SOLVED], df[consts.PREMIUM]
    for difficulty in [consts.EASY, consts.MEDIUM, consts.HARD]:
        diff_flt = df[consts.DIFFICULTY] == difficulty
        print('{:>7}: {:>7}/{:<4} (Solved/Total) | Unsolved: {:>4}/{:<4} (Non-premium/Premium)'.format(
            difficulty,
            _get_count(df, diff_flt & solved_flt), _get_count(df, diff_flt),
            _get_count(df, diff_flt & ~solved_flt & ~premium_flt), _get_count(df, diff_flt & ~solved_flt & premium_flt)
        ))
    print('{:>7}: {:>7.1f}/{:.0f} (Solved/Total)'.format(
        'Score', _get_scores(df, solved_flt), _get_scores(df, [True] * len(df.index))
    ))
    print('-' * 80)
