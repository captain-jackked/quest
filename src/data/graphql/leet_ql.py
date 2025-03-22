import pandas as pd
import requests

from src.leet_path.helper import consts

LEETCODE = 'https://leetcode.com'


def _get_graphql_query() -> dict:
    return {
        'query': """
            query($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
                    questions: data {
                        Index: questionFrontendId
                        Title: title
                        TitleSlug: titleSlug
                        Premium: isPaidOnly
                        Tags: topicTags {slug}
                        Difficulty: difficulty
                        Acceptance: acRate
                    }
                }
            }
        """,
        'variables': {'categorySlug': '', 'skip': 0, 'limit': 1e5, 'filters': {}},
    }


def _get_questions_as_df() -> pd.DataFrame:
    response = requests.post(f'{LEETCODE}/graphql', json=_get_graphql_query())
    df = pd.json_normalize(response.json()['data']['questionList']['questions'])
    df[consts.INDEX] = pd.to_numeric(df[consts.INDEX])
    df[consts.ACCEPTANCE] /= 100
    return df.sort_values(by=[consts.INDEX]).set_index(consts.INDEX)


def _get_hyperlink(title: str, slug: str) -> str:
    return f'=HYPERLINK("{LEETCODE}/problems/{slug}", "{title}")'


def _overload_title(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy(deep=True)
    df[consts.TITLE] = [_get_hyperlink(title, slug) for title, slug in zip(
        df[consts.TITLE], df[consts.TITLE_SLUG]
    )]
    return df.drop(columns=[consts.TITLE_SLUG])


def _flatten_dict_vals_list(tags_data: list[dict]) -> str:
    tags = set(y for x in tags_data for y in x.values())
    if not tags:
        return 'NA'
    for indicator in ['shell', 'concurrency', 'database']:
        if indicator in tags:
            return indicator
    return ''


def _refine_tags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy(deep=True)
    df[consts.TAGS] = [_flatten_dict_vals_list(x) for x in df[consts.TAGS]]
    return df


def get_all_questions() -> pd.DataFrame:
    return _refine_tags(_overload_title(_get_questions_as_df()))
