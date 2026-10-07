import tkinter as tk
import sys
import os
import pygame

import navigation
from PIL import Image, ImageTk
from save_manager import load_data, save_data

pygame.mixer.init()


#RESOURCE PATH
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


def return_to_main():

    pygame.mixer.music.stop()

    navigation.go_to(root, "main")

def play_store_music():

    if not pygame.mixer.music.get_busy():

        pygame.mixer.music.load(
            resource_path("sounds/store_music.mp3")
        )

        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)


# Same clicking sound as the main menu, played when buying an item
click_sound = pygame.mixer.Sound(
    resource_path("sounds/clicking_sound.mp3")
)
click_sound.set_volume(0.5)


def play_click_sound():
    click_sound.play()


#Player data
player_data = load_data()

detective_money = player_data["detective_money"]

magnifying_glass_price = 200
detective_notebook_price = 100
camera_price = 150
fingerprint_kit_price = 200
case_files_price = 250


#Window

root = tk.Tk()
root.title("Murdle - Detective Store")
root.geometry("1200x800")
root.resizable(False, False)

play_store_music()

#Canvas or Desk

canvas = tk.Canvas(
    root,
    width=1200,
    height=800,
    highlightthickness=0
)

canvas.pack()

#Background Main canvas

store_image = Image.open(
    resource_path("assets/detective_store.png")
)

store_image = store_image.resize(
    (1200, 800)
)

store_background = ImageTk.PhotoImage(
    store_image
)


canvas.create_image(
    0,
    0,
    image=store_background,
    anchor="nw"
)

canvas.background = store_background



GRID_SUSPECTS = ["DR. EVELYN ROSE", "LUCA MORETTI", "AMELIA HART"]
GRID_WEAPONS = ["SHEARS", "THE MARBLE ORCHID STATUE", "WOODEN MALLET"]
GRID_LOCATIONS = ["THE ORCHID PAVILION", "THE FOUNTAIN COURTYARD", "THE BUTTERFLY HOUSE"]

# Grid colors
GRID_PAPER = "#D8C49C"        # window background
GRID_INK = "#2B2118"          # dark brown text
GRID_BRASS = "#8A6A32"        # headers and buttons
GRID_CREAM = "#F1E5C8"        # empty squares
GRID_X_COLOR = "#8B1E1E"      # deep red for "not them"
GRID_CHECK_COLOR = "#2E5E3A"  # dark green for "it's them!"

# What each square can show: (symbol, background, text color)
SQUARE_STYLES = [
    ("", GRID_CREAM, GRID_INK),                # 0 = empty
    ("✗", GRID_X_COLOR, GRID_CREAM),           # 1 = not them
    ("✓", GRID_CHECK_COLOR, GRID_CREAM),       # 2 = it's them!
]

# Remembers the marks while the store is open, so closing and
# reopening the grid doesn't erase the player's work
grid_marks = {}
grid_window = None


