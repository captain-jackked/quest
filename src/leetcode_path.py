import typing

import pandas as pd
import requests

INDEX = 'Index'
TITLE = 'Title'
LINK = 'Link'
PREMIUM = 'Premium'

TAGS = 'Tags'

DIFFICULTY = 'Difficulty'
EASY = 'Easy'
MEDIUM = 'Medium'
HARD = 'Hard'

ACCEPTANCE = 'Acceptance'
ACC_ROLL_AVG = 'Acc Avg (Rolling)'
ACC_DE_SKEWED = 'Acc (De-skewed)'
ACC_NORMALIZED = 'Acc (Normalized)'

SCORE = 'Score'

BASE_SCORES = {EASY: 1, MEDIUM: 2, HARD: 4}
AVG_WINDOW = 500
DECAY_RATE = 2
DECAY_FLOOR = 0.5


def _get_all_questions() -> pd.DataFrame:
    def _flatten_dict_vals_list(data: list[dict]) -> list:
        return list(sorted(set(y for x in data for y in x.values())))

    query = {
        'query': """
            query($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
                    questions: data {
                        Index: questionFrontendId
                        Title: title
                        Link: titleSlug
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
    response = requests.post('https://leetcode.com/graphql', json=query)

    df = pd.json_normalize(response.json()['data']['questionList']['questions'])
    df['Index'] = pd.to_numeric(df['Index'])
    df = df.sort_values(by=['Index']).set_index('Index')

    # TODO: create link out of title slug

    df['Tags'] = df['Tags'].apply(lambda x: _flatten_dict_vals_list(x))
    # TODO: refine tags into problem categories

    return df


def _get_rolling_acceptance(df: pd.DataFrame, window) -> pd.Series:
    return df.rolling(window=window, min_periods=0, center=True)[ACCEPTANCE].mean()


def _get_de_skewed_acceptance(df: pd.DataFrame) -> pd.Series:
    return df[ACCEPTANCE] - df[ACC_ROLL_AVG]


def _get_normalized_acceptance(df: pd.DataFrame, difficulties: typing.Iterable) -> pd.Series:
    ans = []
    for diff in difficulties:
        df_diff = df[df[DIFFICULTY] == diff]
        avg_acc, std_acc = df_diff[ACC_DE_SKEWED].mean(), df_diff[ACC_DE_SKEWED].std()
        ans.append(df_diff[ACC_DE_SKEWED].apply(lambda x: (x - avg_acc) / std_acc))
    return pd.concat(ans).squeeze()


def _get_score(df: pd.DataFrame, base_scores: dict, decay_rate: float, decay_floor: float) -> pd.Series:
    def _acc_to_score(normalized_acc: float, b_score: float, decay_r: float, decay_f: float) -> float:
        decay_factor = decay_f + (1 - decay_f) * decay_r ** (-abs(normalized_acc))
        if normalized_acc < 0:  # is_tougher
            decay_factor = 1 / decay_factor
        return b_score * decay_factor

    ans = []
    for diff, score in base_scores.items():
        df_diff = df[df[DIFFICULTY] == diff]
        ans.append(df_diff[ACC_NORMALIZED].apply(lambda x: _acc_to_score(x, score, decay_rate, decay_floor)))
    return pd.concat(ans).squeeze()


def get_questions() -> pd.DataFrame:
    questions = _get_all_questions()
    questions[ACC_ROLL_AVG] = _get_rolling_acceptance(questions, AVG_WINDOW)
    questions[ACC_DE_SKEWED] = _get_de_skewed_acceptance(questions)
    questions[ACC_NORMALIZED] = _get_normalized_acceptance(questions, BASE_SCORES.keys())
    questions[SCORE] = _get_score(questions, BASE_SCORES, DECAY_RATE, DECAY_FLOOR)
    return questions


if __name__ == '__main__':
    print(get_questions())
