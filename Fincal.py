from PIL import Image, ImageTk
import tkinter as tk 
from tkinter import ttk, PhotoImage
import webbrowser
import time
from time import sleep
import random
import os
import winsound
from tkinter import messagebox
from scapy.all import IP, TCP, sr1
import ipaddress

root = tk.Tk()
root.title("FinanceCalc Pro Max Ultra")
root.geometry("600x500")
root.resizable(False, True)
bitmap_filename = "iconbitmap.ico"
bitmap_current_dir = os.path.dirname(os.path.abspath(__file__))
bitmap_file_path = os.path.join(bitmap_current_dir, "design", bitmap_filename)
root.iconbitmap(bitmap_file_path)



def aktien_append():
    global aktien_button, chosen_investments
    if "aktien" in chosen_investments:
        chosen_investments.remove("aktien")
        aktien_button.config(fg="black", relief="raised")
        print(chosen_investments)
    else:
        chosen_investments.append("aktien")
        aktien_button.config(fg="green", relief="sunken")
        print(chosen_investments)

def immobilien_append():
    global immobilien_button, chosen_investments
    if "immobilien" in chosen_investments:
        chosen_investments.remove("immobilien")
        immobilien_button.config(fg="black", relief="raised")
        print(chosen_investments)
    else:
        chosen_investments.append("immobilien")
        immobilien_button.config(fg="green", relief="sunken")
        print(chosen_investments)

def edelmetalle_append():
    global edelmetalle_button, chosen_investments
    if "edelmetalle" in chosen_investments:
        chosen_investments.remove("edelmetalle")
        edelmetalle_button.config(fg="black", relief="raised")
        print(chosen_investments)
    else:
        chosen_investments.append("edelmetalle")
        edelmetalle_button.config(fg="green", relief="sunken")
        print(chosen_investments)

def anleihen_append():
    global anleihen_button, chosen_investments
    if "anleihen" in chosen_investments:
        chosen_investments.remove("anleihen")
        anleihen_button.config(fg="black", relief="raised")
        print(chosen_investments)
    else:
        chosen_investments.append("anleihen")
        anleihen_button.config(fg="green", relief="sunken")
        print(chosen_investments)

def go_to_chatgpt():
    webbrowser.open("chatgpt.com")