def open_deduction_grid():

    global grid_window

    # If the grid is already open, just bring it to the front
    if grid_window is not None and grid_window.winfo_exists():
        grid_window.lift()
        return

    grid_window = tk.Toplevel(root)
    grid_window.title("Detective Notebook - Deduction Grid")
    grid_window.configure(bg=GRID_PAPER)
    grid_window.resizable(False, False)

    # ----------------------------
    # TITLE AND INSTRUCTIONS
    # ----------------------------

    title = tk.Label(
        grid_window,
        text="📓 DEDUCTION GRID",
        font=("Georgia", 20, "bold"),
        bg=GRID_PAPER,
        fg=GRID_INK
    )
    title.pack(pady=(20, 5))

    instructions = tk.Label(
        grid_window,
        text="Click a square to mark it.   "
             "Once = ✗ not them     Twice = ✓ it's them!     "
             "Three times = clear",
        font=("Georgia", 10, "italic"),
        bg=GRID_PAPER,
        fg=GRID_INK
    )
    instructions.pack(pady=(0, 15), padx=20)

    # ----------------------------
    # THE GRID ITSELF
    # ----------------------------

    table = tk.Frame(grid_window, bg=GRID_PAPER)
    table.pack(padx=20)

    all_squares = []

    def make_square(row, column, suspect, item):

        key = (suspect, item)
        symbol, background, text_color = SQUARE_STYLES[grid_marks.get(key, 0)]

        square = tk.Label(
            table,
            text=symbol,
            font=("Georgia", 14, "bold"),
            width=4,
            height=1,
            bg=background,
            fg=text_color,
            relief="solid",
            bd=1,
            cursor="hand2"
        )
        square.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")

        def on_click(event):
            new_state = (grid_marks.get(key, 0) + 1) % 3
            grid_marks[key] = new_state
            new_symbol, new_background, new_text = SQUARE_STYLES[new_state]
            square.config(text=new_symbol, bg=new_background, fg=new_text)

        square.bind("<Button-1>", on_click)
        all_squares.append((square, key))

    def make_header(row, column, text, span=1, big=False):
        header = tk.Label(
            table,
            text=text,
            font=("Georgia", 11 if big else 9, "bold"),
            bg=GRID_BRASS if big else GRID_PAPER,
            fg=GRID_CREAM if big else GRID_INK,
            wraplength=70,
            justify="center"
        )
        header.grid(
            row=row,
            column=column,
            columnspan=span,
            padx=1,
            pady=1,
            sticky="nsew"
        )

    # Column numbers: names in column 0, weapons next,
    # a small gap, then locations
    first_weapon_column = 1
    gap_column = first_weapon_column + len(GRID_WEAPONS)
    first_location_column = gap_column + 1

    # Top row: the two group titles
    make_header(0, first_weapon_column, "WEAPONS",
                span=len(GRID_WEAPONS), big=True)
    make_header(0, first_location_column, "LOCATIONS",
                span=len(GRID_LOCATIONS), big=True)

    # Second row: each weapon and location name
    for i, weapon in enumerate(GRID_WEAPONS):
        make_header(1, first_weapon_column + i, weapon)

    for i, location in enumerate(GRID_LOCATIONS):
        make_header(1, first_location_column + i, location)

    # Little empty gap between the weapons and locations sections
    tk.Label(table, text="", bg=GRID_PAPER, width=1).grid(
        row=0, column=gap_column
    )

    # One row per suspect
    for r, suspect in enumerate(GRID_SUSPECTS):

        row = r + 2

        name_label = tk.Label(
            table,
            text=suspect,
            font=("Georgia", 11, "bold"),
            bg=GRID_BRASS,
            fg=GRID_CREAM,
            anchor="e",
            padx=8
        )
        name_label.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")

        for i, weapon in enumerate(GRID_WEAPONS):
            make_square(row, first_weapon_column + i, suspect, weapon)

        for i, location in enumerate(GRID_LOCATIONS):
            make_square(row, first_location_column + i, suspect, location)

    # ----------------------------
    # BUTTONS
    # ----------------------------

    def clear_grid():
        for square, key in all_squares:
            grid_marks[key] = 0
            symbol, background, text_color = SQUARE_STYLES[0]
            square.config(text=symbol, bg=background, fg=text_color)

    button_row = tk.Frame(grid_window, bg=GRID_PAPER)
    button_row.pack(pady=20)

    clear_button = tk.Button(
        button_row,
        text="CLEAR GRID",
        font=("Georgia", 11, "bold"),
        bg=GRID_X_COLOR,
        fg=GRID_CREAM,
        activebackground="#5C1414",
        activeforeground="white",
        cursor="hand2",
        command=clear_grid
    )
    clear_button.pack(side="left", padx=10)

    close_button = tk.Button(
        button_row,
        text="CLOSE",
        font=("Georgia", 11, "bold"),
        bg=GRID_BRASS,
        fg=GRID_CREAM,
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=grid_window.destroy
    )
    close_button.pack(side="left", padx=10)


