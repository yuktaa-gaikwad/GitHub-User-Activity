import json
import http.client
import argparse
import os
import pickle
import time
from datetime import datetime, timedelta
from utils import display_activity, parse_date

CACHE_FILE = "github_cache.pkl"
CACHE_EXPIRY = timedelta(minutes=30)  # Cache for 30 minutes

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as file:
            cache_data = pickle.load(file)
            if datetime.now() - cache_data["timestamp"] < CACHE_EXPIRY:
                return cache_data["events"]
    return None

def save_cache(events):
    with open(CACHE_FILE, "wb") as file:
        pickle.dump({"events": events, "timestamp": datetime.now()}, file)

def fetch_github_activity(username, event_filter=None, max_pages=1):
    cached_data = load_cache()
    if cached_data:
        print("📁 Loading cached data...")
        return cached_data

    conn = http.client.HTTPSConnection("api.github.com")
    headers = {"User-Agent": "GitHub-Activity-CLI"}
    conn.request("GET", f"/users/{username}/events", headers=headers)

    response = conn.getresponse()
    if response.status != 200:
        print(f"❌ Error: Failed to fetch GitHub activity ({response.status})")
        return []

    all_events = json.loads(response.read().decode())

    save_cache(all_events)  # Save to cache before returning
    return all_events

def fetch_repositories(username):
    conn = http.client.HTTPSConnection("api.github.com")
    headers = {"User-Agent": "GitHub-Activity-CLI"}
    conn.request("GET", f"/users/{username}/repos", headers=headers)

    response = conn.getresponse()
    if response.status != 200:
        print("❌ Failed to fetch repositories.")
        return []

    return json.loads(response.read().decode())

def display_repositories(username):
    repos = fetch_repositories(username)
    print(f"\n📂 {username}'s Repositories:")

    for repo in repos:
        print(f"📁 {repo['name']} - ⭐ {repo['stargazers_count']} stars")

def main():
    parser = argparse.ArgumentParser(description="GitHub Activity CLI")
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--repos", action="store_true", help="Fetch user repositories")
    parser.add_argument("--live", action="store_true", help="Enable live updates")

    args = parser.parse_args()

    if args.repos:
        display_repositories(args.username)
        return

    start_date = parse_date(args.start)
    end_date = parse_date(args.end)

    while True:
        events = fetch_github_activity(args.username)
        display_activity(events, args.username, start_date, end_date)

        if not args.live:
            break

        print("\n🔄 Refreshing in 60 seconds...\n")
        time.sleep(60)  # Refresh every 60 seconds

if __name__ == "__main__":
    main()
