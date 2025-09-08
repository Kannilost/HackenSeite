import tkinter as tk
from tkinter import ttk
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import math
import time  
from PIL import Image, ImageTk

def starte_binärfenster():
    fenster = tk.Tk()
    fenster.title("Binärstrom – 80% Power")

    breite = fenster.winfo_screenwidth()
    hoehe = fenster.winfo_screenheight()

    fenster_breite = int(breite * 0.5)
    fenster_hoehe = int(hoehe * 0.5)
    x_pos = int((breite - fenster_breite) / 2)
    y_pos = int((hoehe - fenster_hoehe) / 2)
    fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{x_pos}+{y_pos}")
    fenster.configure(bg="black")

    textfeld = tk.Text(fenster, bg="black", fg="lime", font=("Courier", 12), borderwidth=0, highlightthickness=0)
    textfeld.pack(expand=True, fill="both")

    def binärstrom():
        zeichen_menge = ''
        for _ in range(300):
            zeichen = random.choice(['0', '1'])
            zeichen_menge += zeichen
            if random.random() < 0.02:
                zeichen_menge += '\n'
        textfeld.insert("end", zeichen_menge)
        textfeld.see("end")
        fenster.after(4, binärstrom)

    binärstrom()
    return fenster

def starte_graphfenster():
    graph_fenster = tk.Toplevel()
    graph_fenster.title("Live-Scroll-Graph")
    graph_fenster.geometry("600x400+100+100")

    fig = Figure(figsize=(6, 4), dpi=100, facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_facecolor("black")
    ax.tick_params(colors='white')
    ax.set_title("Live-Daten", color='white')
    for spine in ax.spines.values():
        spine.set_color('white')

    x_data = []
    y_data = []
    line, = ax.plot([], [], color='red')

    canvas = FigureCanvasTkAgg(fig, master=graph_fenster)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Update-Animation
    def update(frame):
        next_x = x_data[-1] + 1 if x_data else 0
        next_y = random.randint(0, 100)
        x_data.append(next_x)
        y_data.append(next_y)

        if len(x_data) >= 100:
            line.set_data(x_data[-100:], y_data[-100:])
            ax.set_xlim(x_data[-100], x_data[-1])
        else:
            line.set_data(x_data, y_data)
            ax.set_xlim(0, 100)

        ax.set_ylim(0, 120)
        canvas.draw()
        return line,

    # starten Fensterobjekt speichern
    graph_fenster.anim = animation.FuncAnimation(
        fig, update, interval=100, cache_frame_data=False
    )

    return graph_fenster

def starte_neuronfenster():
    neuron_fenster = tk.Toplevel()
    neuron_fenster.title("Neuronales Netz")
    neuron_fenster.geometry("600x600+200+200")
    neuron_fenster.configure(bg="#add8e6")  

    def zeichne_radialverlauf():
        center_x, center_y = 300, 300
        max_radius = 300
        steps = 30

        for i in range(steps):
            r = int(max_radius * (1 - i / steps))
            mix = i / steps
            r_blau = int((25 * (1 - mix)) + (30 * mix))     
            g_blau = int((25 * (1 - mix)) + (144 * mix))    
            b_blau = int((112 * (1 - mix)) + (255 * mix))   
            farbe = f"#{r_blau:02x}{g_blau:02x}{b_blau:02x}"

            canvas.create_oval(center_x - r, center_y - r, center_x + r, center_y + r,
                           fill=farbe, outline=farbe, tags="verlauf")
        canvas.tag_lower("verlauf")  # Hintergrund nach unten


    # Haupt-Canvas
    canvas = tk.Canvas(neuron_fenster, bg="#191970", highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    zeichne_radialverlauf()

    punkte = []
    verbindungen = []  # Diese verbindungsteile für Fakeneuronales Netz
    maus_down_zeit = 0  # Zeitstempel für Mausklick (für die Unterscheidung clicken/halten)
    punktradius = 12
    mindestabstand = punktradius * 2.5

    for _ in range(20):
        max_versuche = 100
        for _ in range(max_versuche):
            x = random.randint(60, 540)
            y = random.randint(60, 540)
            kollidiert = False
            for _, px, py, *_ in punkte:
                dist = math.hypot(x - px, y - py)
                if dist < mindestabstand:
                    kollidiert = True
                    break
            if not kollidiert:
                angle = random.uniform(0, 2 * math.pi)
                dx = math.cos(angle) * 0.8
                dy = math.sin(angle) * 0.8
                punkt = canvas.create_oval(x - punktradius, y - punktradius, x + punktradius, y + punktradius,
                                           fill="white", outline="cyan", width=3)
                arrow = canvas.create_line(x, y, x + dx * 15, y + dy * 15, arrow=tk.LAST, fill="orange", width=2)
                punkte.append([punkt, x, y, dx, dy, arrow])
                break

    startpunkt = None
    ziehlinie = None

    def finde_punkt(x, y):
        for i, (punkt_id, px, py, _, _, _) in enumerate(punkte):
            if abs(x - px) < punktradius and abs(y - py) < punktradius:
                return (px, py, i)
        return None

    def maus_down(event):
        nonlocal startpunkt, ziehlinie, maus_down_zeit
        maus_down_zeit = time.time()  # Zeitpunkt merken
        result = finde_punkt(event.x, event.y)
        if result:
            px, py, _ = result
            startpunkt = result
        ziehlinie = canvas.create_line(px, py, event.x, event.y, fill="gray", width=2)

    def maus_bewegung(event):
        nonlocal ziehlinie
        if ziehlinie and startpunkt:
            canvas.coords(ziehlinie, startpunkt[0], startpunkt[1], event.x, event.y)

    def maus_up(event):
        nonlocal startpunkt, ziehlinie, maus_down_zeit
        klick_dauer = time.time() - maus_down_zeit

        if startpunkt:
            endpunkt = finde_punkt(event.x, event.y)
            if endpunkt and endpunkt != startpunkt:
                x1, y1, i1 = startpunkt
                x2, y2, i2 = endpunkt
                linie = canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
                verbindungen.append([linie, i1, i2])
            startpunkt = None

        if ziehlinie:
            canvas.delete(ziehlinie)
            ziehlinie = None

        # Wenn Klick sehr kurz war → Verbindung löschen
        if klick_dauer < 0.2:  
            result = finde_punkt(event.x, event.y)
            if result:
                _, _, index = result
                zu_loeschen = []
                for v in verbindungen:
                    linie_id, i1, i2 = v
                    if index == i1 or index == i2:
                        canvas.delete(linie_id)
                        zu_loeschen.append(v)
                for v in zu_loeschen:
                    verbindungen.remove(v)

    canvas.bind("<ButtonPress-1>", maus_down)
    canvas.bind("<B1-Motion>", maus_bewegung)
    canvas.bind("<ButtonRelease-1>", maus_up)

    def bewege_punkte():
        for i, punkt in enumerate(punkte):
            punkt_id, x, y, dx, dy, arrow_id = punkt
            x_neu = x + dx
            y_neu = y + dy

            x_neu = max(punktradius, min(x_neu, 600 - punktradius))
            y_neu = max(punktradius, min(y_neu, 600 - punktradius))

            kollidiert = False
            for j, anderer in enumerate(punkte):
                if i != j:
                    _, ax, ay, _, _, _ = anderer
                    dist = math.hypot(x_neu - ax, y_neu - ay)
                    if dist < punktradius * 2:
                        kollidiert = True
                        break

            if not kollidiert:
                canvas.coords(punkt_id, x_neu - punktradius, y_neu - punktradius,
                              x_neu + punktradius, y_neu + punktradius)
                punkt[1], punkt[2] = x_neu, y_neu

                arrow_len = 15
                x2 = x_neu + dx * arrow_len
                y2 = y_neu + dy * arrow_len
                canvas.coords(arrow_id, x_neu, y_neu, x2, y2)
        
        # aktualisieren
        for linie_id, i1, i2 in verbindungen:
            x1, y1 = punkte[i1][1], punkte[i1][2]
            x2, y2 = punkte[i2][1], punkte[i2][2]
            canvas.coords(linie_id, x1, y1, x2, y2)

        canvas.after(50, bewege_punkte)

    # Hintergrundanimation
    background_lines = []
    for _ in range(30):
        x1 = random.randint(0, 600)
        y1 = random.randint(0, 600)
        x2 = x1 + random.randint(-50, 50)
        y2 = y1 + random.randint(-50, 50)

        grauwert = random.randint(0, 100) 
        hex_grau = f"#{grauwert:02x}{grauwert:02x}{grauwert:02x}"

        line = canvas.create_line(x1, y1, x2, y2, fill=hex_grau, width=1, tags="hintergrundlinie")
        canvas.tag_lower(line) 
        background_lines.append([line, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)])
    canvas.tag_raise("hintergrundlinie", "verlauf")

    def pulse_background():
        for line_data in background_lines:
            line_id = line_data[0]

            current_width = canvas.itemcget(line_id, "width")
            current_width = float(current_width)

            new_width = 0.5 + abs(math.sin(time.time() * 2)) * 1.5

            canvas.itemconfig(line_id, width=new_width)
        canvas.after(100, pulse_background)
    
    def animate_background():
        for line_data in background_lines:
            line_id, dx, dy = line_data
            coords = canvas.coords(line_id)
            if len(coords) == 4:
                x1, y1, x2, y2 = coords
                x1 += dx
                y1 += dy
                x2 += dx
                y2 += dy

            for val in [x1, x2]:
                if val < 0 or val > 600:
                    dx *= -1
            for val in [y1, y2]:
                if val < 0 or val > 600:
                    dy *= -1

            canvas.coords(line_id, x1, y1, x2, y2)
            line_data[1], line_data[2] = dx, dy

        canvas.after(50, animate_background)
    animate_background()
    pulse_background()

    def rotiere_richtungen():
        winkel = math.radians(60)
        cos_w = math.cos(winkel)
        sin_w = math.sin(winkel)
        for punkt in punkte:
            dx, dy = punkt[3], punkt[4]
            dx_neu = dx * cos_w - dy * sin_w
            dy_neu = dx * sin_w + dy * cos_w
            punkt[3], punkt[4] = dx_neu, dy_neu
        canvas.after(3000, rotiere_richtungen)

    bewege_punkte()
    rotiere_richtungen()

    return neuron_fenster

def starte_weltkarte_hackerstil():
    weltkarte_fenster = tk.Toplevel()
    weltkarte_fenster.title("Weltkarte – Hacker Style")
    weltkarte_fenster.geometry("800x500")
    weltkarte_fenster.configure(bg="black")

    bild = Image.open("weltkarte_hackerstyle.jpg")  
    bild = bild.resize((800, 500), Image.Resampling.LANCZOS)
    bild_tk = ImageTk.PhotoImage(bild)

    canvas = tk.Canvas(weltkarte_fenster, width=800, height=500, bg="black", highlightthickness=0)
    canvas.pack()

    canvas.create_image(0, 0, anchor="nw", image=bild_tk)
    canvas.image = bild_tk  #referenz 

    aktive_zeichen = []
    def bewege_zeichen():
        neue_liste = []
        for text_id in aktive_zeichen:
            coords = canvas.coords(text_id)
            if coords:
                x, y = coords
                canvas.move(text_id, 0, 1.5) 
                neue_liste.append(text_id)
        aktive_zeichen[:] = neue_liste
        canvas.after(50, bewege_zeichen)

    def binärregen():
        for _ in range(20):
            x = random.randint(0, 800)
            y = random.randint(0, 500)
            zeichen = random.choice(["0", "1"])
            farbe = "#00FF00" if random.random() < 0.8 else "#00AA00"
            text_id = canvas.create_text(x, y, text=zeichen, fill=farbe, font=("Courier", 10))
            aktive_zeichen.append(text_id)

            canvas.after(5000, lambda tid=text_id: canvas.delete(tid))
        weltkarte_fenster.after(100, binärregen)

    binärregen()
    bewege_zeichen()
    return weltkarte_fenster

def starte_downloadfenster():
    download_fenster = tk.Tk()
    download_fenster.title("Download läuft...")
    download_fenster.geometry("600x200")
    download_fenster.configure(bg="black")

    blink_text = tk.StringVar(value="Lade geheime Weltkarte...")
    label = tk.Label(download_fenster, textvariable=blink_text, fg="red", bg="black", font=("Courier", 16))
    label.pack(pady=20)

    progress = ttk.Progressbar(download_fenster, orient="horizontal", length=500, mode="determinate")
    progress.pack(pady=10)
    progress["maximum"] = 100
    progress["value"] = 0

    ok_button = tk.Button(download_fenster, text="OK", state="disabled", command=lambda: [download_fenster.destroy(), starte_alle_fenster()])
    ok_button.pack(pady=10)

    def blink():
        current = blink_text.get()
        blink_text.set("" if current else "Lade geheime Weltkarte...")
        download_fenster.after(500, blink)

    def lade_fortschritt():
        if progress["value"] < 100:
            progress["value"] += 2
            download_fenster.after(100, lade_fortschritt)
        else:
            blink_text.set("Download abgeschlossen.")
            ok_button.config(state="normal")

    def starte_alle_fenster():
        binär_fenster = starte_binärfenster()
        graph_fenster = starte_graphfenster()
        neuron_fenster = starte_neuronfenster()
        weltkarte_fenster = starte_weltkarte_hackerstil()
        binär_fenster.mainloop()

    blink()
    lade_fortschritt()
    download_fenster.mainloop()

def starte_loginfenster():
    login_fenster = tk.Tk()
    login_fenster.title("Zugangskontrolle")
    login_fenster.geometry("400x200")
    login_fenster.configure(bg="grey20")

    tk.Label(login_fenster, text="Benutzername:", fg="red", bg="grey20", font=("Courier", 12)).pack(pady=5)
    benutzer_entry = tk.Entry(login_fenster, font=("Courier", 12))
    benutzer_entry.pack()

    tk.Label(login_fenster, text="Passwort:", fg="red", bg="grey20", font=("Courier", 12)).pack(pady=5)
    passwort_entry = tk.Entry(login_fenster, show="*", font=("Courier", 12))
    passwort_entry.pack()

    def prüfe_login():
        benutzer = benutzer_entry.get()
        passwort = passwort_entry.get()
        if benutzer == "Kanni" and passwort == "Kanni5826":
            login_fenster.destroy()
            starte_downloadfenster()
        else:
            login_fenster.destroy()
            exit()  

    tk.Button(login_fenster, text="Login", command=prüfe_login, font=("Courier", 12)).pack(pady=20)
    login_fenster.mainloop()

starte_loginfenster()