from tkinter import *
from PIL import Image, ImageTk
import json

from GraphStructure.tsp_initializer import tsp_executor
from algorithms.held_karp import *

algorithms = {"REC_HELD_KARP": recursive_held_karp, "DYN_HELD_KARP": dynamic_held_karp, "PARA_HELD_KARP": parallel_held_karp}


def load_preferences():
    with open('resources/preferences.json5') as json_data:
        preferences = json.load(json_data)
        return preferences


def save_preferences(preferences):
    with open('resources/preferences.json5', 'w') as json_data:
        json.dump(preferences, json_data)


def latitude_to_pixel(lat):
    return int(- 6649.230906 * lat + 325167.1262024)  # y in the app


def longitude_to_pixel(lng):
    return int(4370.486107 * lng - 9764.321537)  # x in the app


class GlobalButton(Button):
    def __init__(self, father, font_color, color, **kw):
        super().__init__(father,
                         font=("Arial", 15),
                         width=10,
                         fg=font_color,
                         bg=color,
                         activebackground=font_color,
                         activeforeground=color,
                         relief=GROOVE,
                         **kw)


class AlgoRadioButton(Radiobutton):
    def __init__(self, father, text, var, font_color, color, **kw):
        super().__init__(father,
                         text=text,
                         variable=var,
                         value=text,
                         bg=color,
                         fg=font_color,
                         selectcolor=color,
                         activebackground=color,
                         activeforeground=font_color,
                         **kw)


class ChoiceLabel(Label):
    def __init__(self, father, text, font_color, color, **kw):
        super().__init__(father,
                         text=text,
                         borderwidth=0,
                         bg=color,
                         fg=font_color,
                         font=("Arial", 12),
                         **kw)


