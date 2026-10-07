import os
import sys
import tkinter as tk
import pygame
import navigation


from math import ceil
from PIL import Image, ImageTk, ImageDraw
from save_manager import load_data, save_data

pygame.mixer.init()

correct_suspect = "FELIX MONROE - THE SCREENWRITER"
correct_location = "THE VELVET SCREENING ROOM"
correct_weapon = "BRASS FILM REEL CANISTER"


player_data = load_data()
detective_money = player_data["detective_money"]
case_reward = 500
# Already solved before? Then the reward was already paid.
case_reward_claimed = player_data.get("case_001_solved", False)


music_on=True
detective_notes = ""

#==============================
# HELPER FOR TESTING
# =============================
def resource_path(relative_path):

    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


page_sound = pygame.mixer.Sound(resource_path("sounds/open_folder_sound.mp3"))
page_sound.set_volume(0.5)
money_sound = pygame.mixer.Sound(resource_path("sounds/money_sound.mp3"))
money_sound.set_volume(0.5)

# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("Murdle - Case #001")
root.geometry("1200x900")
root.configure(bg="#2b2118")


# ==============================
# TITLE
# ==============================

title = tk.Label(
    root,
    text="M U R D L E",
    font=("Georgia", 30, "bold"),
    fg="#e8d5b5",
    bg="#2b2118"
)

title.pack(pady=30)


subtitle = tk.Label(
    root,
    text="CASE #001 — THE MYSTERY BEGINS",
    font=("Georgia", 13),
    fg="#c7b08a",
    bg="#2b2118"
)

subtitle.pack()

def return_to_main():

    navigation.go_to(root, "main")


def open_next_case():

    navigation.go_to(root, "case_002")


def open_store():

    pygame.mixer.music.stop()

    navigation.go_to(root, "store")


def change_page(next_screen):
    play_page_sound()
    next_screen()

def play_page_sound():
    page_sound.play()

def play_desk_music():

    # Don't restart it every time show_desk() runs
    if not pygame.mixer.music.get_busy():

        pygame.mixer.music.load(resource_path(
            "sounds/studio_sound.mp3")
        )

        # Volume from 0.0 to 1.0
        pygame.mixer.music.set_volume(0.25)

        # -1 means loop forever
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


def create_scrollable_screen():

    # ==============================
    # MAIN CANVAS
    # ==============================

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


    # ==============================
    # SCROLLBAR
    # ==============================

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


    # ==============================
    # CONTENT FRAME
    # ==============================

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


    # ==============================
    # UPDATE SCROLL REGION
    # ==============================

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

# ==============================
# OPEN SUSPECT FILE
# ==============================

