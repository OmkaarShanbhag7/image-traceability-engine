from serpapi import GoogleSearch
import requests

SERPAPI_KEY = "YOUR_SERPAPI_KEY"
IMGBB_KEY = "YOUR_IMGBB_KEY"

def upload_image(image_path):
    with open(image_path, "rb") as file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_KEY},
            files={"image": file}
        )
    return response.json()["data"]["url"]

def search_online(image_path):
    image_url = upload_image(image_path)

    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    matches = []

    if "image_results" in results:
        for item in results["image_results"][:5]:
            matches.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "thumbnail": item.get("thumbnail")
            })

    return matches