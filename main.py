import tkinter as tk
import sys
import os
import pygame

import navigation
from PIL import Image, ImageTk
from save_manager import load_data
from feedback_sender import send_feedback, flush_pending

pygame.mixer.init()

# Send any feedback that was saved while the player was offline
flush_pending()
# ============================================================
# RESOURCE PATH
# ============================================================

def resource_path(relative_path):

    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS

    else:
        base_path = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        base_path,
        relative_path
    )


# ============================================================
# PLAYER DATA
# ============================================================

player_data = load_data()
detective_money = player_data["detective_money"]
case_001_solved = player_data["case_001_solved"]

music_on = True
click_sound = pygame.mixer.Sound(resource_path("sounds/clicking_sound.mp3"))
click_sound.set_volume(0.5)


# ============================================================
# OPEN ANOTHER PROGRAM
# ============================================================
def play_main_music():

    if not pygame.mixer.music.get_busy():

        pygame.mixer.music.load(
            resource_path("sounds/store_music.mp3")
        )

        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

def stop_main_music():
    pygame.mixer.music.stop()

def play_click_sound():
    click_sound.play()


def toggle_music():

    global music_on

    if music_on:

        pygame.mixer.music.pause()
        music_on = False

    else:

        pygame.mixer.music.unpause()
        music_on = True


def open_screen(screen_name):

    stop_main_music()

    navigation.go_to(root, screen_name)


# ============================================================
# OPEN CASES / STORE
# ============================================================

def open_case_001():

    play_click_sound()

    root.after(
        250,
        lambda: open_screen("case_001"))


def open_case_002():

    play_click_sound()

    root.after(
        250,
        lambda: open_screen("case_002"))


def open_store():

    play_click_sound()

    root.after(
        250,
        lambda: open_screen("store"))




# ============================================================
# FEEDBACK
# ============================================================

# ============================================================
# FEEDBACK
# ============================================================

