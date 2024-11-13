from PIL import Image, ImageDraw
import pystray
import threading
from tkinter import Tk, Label, Entry, Button, StringVar
import webbrowser
from flask import Flask

flask_thread_kwargs = {'host': '127.0.0.1', 'port': 5000,
                       'threaded': True, 'use_reloader': False, 'debug': False}

app = Flask(__name__)

data = {"nameA": "BUZZI", "nameB": "RODARI", "scoreA": 9, "scoreB": 2}
ip = "http://127.0.0.1:5000"
root = Tk()


def do_nothing():
    pass


root.protocol("WM_DELETE_WINDOW", do_nothing)


def set_ip():
    ip = ip_entry.get()
    port = port_entry.get()

    ip = f"http://{ip}:{port}"
    ipw.destroy()

    t1 = StringVar(root)
    t2 = StringVar(root)

    def get_ip():
        return ip

    team1_name = data["nameA"]
    team2_name = data["nameB"]
    team1_score = data["scoreA"]
    team2_score = data["scoreB"]

    def set_teams():
        global data
        data = {
            "nameA": str(t1.get().replace("-N", "<br>")),
            "nameB": str(t2.get().replace("-N", "<br>")),
            "scoreA": int(team1__score.cget("text")),
            "scoreB": int(team2__score.cget("text"))
        }
        print(data)

    # team 1
    team1 = Label(root, text="Nome 1:", width=5, height=1)
    team1.grid(row=0, column=0)

    team1_input = Entry(root, width=15, textvariable=t1)
    team1_input.insert(0, team1_name)
    team1_input.grid(row=0, column=1)

    team1__score = Label(root, text=team1_score, width=5, height=1)
    team1__score.grid(row=0, column=2)

    team1_plus = Button(root, text="+", command=lambda: team1__score.config(
        text=str(int(team1__score.cget("text")) + 1)), width=5, height=1)
    team1_plus.grid(row=0, column=3)

    team1_minus = Button(root, text="-", command=lambda: team1__score.config(
        text=str(int(team1__score.cget("text")) - 1)), width=5, height=1)
    team1_minus.grid(row=0, column=4)

    team_check_button = Button(
        root, text="Set", width=5, height=3, command=set_teams)
    team_check_button.grid(rowspan=2, row=0, column=5)

    # team 2
    team2 = Label(root, text="Nome 2:", width=5, height=1)
    team2.grid(row=1, column=0)

    team2_input = Entry(root, width=15, textvariable=t2)
    team2_input.insert(0, team2_name)
    team2_input.grid(row=1, column=1)

    team2__score = Label(root, text=team2_score, width=5, height=1)
    team2__score.grid(row=1, column=2)

    team2_plus = Button(root, text="+", command=lambda: team2__score.config(
        text=str(int(team2__score.cget("text")) + 1)), width=5, height=1)
    team2_plus.grid(row=1, column=3)

    team2_minus = Button(root, text="-", command=lambda: team2__score.config(
        text=str(int(team2__score.cget("text")) - 1)), width=5, height=1)
    team2_minus.grid(row=1, column=4)
    root.mainloop()


def get_ip_port() -> tuple:
    return ip.replace("http://", "").split(":")


# ip config window, only show at start
ipw = Tk()
ipw.protocol("WM_DELETE_WINDOW", do_nothing)

ipw.geometry("200x100")
ip, port = get_ip_port()
ip_label = Label(ipw, text="IP:")
ip_label.grid(row=0, column=0)

ip_entry = Entry(ipw)
ip_entry.insert(0, ip)
ip_entry.grid(row=0, column=1)

port_label = Label(ipw, text="Port:")
port_label.grid(row=1, column=0)

port_entry = Entry(ipw)
port_entry.insert(0, port)
port_entry.grid(row=1, column=1)

ip_button = Button(ipw, text="Connetti", command=set_ip)
ip_button.grid(row=2, column=1)


# get current data
@app.route('/feed', methods=["GET"])
def get_data():
    return data

# table to use inside obs studio


@app.route("/")
def index():
    return open("index.html", "r").read()


# create image for tray icon
def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

# destroy all windows
def quit_all():
    try:
        ipw.destroy()
    except:
        pass
    try:
        root.destroy()
    except:
        pass

# tray icon
icon = pystray.Icon(
    'Filippo Romani',
    icon=create_image(64, 64, 'black', 'yellow'),
    title='Filippo Romani',
    menu=pystray.Menu(
        pystray.MenuItem(
            'Website',
            lambda: webbrowser.open('https://filipporomani.it')
        ),
        pystray.MenuItem(
            'Quit',
            quit_all

        )

    )
)

# start threads
try:
    if __name__ == "__main__":
        flask_thread = threading.Thread(
            target=app.run, daemon=True, kwargs=flask_thread_kwargs).start()
        icon_run = threading.Thread(target=icon.run, daemon=True).start()
        ipw.mainloop()
finally:
    print('end')
