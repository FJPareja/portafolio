import tkinter as tk
from tkinter import messagebox

class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD App")

        self.entries_frame = tk.Frame(root)
        self.entries_frame.pack(padx=10, pady=5)

        self.name_label = tk.Label(self.entries_frame, text="Nombre:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.entries_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.age_label = tk.Label(self.entries_frame, text="Edad:")
        self.age_label.grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(self.entries_frame)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.add_button = tk.Button(self.button_frame, text="Agregar", command=self.add_data)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.display_button = tk.Button(self.button_frame, text="Mostrar", command=self.display_data)
        self.display_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Limpiar", command=self.clear_entries)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        self.data_listbox = tk.Listbox(root, width=50)
        self.data_listbox.pack(padx=10, pady=5)

        self.data = []

    def add_data(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        if name and age:
            self.data.append((name, age))
            self.clear_entries()
            messagebox.showinfo("Éxito", "Datos agregados correctamente.")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def display_data(self):
        self.data_listbox.delete(0, tk.END)
        for item in self.data:
            self.data_listbox.insert(tk.END, f"Nombre: {item[0]}, Edad: {item[1]}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
