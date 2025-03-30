import tkinter as tk
from tkinter import scrolledtext
import requests
from datetime import datetime

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url, headers={"User-Agent": "GitHub-Activity-GUI"})
        response.raise_for_status()
        events = response.json()
        return events if events else []
    except requests.exceptions.RequestException as e:
        return [f"Error: {e}"]

def display_activity():
    username = username_entry.get().strip()
    if not username:
        activity_box.delete(1.0, tk.END)
        activity_box.insert(tk.END, "⚠️ Please enter a GitHub username.")
        return
    
    activity_box.delete(1.0, tk.END)
    activity_box.insert(tk.END, f"📌 Recent Activity for {username}:\n\n")
    events = fetch_github_activity(username)
    
    for event in events[:10]:  # Show only last 10 events for readability
        if isinstance(event, str):  # If error message
            activity_box.insert(tk.END, event + "\n")
            return
        
        event_type = event.get("type", "Unknown Event")
        repo = event.get("repo", {}).get("name", "Unknown Repo")
        event_time = event.get("created_at", "")
        
        if event_time:
            try:
                formatted_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_time = "Invalid Time Format"
        else:
            formatted_time = "Unknown Time"
        
        activity_box.insert(tk.END, f"📍 {event_type} in {repo} on {formatted_time}\n")

# GUI Setup
root = tk.Tk()
root.title("GitHub Activity Viewer")
root.geometry("600x500")
root.configure(bg="#D8BFD8")  # Lavender background

# Title
title_label = tk.Label(root, text="💜 GitHub Activity Viewer 💜", font=("Poppins", 16, "bold"), fg="#4A4E69", bg="#D8BFD8")
title_label.pack(pady=10)

# Username Input
username_label = tk.Label(root, text="Enter GitHub Username:", font=("Poppins", 12, "bold"), fg="#6A5ACD", bg="#D8BFD8")
username_label.pack()
username_entry = tk.Entry(root, font=("Poppins", 12), fg="#333", bg="#FFF0F5", width=30, relief="flat")  # Light pink input
username_entry.pack(pady=5)

# Fetch Button
fetch_button = tk.Button(root, text="✨ Fetch Activity ✨", command=display_activity, font=("Poppins", 12, "bold"), 
                         fg="#FFF", bg="#FF69B4", activebackground="#FF1493", activeforeground="#FFF", relief="flat", padx=10, pady=5)
fetch_button.pack(pady=10)

# Activity Output Box
activity_box = scrolledtext.ScrolledText(root, height=12, width=60, font=("Poppins", 11), fg="#4A4E69", bg="#FFC8DD", wrap="word", borderwidth=2, relief="flat")
activity_box.pack(pady=10)

root.mainloop()