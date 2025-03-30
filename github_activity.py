import argparse
import json
import http.client
from utils import display_activity, save_to_csv  # Import helper functions

# Function to fetch GitHub activity
def fetch_github_activity(username, event_filter=None, max_pages=1):
    all_events = []
    page = 1

    while page <= max_pages:
        try:
            conn = http.client.HTTPSConnection("api.github.com")
            headers = {"User-Agent": "GitHub-Activity-CLI"}  # Required to avoid 403 errors
            conn.request("GET", f"/users/{username}/events?page={page}", headers=headers)
            
            response = conn.getresponse()

            if response.status == 404:
                print(f"❌ Error: GitHub user '{username}' not found.")
                return
            elif response.status != 200:
                print(f"❌ Error: API request failed (HTTP {response.status}).")
                return

            events = json.loads(response.read().decode())

            if not events:
                break  # No more events to fetch

            all_events.extend(events)
            page += 1

        except Exception as e:
            print("❌ Error:", e)
            return

    # Filter events if needed
    if event_filter:
        all_events = [event for event in all_events if event["type"] == event_filter]

    return all_events

# Main function
def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub user activity from the command line.")
    parser.add_argument("username", help="GitHub username to fetch activity for")
    parser.add_argument("--filter", help="Filter by event type (e.g., PushEvent, IssuesEvent)")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to fetch (default: 1)")

    args = parser.parse_args()
    events = fetch_github_activity(args.username, args.filter, args.pages)

    if events:
        display_activity(events, args.username)  # Show output
        save_to_csv(events, args.username)  # Save to CSV

if __name__ == "__main__":
    main()
