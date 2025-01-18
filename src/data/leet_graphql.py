import pandas as pd
import requests


def get_all_questions_raw() -> pd.DataFrame:
    def _flatten_dict_vals_list(data: list[dict]) -> list:
        return list(sorted(set(y for x in data for y in x.values())))

    graphql_query = {
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
    response = requests.post('https://leetcode.com/graphql', json=graphql_query)

    df = pd.json_normalize(response.json()['data']['questionList']['questions'])
    df['Index'] = pd.to_numeric(df['Index'])
    df = df.sort_values(by=['Index']).set_index('Index')

    # TODO: create link out of title slug

    df['Tags'] = df['Tags'].apply(lambda x: _flatten_dict_vals_list(x))
    # TODO: refine tags into problem categories

    return df