def open_feedback():

    play_click_sound()

    feedback_window = tk.Toplevel(root)

    feedback_window.title("Murdle - Feedback")
    feedback_window.geometry("500x600")
    feedback_window.configure(bg="#D8C49C")
    feedback_window.resizable(False, False)


    # ----------------------------
    # TITLE
    # ----------------------------

    title = tk.Label(
        feedback_window,
        text="CASE FEEDBACK",
        font=("Georgia", 24, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )

    title.pack(
        pady=(25, 5)
    )


    # ----------------------------
    # SUBTITLE
    # ----------------------------

    subtitle = tk.Label(
        feedback_window,
        text="Help improve future investigations.",
        font=("Georgia", 12),
        bg="#D8C49C",
        fg="#2B2118"
    )

    subtitle.pack(
        pady=(0, 15)
    )


    # ----------------------------
    # RATING
    # ----------------------------

    rating_label = tk.Label(
        feedback_window,
        text="How was your investigation?",
        font=("Georgia", 14, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )

    rating_label.pack(
        pady=5
    )


    rating = tk.IntVar(
        value=0
    )


    rating_frame = tk.Frame(
        feedback_window,
        bg="#D8C49C"
    )

    rating_frame.pack(
        pady=10
    )


    for number in range(1, 6):

        button = tk.Radiobutton(
            rating_frame,
            text=f"{number} ★",
            variable=rating,
            value=number,
            font=("Georgia", 11),
            bg="#D8C49C"
        )

        button.pack(
            side="left",
            padx=5
        )


    # ----------------------------
    # COMMENT
    # ----------------------------

    comment_label = tk.Label(
        feedback_window,
        text="What would you improve?",
        font=("Georgia", 14, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )

    comment_label.pack(
        pady=(15, 5)
    )


    comment_box = tk.Text(
        feedback_window,
        width=45,
        height=7,
        font=("Georgia", 11),
        wrap="word"
    )

    comment_box.pack(
        pady=10
    )


    # ----------------------------
    # STATUS LABEL
    # ----------------------------

    status_label = tk.Label(
        feedback_window,
        text="",
        font=("Georgia", 11),
        bg="#D8C49C",
        fg="#2B2118"
    )


    # ----------------------------
    # SUBMIT FUNCTION
    # ----------------------------

    def submit_feedback():

        selected_rating = rating.get()

        comment = comment_box.get(
            "1.0",
            "end-1c"
        )

        if selected_rating == 0:

            status_label.config(
                text="Please select a rating."
            )

            return


        # Send the feedback to your Google Form
        submit_button.config(state="disabled")

        status_label.config(
            text="Sending..."
        )

        result = send_feedback(
            selected_rating,
            comment
        )


        # Check every 0.2 seconds whether sending has finished
        def check_result():

            if result.empty():
                feedback_window.after(200, check_result)
                return

            sent = result.get()

            if sent:
                status_label.config(
                    text="Thank you, Detective! Feedback submitted."
                )
            else:
                status_label.config(
                    text="No internet right now. Saved, will send next time."
                )

            submit_button.config(state="normal")


        check_result()


        comment_box.delete(
            "1.0",
            "end"
        )


        rating.set(0)


    # ----------------------------
    # SUBMIT BUTTON
    # ----------------------------

    submit_button = tk.Button(
        feedback_window,
        text="SUBMIT FEEDBACK",
        font=("Georgia", 12, "bold"),
        command=submit_feedback
    )

    submit_button.pack(
        pady=15
    )


    status_label.pack(
        pady=5
    )






# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Murdle")

root.geometry("1200x900")



# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    root,
    width=1200,
    height=900,
    highlightthickness=0
)

canvas.pack()


# ============================================================
# BACKGROUND IMAGE
# ============================================================

main_image = Image.open(
    resource_path(
        "assets/murdle_main_menu.png"
    )
)

main_image = main_image.resize(
    (1200, 800)
)

main_background = ImageTk.PhotoImage(
    main_image
)

canvas.create_image(
    0,
    0,
    image=main_background,
    anchor="nw"
)

canvas.background = main_background


# ============================================================
# CLICKABLE AREAS
# ============================================================

case_001_area = canvas.create_rectangle(
    310,
    280,
    585,
    440,
    fill="",
    outline="",
    tags="case_001"
)


case_002_area = canvas.create_rectangle(
    625,
    280,
    910,
    440,
    fill="",
    outline="",
    tags="case_002"
)


store_area = canvas.create_rectangle(
    410,
    465,
    815,
    575,
    fill="",
    outline="",
    tags="store"
)


feedback_area = canvas.create_rectangle(
    455,
    680,
    775,
    770,
    fill="",
    outline="",
    tags="feedback"
)


# ============================================================
# CLICK EVENTS
# ============================================================

canvas.tag_bind(
    case_001_area,
    "<Button-1>",
    lambda event: open_case_001()
)


canvas.tag_bind(
    store_area,
    "<Button-1>",
    lambda event: open_store()
)

canvas.tag_bind(
    feedback_area,
    "<Button-1>",
    lambda event: open_feedback()
)

# LOCKED MAIN PAGE
if not case_001_solved:

    case_002_lock = canvas.create_rectangle(
        620,
        280,
        910,
        450,
        fill="#555555",
        stipple="gray50",
        outline=""
    )

    canvas.create_text(
        765,
        365,
        text="🔒\nLOCKED\nSolve Murdle 001 first",
        font=("Georgia", 14, "bold"),
        fill="white",
        justify="center"
    )

else:

    canvas.tag_bind(
        case_002_area,
        "<Button-1>",
        lambda event: open_case_002()
    )


# ============================================================
# CURSOR EFFECT
# ============================================================

def button_enter(event):

    canvas.config(
        cursor="hand2"
    )


def button_leave(event):

    canvas.config(
        cursor=""
    )


clickable_areas = [
    case_001_area,
    store_area,
    feedback_area
]

if case_001_solved:
    clickable_areas.append(case_002_area)


for area in clickable_areas:

    canvas.tag_bind(
        area,
        "<Enter>",
        button_enter
    )

    canvas.tag_bind(
        area,
        "<Leave>",
        button_leave
    )


# ============================================================
# START
# ============================================================

play_main_music()
root.mainloop()
