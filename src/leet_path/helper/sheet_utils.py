import pandas as pd

MARKDOWN = 'markdown'
EXCEL = 'excel'


def _get_hyperlink(title: str, link: str, style: str | None) -> str:
    if style == MARKDOWN:
        return f'[{title}]({link})'
    elif style == EXCEL:
        return f'=HYPERLINK("{link}", "{title}")'
    return title


def overload_title(df: pd.DataFrame, title_col: str, link_col: str, style: str | None) -> pd.DataFrame:
    df = df.copy(deep=True)
    df[title_col] = [_get_hyperlink(title, link, style) for title, link in zip(df[title_col], df[link_col])]
    return df.drop(columns=[link_col])