def open_suspects():

    play_page_sound()

    # Remove everything currently on the screen
    for widget in root.winfo_children():
        widget.destroy()

    content = create_scrollable_screen()


    # File title
    file_title = tk.Label(
        content,
        text="SUSPECT FILE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    file_title.pack(fill="x", pady=(40, 20))


    # Suspect information
    suspect = tk.Label(
        content,
        text="""
VICTIM: VICTOR MARLOWE- THE FILM PRODUCER

    Found dead shortly before the private screening of
    his studio's newest picture. Three people had reasons
    to want him gone, and everyone insists they were
    somewhere else when the studio lights went dark.

---------------------------------------------------------


NAME: VIVIENNE VALE — THE SILENT FILM STAR

    Once the studio's biggest actress. Marlowe planned to
    replace her in his next production and had threatened
    to reveal a scandal from her past.

HEIGHT: 5'7
DESCRIPTION:    BLACK HAIR
                HAZEL-GREEN EYES
                A TINY BEAUTY MARK UNDER HER LEFT EYE

=========================================================

NAME:   FELIX MONROE — THE SCREENWRITER

    A talented but frustrated writer who discovered
    Marlowe had been taking credit for his scripts.

HEIGHT: 5'10
DESCRIPTION:    WAVY CHESTNUT BROWN HAIR
                DARK BROWN EYES
                WEARS ROUND TORTOISESHELL GLASSES

=========================================================

NAME: CELIA STERLING — THE COSTUME DESIGNER

    Quiet and observant. Marlowe recently accused
    her of stealing expensive jewelry from the costume
    department, an accusation that could end her career.

HEIGHT: 5'3
DESCRIPTION:    BLACK HAIR
                PALE BLUE EYES
                OFTEN CARRIES MEASURING TAPE AND
                FABRIC SCISSORS IN THE HANDS

=========================================================

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



def open_evidence():

    play_page_sound()

    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()

    # ==============================
    # TITLE
    # ==============================

    title = tk.Label(
        content,
        text="EVIDENCE FILE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 5))


    subtitle = tk.Label(
        content,
        text="CASE #001 — ITEMS RECOVERED FROM THE SCENE",
        font=("Courier New", 12),
        fg="#5c4631",
        bg="#d8c49c"
    )

    subtitle.pack(pady=10)


    # ==============================
    # EVIDENCE
    # ==============================

    evidence_text = """
EVIDENCE ITEM #001

Brass Film Reel Canister —
Heavy enough to cause a fatal injury.


EVIDENCE ITEM #002

Silver Letter Opener —
Normally kept on Marlowe's office desk.


EVIDENCE ITEM #003

Crystal Champagne Bottle —
Taken from the studio's celebration table.


"""


    evidence_label = tk.Label(
        content,
        text=evidence_text,
        font=("Courier New", 13),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    evidence_label.pack(
        padx=80,
        pady=20
    )


    # ==============================
    # RETURN TO DESK
    # ==============================

    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=35)


def open_notes():

    play_page_sound()

    global detective_notes

    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()

    # ==============================
    # TITLE
    # ==============================

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
        text="CASE #001 — PERSONAL INVESTIGATION NOTES",
        font=("Courier New", 12),
        fg="#5c4631",
        bg="#d8c49c"
    )

    subtitle.pack(pady=10)


    # ==============================
    # NOTEBOOK
    # ==============================

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

    # ==============================
    # RETURN TO DESK
    # ==============================

    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=15)

def open_velvet_room():

    play_page_sound()

    # Clear current screen
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    # Make page scrollable
    content = create_scrollable_screen()


    # ==============================
    # TITLE
    # ==============================

    title = tk.Label(
        content,
        text="LOCATION FILE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 5))


    location_name = tk.Label(
        content,
        text="THE VELVET SCREENING ROOM",
        font=("Courier New", 20, "bold"),
        fg="#5c4631",
        bg="#d8c49c"
    )

    location_name.pack(pady=10)


    # ==============================
    # LOCATION IMAGE
    # ==============================

    velvet_room_image = Image.open(
        resource_path("assets/velvet_room.png")
    )

    velvet_room_image = velvet_room_image.resize(
        (500, 300)
    )

    velvet_room_photo = ImageTk.PhotoImage(
        velvet_room_image
    )


    image_label = tk.Label(
        content,
        image=velvet_room_photo,
        bg="#d8c49c"
    )

    image_label.image = velvet_room_photo

    image_label.pack(pady=20)


    # ==============================
    # DESCRIPTION
    # ==============================

    description = """
LOCATION REPORT

🎬 THE VELVET SCREENING ROOM

A private theater reserved for studio executives, stars,
and special guests. Deep crimson velvet seats face a silver
screen surrounded by heavy curtains.

Golden Art Deco lamps softly illuminate the dark wood-paneled
walls. An old projector operates from the back of the theater
during screenings.

Thick carpeting makes footsteps difficult to hear between the
rows. When the lights go down, the room becomes almost completely
dark.

"""


    description_label = tk.Label(
        content,
        text=description,
        font=("Courier New", 13),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    description_label.pack(
        padx=70,
        pady=20
    )


    # ==============================
    # BACK TO LOCATIONS
    # ==============================

    back_button = tk.Button(
        content,
        text="← BACK TO LOCATIONS",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(open_locations)
    )

    back_button.pack(pady=30)

def open_starlet_room():

    play_page_sound()

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()


    title = tk.Label(
        content,
        text="LOCATION FILE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 5))


    location_name = tk.Label(
        content,
        text="THE STARLET DRESSING ROOM",
        font=("Courier New", 20, "bold"),
        fg="#5c4631",
        bg="#d8c49c"
    )

    location_name.pack(pady=10)


    starlet_room_image = Image.open(
        resource_path("assets/starlet_room.png")
    )

    starlet_room_image = starlet_room_image.resize(
        (500, 300)
    )

    starlet_room_photo = ImageTk.PhotoImage(
        starlet_room_image
    )


    image_label = tk.Label(
        content,
        image=starlet_room_photo,
        bg="#d8c49c"
    )

    image_label.image = starlet_room_photo

    image_label.pack(pady=20)


    description = """
LOCATION REPORT

💄 THE STARLET DRESSING ROOM

An elegant backstage room where Starlight Studios' leading
actresses prepare. Bright vanity bulbs surround mirrors covered
with photographs and handwritten notes.

Perfumes, cosmetics, jewelry, and flowers crowd the dressing
tables. Sequined gowns and feathered costumes hang from brass
clothing racks.

Costume trunks and hatboxes are constantly moved between productions.
With so many personal belongings around, small objects can easily go
unnoticed.

"""


    description_label = tk.Label(
        content,
        text=description,
        font=("Courier New", 13),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    description_label.pack(
        padx=70,
        pady=20
    )


    back_button = tk.Button(
        content,
        text="← BACK TO LOCATIONS",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(open_locations)
    )

    back_button.pack(pady=30)

def open_producer_room():

    play_page_sound()

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()


    title = tk.Label(
        content,
        text="LOCATION FILE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 5))


    location_name = tk.Label(
        content,
        text="THE PRODUCER'S OFFICE",
        font=("Courier New", 20, "bold"),
        fg="#5c4631",
        bg="#d8c49c"
    )

    location_name.pack(pady=10)


    producer_room_image = Image.open(
        resource_path("assets/producer_room.png")
    )

    producer_room_image = producer_room_image.resize(
        (500, 300)
    )

    producer_room_photo = ImageTk.PhotoImage(
        producer_room_image
    )


    image_label = tk.Label(
        content,
        image=producer_room_photo,
        bg="#d8c49c"
    )

    image_label.image = producer_room_photo

    image_label.pack(pady=20)


    description = """
LOCATION REPORT


🥃 THE PRODUCER'S PRIVATE OFFICE

Victor Marlowe's luxurious office overlooks the grounds of
Starlight Studios.A large mahogany desk is covered with scripts,
contracts, and correspondence.

Bookshelves display awards, photographs, and memorabilia from
successful films.A crystal decanter and glasses sit beside his
private liquor cabinet.

Important studio documents are kept here, including valuable
contracts. Away from the busy studio halls, the office offers
complete privacy for sensitive conversations.

"""


    description_label = tk.Label(
        content,
        text=description,
        font=("Courier New", 13),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    description_label.pack(
        padx=70,
        pady=20
    )


    back_button = tk.Button(
        content,
        text="← BACK TO LOCATIONS",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(open_locations)
    )

    back_button.pack(pady=30)



def open_locations():

    play_page_sound()

    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Change background to old paper color
    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()

    # ==============================
    # FILE TITLE
    # ==============================

    title = tk.Label(
        content,
        text="LOCATION FILES",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 10))


    subtitle = tk.Label(
        content,
        text="CASE #001 — PLACES OF INTEREST",
        font=("Courier New", 13),
        fg="#5c4631",
        bg="#d8c49c"
    )

    subtitle.pack(pady=5)


    # ==============================
    # LOCATION 1
    # ==============================

    bathroom_button = tk.Button(
        content,
        text="📁  THE VELVET SCREENING ROOM",
        font=("Courier New", 14, "bold"),
        width=35,
        height=2,
        command=open_velvet_room
    )

    bathroom_button.pack(pady=15)


    # ==============================
    # LOCATION 2
    # ==============================

    bedroom_button = tk.Button(
        content,
        text="📁  THE STARLET DRESSING ROOM",
        font=("Courier New", 14, "bold"),
        width=35,
        height=2,
        command=open_starlet_room
    )

    bedroom_button.pack(pady=15)


    # ==============================
    # LOCATION 3
    # ==============================

    screening_button = tk.Button(
        content,
        text="📁  THE PRODUCER'S PRIVATE OFFICE",
        font=("Courier New", 14, "bold"),
        width=35,
        height=2,
        command=open_producer_room
    )

    screening_button.pack(pady=15)


    # ==============================
    # RETURN TO DESK
    # ==============================

    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=35)

def open_clues():

    play_page_sound()

    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()

    # ==============================
    # TITLE
    # ==============================

    title = tk.Label(
        content,
        text="CLUES & EVIDENCE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 10))


    subtitle = tk.Label(
        content,
        text="CASE #001 — INVESTIGATOR'S NOTES",
        font=("Courier New", 13),
        fg="#5c4631",
        bg="#d8c49c"
    )

    subtitle.pack(pady=10)


    # ==============================
    # CLUES
    # ==============================

    clues_text = """

    Clue #1 THE MISSING REEL
        The brass canister for Reel #4 is missing from the projection
        booth.

    Clue #2 THE TORN CONTRACT
        Pieces of Felix Monroe's original screenplay contract are discovered
        inside Marlowe's office fireplace.

    Clue #3 THE LIPSTICK GLASS
        A champagne glass carrying Vivienne's distinctive dark lipstick is
        sitting in the dressing room.

    Clue #4 THE PROJECTION LOG
        The projectionist recorded Reel #4 being loaded shortly before the
        screening but its canister was never returned.

    Clue #5 THE LETTER OPENER
        The silver letter opener is still sitting on Marlowe's desk and has
        no blood on it.

    Clue #6 THE FILM DUST
        Fine metallic dust from an old film canister is discovered on Felix's
        jacket sleeve.

    Clue #7 THE CHAMPAGNE BOTTLE
        Several witnesses remember the bottle remaining on the celebration
        table until after the body was discovered.

    Clue #8 THE TICKET STUB
        A torn screening-room ticket belonging to Felix is discovered beneath
        one of the red velvet seats.

"""


    clues_label = tk.Label(
        content,
        text=clues_text,
        font=("Courier New", 14),
        justify="left",
        fg="#2b2118",
        bg="#d8c49c"
    )

    clues_label.pack(
        padx=70,
        pady=20
    )


    # ==============================
    # RETURN BUTTON
    # ==============================

    back_button = tk.Button(
        content,
        text="← RETURN TO DESK",
        font=("Georgia", 12, "bold"),
        command=lambda: change_page(show_desk)
    )

    back_button.pack(pady=20)


def solve_case():

    play_page_sound()

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#d8c49c")

    content = create_scrollable_screen()



    title = tk.Label(
        content,
        text="SOLVE THE CASE",
        font=("Georgia", 28, "bold"),
        fg="#2b2118",
        bg="#d8c49c"
    )

    title.pack(pady=(40, 10))


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
        "VIVIENNE VALE - THE SILENT FILM STAR",
        "FELIX MONROE - THE SCREENWRITER",
        "CELIA STERLING - THE COSTUME DESIGNER"
    )

    suspect_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    suspect_menu.pack(pady=5)


    # ==============================
    # LOCATION CHOICE
    # ==============================

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
        "THE VELVET SCREENING ROOM",
        "THE STARLET DRESSING ROOM",
        "THE PRODUCER'S PRIVATE OFFICE"
    )

    location_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    location_menu.pack(pady=5)


    # ==============================
    # WEAPON CHOICE
    # ==============================

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
        "BRASS FILM REEL CANISTER",
        "SILVER LETTER OPENER",
        "CRYSTAL CHAMPAGNE BOTTLE"
    )

    weapon_menu.config(
        width=25,
        font=("Courier New", 12)
    )

    weapon_menu.pack(pady=5)

    #=================================
    # HELPER CONDITIONAL FOR MONEY REWARD
    # =================================

    # The NEXT CASE and STORE buttons only need to appear once
    buttons_shown = []

    def show_next_buttons():

        if buttons_shown:
            return

        buttons_shown.append(True)

        next_case_button = tk.Button(
            content,
            text="NEXT CASE",
            font=("Georgia", 14, "bold"),
            bg="#24382B",
            fg="#F1E5C8",
            cursor="hand2",
            command=open_next_case
        )

        next_case_button.pack(pady=10)

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
            player_data["case_001_solved"] = True

            save_data(player_data)
            money_sound.play()

            case_reward_claimed = True
            paid = True

        show_next_buttons()

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
                text=
                    ("CASE SOLVED! You caught the killer.\n\n"
                    "MOTIVE:\n"
                    "Marlowe had been taking credit for Felix's work\n"
                    "and was preparing to destroy the contract that proved\n"
                    "Felix had written the studio's successful films.\n\n"
                    + reward_text
                    ),
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
        font=("Georgia", 14),
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



def folder_enter(event):
    canvas.config(cursor="hand2")
    canvas.itemconfig(
            event.widget.find_withtag("current"),
            outline="",
            width=0
    )


def folder_leave(event):
    canvas.config(cursor="")
    canvas.itemconfig(
            event.widget.find_withtag("current"),
            outline="",
            width=0
        )


# ==============================
# SHOW DESK
# ==============================

def show_desk():

    # Remove everything currently on the screen
    for widget in root.winfo_children():
        widget.destroy()

    play_desk_music()


    # ==============================
    # CREATE CANVAS
    # ==============================
    canvas = tk.Canvas(
            root,
            width=1200,
            height=900,
            highlightthickness=0
        )

    canvas.pack()

    # ==============================
    # LOAD DETECTIVE DESK IMAGE
    # ==============================

    image = Image.open(resource_path("assets/detective_desk_bg.png.png"))

    image = image.resize((1200, 900))

    background = ImageTk.PhotoImage(image)


    # ==============================
    # PUT IMAGE ON CANVAS
    # ==============================

    canvas.create_image(
        0,
        0,
        image=background,
        anchor="nw"
    )
    #Keep the image in memory
    canvas.background = background


    #==============================
    # CREATE MUSIC ICON ON CANVAS
    # ============================

    music_button = tk.Button(
        root,
        text="♫",
        font=("Geogia", 16, "bold"),
        command=toggle_music,
        bg="#2b2118",
        fg="#d4af37",
        activebackground="#5c4631",
        activeforeground="white",
        width=3
    )

    canvas.create_window(
        1150,
        45,
        window=music_button
    )

    #==================================
    # CREATE MONEY ICON ON CANVAS
    # =================================

    money_display = canvas.create_text(
        1060,
        45,
        text=f"🪙  ${detective_money}",
        font=("Courier New", 16, "bold"),
        fill="#d4af37",
        tags="money_display"
    )



    #=============================
    # INSTRUCTIONS
    # ============================

    instruction = canvas.create_text(
        600,
        50,
        text="Click a case folder to investigate",
        font=("Courier New", 14, "bold"),
        fill="#2b2118",
        tags="instruction"
    )

    canvas.tag_raise("instruction")

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

    # ============================
    # SUSPECT CLICK AREA
    # ============================

    suspect_area = canvas.create_rectangle(
        200,
        290,
        460,
        510,
        fill="",
        stipple="",
        outline="",
        tags="suspects"
    )

    # ==============================
    # LOCATIONS AREA
    # ==============================

    location_area = canvas.create_rectangle(
        470, 280, 720, 500,
        fill="",
        stipple="",
        outline="",
        tags="locations"
    )


    # ==============================
    # CLUES AREA
    # ==============================

    clue_area = canvas.create_rectangle(
        730, 280, 980, 500,
        fill="",
        stipple="",
        outline="",
        tags="clues"
    )


    # ==============================
    # EVIDENCE AREA
    # ==============================

    evidence_area = canvas.create_rectangle(
        240, 520, 480, 740,
        fill="",
        stipple="",
        outline="",
        tags="evidence"
    )


    # ==============================
    # DETECTIVE NOTES AREA
    # ==============================

    notes_area = canvas.create_rectangle(
        500, 520, 740, 740,
        fill="",
        stipple="",
        outline="",
        tags="notes"
    )
    # ==============================
    # SOLVE AREA
    # ==============================

    solve_area = canvas.create_rectangle(
        780, 520,
        1000, 740,
        fill="",
        stipple="",
        outline="",
        tags="solve area"
    )



    # ==============================
    # MAKE FOLDERS CLICKABLE
    # ==============================

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
        lambda event: solve_case()
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


# ==============================
# START GAME
# ==============================

show_desk()

root.mainloop()
