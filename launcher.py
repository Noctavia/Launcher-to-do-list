import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Fichiers de données
APP_FILE = "data/apps.json"
SETTINGS_FILE = "data/settings.json"

# Chargement des données
def load_data(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

# Sauvegarde des données
def save_data(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# Classe principale
class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Simple Launcher")
        self.root.geometry("600x400")
        self.root.configure(bg="#181818")

        # Chargement des applications et des paramètres
        self.apps = load_data(APP_FILE, [])
        self.settings = load_data(SETTINGS_FILE, {"theme": "dark", "favorites": []})

        # Interface
        self.create_widgets()
        self.refresh_app_list()

    # Interface utilisateur
    def create_widgets(self):
        # Barre de recherche
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.root, textvariable=self.search_var, bg="#303030", fg="white")
        search_entry.pack(fill="x", padx=10, pady=5)
        search_entry.bind("<KeyRelease>", lambda e: self.search_apps())

        # Liste des applications
        self.app_listbox = tk.Listbox(self.root, bg="#202020", fg="white", selectbackground="#00bcd4")
        self.app_listbox.pack(expand=True, fill="both", padx=10, pady=5)
        self.app_listbox.bind("<Double-1>", lambda e: self.launch_app())
        self.app_listbox.bind("<Button-3>", lambda e: self.toggle_favorite())

        # Boutons
        btn_frame = tk.Frame(self.root, bg="#181818")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="➕ Ajouter", command=self.add_app, bg="#4caf50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="🚀 Lancer", command=self.launch_app, bg="#2196f3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_app, bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="⚙️ Paramètres", command=self.open_settings, bg="#9c27b0", fg="white").pack(side="left", padx=5)

    # Rafraîchissement de la liste des applications
    def refresh_app_list(self):
        self.app_listbox.delete(0, tk.END)
        for app in self.apps:
            prefix = "⭐ " if app["name"] in self.settings["favorites"] else ""
            self.app_listbox.insert(tk.END, f"{prefix}{app['name']}")

    # Ajouter une application
    def add_app(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            name = simpledialog.askstring("Nom de l'application", "Entrez un nom pour l'application :")
            if name:
                self.apps.append({"name": name, "path": filepath})
                save_data(APP_FILE, self.apps)
                self.refresh_app_list()

    # Lancer une application
    def launch_app(self):
        selected = self.app_listbox.curselection()
        if selected:
            app = self.apps[selected[0]]
            try:
                os.startfile(app["path"])
                messagebox.showinfo("Succès", f"L'application {app['name']} a été lancée !")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lancer l'application : {e}")

    # Supprimer une application
    def delete_app(self):
        selected = self.app_listbox.curselection()
        if selected:
            del self.apps[selected[0]]
            save_data(APP_FILE, self.apps)
            self.refresh_app_list()

    # Ajouter/Retirer des favoris
    def toggle_favorite(self):
        selected = self.app_listbox.curselection()
        if selected:
            app_name = self.apps[selected[0]]["name"]
            if app_name in self.settings["favorites"]:
                self.settings["favorites"].remove(app_name)
            else:
                self.settings["favorites"].append(app_name)
            save_data(SETTINGS_FILE, self.settings)
            self.refresh_app_list()

    # Recherche d'applications
    def search_apps(self):
        query = self.search_var.get().lower()
        self.app_listbox.delete(0, tk.END)
        for app in self.apps:
            if query in app["name"].lower():
                prefix = "⭐ " if app["name"] in self.settings["favorites"] else ""
                self.app_listbox.insert(tk.END, f"{prefix}{app['name']}")

    # Paramètres
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Paramètres")
        settings_window.geometry("300x200")
        settings_window.configure(bg="#181818")

        theme_label = tk.Label(settings_window, text="Thème", fg="white", bg="#181818")
        theme_label.pack(pady=10)

        theme_btn = tk.Button(settings_window, text="Changer de thème", command=self.toggle_theme, bg="#00bcd4", fg="white")
        theme_btn.pack(pady=10)

    # Changement de thème
    def toggle_theme(self):
        self.settings["theme"] = "light" if self.settings["theme"] == "dark" else "dark"
        save_data(SETTINGS_FILE, self.settings)
        self.update_theme()

    # Appliquer le thème
    def update_theme(self):
        if self.settings["theme"] == "dark":
            self.root.configure(bg="#181818")
            self.app_listbox.configure(bg="#202020", fg="white")
        else:
            self.root.configure(bg="#f0f0f0")
            self.app_listbox.configure(bg="white", fg="black")
        self.refresh_app_list()

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
