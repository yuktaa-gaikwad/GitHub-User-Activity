import tkinter as tk
from github_activity import fetch_github_activity

# Function to fetch and display activity
def show_activity():
    username = entry.get().strip()
    if not username:
        text_box.config(state=tk.NORMAL)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "⚠️ Please enter a GitHub username.\n")
        text_box.config(state=tk.DISABLED)
        return

    events = fetch_github_activity(username)

    text_box.config(state=tk.NORMAL)
    text_box.delete(1.0, tk.END)

    if not events:
        text_box.insert(tk.END, "⚠️ No activity found or invalid username.\n")
    else:
        text_box.insert(tk.END, f"✨ Recent Activity for {username}:\n\n")
        for event in events[:5]:  # Show last 5 events
            text_box.insert(tk.END, f"📌 {event['type']} in {event['repo']['name']}\n")

    text_box.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("GitHub Activity Viewer")
root.geometry("520x460")
root.configure(bg="#CDB4DB")  # Soft Lavender Background

# Apply new font
font_main = ("Poppins", 12, "bold")
font_title = ("Poppins", 16, "bold")

# Title Label
title_label = tk.Label(root, text="🌸 GitHub Activity Viewer 🌙", font=font_title, fg="#4A4E69", bg="#CDB4DB")
title_label.pack(pady=10)

# Entry for Username
entry_frame = tk.Frame(root, bg="#CDB4DB")
entry_frame.pack(pady=5)

entry_label = tk.Label(entry_frame, text="Enter GitHub Username:", font=font_main, fg="#4A4E69", bg="#CDB4DB")
entry_label.pack()

entry = tk.Entry(entry_frame, font=("Poppins", 12), fg="#222", bg="#FFC8DD", width=30, bd=3, relief="ridge")
entry.pack(pady=5)

# Fetch Button
fetch_button = tk.Button(root, text="💫 Fetch Activity 💫", command=show_activity, font=font_main, fg="white", bg="#FFAFCC", relief="raised", bd=3, activebackground="#FF70A6", activeforeground="white", padx=10, pady=5)
fetch_button.pack(pady=10)

# Text Box for Displaying Activity
text_box = tk.Text(root, height=10, width=55, font=("Poppins", 11), fg="#4A4E69", bg="#FFC8DD", wrap="word", borderwidth=3, relief="ridge")
text_box.pack(pady=10)
text_box.config(state=tk.DISABLED)

# Run the GUI
root.mainloop()
