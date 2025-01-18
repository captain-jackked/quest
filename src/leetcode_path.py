import pandas as pd
import requests


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
                        TitleSlug: titleSlug
                        Difficulty: difficulty
                        Acceptance: acRate
                        Premium: isPaidOnly
                        Tags: topicTags {slug}
                    }
                }
            }
        """,
        'variables': {'categorySlug': '', 'skip': 0, 'limit': 1e5, 'filters': {}},
    }

    result = requests.post('https://leetcode.com/graphql', json=query)
    result = pd.json_normalize(result.json()['data']['questionList']['questions'])
    result['Tags'] = result['Tags'].apply(lambda x: _flatten_dict_vals_list(x))
    return result


if __name__ == '__main__':
    questions = _get_all_questions()
    print(questions)
