from datetime import datetime

def display_activity(events, username, start_date=None, end_date=None):
    print(f"\n🔹 Recent GitHub Activity of {username}:\n")

    for event in events:
        event_date = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        # Filter by date range
        if start_date and event_date < start_date:
            continue
        if end_date and event_date > end_date:
            continue

        event_type = event["type"]
        repo_name = event["repo"]["name"]

        print(f"📌 {event_type} in {repo_name} on {event_date.strftime('%Y-%m-%d %H:%M:%S')}")

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None
