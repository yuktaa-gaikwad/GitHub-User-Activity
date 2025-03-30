import csv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to display activity in the terminal
def display_activity(events, username):
    print(f"\n🔹 Recent GitHub Activity of {username}:\n")
    
    for event in events[:5]:  # Show only latest 5 events
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        if event_type == "PushEvent":
            commit_count = len(event["payload"].get("commits", []))
            print(Fore.GREEN + f"📌 Pushed {commit_count} commits to {repo_name}")

        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(Fore.YELLOW + f"🐛 {action.capitalize()} an issue in {repo_name}")

        elif event_type == "WatchEvent":
            print(Fore.CYAN + f"⭐ Starred {repo_name}")

        elif event_type == "ForkEvent":
            print(Fore.BLUE + f"🍴 Forked {repo_name}")

        else:
            print(Fore.MAGENTA + f"🔹 {event_type} in {repo_name}")

# Function to save activity to a CSV file
def save_to_csv(events, username):
    filename = f"{username}_activity.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Event Type", "Repository", "Details"])

        for event in events:
            event_type = event["type"]
            repo_name = event["repo"]["name"]
            details = ""

            if event_type == "PushEvent":
                commit_count = len(event["payload"].get("commits", []))
                details = f"Pushed {commit_count} commits"
            elif event_type == "IssuesEvent":
                action = event["payload"]["action"]
                details = f"Issue {action}"
            elif event_type == "WatchEvent":
                details = "Starred"
            elif event_type == "ForkEvent":
                details = "Forked"
            else:
                details = "Performed action"

            writer.writerow([event_type, repo_name, details])

    print(f"\n📁 Activity saved to {filename}")
