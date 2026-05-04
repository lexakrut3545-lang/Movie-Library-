import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.file_path = "movies.json"
        self.movies = self.load_data()

        # --- Поля ввода ---
        frame_input = tk.Frame(root, padx=10, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(frame_input)
        self.ent_title.grid(row=0, column=1)

        tk.Label(frame_input, text="Жанр:").grid(row=0, column=2)
        self.ent_genre = tk.Entry(frame_input)
        self.ent_genre.grid(row=0, column=3)

        tk.Label(frame_input, text="Год:").grid(row=1, column=0)
        self.ent_year = tk.Entry(frame_input)
        self.ent_year.grid(row=1, column=1)

        tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=1, column=2)
        self.ent_rating = tk.Entry(frame_input)
        self.ent_rating.grid(row=1, column=3)

        btn_add = tk.Button(frame_input, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
        frame_filter.pack(fill="x", padx=10)

        tk.Label(frame_filter, text="Жанр:").pack(side="left")
        self.flt_genre = tk.Entry(frame_filter)
        self.flt_genre.pack(side="left", padx=5)
        self.flt_genre.bind("<KeyRelease>", lambda e: self.apply_filter())

        tk.Label(frame_filter, text="Год:").pack(side="left")
        self.flt_year = tk.Entry(frame_filter)
        self.flt_year.pack(side="left", padx=5)
        self.flt_year.bind("<KeyRelease>", lambda e: self.apply_filter())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table(self.movies)

    def add_movie(self):
        title = self.ent_title.get()
        genre = self.ent_genre.get()
        year = self.ent_year.get()
        rating = self.ent_rating.get()

        # Валидация
        if not (title and genre and year and rating):
            return messagebox.showerror("Ошибка", "Заполните все поля!")

        if not year.isdigit():
            return messagebox.showerror("Ошибка", "Год должен быть числом!")

        try:
            r = float(rating.replace(',', '.'))
            if not (0 <= r <= 10): raise ValueError
        except ValueError:
            return messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")

        new_movie = {"title": title, "genre": genre, "year": year, "rating": str(r)}
        self.movies.append(new_movie)
        self.save_data()
        self.apply_filter()

        # Очистка полей
        for entry in [self.ent_title, self.ent_genre, self.ent_year, self.ent_rating]:
            entry.delete(0, tk.END)

    def apply_filter(self):
        g_val = self.flt_genre.get().lower()
        y_val = self.flt_year.get()
        filtered = [m for m in self.movies if g_val in m['genre'].lower() and y_val in m['year']]
        self.update_table(filtered)

    def update_table(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in data:
            self.tree.insert("", "end", values=(m['title'], m['genre'], m['year'], m['rating']))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
