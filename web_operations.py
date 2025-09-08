from serpapi import GoogleSearch
import requests
import os

from dotenv import load_dotenv
load_dotenv()
SC_API_KEY = os.getenv("SC_API_KEY")



def google_search_func(query):
    params = {
    "api_key": "adfddf622694617e348f915e7cdd545f4076aa781148dff3d766123dc161f47a",
    "engine": "google",
    "q": query,
    "google_domain": "google.com",
    "gl": "in",
    "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    extracted_data = {
        "knowledge" : results.get("knowledge_graph", {}),
        "organic" : results.get("organic_results", [])
    }

    print(extracted_data)
    return extracted_data


def bing_search_func(query):
    params = {
    "api_key": "adfddf622694617e348f915e7cdd545f4076aa781148dff3d766123dc161f47a",
    "engine": "bing",
    "q": query,
    "google_domain": "google.com",
    "hl": "en",
    "gl": "us",
    "cc": "IN"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    extracted_data = {
        "organic" : results.get("organic_results", [])
    }

    print(extracted_data)
    return extracted_data


def get_reddit_posts(query):
    
    url = f"https://api.scrapecreators.com/v1/reddit/search?query={query}&sort=relevance&trim=True"
    headers = {
        "x-api-key": SC_API_KEY,
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    parsed_data = []
    for post in data["posts"]:
        parsed_post = {
            "title": post["title"],
            "url": post["url"]
        }
        parsed_data.append(parsed_post)

    parsed_data = parsed_data[:5]

    return {"parsed_posts": parsed_data, "total_found":len(data["posts"])}


def get_reddit_comments(post_urls):

    if not post_urls:
        return None

    
    headers = {
        "x-api-key": "ahkwZqktvnWl73uadPlcJAiTKTs2"
    }
    parsed_comments = []

    for url in post_urls:
        url = f"https://api.scrapecreators.com/v1/reddit/post/comments?url={url}&trim=True"
        response = requests.get(url, headers=headers)
        data = response.json()

        

        post_title = data['post']['title']
        for comment in data["comments"]:
            parsed_comment = {
                "comment_id" : comment["id"],
                "content": comment["body"],
                "date": comment["created_at_iso"],
                "parent_comment_id": comment["parent_id"],
                "post_title" : post_title
            }
            parsed_comments.append(parsed_comment)
        
    return {"comments":parsed_comments, "total_retrieved":len(parsed_comments)}



if __name__ == "__main__":
    #get_reddit_posts("Nvidia")
    get_reddit_comments("https://www.reddit.com/r/stocks/comments/1ibkcex/nvidia_sheds_almost_600_billion_in_market_cap/")