def ergebnisse_ausgeben():
    global ergebnis_liste, y, last_time_label, text_last_time_error, text_better_worse, sounds
    for w in root.winfo_children():
        w.destroy()

    last_time_label = tk.Label(root, text="")
    last_time_label.place(x=300, y=480, anchor="center")

    title_label = tk.Label(root, text="""Jahr  |  Startkapital  |  Rendite (%)  |  Endkapital
                                      -------------------------------------------------------""")
    title_label.place(x=300, y=50, anchor="center")

    y = 70

    for ergebnis in ergebnis_liste:

        label = tk.Label(root, text=ergebnis)
        label.place(x=300, y=y, anchor="center")

        y += 30

    back = tk.Button(root, text="Zurück", command=main_menu)
    back.place(x=570, y=480, anchor="center")
    
    file = get_controls_dir("last_invest.txt")
    with open(file) as f:
        firstline = f.readline().rstrip()

    print(firstline)
    
    try:
        int_firstline = int(firstline)

    except ValueError:
        text_last_time_error = "Es ist ein Fehler beim Vergleich zum letzten Investment aufgetreten."
        def type_error(index=0):
            global last_time_label, text_last_time_error
            if index < len(text_last_time_error):
                last_time_label.config(text=last_time_label.cget("text") + text_last_time_error[index])
                root.after(50, type_error, index + 1)
        type_error()

    if gesamtverdienst > int_firstline:
        key_better_worse = "besser"
        fg = "green"
    else:
        key_better_worse = "schlechter"
        fg = "red"

    text_better_worse = f"  Insgesamt war dein Profit {key_better_worse} als letztes mal."

    def type_comparission(index=0):
        global text_better_worse, last_time_label
        if index < len(text_better_worse):
            last_time_label.config(text=last_time_label.cget("text") + text_better_worse[index], fg=fg)
            root.after(50, type_comparission, index + 1)
    type_comparission()

    with open(file, "w") as datei:
        datei.write(str(gesamtverdienst))

    if gesamtverdienst > 0:
        print("Gewinn gemacht")
        if sounds:
            sound = get_sound_dir("wow.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        global y_bizhar, bizhar_laughing_label, text_bizhar
        y_bizhar = y + 35
        y_pic = y + 15
        y_summary = y + 20

        bizhar_laughing_label = tk.Label(root, text="")
        bizhar_laughing_label.place(x=300, y=y_bizhar, anchor="center")

        summary_label = tk.Label(root, text="Zusammenfassung mit BI:")
        summary_label.place(x=300, y=y_summary, anchor="center")

        file_path = get_file_dir("ai.png")  
        pic = Image.open(file_path).resize((25, 25))
        bizhar_laughing_label_image = ImageTk.PhotoImage(pic)

        bizhar_laughing_pic_label = tk.Label(root, image=bizhar_laughing_label_image)
        bizhar_laughing_pic_label.place(x=190, y=y_pic)

        bizhar_laughing_pic_label.image = bizhar_laughing_label_image

        text_bizhar = "HA HA HA HA HA HA HA HA"

        if sounds:
            sound = get_sound_dir("spongebob-fail.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

        def bizhar_laughing(index=0):
            global bizhar_laughing_label, text_bizhar
            if index < len(text_bizhar):
                bizhar_laughing_label.config(text=bizhar_laughing_label.cget("text") + text_bizhar[index])
                root.after(50, bizhar_laughing, index + 1)
        bizhar_laughing()

def simulate_year(K0, r, o):
    z = random.randint(-2, 2)
    return K0 * (1 + (r + o * z))

def calculate():
    global int_startkapital, int_laufzeit, chosen_investments, investment_params, ergebnis_liste, called_by_ai

    ergebnis_liste = []

    count_investments = len(chosen_investments)
    if called_by_ai:
        pass
    elif count_investments == 0:
        value_error_label.config(text="Du musst mindestens ein Investment auswählen!", fg="red")
        value_error_label.place(y=370)
        sound = get_sound_dir("nope-sound.wav")
        winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
        return

    investment_params = {
    "aktien":      {"r": 0.15, "o": 0.15},
    "immobilien": {"r": 0.08, "o": 0.10},
    "anleihen":   {"r": 0.03, "o": 0.05},
    "edelmetalle":{"r": 0.05, "o": 0.12},
    }

    single_budget = int_startkapital / count_investments
    
    capitals = {name: single_budget for name in chosen_investments}

    for year in range(1, int_laufzeit +1):
        total = 0

        year_start = sum(capitals.values())

        for name in capitals:
            params = investment_params[name]
            capitals[name] = simulate_year(capitals[name], params["r"], params["o"])

            year_end = sum(capitals.values())
            year_return = (year_end - year_start) / year_start * 100

        ergebnis_liste.append(f"{year:>4}   | {year_start:>12,.2f} | {year_return:>10.2f}% | {year_end:>12,.2f}")

    endkapital = sum(capitals.values())
    global gesamtverdienst
    gesamtverdienst = int(endkapital) - int_startkapital
    ergebnis_liste.append(f"\nZusammenfassung: {endkapital:,.2f}€")
    ergebnis_liste.append(f"\nGewinn/Verlust: {gesamtverdienst:,.2f}€")

    ergebnisse_ausgeben()

def get_file_dir(file_pic):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(current_dir, "design", file_pic)
    return file_dir

def get_sound_dir(file_sound):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(current_dir, "sounds", file_sound)
    return file_dir

def get_controls_dir(control_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(current_dir, "controls", control_file)
    return file_dir

def anlageklassen():
    global startkapital_info_label, laufzeit_entry, laufzeit_button, euro_sign, aktien_button, immobilien_button, anleihen_button, edelmetalle_button, chosen_investments, called_by_ai, casino_button
    laufzeit_entry.destroy()
    laufzeit_button.destroy()
    euro_sign.destroy()

    chosen_investments = []

    startkapital_info_label.config(text="Wähle eine oder mehrere Anlageklassen aus")
    startkapital_info_label.place(y=250)

    aktien_button = tk.Button(root, text="Aktien", command=aktien_append)
    aktien_button.place(x=150, y=300, anchor="center")

    immobilien_button = tk.Button(root, text="Immobilien", command=immobilien_append)
    immobilien_button.place(x=450, y=300, anchor="center")

    anleihen_button = tk.Button(root, text="Anleihen", command=anleihen_append)
    anleihen_button.place(x=150, y=350, anchor="center")

    edelmetalle_button = tk.Button(root, text="Edelmetalle", command=edelmetalle_append)
    edelmetalle_button.place(x=450, y=350, anchor="center")

    file_path = get_file_dir("ausr.png")
    ausrechnen_resize = Image.open(file_path).resize((50, 50))
    ausrechnen_button_pic = ImageTk.PhotoImage(ausrechnen_resize)

    called_by_ai = False
    ausrechnen_button = tk.Button(root, image=ausrechnen_button_pic, borderwidth=0, highlightthickness=0, cursor="hand2", command=calculate)
    ausrechnen_button.place(x=300, y=300, anchor="center")

    ausrechnen_button.image = ausrechnen_button_pic



def laufzeit_check():
    global value_error_label, startkapital_info_label, laufzeit_entry, int_laufzeit, sounds
    laufzeit = laufzeit_entry.get()
    try:
        if int(laufzeit) > 0:
            int_laufzeit = int(laufzeit)
            anlageklassen()
        else:
            value_error_label.config(text="Die Laufzeit darf nicht negativ sein!", fg="red")
            if sounds:
                sound = get_sound_dir("nope-sound.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except ValueError:
        value_error_label.config(text="Die Eingabe darf nur auf Zahlen bestehen!", fg="red")
        if sounds:
            sound = get_sound_dir("nope-sound.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

def laufzeit():
    global value_error_label, startkapital_entry,  startkapital_button, startkapital_info_label, premium_button, credits_button, button_disabled_info, laufzeit_entry, laufzeit_button, euro_sign
    startkapital_entry.destroy()
    startkapital_button.destroy()
    value_error_label.config(text="")

    euro_sign.config(text="Jahre")

    premium_button.config(state=tk.DISABLED)
    credits_button.config(state=tk.DISABLED)

    button_disabled_info = tk.Label(root, text="Funktionen sind eingeschränkt bis der Vorgang beendet ist")
    button_disabled_info.place(x=300, y=480, anchor="center")
    
    startkapital_info_label.config(text="Laufzeit")

    laufzeit_entry = ttk.Entry(root, width=25)
    laufzeit_entry.place(x=300, y=300, anchor="center")

    file_path = get_file_dir("continue.png")
    pic = Image.open(file_path).resize((30, 30))
    continue_image = ImageTk.PhotoImage(pic)

    laufzeit_button = tk.Button(root, image=continue_image, borderwidth=0, highlightthickness=0, cursor="hand2", command=laufzeit_check)
    laufzeit_button.place(x=300, y=330, anchor="center")

    laufzeit_button.image = continue_image


def check_startkapital():
    global startkapital_entry, value_error_label, int_startkapital, sounds
    startkapital = startkapital_entry.get()
    try:
        if int(startkapital) > 0:
            int_startkapital = int(startkapital)
            laufzeit()
        else:
            if sounds:
                value_error_label.config(text="Das Startkapital darf nicht negativ sein!", fg="red")
                sound = get_sound_dir("nope-sound.wav")
                winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except ValueError:
        value_error_label.config(text="Die Eingabe darf nur auf Zahlen bestehen!", fg="red")
        if sounds:
            sound = get_sound_dir("nope-sound.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

def show_credits():
    global credits_label, back_button
    for widget in root.winfo_children():
        widget.destroy()
    credits_label = tk.Label(root, text="Fast alles: Maxi | Design der Bilder: ChatGPT (der süße 💕)")
    credits_label.place(x=300, y=100, anchor="center")

    back_button = tk.Button(root, text="Zurück zum Menü", command=main_menu)
    back_button.pack()

    mdm_button = tk.Button(root, text="Mitarbeiter des Monats (nicht von Lennart geklaut):", command=go_to_chatgpt)
    mdm_button.place(x=300, y=250, anchor="center")

    file_path = get_file_dir("mdm.jpg")
    mdm_logo = Image.open(file_path)
    mdm_logo = mdm_logo.resize((200, 200))
    mdm = ImageTk.PhotoImage(mdm_logo)

    mdm_logo_label = tk.Label(root, image=mdm)
    mdm_logo_label.place(x=300, y=400, anchor="center")
    mdm_logo_label.image = mdm

class settings:
    def impressum():
        webbrowser.open("https://notyoucrack.wixsite.com/finance-calculator-p")
        main_menu()

def on_music_toggle():
    global var_music, sounds, mute_label

    file = get_controls_dir("music_control.txt")
    if var_music.get():
        control = open(file, "w")
        control.close()

        sounds = False

        file = get_file_dir("mute.jpg")
        pic = Image.open(file).resize((30, 30))
        mute_image = ImageTk.PhotoImage(pic)
        
        mute_label.config(image=mute_image)
        mute_label.image = mute_image
    else:
        if os.path.isfile(file):
            os.remove(file)
            sounds = True

            file = get_file_dir("unmute.png")
            pic = Image.open(file).resize((30, 30))
            unmute_image = ImageTk.PhotoImage(pic)

            mute_label.config(image=unmute_image)
            mute_label.image = unmute_image

        else:
            pass

def settings_gui():
    for w in root.winfo_children():
        w.destroy()

    impressum = tk.Button(root, text="Impressum", command=settings.impressum)
    impressum.pack()

    global mute_label
    mute_label = tk.Label(root)
    mute_label.place(x=30, y=470, anchor="center")

    file = get_controls_dir("music_control.txt")
    if os.path.isfile(file):
        value = 1
        file = get_controls_dir("music_control.txt")
        pic = Image.open(get_file_dir("mute.jpg")).resize((30, 30))
        mute_image = ImageTk.PhotoImage(pic)

        mute_label.config(image=mute_image)
        mute_label.image = mute_image

    else:
        value = 0
        file = get_controls_dir("music_control.txt")
        pic = Image.open(get_file_dir("unmute.png")).resize((30, 30))
        unmute_image = ImageTk.PhotoImage(pic)

        mute_label.config(image=unmute_image)
        mute_label.image = unmute_image

    global var_music
    var_music = tk.IntVar(value=value)
    checkbox_music = tk.Checkbutton(root, text="Musik stummschalten", variable=var_music, command=on_music_toggle)
    checkbox_music.place(x=300, y=350, anchor="center")

    file_path = get_file_dir("back.png")
    pic = Image.open(file_path).resize((50, 50))
    back_arrow_image = ImageTk.PhotoImage(pic)

    back = tk.Button(root, image=back_arrow_image, highlightthickness=0, borderwidth=0, cursor="hand2", command=main_menu)
    back.place(x=300, y=250, anchor="center")

    back.image = back_arrow_image

class ai:
    global answer_label, ai_button1, ai_button2, portscanner_open_ports, ip_entry, scan_button
    @staticmethod
    def testdurchlauf():

        answer = "Gerne! Hier dein Testdurchlauf."
        def type_text(index=0):
            global int_startkapital, int_laufzeit, chosen_investments, called_by_ai
            if index < len(answer):
                answer_label.config(text=answer_label.cget("text") + answer[index])
                root.after(50, type_text, index + 1)
            else:
                int_startkapital = random.randint(500, 10000)
                int_laufzeit = random.randint(1, 10)
                chosen_investments_example = ["immobilien", "aktien", "edelmetalle", "anleihen"]
                chosen_investments = []
                random_invest1 = random.choice(chosen_investments_example)
                chosen_investments.append(random_invest1)
                chosen_investments_example.remove(random_invest1)
                random_invest2 = random.choice(chosen_investments_example)
                chosen_investments.append(random_invest2)
                chosen_investments_example.remove(random_invest2)

                called_by_ai = True

                root.after(500, calculate())
        type_text()

    @staticmethod
    def portscanner():
        global ip_entry, scan_button, answer_label
        ai_button1.destroy()
        ai_button2.destroy()

        answer_label.config(text="Klar! Trage die IP-Adresse ein, die du scannen möchtest.")


        ip_entry = ttk.Entry(root, width=30)
        ip_entry.place(x=300, y=250, anchor="center")
        scan_button = tk.Button(root, text="Scan starten", command=lambda: ai.start_portscan(ip_entry.get()))
        scan_button.place(x=300, y=275, anchor="center")
        
    @staticmethod
    def start_portscan(ip_address):
        global ip_entry, scan_button, portscanner_open_ports
        portscanner_open_ports = []
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            answer_label.config(text="Diese IP-Adresse ist ungültig.", fg="red")
            return
        
        answer_label.config(text="Starte Portscan...", fg="black")

        ip_entry.destroy()
        scan_button.destroy()

        for port in range(1, 1025):
            pkt = IP(dst=ip_address) / TCP(dport=port, flags="S")
            response = sr1(pkt, timeout=0.5, verbose=False)
            if response and response.haslayer(TCP) and response[TCP].flags == 0x12:
                portscanner_open_ports.append(port)
            else:
                pass

        if portscanner_open_ports == []:
            answer = f"Es wurden keine offenen Ports auf {ip_address} gefunden."
        else:
            answer = f"Offene Ports auf {ip_address}: {', '.join(map(str, portscanner_open_ports))}"

        portscanner_label = tk.Label(root, text="")
        portscanner_label.place(x=300, y=400, anchor="center")

        def type_text(index=0):
            if index < len(answer):
                portscanner_label.config(text=portscanner_label.cget("text") + answer[index])
                root.after(50, type_text, index + 1)

            else:
                print(portscanner_open_ports)

                if portscanner_open_ports != []:
                    global print_button
                    print_button = tk.Button(root, text="Ergebnisse ausdrucken", command=lambda: ai.portscanner_results(ip_address))
                    print_button.place(x=300, y=470, anchor="center")

                else:
                    pass
        type_text()


    @staticmethod
    def portscanner_results(ip_address):
        global print_button, portscanner_open_ports, answer_label

        current_dir = os.path.dirname(os.path.abspath(__file__))

        with open(f"{current_dir}\\portscanner_results.txt", "w") as file:
            file.write(f"Offene Ports bei {ip_address}:\n")
            for port in portscanner_open_ports:
                file.write(f"{port}\n")

        answer_label.config(text="")

        answer = "Die Ergebnisse wurden in 'portscanner_results.txt' gespeichert."

        def type_text(index=0):
            if index < len(answer):
                answer_label.config(text=answer_label.cget("text") + answer[index])
                root.after(50, type_text, index + 1)
        type_text()

        print_button.config(state=tk.DISABLED)

    @staticmethod
    def ai_chat():
        for w in root.winfo_children():
            w.destroy()

        global ip_entry, scan_button, ai_button1, ai_button2, answer_label

        answer_label = tk.Label(root, text="")
        answer_label.place(x=300, y=220, anchor="center")

        file_path = get_file_dir("ai_advertise.png")
        pic = Image.open(file_path).resize((200, 200))
        ai_advertise_image = ImageTk.PhotoImage(pic)

        ai_adversitement = tk.Label(root, image=ai_advertise_image)
        ai_adversitement.pack()
        ai_adversitement.image = ai_advertise_image

        ai_button1 = tk.Button(root, text="Ich möchte einen Test Durchlauf mit zufälligen Zahlen.", command=ai.testdurchlauf)
        ai_button1.place(x=300, y=300, anchor="center")

        ai_button2 = tk.Button(root, text="Starte einen Portscanner", command=ai.portscanner)
        ai_button2.place(x=300, y=350, anchor="center")

        ai_back = tk.Button(root, text="Zurück", command=main_menu)
        ai_back.place(x=570, y=490, anchor="center")

    @staticmethod
    def ai_assistant():
        for w in root.winfo_children():
            w.destroy()
        file_path = get_file_dir("ai_advertise.png")
        pic = Image.open(file_path).resize((400, 400))
        ai_advertise_image = ImageTk.PhotoImage(pic)

        ai_adversitement = tk.Label(root, image=ai_advertise_image)
        ai_adversitement.pack()
        ai_adversitement.image = ai_advertise_image

        file_path = get_file_dir("start_chat.png")
        pic = Image.open(file_path).resize((150, 75))
        start_chat_image = ImageTk.PhotoImage(pic)

        start_chat = tk.Button(root, image=start_chat_image, highlightthickness=0, borderwidth=0, cursor="hand2", command=ai.ai_chat)
        start_chat.place(x=300, y=455, anchor="center")
        start_chat.image = start_chat_image

        ai_back_button = tk.Button(root, text="Zurück", command=main_menu)
        ai_back_button.place(x=570, y=480, anchor="center")

def main_menu():
    global startkapital_entry, value_error_label, credits_label, back_button, startkapital_button, startkapital_info_label, premium_button, credits_button, euro_sign
    for widget in root.winfo_children():
        widget.destroy()

    file_path = get_file_dir("menu_pic.png")
    pic = Image.open(file_path)
    pic = pic.resize((600, 250))
    menu_pic = ImageTk.PhotoImage(pic)

    settings_button = tk.Button(root, image=menu_pic, borderwidth=0, highlightthickness=0, cursor="hand2", command=settings_gui)
    settings_button.place(x=300, y=100, anchor="center")

    settings_button.image = menu_pic

    startkapital_entry = ttk.Entry(root, width=25)
    startkapital_entry.place(x=300, y=300, anchor="center")

    startkapital_info_label = tk.Label(root, text="Startkapital")
    startkapital_info_label.place(x=300, y=280, anchor="center")

    euro_sign = tk.Label(root, text="€")
    euro_sign.place(x=395, y=300, anchor="center")

    file_path = get_file_dir("continue.png")
    pic = Image.open(file_path).resize((30, 30))
    continue_image = ImageTk.PhotoImage(pic)

    startkapital_button = tk.Button(root, image=continue_image, borderwidth=0, highlightthickness=0, cursor="hand2", command=check_startkapital)
    startkapital_button.place(x=300, y=330, anchor="center")

    startkapital_button.image = continue_image

    value_error_label = tk.Label(root, text="", fg="red")
    value_error_label.place(x=300, y=360, anchor="center")

    premium_button = tk.Button(root, text="Premium kaufen", command=show_premium_popup)
    premium_button.place(x=300, y=400, anchor="center")

    credits_button = tk.Button(root, text="Credits", command=show_credits)
    credits_button.place(x=300, y=440, anchor="center")

    file_path = get_file_dir("ai.png")
    pic = Image.open(file_path).resize((50, 50))
    bizhar_ai_image = ImageTk.PhotoImage(pic)

    bizhar_ai_button = tk.Button(root, image=bizhar_ai_image, borderwidth=0, highlightthickness=0, cursor="hand2", command=ai.ai_assistant)
    bizhar_ai_button.place(x=565, y=465, anchor="center")

    bizhar_ai_button.image = bizhar_ai_image

    speech_bubble = tk.Label(root, text="""   BI
    Assistent""")
    speech_bubble.place(x=500, y=465, anchor="center")

def on_checkbox_toggle():
    global var_checkbox
    if var_checkbox.get():
        path = get_controls_dir("popupcontrol.txt")
        control = open(path, "w")
        control.close()
    else:
        path = get_controls_dir("popupcontrol.txt")
        if os.path.isfile(path):
            os.remove(path)
        else:
            pass

def show_premium_popup():
    global var_checkbox, sounds
    popup = tk.Toplevel(root)
    popup.title("FinanceCalc Pro Max Ultra +")
    popup.geometry("400x300")
    popup.resizable(False, False)
    file_path = get_file_dir("popupicon.ico")
    popup.iconbitmap(file_path)

    popup.grab_set()

    file_path = get_file_dir("popup.png")
    img = Image.open(file_path)
    img = img.resize((170, 170), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    img_label = tk.Label(popup, image=photo)
    img_label.image = photo 
    img_label.pack(pady=10)

    text = tk.Label(popup, text="Möchtest du ein FinanceCalc Pro Max Ultra + Abo abschließen?")
    text.pack(pady=10)

    button_frame = tk.Frame(popup)
    button_frame.pack(pady=15)

    def yes():
        if sounds:
            sound = get_sound_dir("applepay.wav")
            winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
        remove_labels()
        popup.destroy()

    def no():
        messagebox.showinfo(title="Außer Betrieb", message="Dieser Knopf ist gerade leider außer Betrieb. Die Alternative ist natürlich bereit für sie.", icon="error")

    yes = tk.Button(button_frame, text="Ja (239,99€ /m)", width=15, command=yes).pack(side="left", padx=10)
    no = tk.Button(button_frame, text="Nein", width=15, command=no).pack(side="right", padx=10)

    file_path = get_controls_dir("popupcontrol.txt")
    if os.path.isfile(file_path):
        var_checkbox = tk.IntVar(value=1)
    else:
        var_checkbox = tk.IntVar(value=0)
    checkbox = tk.Checkbutton(popup, text="Zeig mir das nicht wieder.", variable=var_checkbox, command=on_checkbox_toggle)
    checkbox.pack(padx=20)

    def on_closing_popup():
        if messagebox.askyesno("Beenden", "Wirklich schließen?"):
            remove_labels()
        

    popup.protocol("WM_DELETE_WINDOWS", on_closing_popup)

def remove_labels():
    global label_start 
    label_start.destroy()
    main_menu()

def start_loading():
    global label_start, sounds
    if sounds:
        sound_path = get_sound_dir("open.wav")
        print(sound_path)
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    file_path = get_file_dir("startpic.png")
    pic_start = Image.open(file_path)
    pic_start = pic_start.resize((600, 500))
    start_pic = ImageTk.PhotoImage(pic_start)

    label_start = tk.Label(root, image=start_pic)
    label_start.pack()

    label_start.image = start_pic
    file_path = get_controls_dir("popupcontrol.txt")
    if os.path.isfile(file_path):
        remove_labels()
    else: 
        show_premium_popup()

def on_closing():
    if messagebox.askyesno("Beenden", "Wirklich schließen?"):
        root.destroy()

def define_sounds():
    global sounds
    file = get_controls_dir("music_control.txt")
    if os.path.isfile(file):
        sounds = False
        start_loading()
    else:
        sounds = True
        start_loading()

root.protocol("WM_DELETE_WINDOW", on_closing)

define_sounds()
root.mainloop()