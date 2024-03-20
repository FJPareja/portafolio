import requests
import tkinter as tk
from tkinter import messagebox
from io import BytesIO
from PIL import Image, ImageTk

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(pokemon_name_or_id):
    url = f"{base_url}pokemon/{pokemon_name_or_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        show_pokemon_info(data)
    else:
        messagebox.showerror("Error", f"No se pudo encontrar el Pokémon {pokemon_name_or_id}")

def show_pokemon_info(data):
    result_label.config(text=data["name"].upper())
    height_label.config(text="Altura: " + str(data["height"] / 10.0) + " m")  
    weight_label.config(text="Peso: " + str(data["weight"] / 10.0) + " kg")  

    types = [type_data["type"]["name"] for type_data in data["types"]]
    types_label.config(text="Tipos: " + ", ".join(types))


    sprite_url = data["sprites"]["front_default"]
    sprite_response = requests.get(sprite_url)
    sprite_data = Image.open(BytesIO(sprite_response.content))
    sprite = ImageTk.PhotoImage(sprite_data)
    sprite_label.config(image=sprite)
    sprite_label.image = sprite

def search_pokemon():
    pokemon_name_or_id = entry.get()
    get_pokemon_info(pokemon_name_or_id)

# The window!
window = tk.Tk()

window.title("Pokedex")
window.geometry("800x500")
window.configure(background = "crimson")

# Configure 4 rows and 3 columns.
window.rowconfigure([i for i in range(4)], minsize = 50, weight = 1)
window.columnconfigure([i for i in range(3)], minsize = 50, weight = 1)

### Name Frame
name_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 4)
label = tk.Label(name_frame, text = "Pokemon", font = ("Futura", 16))
# One of the few cases where you can mix pack() with grid().
label.pack()
name_frame.grid(row = 0, column = 0)

### Picture Frame

picture_frame = tk.Frame(window, relief = tk.SUNKEN, borderwidth = 2)
sprite_label = tk.Label(picture_frame, text = "Pokemon Picture Here", font = ("Futura", 16))
sprite_label.pack()
picture_frame.grid(row = 1, column = 0, rowspan = 2, sticky = "ns")

### Type Frame
type_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 2)
types_label = tk.Label(window, text="")
types_label.grid(row = 3, column = 0)


### Search Frame
search_frame = tk.Frame(window, relief = tk.RAISED, borderwidth = 2)

# Calling rowconfigure and columnfigure within the info_frame
# causes the contents of the frame (label) to be centered within it.
search_frame.columnconfigure([0,1,2,3], weight = 1)


entry = tk.Entry(window, width=70)
entry.grid(row = 0, column = 1, columnspan = 2)


search_button = tk.Button(window, text="Buscar", command=search_pokemon, font=("Futura", 16))
search_button.grid(row=0, column=3)

search_frame.grid(row = 0, column = 1, columnspan = 2, sticky = "ew")

### Info Frame
info_frame = tk.Frame(window, relief = tk.SUNKEN, borderwidth = 4)

# Calling rowconfigure and columnfigure within the info_frame
# causes the contents of the frame (label) to be centered within it.
info_frame.rowconfigure([0,1,2], weight = 1)
info_frame.columnconfigure([0,1], weight = 1)

## Various Information

# The Pokedex entry is long, so we'll let it take up two columns
result_label = tk.Label(info_frame, text = "Nombre", font = ("Futura", 16))
result_label.grid(row = 0, column = 0, columnspan = 2)

#height_label = tk.Label(window, text="")
#height_label.grid(row = 1, column = 0)

height_label = tk.Label(info_frame, text = "Height", font = ("Futura", 16))
height_label.grid(row = 1, column = 0)

weight_label = tk.Label(info_frame, text = "Weight", font = ("Futura", 16))
weight_label.grid(row = 1, column = 1)



info_frame.grid(row = 1, rowspan = 3, column = 1, columnspan = 2, sticky = "nsew")

# Run the App
window.mainloop()
