# github_api.py
import urllib.request
import urllib.error
import json
import os
from typing import Tuple

def fetch_github_stats(username: str) -> Tuple[str, str, str]:
    """Fetches follower count, repository count, and total stars across all repos."""
    print(f"Fetching GitHub stats for {username}...")
    headers = {"User-Agent": "Mozilla/5.0 (Python-urllib)"}
    
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    else:
        print("Warning: GITHUB_TOKEN not found. You may hit API rate limits.")

    try:
        user_req = urllib.request.Request(f"https://api.github.com/users/{username}", headers=headers)
        with urllib.request.urlopen(user_req) as response:
            user_data = json.loads(response.read())
            
        followers = str(user_data.get("followers", 0))
        repos = str(user_data.get("public_repos", 0))

        stars = 0
        page = 1
        while True:
            repo_req = urllib.request.Request(
                f"https://api.github.com/users/{username}/repos?per_page=100&page={page}", 
                headers=headers
            )
            with urllib.request.urlopen(repo_req) as response:
                repos_data = json.loads(response.read())
            
            if not repos_data:
                break
                
            stars += sum(repo.get("stargazers_count", 0) for repo in repos_data)
            page += 1
            
        return repos, str(stars), followers

    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching stats: {e.code} - {e.reason}")
        return "ERR", "ERR", "ERR"
    except Exception as e:
        print(f"Unexpected error fetching stats: {e}")
        return "ERR", "ERR", "ERR"