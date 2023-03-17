import tkinter as tk
import random
import time

WIDTH = 800
HEIGHT = 600
TARGET_RADIUS = 30
SCREEN_MARGIN = 20

score = 0
highscore = 0
start_time = 0
time_limit = 30
sensitivity = 1  # added sensitivity variable with default value of 1

def new_target():
    global target_coords, target
    if 'target' in globals():
        canvas.delete(target)
    target_coords = [random.randint(SCREEN_MARGIN + TARGET_RADIUS, WIDTH - SCREEN_MARGIN - TARGET_RADIUS), 
                     random.randint(SCREEN_MARGIN + TARGET_RADIUS, HEIGHT - SCREEN_MARGIN - TARGET_RADIUS)]
    target = canvas.create_oval(target_coords[0] - TARGET_RADIUS, target_coords[1] - TARGET_RADIUS, 
                                target_coords[0] + TARGET_RADIUS, target_coords[1] + TARGET_RADIUS, 
                                fill="red")

def click_target(event):
    global score, target, target_coords, highscore
    if abs(event.x - target_coords[0]) < TARGET_RADIUS*sensitivity and abs(event.y - target_coords[1]) < TARGET_RADIUS*sensitivity:
        score += 1
        if score > highscore:
            highscore = score
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
        score_label.config(text=f"Score: {score}")
        canvas.delete(target)
        new_target()
    else:
        pass

def update_timer():
    global start_time
    elapsed_time = time.time() - start_time
    remaining_time = time_limit - elapsed_time
    if remaining_time <= 0:
        canvas.delete("all")
        score_label.config(text=f"Final score: {score}")
        highscore_label.config(text=f"Highscore: {highscore}")
        restart_button.pack()
        return
    time_label.config(text=f"Time remaining: {int(remaining_time)}")
    root.after(100, update_timer)

def update_sensitivity(value):
    global sensitivity
    sensitivity = float(value)

root = tk.Tk()
root.title("Aim Trainer")
root.attributes("-fullscreen", True)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

score_label = tk.Label(root, text=f"Score: {score}")
score_label.pack()

highscore_label = tk.Label(root, text=f"Highscore: {highscore}")
highscore_label.pack()

time_label = tk.Label(root, text=f"Time remaining: {time_limit}")
time_label.pack()

sensitivity_label = tk.Label(root, text="Sensitivity")
sensitivity_label.pack()

sensitivity_scale = tk.Scale(root, from_=0.5, to=2, resolution=0.1, orient="horizontal", command=update_sensitivity)
sensitivity_scale.set(sensitivity)
sensitivity_scale.pack()

new_target()

canvas.bind("<Button-1>", click_target)

start_time = time.time()
update_timer()

restart_button = tk.Button(root, text="Restart", command=lambda: [canvas.delete("all"), restart_game()])
restart_button.pack()
restart_button.pack_forget()

def restart_game():
    global score, start_time
    score = 0
    start_time = time.time()
    score_label.config(text=f"Score: {score}")
    new_target()
    update_timer()
    restart_button.pack_forget()

root.mainloop()
