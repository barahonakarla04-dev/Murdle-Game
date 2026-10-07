
import tkinter as tk
import pygame
import os
import sys

import navigation

from PIL import Image, ImageTk, ImageDraw
from math import ceil
from save_manager import load_data, save_data




#---------------------
# RESOURCE PATH
# --------------------


def resource_path(relative_path):

    # When running as an EXE
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS

    # When running normally as a Python file
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)



pygame.mixer.init()

correct_suspect= "AMELIA HART"
correct_location= "THE BUTTERFLY HOUSE"
correct_weapon= "THE MARBLE ORCHID STATUE"


player_data = load_data()
detective_money= player_data["detective_money"]
case_reward= 500
# Already solved before? Then the reward was already paid.
case_reward_claimed = player_data.get("case_002_solved", False)
detective_notes= ""
music_on=True

money_sound = pygame.mixer.Sound(resource_path("sounds/money_sound.mp3") )
money_sound.set_volume(0.5)
page_sound = pygame.mixer.Sound(resource_path("sounds/open_folder_sound.mp3"))
page_sound.set_volume(0.5)

#--------------------------------------------------------------------------------------
# MAIN WINDOW/ FIRST VIEW
# -------------------------------------------------------------------------------------

root=tk.Tk()
root.title("Murdle - Case #002")
root.geometry("1200x900")
root.configure(bg="#1F3026")


#----------------------------------
# TITLE & SUBTITLE OF THE MAIN WINDOW
# ---------------------------------
title=tk.Label(
    root,
    text=" M U R D L E ",
    font=("Geogia", 30 , "bold"),
    bg="#1F3026",
    fg="#e8d5b5"
)
title.pack(pady=30)

subtitle = tk.Label(
    root,
    text="CASE #002 — DEATH IN THE GLASS GARDEN",
    font=("Georgia", 13),
    fg="#c7b08a",
    bg="#1F3026"
)

subtitle.pack()

#----------------------------------
# DEF ALL HELPER FUNCTIONS
# ---------------------------------
# a. MUSIC
# ---------------------------------

def play_page_sound():
    page_sound.play()


def change_page(next_screen):
    play_page_sound()
    next_screen()

#---------------------------------------
def play_desk_music():

    #it will not restart every time player goes back into the desk
    if not pygame.mixer.music.get_busy():

        pygame.mixer.music.load(resource_path("sounds/garden_sound.mp3"))

    #volume control from 0 - 1
        pygame.mixer.music.set_volume(0.25)

    #loop for the music
        pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def toggle_music():
    global music_on

    if music_on:

       pygame.mixer.music.pause()
       music_on = False

    else:

        pygame.mixer.music.unpause()
        music_on = True

def open_store():

    pygame.mixer.music.stop()

    navigation.go_to(root, "store")

#Return to main view


def return_to_main():

    navigation.go_to(root, "main")

#--------------------------------------
# SCROLL BAR FOR ALL WINDOWS
# -------------------------------------



def create_scroll_bar():


    canvas = tk.Canvas(
        root,
        bg="#d8c49c",
        highlightthickness=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True

    )

    scrollbar = tk.Scrollbar(
        root,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # Connect canvas to scrollbar
    canvas.configure(
        yscrollcommand=scrollbar.set
    )

#----------------------------------------
# FRAME CONTENT
# ---------------------------------------

    content_frame = tk.Frame(
        canvas,
        bg="#d8c49c"
    )


# Put frame inside canvas
    canvas_window = canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )

    def update_scroll_region(event):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    content_frame.bind(
        "<Configure>",
        update_scroll_region
    )

# ==============================
# KEEP CONTENT CENTERED
# ==============================

    def resize_content(event):

        canvas.itemconfig(
            canvas_window,
            width=event.width
        )


    canvas.bind(
        "<Configure>",
        resize_content
    )


# ==============================
# MOUSE WHEEL
# ==============================

    def mouse_wheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
        )


    return content_frame