class BarBarGUI(Tk):
    def __init__(self):
        self.pref = load_preferences()
        self.active_page = self.start_page
        self.color, self.font_color, self.label_mode = self.load_color()
        super().__init__()
        self.var = StringVar()
        self.geometry('1100x600')
        self.title("BarBar")
        self.configure(background=self.color)
        self.maxsize(1300, 600)
        self.minsize(1300, 600)
        self.add_menubar()
        self.start_page()

    def load_color(self):
        mode = self.pref['preferences']
        if mode == 'dark':
            return 'gray20', 'white', 'Light'
        else:
            return 'white', 'black', 'Dark'

    def refresh_pane(self):
        for child in self.winfo_children():
            child.destroy()

    def change_mode(self, option_menu):
        mode = self.pref['preferences']
        if mode == 'dark':
            self.pref['preferences'] = 'light'
            save_preferences(self.pref)
            option_menu.entryconfigure(0, label="Dark Mode")
        else:
            self.pref['preferences'] = 'dark'
            save_preferences(self.pref)
            option_menu.entryconfigure(0, label="Light Mode")
        self.refresh_pane()
        self.color, self.font_color, self.label_mode = self.load_color()
        self.configure(background=self.color)
        self.active_page()

    def add_menubar(self):
        menubar = Menu(self)  # create the menu bar
        # add the options buttons
        option_menu = Menu(menubar, tearoff=0)
        option_menu.add_command(label=self.label_mode + " Mode",
                                command=lambda: self.change_mode(option_menu))
        menubar.add_separator()
        option_menu.add_command(label="Exit", command=self.quit)
        # give label
        menubar.add_cascade(label="Options", menu=option_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help Index", )
        help_menu.add_command(label="About...", )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def action(self, error_label, city_map, position_entry, nb_bar_entry, price_entry, result):
        try:
            algorithm = algorithms[self.var.get()]
            address = position_entry.get()
            bar_number = nb_bar_entry.get()
            price = price_entry.get()
            error_label.configure(text="")
            coords, result_text = tsp_executor(algorithm, address, bar_number, price)
            result.configure(state=NORMAL)
            result.insert(END, result_text)
            result.configure(state=DISABLED)
            self.trace_graph(city_map, coords)
        except IndexError:
            self.error(error_label)
            # TODO: Remove the following line
            self.trace_graph(city_map, [(2.338028, 48.861147), (2.35005, 48.852937)])

    def error(self, error_label):
        error_label.configure(text="Error")

    def trace_graph(self, city_map, coords):
        pixel_coords = self.coords_to_pixels(coords)
        for i in range(len(pixel_coords) - 1):
            x1 = pixel_coords[i][0]
            y1 = pixel_coords[i][1]
            x2 = pixel_coords[i + 1][0]
            y2 = pixel_coords[i + 1][1]
            city_map.create_oval(x1 - 1, y1 - 1, x1 + 1, y1 + 1, width=8, outline='blue')
            city_map.create_oval(x2 - 1, y2 - 1, x2 + 1, y2 + 1, width=8, outline='blue')
            city_map.create_line(x1, y1, x2, y2, arrow='last', capstyle='round', width=4, fill=self.color)

    def coords_to_pixels(self, coords):
        pixel_coords = []
        for i in range(len(coords)):
            x = longitude_to_pixel(coords[i][0])
            y = latitude_to_pixel(coords[i][1])
            pixel_coords.append((x, y))
        return pixel_coords

    def search_page(self):
        self.refresh_pane()
        self.add_menubar()
        self.active_page = self.search_page
        control_panel = Frame(self, width=400, bd=3, relief=GROOVE, bg=self.color)
        control_panel.grid(row=0, column=0, sticky='nsew')

        city_map = Canvas(self, width=700, bd=3, relief=GROOVE, bg=self.color)  # 700*600
        load = Image.open("resources/" + "city_map.png")
        image = load.resize((800, 600), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        city_map.create_image(0, 0, image=img, anchor=NW)
        city_map.image = img
        city_map.grid(row=0, column=1, sticky='nsew')

        position_label = ChoiceLabel(control_panel, "Position", self.font_color, self.color)
        position_entry = Entry(control_panel, width=21, bd=3, font=("Arial", 12))
        position_label.pack()
        position_entry.pack(padx=10, pady=10)

        nb_bar_label = ChoiceLabel(control_panel, "Number of Bars", self.font_color, self.color)
        nb_bar_entry = Spinbox(control_panel, bd=3, font=("Arial", 12), from_=2, to=100, wrap=True, state="readonly")
        nb_bar_label.pack()
        nb_bar_entry.pack(padx=10, pady=10)

        price_label = ChoiceLabel(control_panel, "Price", self.font_color, self.color)
        price_entry = Entry(control_panel, width=21, bd=3, font=("Arial", 12))
        price_label.pack()
        price_entry.pack(padx=10, pady=10)

        algorithm_label = ChoiceLabel(control_panel, "Algorithm", self.font_color, self.color)
        algorithm_label.pack()
        self.var.set("REC_HELD_KARP")
        for key in algorithms:
            choice = AlgoRadioButton(control_panel, key, self.var, self.font_color, self.color)
            choice.pack()

        error_label = ChoiceLabel(control_panel, "", self.font_color, self.color)
        result = Text(control_panel, relief=GROOVE, width=50, height=200, padx=0, pady=0, state=DISABLED)

        validate_choice = GlobalButton(control_panel, self.font_color, self.color, text="NEXT",
                                       command=lambda: self.action(error_label, city_map, position_entry, nb_bar_entry, price_entry, result))

        validate_choice.pack(padx=10, pady=10)
        error_label.pack(padx=10, pady=10)
        result.pack()

        self.grid_rowconfigure(0, minsize=200, weight=1)
        self.grid_columnconfigure(0, minsize=200, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_page(self):
        self.refresh_pane()
        self.add_menubar()
        self.active_page = self.start_page
        zoom = 0.3
        load = Image.open("resources/" + self.pref['preferences'] + "BarBar.jpg")
        pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])
        image = load.resize((pixels_x, pixels_y), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        img = Label(self, image=render, borderwidth=0)
        img.image = render
        enter_app = GlobalButton(self, self.font_color, self.color, text="ENTER", command=self.search_page)
        quit_app = GlobalButton(self, self.font_color, self.color, text="QUIT", command=self.quit)
        enter_app.place(relx=0.5, rely=0.45, anchor=CENTER)
        img.place(relx=0.5, rely=0, anchor=N)
        quit_app.place(relx=0.5, rely=0.55, anchor=CENTER)


if __name__ == "__main__":
    app = BarBarGUI()
    app.mainloop()
