import pandas as pd
import requests

query = {
    "query": """
        query problemsetQuestionList(
            $categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput
        ) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters
            ) {
                total: totalNum
                questions: data {
                    Acceptance: acRate
                    Difficulty: difficulty
                    Index: questionFrontendId
                    Premium: isPaidOnly
                    Title: title
                    TitleSlug: titleSlug
                    Tags: topicTags {slug}
                }
            }
        }
    """,
    "variables": {"categorySlug": "", "skip": 0, "limit": 1e5, "filters": {}},
}

response = requests.post("https://leetcode.com/graphql", json=query)
response = response.json()["data"]["problemsetQuestionList"]["questions"]
questions = pd.json_normalize(response)[[
    "Index", "Title", "TitleSlug", "Difficulty", "Acceptance", "Premium", "Tags",
]]
print("Done")
