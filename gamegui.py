
import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk, ImageSequence
import pygame  
from pymongo import MongoClient
from tkinter import ttk

pygame.mixer.init()


logged_in_username = None

def open_game_zone():
    global logged_in_username
    logged_in_username = username_entry.get()  
    login_screen.destroy()
    main_game_screen()

def login():
    # Kết nối tới MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['mario']
    users_collection = db['users']
    
    
    username = username_entry.get()
    password = password_entry.get()
    
    
    user = users_collection.find_one({"username": username, "password": password})
    
    
    if user:
        open_game_zone()
    else:
        messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")
    
    
    client.close()

def main_game_screen():
    global root
    root = tk.Tk()
    root.title("Game Zone")
    
    pygame.mixer.music.load("mario_music.mp3")
    pygame.mixer.music.play(-1)
    
    root.attributes('-fullscreen', True)
    root.configure(bg='black')

    
    user_label = tk.Label(root, text=f"Xin chào, {logged_in_username}", font=('Arial', 16), bg='black', fg='white')
    user_label.place(x=root.winfo_screenwidth() - 200, y=10)

    label = tk.Label(root, text="Chọn Trò Chơi của Bạn", font=('Arial', 48), bg='black', fg='white')
    label.pack(pady=20)

    button_width = 20
    snake_button = tk.Button(root, text="Rank", font=('Arial', 24), command=get_score,
                             bg='red', activebackground='blue', fg='white', width=button_width)
    snake_button.pack(pady=10)

    mario_button = tk.Button(root, text="Mario Bros", font=('Arial', 24), command=play_mario,
                             bg='red', activebackground='blue', fg='white', width=button_width)
    mario_button.pack(pady=10)

    gif_label = tk.Label(root, bg='black')
    gif_label.pack(pady=20)

    def play_gif():
        gif_image = Image.open("mario.gif")
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]

        def update(index):
            frame = frames[index]
            gif_label.configure(image=frame)
            root.after(100, update, (index + 1) % len(frames))

        update(0)

    play_gif()

    root.bind("<Escape>", exit_fullscreen)
    root.mainloop()

def get_score():
    pygame.mixer.music.stop()

    
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client['mario']
        collection = db['leaderboard']
        
        top_scores = list(collection.find().sort("score", -1))

        unique_scores = []
        seen = set()
        for player in top_scores:
            identifier = (player.get('name'), player.get('score'))
            if identifier not in seen:
                seen.add(identifier)
                unique_scores.append(player)
            if len(unique_scores) == 10:
                break

        if not unique_scores:
            messagebox.showinfo("Thông báo", "Không có dữ liệu điểm nào để hiển thị.")
            return

    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến MongoDB: {e}")
        return

    top_score_window = tk.Toplevel(root)
    top_score_window.title("Top Scores")
    top_score_window.geometry("400x400")
    top_score_window.configure(bg='black')

    title_label = tk.Label(top_score_window, text="Top 10 Scores", font=('Arial', 24), bg='black', fg='white')
    title_label.pack(pady=20)

    columns = ("Rank", "Player Name", "Score")
    tree = ttk.Treeview(top_score_window, columns=columns, show="headings", height=10)
    tree.heading("Rank", text="Rank")
    tree.heading("Player Name", text="Player Name")
    tree.heading("Score", text="Score")

    tree.column("Rank", anchor="center", width=50)
    tree.column("Player Name", anchor="center", width=200)
    tree.column("Score", anchor="center", width=100)

    for idx, player in enumerate(unique_scores):
        tree.insert("", "end", values=(idx + 1, player.get('name', 'Unknown'), player.get('score', 0)))

    tree.pack(pady=10)

    client.close()
    
def play_mario():
    pygame.mixer.music.stop()
    with open('error_log.txt', 'w') as f:
        subprocess.Popen(['D:/LTPYTHON/GameGui/mario_level_1.exe'], stderr=f, stdout=f)

def exit_fullscreen(event):
    root.destroy()

login_screen = tk.Tk()
login_screen.title("Login")
login_screen.geometry("800x600")

screen_width = login_screen.winfo_screenwidth()
screen_height = login_screen.winfo_screenheight()
x_position = (screen_width // 2) - (800 // 2)
y_position = (screen_height // 2) - (600 // 2)
login_screen.geometry(f"800x600+{x_position}+{y_position}")
login_screen.configure(bg='black')

title_label = tk.Label(login_screen, text="Đăng Nhập", font=('Arial', 36), bg='black', fg='white')
title_label.pack(pady=40)

tk.Label(login_screen, text="Tên đăng nhập:", font=('Arial', 18), bg='black', fg='white').pack(pady=10)
username_entry = tk.Entry(login_screen, font=('Arial', 18))
username_entry.pack(pady=10)

tk.Label(login_screen, text="Mật khẩu:", font=('Arial', 18), bg='black', fg='white').pack(pady=10)
password_entry = tk.Entry(login_screen, show="*", font=('Arial', 18))
password_entry.pack(pady=10)

login_button = tk.Button(login_screen, text="Đăng nhập", font=('Arial', 18), command=login,
                         bg='red', activebackground='blue', fg='white')
login_button.pack(pady=40)

login_screen.mainloop()


