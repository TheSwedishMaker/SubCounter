import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import requests
from datetime import datetime

# Set up the main application window
root = tk.Tk()
root.title("YouTube Subscriber Counter")
root.geometry("1280x400")  # Set to match your display resolution
root.configure(bg='black')
root.attributes('-fullscreen', True)  # Set the window to full screen
root.overrideredirect(True)  # Removes the window decorations (title bar, close button, etc.)

# Function to handle exiting full-screen mode
def exit_fullscreen(event=None):
    print("Exiting full-screen mode...")
    root.attributes('-fullscreen', False)
    root.overrideredirect(False)  # Restore window decorations

# Function to handle closing the app
def exit_app(event=None):
    print("Closing application...")
    root.quit()  # Quit the mainloop
    root.destroy()  # Completely close the application

# Bindings for exiting full-screen mode
root.bind("<Escape>", exit_fullscreen)  # Bind the Escape key to exit full screen
root.bind("<Control-q>", exit_app)  # Binds Ctrl+Q to exit the application

# Create a canvas and expand it to cover the entire window fully
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Create an invisible exit button in the top-left corner
exit_button = tk.Button(root, command=exit_app, bg='black', bd=0, highlightthickness=0)
exit_button.place(x=0, y=0, width=60, height=60)  # Adjust size and position to suit

# Global variables for display
subscriber_count = 0
current_screen = "main"

# Function to fetch channel statistics
def fetch_youtube_stats():
    global subscriber_count
    channel_id = 'YOUR CHANNEL ID HERE'
    api_key = 'YOUR API KEY HERE'
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            stats = data['items'][0]['statistics']
            subscriber_count = stats.get('subscriberCount', 0)
    else:
        print("Failed to fetch data:", response.status_code)

# Function to update the small clock on the main screen
def update_small_clock():
    if current_screen == "main":
        current_time = datetime.now().strftime("%H:%M")  # Format time as HH:MM
        canvas.delete("clock")  # Clear the previous time display
        clock_spacing = 150  # Adjust this to match the spacing of MON from the left
        # Adjust the font size as needed
        canvas.create_text(1280 - clock_spacing, 350, text=current_time, font=("LED Counter 7", 30), fill="white", tags="clock")
    root.after(1000, update_small_clock)  # Update the clock every second

# Function to display weekdays
def display_weekdays():
    weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    x_start = 120
    y_position = 350
    spacing = 120

    # Adjust the font size as needed
    current_day_index = datetime.now().weekday()
    for i, day in enumerate(weekdays):
        color = "white" if i == current_day_index else "grey"
        canvas.create_text(x_start + i * spacing, y_position, text=day, font=("LED Counter 7", 30), fill=color, tags="weekdays")

# Function to display the channel name at the top
def display_channel_name():
    channel_name = "YOUR CHANNEL NAME HERE"
    canvas.delete("channel_name")
    # Adjust the font size for the channel name here
    canvas.create_text(640, 50, text=' '.join(channel_name), font=("Kiona", 35), fill="lightgreen", tags="channel_name")

# Function to display the main subscriber screen
def display_main_screen():
    global current_screen
    current_screen = "main"
    canvas.delete("all")
    fetch_youtube_stats()

    # Display the channel name at the top
    display_channel_name()

    # Display YouTube logo with black background and adjusted position
    logo = Image.open("youtube_logo.png")
    logo = ImageOps.expand(logo, border=0, fill='black')
    logo = logo.resize((300, 200), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)

    # Adjust the position of the logo for better spacing
    canvas.create_image(200, 200, image=logo_img, anchor="center")  # Moved to the right for better spacing
    canvas.logo_img = logo_img

    # Display subscriber count with adjusted vertical positioning for better centering
    canvas.create_text(800, 220, text=f"{subscriber_count}", font=("LED Counter 7", 170), fill="white")  # Adjusted y-coordinate slightly for centering

    # Display weekdays
    display_weekdays()

    # Display the small clock in the bottom right corner
    update_small_clock()

    # Bind touch event to show the clock screen
    canvas.bind("<Button-1>", lambda event: display_clock_screen())
    root.after(600000, display_main_screen)  # Refresh every 10 minutes

# Function to display a large centered clock when touched
def display_clock_screen(event=None):
    global current_screen
    current_screen = "clock"
    canvas.delete("all")
    canvas.unbind("<Button-1>")

    # Display a large clock centered on the screen
    # Adjust the vertical positioning slightly for better centering
    current_time = datetime.now().strftime("%H:%M")
    canvas.create_text(640, 220, text=current_time, font=("LED Counter 7", 180), fill="white", tags="large_clock")  # Adjusted y-coordinate slightly for centering

    # Update the clock every second while on this screen
    def update_large_clock():
        if current_screen == "clock":
            current_time = datetime.now().strftime("%H:%M")
            canvas.itemconfig("large_clock", text=current_time)
            root.after(1000, update_large_clock)

    update_large_clock()

    # Bind touch event to return to the main screen
    canvas.bind("<Button-1>", lambda event: display_main_screen())

# Start with the main screen and clock
display_main_screen()

# Run the main loop
root.mainloop()