def buy_detective_notebook():

    global detective_money

    if "detective_notebook" in player_data["purchased_items"]:
        purchase_message.config(
            text="You already own the Detective Notebook."
        )
        return

    if detective_money >= detective_notebook_price:

        detective_money -= detective_notebook_price

        player_data["detective_money"] = detective_money
        player_data["purchased_items"].append(
            "detective_notebook"
        )

        save_data(player_data)

        # Purchase sound
        play_click_sound()

        canvas.itemconfig(
            money_display,
            text=f"DETECTIVE FUNDS\n${detective_money:,}"
        )

        # The notebook's button now opens the grid
        notebook_button.config(
            text="OPEN GRID",
            bg="#8A6A32",
            fg="#F1E5C8",
            command=open_deduction_grid
        )

        purchase_message.config(
            text="Detective Notebook purchased!"
        )

        # Open the deduction grid right away
        open_deduction_grid()

    else:
        purchase_message.config(
            text="Not enough Detective Funds."
        )



camera_window = None


def show_camera_evidence():

    global camera_window

    # If the photos are already open, just bring them to the front
    if camera_window is not None and camera_window.winfo_exists():
        camera_window.lift()
        return

    camera_window = tk.Toplevel(root)
    camera_window.title("Camera - Evidence Photos")
    camera_window.configure(bg="#D8C49C")
    camera_window.resizable(False, False)

    title = tk.Label(
        camera_window,
        text="📷 EVIDENCE PHOTOS",
        font=("Georgia", 20, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )
    title.pack(pady=(20, 5))

    subtitle = tk.Label(
        camera_window,
        text="Your camera caught something at the scene...\n"
             "Look closely. These may point to the guilty one.",
        font=("Georgia", 11, "italic"),
        bg="#D8C49C",
        fg="#2B2118",
        justify="center"
    )
    subtitle.pack(pady=(0, 10))

    # Frame that holds the two photos side by side
    photos_frame = tk.Frame(camera_window, bg="#D8C49C")
    photos_frame.pack(padx=20, pady=10)

    picture_files = [
        ("assets/pic_evidence1.png", "PHOTO #1"),
        ("assets/pic_evidence2.png", "PHOTO #2"),
    ]

    for picture_path, caption in picture_files:

        # Each photo gets its own little "card" with a caption
        photo_card = tk.Frame(photos_frame, bg="#F1E5C8", bd=2, relief="ridge")
        photo_card.pack(side="left", padx=10)

        try:
            evidence_image = Image.open(
                resource_path(picture_path)
            )

            # Shrink big pictures so both fit, without stretching them
            evidence_image.thumbnail((450, 400))

            evidence_photo = ImageTk.PhotoImage(evidence_image)

            image_label = tk.Label(
                photo_card,
                image=evidence_photo,
                bg="#F1E5C8"
            )

            # Tkinter forgets pictures unless we hold on to them
            image_label.image = evidence_photo

            image_label.pack(padx=8, pady=(8, 4))

        except FileNotFoundError:

            missing_label = tk.Label(
                photo_card,
                text=f"(Picture not found:\n{picture_path})",
                font=("Georgia", 11),
                bg="#F1E5C8",
                fg="#8B0000"
            )
            missing_label.pack(padx=30, pady=40)

        caption_label = tk.Label(
            photo_card,
            text=caption,
            font=("Georgia", 11, "bold"),
            bg="#F1E5C8",
            fg="#2B2118"
        )
        caption_label.pack(pady=(0, 8))

    close_button = tk.Button(
        camera_window,
        text="CLOSE",
        font=("Georgia", 12, "bold"),
        bg="#8A6A32",
        fg="#F1E5C8",
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=camera_window.destroy
    )
    close_button.pack(pady=(10, 20))


def buy_camera():

    global detective_money

    if "camera" in player_data["purchased_items"]:
        purchase_message.config(
            text="You already own the Camera."
        )
        return

    if detective_money >= camera_price:

        detective_money -= camera_price

        player_data["detective_money"] = detective_money
        player_data["purchased_items"].append(
            "camera"
        )

        save_data(player_data)

        # Purchase sound
        play_click_sound()

        canvas.itemconfig(
            money_display,
            text=f"DETECTIVE FUNDS\n${detective_money:,}"
        )

        # The camera's button now opens the photos
        camera_button.config(
            text="VIEW PHOTOS",
            bg="#8A6A32",
            fg="#F1E5C8",
            command=show_camera_evidence
        )

        purchase_message.config(
            text="Camera purchased!"
        )

        # Show the evidence photos right away
        show_camera_evidence()

    else:
        purchase_message.config(
            text="Not enough Detective Funds."
        )



forensic_window = None


def show_forensic_report():

    global forensic_window

    # If the report is already open, just bring it to the front
    if forensic_window is not None and forensic_window.winfo_exists():
        forensic_window.lift()
        return

    forensic_window = tk.Toplevel(root)
    forensic_window.title("Fingerprint Kit - Forensic Report")
    forensic_window.configure(bg="#D8C49C")
    forensic_window.resizable(False, False)

    title = tk.Label(
        forensic_window,
        text="🔎 FORENSIC REPORT",
        font=("Georgia", 20, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )
    title.pack(pady=(20, 5))

    subtitle = tk.Label(
        forensic_window,
        text="You dusted the evidence and found hidden fingerprints...\n"
             "Whose prints are these, Detective?",
        font=("Georgia", 11, "italic"),
        bg="#D8C49C",
        fg="#2B2118",
        justify="center"
    )
    subtitle.pack(pady=(0, 10))

    # A cream "lab file" card around the picture
    report_card = tk.Frame(forensic_window, bg="#F1E5C8", bd=2, relief="ridge")
    report_card.pack(padx=20, pady=10)

    try:
        forensic_image = Image.open(
            resource_path("assets/forensic_pic.png")
        )

        # Shrink big pictures so they fit, without stretching them
        forensic_image.thumbnail((700, 500))

        forensic_photo = ImageTk.PhotoImage(forensic_image)

        image_label = tk.Label(
            report_card,
            image=forensic_photo,
            bg="#F1E5C8"
        )

        # Tkinter forgets pictures unless we hold on to them
        image_label.image = forensic_photo

        image_label.pack(padx=8, pady=(8, 4))

    except FileNotFoundError:

        missing_label = tk.Label(
            report_card,
            text="(Picture not found:\nassets/forensic_pic.png)",
            font=("Georgia", 11),
            bg="#F1E5C8",
            fg="#8B0000"
        )
        missing_label.pack(padx=40, pady=40)

    stamp_label = tk.Label(
        report_card,
        text="EVIDENCE - FINGERPRINT ANALYSIS",
        font=("Georgia", 11, "bold"),
        bg="#F1E5C8",
        fg="#8B1E1E"
    )
    stamp_label.pack(pady=(0, 8))

    close_button = tk.Button(
        forensic_window,
        text="CLOSE",
        font=("Georgia", 12, "bold"),
        bg="#8A6A32",
        fg="#F1E5C8",
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=forensic_window.destroy
    )
    close_button.pack(pady=(10, 20))


def buy_fingerprint_kit():

    global detective_money

    if "fingerprint_kit" in player_data["purchased_items"]:
        purchase_message.config(
            text="You already own the Fingerprint Kit."
        )
        return

    if detective_money >= fingerprint_kit_price:

        detective_money -= fingerprint_kit_price

        player_data["detective_money"] = detective_money
        player_data["purchased_items"].append(
            "fingerprint_kit"
        )

        save_data(player_data)

        # Purchase sound
        play_click_sound()

        canvas.itemconfig(
            money_display,
            text=f"DETECTIVE FUNDS\n${detective_money:,}"
        )

        # The kit's button now opens the forensic report
        fingerprint_button.config(
            text="VIEW PRINTS",
            bg="#8A6A32",
            fg="#F1E5C8",
            command=show_forensic_report
        )

        purchase_message.config(
            text="Fingerprint Kit purchased!"
        )

        # Show the forensic report right away
        show_forensic_report()

    else:
        purchase_message.config(
            text="Not enough Detective Funds."
        )



CASE_FILE_MAX_VIEWS = 2

case_file_warning_window = None
case_file_window = None


def case_file_views_left():
    views_used = player_data.get("case_file_views", 0)
    return max(CASE_FILE_MAX_VIEWS - views_used, 0)


def update_case_files_button():

    views_left = case_file_views_left()

    if views_left > 0:
        case_files_button.config(
            text=f"READ FILE ({views_left} LEFT)",
            bg="#8A6A32",
            fg="#F1E5C8",
            state="normal",
            command=show_case_file_warning
        )

    else:
        case_files_button.config(
            text="FILE SEALED",
            bg="#5C4631",
            fg="#F1E5C8",
            state="disabled"
        )


def show_case_file_warning():

    global case_file_warning_window

    views_left = case_file_views_left()

    if views_left <= 0:
        purchase_message.config(
            text="This file has been sealed."
        )
        return

    # If the warning is already open, just bring it to the front
    if (case_file_warning_window is not None
            and case_file_warning_window.winfo_exists()):
        case_file_warning_window.lift()
        return

    warning_window = tk.Toplevel(root)
    warning_window.title("Case Files - Warning")
    warning_window.configure(bg="#D8C49C")
    warning_window.resizable(False, False)
    case_file_warning_window = warning_window

    title = tk.Label(
        warning_window,
        text="⚠ CONFIDENTIAL ⚠",
        font=("Georgia", 22, "bold"),
        bg="#D8C49C",
        fg="#8B1E1E"
    )
    title.pack(pady=(25, 10), padx=40)

    message = tk.Label(
        warning_window,
        text="The following file will only open twice.\n"
             "Study it carefully, Detective.",
        font=("Georgia", 13),
        bg="#D8C49C",
        fg="#2B2118",
        justify="center"
    )
    message.pack(pady=(0, 10), padx=40)

    if views_left == 1:
        times_left_text = "This is your LAST chance to read it."
    else:
        times_left_text = f"Times left to open: {views_left}"

    times_left = tk.Label(
        warning_window,
        text=times_left_text,
        font=("Georgia", 12, "bold"),
        bg="#D8C49C",
        fg="#8B1E1E"
    )
    times_left.pack(pady=(0, 15))

    button_row = tk.Frame(warning_window, bg="#D8C49C")
    button_row.pack(pady=(0, 25))

    def open_it():
        warning_window.destroy()
        open_confidential_file()

    open_button = tk.Button(
        button_row,
        text="OPEN FILE",
        font=("Georgia", 12, "bold"),
        bg="#8B1E1E",
        fg="#F1E5C8",
        activebackground="#5C1414",
        activeforeground="white",
        cursor="hand2",
        command=open_it
    )
    open_button.pack(side="left", padx=10)

    later_button = tk.Button(
        button_row,
        text="NOT YET",
        font=("Georgia", 12, "bold"),
        bg="#8A6A32",
        fg="#F1E5C8",
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=warning_window.destroy
    )
    later_button.pack(side="left", padx=10)


def open_confidential_file():

    global case_file_window

    # Count this view and save it, so it's remembered next time
    player_data["case_file_views"] = player_data.get("case_file_views", 0) + 1
    save_data(player_data)

    update_case_files_button()

    views_left = case_file_views_left()

    case_file_window = tk.Toplevel(root)
    case_file_window.title("Case Files - Confidential")
    case_file_window.configure(bg="#D8C49C")
    case_file_window.resizable(False, False)

    title = tk.Label(
        case_file_window,
        text="📁 CONFIDENTIAL FILE",
        font=("Georgia", 20, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )
    title.pack(pady=(20, 5))

    if views_left == 1:
        reminder_text = "You can open this file 1 more time."
    else:
        reminder_text = "This was your last look. After closing, the file will be sealed."

    reminder = tk.Label(
        case_file_window,
        text=reminder_text,
        font=("Georgia", 11, "italic"),
        bg="#D8C49C",
        fg="#8B1E1E"
    )
    reminder.pack(pady=(0, 10))

    try:
        file_image = Image.open(
            resource_path("assets/confidential_file.png")
        )

        # Shrink big pictures so they fit, without stretching them
        file_image.thumbnail((750, 650))

        file_photo = ImageTk.PhotoImage(file_image)

        image_label = tk.Label(
            case_file_window,
            image=file_photo,
            bg="#D8C49C"
        )

        # Tkinter forgets pictures unless we hold on to them
        image_label.image = file_photo

        image_label.pack(padx=20, pady=10)

    except FileNotFoundError:

        missing_label = tk.Label(
            case_file_window,
            text="(Picture not found:\nassets/confidential_file.png)",
            font=("Georgia", 11),
            bg="#D8C49C",
            fg="#8B0000"
        )
        missing_label.pack(padx=40, pady=30)

    close_button = tk.Button(
        case_file_window,
        text="CLOSE",
        font=("Georgia", 12, "bold"),
        bg="#8A6A32",
        fg="#F1E5C8",
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=case_file_window.destroy
    )
    close_button.pack(pady=(5, 20))


def buy_case_files():

    global detective_money

    if "case_files" in player_data["purchased_items"]:
        purchase_message.config(
            text="You already own Case Files Access."
        )
        return

    if detective_money >= case_files_price:

        detective_money -= case_files_price

        player_data["detective_money"] = detective_money
        player_data["purchased_items"].append(
            "case_files"
        )

        save_data(player_data)

        # Purchase sound
        play_click_sound()

        canvas.itemconfig(
            money_display,
            text=f"DETECTIVE FUNDS\n${detective_money:,}"
        )

        # The button now shows how many times the file can be opened
        update_case_files_button()

        purchase_message.config(
            text="Case Files Access purchased!"
        )

        # Show the warning, then the file
        show_case_file_warning()

    else:
        purchase_message.config(
            text="Not enough Detective Funds."
        )

# ============================================================
# MAGNIFYING GLASS HINT WINDOW
# Opens once, right after the Magnifying Glass is bought.
# Put your hint picture in: assets/magnifying_hint.png
# ============================================================

def show_magnifying_hint():

    hint_window = tk.Toplevel(root)
    hint_window.title("Magnifying Glass - A Closer Look")
    hint_window.configure(bg="#D8C49C")
    hint_window.resizable(False, False)

    # Keep the hint window on top of the store
    hint_window.transient(root)
    hint_window.grab_set()

    title = tk.Label(
        hint_window,
        text="🔍 A CLOSER LOOK",
        font=("Georgia", 20, "bold"),
        bg="#D8C49C",
        fg="#2B2118"
    )
    title.pack(pady=(20, 5))

    subtitle = tk.Label(
        hint_window,
        text="Under the glass, you notice something new...\n"
             "Study it well, Detective. You'll only see this once.",
        font=("Georgia", 11, "italic"),
        bg="#D8C49C",
        fg="#2B2118",
        justify="center"
    )
    subtitle.pack(pady=(0, 10))

    try:
        hint_image = Image.open(
            resource_path("assets/magnifying_hint.png")
        )

        # Shrink big pictures so they fit, without stretching them
        hint_image.thumbnail((700, 500))

        hint_photo = ImageTk.PhotoImage(hint_image)

        image_label = tk.Label(
            hint_window,
            image=hint_photo,
            bg="#D8C49C"
        )

        # Tkinter forgets pictures unless we hold on to them
        image_label.image = hint_photo

        image_label.pack(padx=20, pady=10)

    except FileNotFoundError:

        missing_label = tk.Label(
            hint_window,
            text="(Hint picture not found:\nassets/magnifying_hint.png)",
            font=("Georgia", 11),
            bg="#D8C49C",
            fg="#8B0000"
        )
        missing_label.pack(padx=40, pady=30)

    close_button = tk.Button(
        hint_window,
        text="CLOSE",
        font=("Georgia", 12, "bold"),
        bg="#8A6A32",
        fg="#F1E5C8",
        activebackground="#5C4631",
        activeforeground="white",
        cursor="hand2",
        command=hint_window.destroy
    )
    close_button.pack(pady=(5, 20))


def buy_magnifying_glass():

    global detective_money

    if "magnifying_glass" in player_data["purchased_items"]:

        purchase_message.config(
            text="You already own this item."
        )

        return


    if detective_money >= magnifying_glass_price:

        detective_money -= magnifying_glass_price

        player_data["detective_money"] = detective_money

        player_data["purchased_items"].append(
            "magnifying_glass"
        )

        save_data(player_data)


        # Purchase sound
        play_click_sound()

        canvas.itemconfig(
            money_display,
            text=f"DETECTIVE FUNDS\n${detective_money:,}"
        )

        buy_magnifying_button.config(
            text="PURCHASED",
            bg="#8A6A32",
            fg="#F1E5C8",
            state="disabled"
        )

        purchase_message.config(
            text="Magnifying Glass purchased!"
        )

        # Show the secret hint picture (only happens once, at purchase)
        show_magnifying_hint()


    else:

        purchase_message.config(
            text="Not enough Detective Funds."
        )

buy_magnifying_button = tk.Button(
    root,
    text="BUY - $200",
    font=("Georgia", 11, "bold"),
    bg="#8A6A32",
    fg="#F1E5C8",
    activebackground="#5C4631",
    activeforeground="white",
    cursor="hand2",
    command=buy_magnifying_glass
)

canvas.create_window(
    140,
    620,
    window=buy_magnifying_button
)
notebook_button = tk.Button(
    root,
    text="BUY - $100",
    font=("Georgia", 11, "bold"),
    bg="#8A6A32",
    fg="#F1E5C8",
    cursor="hand2",
    command=buy_detective_notebook
)

canvas.create_window(
    370,
    620,
    window=notebook_button
)


camera_button = tk.Button(
    root,
    text="BUY - $150",
    font=("Georgia", 11, "bold"),
    bg="#8A6A32",
    fg="#F1E5C8",
    cursor="hand2",
    command=buy_camera
)

canvas.create_window(
    600,
    620,
    window=camera_button
)


fingerprint_button = tk.Button(
    root,
    text="BUY - $200",
    font=("Georgia", 11, "bold"),
    bg="#8A6A32",
    fg="#F1E5C8",
    cursor="hand2",
    command=buy_fingerprint_kit
)

canvas.create_window(
    840,
    620,
    window=fingerprint_button
)


case_files_button = tk.Button(
    root,
    text="BUY - $250",
    font=("Georgia", 11, "bold"),
    bg="#8A6A32",
    fg="#F1E5C8",
    cursor="hand2",
    command=buy_case_files
)

canvas.create_window(
    1070,
    620,
    window=case_files_button
)
purchase_message = tk.Label(
    root,
    text="",
    font=("Georgia", 12, "bold"),
    bg="#1F3026",
    fg="#F1E5C8"
)

canvas.create_window(
    600,
    660,
    window=purchase_message
)

if "magnifying_glass" in player_data["purchased_items"]:
    buy_magnifying_button.config(
        text="PURCHASED",
        state="disabled"
    )

if "detective_notebook" in player_data["purchased_items"]:
    notebook_button.config(
        text="OPEN GRID",
        command=open_deduction_grid
    )

if "camera" in player_data["purchased_items"]:
    camera_button.config(
        text="VIEW PHOTOS",
        command=show_camera_evidence
    )

if "fingerprint_kit" in player_data["purchased_items"]:
    fingerprint_button.config(
        text="VIEW PRINTS",
        command=show_forensic_report
    )

if "case_files" in player_data["purchased_items"]:
    update_case_files_button()


main_menu_button = tk.Button(
    root,
    text="MAIN MENU",
    font=("Georgia", 14, "bold"),
    bg="#1F3026",
    fg="#d4af37",
    activebackground="#5c4631",
    activeforeground="white",
    cursor="hand2",
    command=return_to_main
)

canvas.create_window(
    115,
    55,
    window=main_menu_button
)

money_display = canvas.create_text(
    1050,
    75,
    text=f"DETECTIVE FUNDS\n${detective_money:,}",
    font=("Georgia", 14, "bold"),
    fill="white",
    justify="center"
)


root.mainloop()