def folder_enter(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(
            event.widget.find_withtag("current"),
            outline="",
            width=0
    )


def folder_leave(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(
            event.widget.find_withtag("current"),
            outline="",
            width=0
        )

#------------------------------
# DEFINE ALL FOLDERS AND CONTENT
# -----------------------------

def open_suspects():

    play_page_sound()


    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()

    file_title = tk.Label(
        content,
        text="SUSPECTS FILE",
        font=("Geogia",20,"bold"),
        fg="#24382B",
        bg="#D8C49C"
    )

    file_title.pack(fill="x",pady=(40, 20))

    suspect = tk.Label(
        content,
        text="""
        VICTIM: DR. ADRIAN BELL
        Renowned botanist known for his research into rare and exotic orchids.
        Brilliant but outspoken, his work often placed him at the center of professional
        rivalries and disagreements.

        Recently, Bell had begun asking uncomfortable questions about activities
        inside the Orchid Crown Conservatory.

        At 2:15 PM, he was discovered dead behind several people with reasons
        to want him silenced.

        ---------------------------------------------------------------------------------------

        🌺 DR. EVELYN ROSE — THE RIVAL BOTANIST

        Brilliant, competitive, and furious. Bell recently took credit for discovering a rare
        orchid they had researched together.

            HEIGHT: 5'8
            DESCRIPTION:    DARK BROWN HAIR
                            GREEN EYES
                            CARRIES HER NOTEBOOK AND SHARPENED PENS TO TAKE NOTES

        =======================================================================================

        📸 LUCA MORETTI — THE PHOTOGRAPHER

        Hired to photograph the exhibition. Bell demanded that Luca delete several photographs
        taken earlier that afternoon but wouldn't explain why.

            HEIGHT: 5"11
            DESCRIPTION:    DARK BROWN HAIR
                            BROWN EYES
                            FREQUENTLY PUSHES HIS SLEEVES UP HIS ELBOWS TO AVOID STAINING
                            HIMSELF DURING WORK

        =======================================================================================

        🦋 AMELIA HART — THE GARDEN DIRECTOR

        Elegant and respected. Bell had recently discovered something about the conservatory's
        finances that could destroy her career.

            HEIGHT: 5"6
            DESCRIPTION:    DARK BLONDE HAIR
                            GRAY-BLUE EYES
                            LIGHT ON HER FEET, EVER SINCE SHE STARTED BALLET CLASSES



        """,

        font=("Courier New", 14),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    suspect.pack(padx=80, pady=30)


    # Close file button
    close_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    close_button.pack(pady=35)

def open_locations():

    play_page_sound()


    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()

    file_title = tk.Label(
        content,
        text="LOCATIONS FILE",
        font=("Georgia", 20, "bold"),
        fg="#24382B",
        bg="#D8C49C"
    )

    file_title.pack(
        fill="x",
        pady=(40, 20)
    )


    #--------------------
    # CREATING THE IMAGE
    # -------------------

    three_locations_image = Image.open(
        resource_path("assets/three_locations.png")
    )

    three_locations_image = three_locations_image.resize(
        (500,300)
    )

    three_locations_image = ImageTk.PhotoImage(
        three_locations_image
    )

    image_label=tk.Label(
        content,
        image= three_locations_image,
        bg="#d8c49c"
    )

    image_label.Image = three_locations_image

    image_label.pack(pady=20)



    locations = tk.Label(
        content,
        text="""
🌸 THE ORCHID PAVILION

A brilliant glass room filled with hundreds of orchids.
Workers spent most of the afternoon preparing plants and
displays for the upcoming exhibition.


==============================================================


⛲ THE FOUNTAIN COURTYARD

An open air courtyard surrounded by palms and stone benches.
Water constantly splashes from the central fountain, leaving
sections of the stone floor damp.


==============================================================


🦋 THE BUTTERFLY HOUSE

Warm, humid, and filled with plants and free-flying butterflies.
Thick vegetation creates several areas completely hidden
from the main visitor path.

""",
        font=("Courier New", 14),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    locations.pack(
        padx=80,
        pady=30
    )

    close_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    close_button.pack(
        pady=35
    )



def open_clues():
    play_page_sound()


    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()

    file_title= tk.Label(
        content,
        text="CLUES FILE",
        font=("Geogia", 20,"bold"),
        fg="#24382B",
        bg="#D8C49C"
    )

    file_title.pack(
        fill="x",
        pady=(40,20)
    )

    clues = tk.Label(
        content,
        text="""
        🔎 Clue #1 — The Dry Shoes
        Bell's shoes are completely dry.
        If he had crossed the wet Fountain Courtyard shortly before his death,
        investigators would expect moisture or marks on them.

        --------------------------------------------------------------------------------
        🔎 Clue #2 — The Missing Statue
        One of the decorative marble orchid statues is missing from the Orchid Pavilion.
        Nobody remembers seeing it removed officially.

        --------------------------------------------------------------------------------
        🔎 Clue #3 — The Butterfly Wing
        A tiny bright-blue butterfly wing is caught on Bell's jacket.
        The species is kept inside the Butterfly House.

        --------------------------------------------------------------------------------
        🔎 Clue #4 — The Photograph
        Luca's camera contains a photograph timestamped 2:03 PM.
        In the distant background, Amelia Hart can be seen entering the Butterfly House
        carrying an object wrapped in white cloth.

        --------------------------------------------------------------------------------
        🔎 Clue #5 — The Gardening Shears
        Investigators examine the shears.
        Fresh orchid stems remain between the blades.
        There is no blood on them.

        --------------------------------------------------------------------------------
        🔎 Clue #6 — The White Dust
        Fine white marble dust is discovered on Amelia's sleeve.
        She claims she doesn't know how it got there.

        --------------------------------------------------------------------------------
        🔎 Clue #7 — The Mallet
        Two gardeners confirm that the wooden planting mallet was being used at the Orchid
        Pavilion during the relevant period. That makes it highly unlikely to be the murder
        weapon.

        --------------------------------------------------------------------------------
        🔎 Clue #8 — The Hidden Fragment
        Behind a large fern inside the Butterfly House, investigators discover a small broken
        piece of white marble.
        There is blood on its edge.""",

        font=("Courier New", 14),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    clues.pack(
        padx=80,
        pady=30
    )

    close_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    close_button.pack(
        pady=35
    )


def open_evidence():
    play_page_sound()


    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()

    file_title=tk.Label(
        content,
        text="EVIDENCE FILE",
        font=("Georgia", 20, "bold"),
        fg="#24382B",
        bg="#D8C49C"
    )
    file_title.pack(
         fill="x",
         pady=(40,20)
     )
    evidence = tk.Label(
        content,
        text="""
        ✂️ Gardening Shears

        Heavy steel shears normally stored at the gardeners' workstation.
        They could certainly cause a serious injury.

        ===================================================================

        🗿 Marble Orchid Statue

        A small decorative statue displayed as part of the orchid exhibition.
        Beautiful—but surprisingly heavy.

        ===================================================================

        🔨 Wooden Planting Mallet

        A gardening mallet used to secure stakes around larger plants and
        displays. Several gardeners had access to it.

        """,

        font=("Courier New", 14),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    evidence.pack(
        padx=80,
        pady=30
    )

    close_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    close_button.pack(
        pady=35
    )

def open_notes():
    play_page_sound()


    global detective_notes
    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()
    root.config(bg="#D8C49C")

    title = tk.Label(
        content,
        text="DETECTIVE'S NOTEBOOK",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 5))


    subtitle = tk.Label(
        content,
        text="CASE #002 — PERSONAL INVESTIGATION NOTES",
        font=("Courier New", 12),
        fg="#5c4631",
        bg="#d8c49c"
    )

    subtitle.pack(pady=10)

    notes_box = tk.Text(
        content,
        width=65,
        height=20,
        font=("Courier New", 13),
        bg="#eee1bd",
        fg="#2b2118",
        padx=20,
        pady=20,
        wrap="word"
    )

    notes_box.pack(pady=20)


    # Starting message
    notes_box.insert("1.0",detective_notes)

    def save_notes():

        play_page_sound()

        global detective_notes

        detective_notes = notes_box.get(
            "1.0",
            "end-1c"
        )

        print("Notes saved!")

    save_button = tk.Button(
        content,
        text="SAVE NOTES",
        font=("Georgia", 12, "bold"),
        command=save_notes
    )

    save_button.pack(pady=5)

    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=15)

def open_solve_area():

    play_page_sound()


    for widget in root.winfo_children():
        widget.destroy()

    content = create_scroll_bar()

    file_title=tk.Label(
        content,
        text="SOLVE CASE FILE",
        font=("Georgia",20,"bold"),
        fg="#24382B",
        bg="#D8C49C"
    )

    file_title.pack(
        fill="x",
        pady=(40,20)
    )

    instructions = tk.Label(
        content,
        text="Make your final accusation.",
        font=("Courier New", 13),
        fg="#5c4631",
        bg="#d8c49c"
    )

    instructions.pack(pady=10)


    # ==============================
    # SUSPECT CHOICE
    # ==============================

    tk.Label(
        content,
        text="WHO committed the murder?",
        font=("Georgia", 14, "bold"),
        bg="#d8c49c",
        fg="#2b2118"
    ).pack(pady=(30, 5))


    suspect_choice = tk.StringVar(value="Choose a suspect")

    suspect_menu = tk.OptionMenu(
        content,
        suspect_choice,
        "DR. EVELYN ROSE",
        "LUCA MORETTI",
        "AMELIA HART"
    )

    suspect_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    suspect_menu.pack(pady=5)

    tk.Label(
        content,
        text="WHERE did it happen?",
        font=("Georgia", 14, "bold"),
        bg="#d8c49c",
        fg="#2b2118"
    ).pack(pady=(30, 5))


    location_choice = tk.StringVar(value="Choose a location")

    location_menu = tk.OptionMenu(
        content,
        location_choice,
        "THE ORCHID PAVILION",
        "THE FOUNTAIN COURTYARD",
        "THE BUTTERFLY HOUSE"
    )

    location_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    location_menu.pack(pady=5)


    tk.Label(
        content,
        text="WHAT was the murder weapon?",
        font=("Georgia", 14, "bold"),
        bg="#d8c49c",
        fg="#2b2118"
    ).pack(pady=(30, 5))


    weapon_choice = tk.StringVar(value="Choose a weapon")

    weapon_menu = tk.OptionMenu(
        content,
        weapon_choice,
        "GARDENING SHEARS",
        "THE MARBLE ORCHID STATUE",
        "WOODEN PLANTING MALLET"
    )

    weapon_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    weapon_menu.pack(pady=5)

    # The STORE button only needs to appear once
    buttons_shown = []

    def show_store_button():

        if buttons_shown:
            return

        buttons_shown.append(True)

        store_button = tk.Button(
            content,
            text="DETECTIVE STORE",
            font=("Georgia", 14, "bold"),
            bg="#8A6A32",
            fg="#F1E5C8",
            cursor="hand2",
            command=open_store
        )

        store_button.pack(pady=10)


    def reward_player():
        """Pays the reward ONLY the first time the case is ever solved.
        Returns True if money was paid this time."""

        global detective_money
        global case_reward_claimed

        paid = False

        if not case_reward_claimed:

            detective_money += case_reward

            player_data["detective_money"] = detective_money
            player_data["case_002_solved"] = True

            save_data(player_data)

            money_sound.play()

            case_reward_claimed = True
            paid = True

        show_store_button()

        return paid


    # ==============================
    # CHECK ACCUSATION
    # ==============================

    def check_accusation():

        play_page_sound()

        suspect = suspect_choice.get()
        location = location_choice.get()
        weapon = weapon_choice.get()

        if (
            suspect == correct_suspect
            and location == correct_location
            and weapon == correct_weapon
        ):
            paid = reward_player()

            if paid:
                reward_text = f"REWARD: ${case_reward}"
            else:
                reward_text = "You already earned the reward for this case."

            result_label.config(
                text="CASE SOLVED!\nYou caught the killer. \n\n "
                    "Dr. Bell discovered financial irregularities in the conservatory's records that could\n\n"
                    "expose Amelia and destroy her career as Garden Director. Fearing that Bell was about to\n\n"
                    "reveal what he knew,"
                    "Amelia decided to silence him before the truth could come out.\n\n"
                    + reward_text,
                fg="darkgreen"
            )

        else:

            result_label.config(
                text="WRONG ACCUSATION.\nSomething does not match the evidence.",
                fg="darkred"
            )


    accuse_button = tk.Button(
        content,
        text="MAKE ACCUSATION",
        font=("Georgia", 13, "bold"),
        command=check_accusation
    )

    accuse_button.pack(pady=30)


    result_label = tk.Label(
        content,
        text="",
        font=("Courier New", 15, "bold"),
        bg="#d8c49c",
        justify="center",
        anchor="center"
    )

    result_label.pack(
        padx=0,
        pady=20,
        fill="x"
    )


    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=25)

#---------------------------
# SHOW DESK
# --------------------------

#Main Brackground
def show_desk():

    global canvas
    for widget in root.winfo_children():
        widget.destroy()

    play_desk_music()

    #--------------------------------------
    # CREATING THE CANVAS
    # -------------------------------------

    canvas = tk.Canvas(
        root,
        width=1200,
        height=900,
        highlightthickness=0

    )

    canvas.pack()

    #--------------------
    # IMAGE BACKGROUND
    # -------------------

    image = Image.open(resource_path("assets/detective_desk_garden.png"))
    image = image.resize((1200,900))
    background = ImageTk.PhotoImage(image)

    canvas.create_image(
        0,
        0,
        image = background,
        anchor="nw"
    )
    canvas.background = background

    #------------------------
    # MUSIC BUTTON INSIDE THE CANVAS
    # -----------------------

    music_button = tk.Button(
        root,
        text="♫",
        font=("Georgia",16,"bold"),
        command = toggle_music,
        bg="#1F3026",
        fg="#d4af37",
        activebackground="#5c4631",
        activeforeground="white",
        width=3
    )

    money_display = canvas.create_text(
         1060,
         45,
         text=f"🪙  ${detective_money}",
         font=("Courier New", 16, "bold"),
         fill="#d4af37",
         tags="money_display"
     )

    canvas.create_window(
         1150,
         45,
         window=music_button
     )

     #--------------------
     # FOLDERS AREA CREATION
     # -------------------


    main_menu_button = tk.Button(
        root,
        text="MAIN MENU",
        font=("Georgia", 11, "bold"),
        bg="#1F3026",
        fg="#d4af37",
        activebackground="#5c4631",
        activeforeground="white",
        cursor="hand2",
        command=return_to_main
    )

    canvas.create_window(
        100,
        45,
        window=main_menu_button
    )


    suspect_area = canvas.create_rectangle(
        30,
        470,
        200,
        720,
        fill="",
        stipple="",
        outline="",
        tags="suspects"
    )

    location_area = canvas.create_rectangle(
        210, 470, 400, 720,
        fill="",
        stipple="",
        outline="",
        tags="locations"
    )

    clue_area = canvas.create_rectangle(
        410, 470, 590, 720,
        fill="",
        stipple="",
        outline="",
        tags="clues"
    )

    evidence_area = canvas.create_rectangle(
        605, 470, 780, 720,
        fill="",
        stipple="",
        outline="",
        tags="evidence"
    )

    notes_area= canvas.create_rectangle(
        800, 470, 980,720,
        fill="",
        stipple="",
        outline="",
        tags="notes"
    )

    solve_area= canvas.create_rectangle(
        1000,480,1170,720,
        fill="",
        stipple="",
        outline="",
        tags="solve_area"
    )

    canvas.tag_bind(
        suspect_area,
        "<Button-1>",
        lambda event: open_suspects()
    )

    canvas.tag_bind(
        location_area,
        "<Button-1>",
        lambda event: open_locations()
    )

    canvas.tag_bind(
        clue_area,
        "<Button-1>",
        lambda event: open_clues()
    )

    canvas.tag_bind(
        evidence_area,
        "<Button-1>",
        lambda event: open_evidence()
    )

    canvas.tag_bind(
        notes_area,
        "<Button-1>",
        lambda event: open_notes()
    )

    canvas.tag_bind(
        solve_area,
        "<Button-1>",
        lambda event: open_solve_area()
    )

    canvas.tag_bind(
        suspect_area,
        "<Enter>",
        folder_enter
    )

    canvas.tag_bind(
        suspect_area,
        "<Leave>",
        folder_leave
    )

show_desk()

root.mainloop()
