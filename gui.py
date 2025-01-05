import tkinter as tk
from tkinter import ttk
from ncf import ncf_recommended
from cosine_similarity import cosine_recommended

root = tk.Tk()
root.title("Steam Recommender System")

window_width = 1280
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

label_title = ttk.Label(root, text='Steam Recommender System', font=("Open Sans", 14))
label_title.pack(padx=10, pady=10)

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill='x')

label_steam_id = ttk.Label(frame, text="Steam ID:", font=("Open Sans", 12))
label_steam_id.grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_steam_id = ttk.Entry(frame, width=40)
entry_steam_id.grid(row=1, column=1, padx=10, pady=5)
button_steam_id = ttk.Button(frame, text='Search NCF', width=15)
button_steam_id.grid(row=1, column=2, padx=10, pady=5)

label_game_title = ttk.Label(frame, text="Judul Game:", font=("Open Sans", 12))
label_game_title.grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_game_title = ttk.Entry(frame, width=40)
entry_game_title.grid(row=2, column=1, padx=10, pady=5)
button_game_title = ttk.Button(frame, text='Search Cosine', width=15)
button_game_title.grid(row=2, column=2, padx=10, pady=5)

label_user_preferences = ttk.Label(frame, text="Preferensi:", font=("Open Sans", 12))
label_user_preferences.grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_user_preferences = ttk.Entry(frame, width=40)
entry_user_preferences.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(frame, text="").grid(row=3, column=2, padx=10, pady=20)

table_frame = ttk.Frame(root)
table_frame.pack(padx=10, pady=10, fill='both')

scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
scrollbar.pack(side='right', fill='y')

recommendation_table = ttk.Treeview(table_frame, columns=("Name", "Price", "Publisher", "Developer", "Categories", "Genres", "Tags", "Score"), show='headings', yscrollcommand=scrollbar.set)
scrollbar.config(command=recommendation_table.yview)

recommendation_table.heading("Name", text="Name")
recommendation_table.heading("Price", text="Price")
recommendation_table.heading("Publisher", text="Publisher")
recommendation_table.heading("Developer", text="Developer")
recommendation_table.heading("Categories", text="Categories")
recommendation_table.heading("Genres", text="Genres")
recommendation_table.heading("Tags", text="Tags")
recommendation_table.heading("Score", text="Score")

recommendation_table.column("Name", width=220)
recommendation_table.column("Price", width=50)
recommendation_table.column("Publisher", width=100)
recommendation_table.column("Developer", width=100)
recommendation_table.column("Categories", width=200)
recommendation_table.column("Genres", width=200)
recommendation_table.column("Tags", width=200)
recommendation_table.column("Score", width=200)
recommendation_table.pack(fill='both', expand=True)

def get_ncf_recommendations():
    steam_id = entry_steam_id.get() 
    if not steam_id.isdigit():
        print("Invalid Steam ID")
        return

    recommendations_df = ncf_recommended(int(steam_id))

    for row in recommendation_table.get_children():
        recommendation_table.delete(row)

    for index, row in recommendations_df.iterrows():
        recommendation_table.insert("", "end", values=( row['name'], row['price'], row['publisher'], row['developer'], row['categories'], row['genres'], row['tags'], row['score']))
    
    entry_steam_id.delete(0, tk.END)

def get_cosine_recommendations():
    # game_title = entry_game_title.get()

    # close_match, recommended_games = cosine_recommended(game_title)

    game_title = entry_game_title.get().strip()
    user_preferences = entry_user_preferences.get().strip()

    if not game_title and not user_preferences:
        print("Tolong tambahkan game atau preferensi user.")
        return

    close_match, recommended_games = cosine_recommended(game_title, user_preferences)

    if close_match is None:
        print("Game tidak ditemukan!")
        return

    for row in recommendation_table.get_children():
        recommendation_table.delete(row)

    for game in recommended_games:
        recommendation_table.insert("", "end", values=( game['name'], game['price'], game['publisher'], game['developer'], game['categories'], game['genres'], game['tags'], game['score']))
    
    entry_game_title.delete(0, tk.END)
    entry_user_preferences.delete(0, tk.END)

button_steam_id.config(command=get_ncf_recommendations)
button_game_title.config(command=get_cosine_recommendations)

root.mainloop()