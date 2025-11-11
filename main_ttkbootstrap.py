from tkinter import *
import os, math
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Segoe UI"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
is_paused = False
remaining_time = 0

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer, reps, is_paused, remaining_time
    if timer:
        window.after_cancel(timer)
    timer = None
    is_paused = False
    remaining_time = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Ready to Focus")
    check_marks.config(text="")
    reps = 0
    
    # Show start button, hide pause button
    start_button.grid(column=0, row=3, padx=10)
    pause_button.grid_remove()
    
    # Enable time adjustment controls
    work_scale.config(state=NORMAL)
    break_scale.config(state=NORMAL)
    progress_bar['value'] = 0

# ---------------------------- TIMER PAUSE ------------------------------- # 
def pause_timer():
    global is_paused, timer
    if timer:
        window.after_cancel(timer)
        timer = None
    is_paused = True
    pause_button.config(text="▶ Resume", command=resume_timer)

# ---------------------------- TIMER RESUME ------------------------------- # 
def resume_timer():
    global is_paused
    is_paused = False
    pause_button.config(text="⏸ Pause", command=pause_timer)
    count_down(remaining_time)

# ---------------------------- TIMER START ------------------------------- # 
def start_timer():
    global reps
    
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Hide start button, show pause button
    start_button.grid_remove()
    pause_button.grid(column=0, row=3, padx=10)
    pause_button.config(text="⏸ Pause", command=pause_timer)
    
    # Disable time adjustment controls once started
    work_scale.config(state=DISABLED)
    break_scale.config(state=DISABLED)

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="🎉 Long Break", bootstyle="danger")
        show_notification("Long Break Time!", f"Take a {LONG_BREAK_MIN}-minute break!")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="☕ Short Break", bootstyle="warning")
        show_notification("Break Time!", f"Take a {SHORT_BREAK_MIN}-minute break!")
    else:
        count_down(work_sec)
        title_label.config(text="💼 Work Time", bootstyle="success")
        show_notification("Focus Time!", f"Work for {WORK_MIN} minutes!")

# ---------------------------- TIME ADJUSTMENT ------------------------------- #
def update_work_time(value=None):
    global WORK_MIN
    WORK_MIN = int(float(work_scale.get()))
    work_value_label.config(text=f"{WORK_MIN} min")

def update_break_time(value=None):
    global SHORT_BREAK_MIN, LONG_BREAK_MIN
    SHORT_BREAK_MIN = int(float(break_scale.get()))
    LONG_BREAK_MIN = SHORT_BREAK_MIN * 4
    break_value_label.config(text=f"{SHORT_BREAK_MIN} min")
    long_break_label.config(text=f"(Long break: {LONG_BREAK_MIN} min)")

# ---------------------------- NOTIFICATION ------------------------------- #
def show_notification(title, message):
    try:
        toast = ToastNotification(
            title=title,
            message=message,
            duration=3000,
            bootstyle=INFO
        )
        toast.show_toast()
    except:
        pass  # Notifications are optional

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global remaining_time, timer
    remaining_time = count
    
    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    
    # Update progress bar
    if reps % 2 == 1:  # Work session
        total_time = WORK_MIN * 60
    elif reps % 8 == 0:  # Long break
        total_time = LONG_BREAK_MIN * 60
    else:  # Short break
        total_time = SHORT_BREAK_MIN * 60
    
    progress = ((total_time - count) / total_time) * 100
    progress_bar['value'] = progress
    
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✅"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = ttk.Window(themename="flatly")
window.title("🍅 Pomodoro Timer")
window.geometry("520x650")
window.resizable(False, False)

# Create a canvas with scrollbar
canvas_container = Canvas(window, highlightthickness=0)
scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas_container.yview, bootstyle="rounded")
scrollable_frame = ttk.Frame(canvas_container)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
)

canvas_container.create_window((250, 0), window=scrollable_frame, anchor="n")
canvas_container.configure(yscrollcommand=scrollbar.set)

canvas_container.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Enable mouse wheel scrolling
def on_mousewheel(event):
    canvas_container.yview_scroll(int(-1*(event.delta/120)), "units")

canvas_container.bind_all("<MouseWheel>", on_mousewheel)

# Main container with padding
main_frame = ttk.Frame(scrollable_frame, padding=20)
main_frame.pack(fill=BOTH, expand=YES)

# Title
title_label = ttk.Label(
    main_frame, 
    text="Ready to Focus", 
    font=(FONT_NAME, 24, "bold"),
    bootstyle="success"
)
title_label.pack(pady=(0, 20))

# Canvas for tomato image and timer
canvas = Canvas(main_frame, width=200, height=224, bg="#f8f9fa", highlightthickness=0)
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "tomato.png")
try:
    tomato_img = PhotoImage(file=image_path)
    canvas.create_image(100, 112, image=tomato_img)
except:
    # If image not found, create a simple circle
    canvas.create_oval(50, 50, 150, 150, fill="#e74c3c", outline="")

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(
    main_frame,
    length=300,
    mode='determinate',
    bootstyle="success-striped"
)
progress_bar.pack(pady=15)
progress_bar['value'] = 0

# Check marks
check_marks = ttk.Label(
    main_frame,
    text="",
    font=(FONT_NAME, 18),
    bootstyle="success"
)
check_marks.pack(pady=10)

# Control buttons frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=15)

start_button = ttk.Button(
    button_frame,
    text="▶ Start",
    command=start_timer,
    bootstyle="success",
    width=12
)
start_button.grid(column=0, row=3, padx=10)

pause_button = ttk.Button(
    button_frame,
    text="⏸ Pause",
    command=pause_timer,
    bootstyle="warning",
    width=12
)
pause_button.grid(column=0, row=3, padx=10)
pause_button.grid_remove()

reset_button = ttk.Button(
    button_frame,
    text="⟲ Reset",
    command=reset_timer,
    bootstyle="danger",
    width=12
)
reset_button.grid(column=1, row=3, padx=10)

# Separator
ttk.Separator(main_frame, orient=HORIZONTAL).pack(fill=X, pady=20)

# Time adjustment section
settings_label = ttk.Label(
    main_frame,
    text="⚙ Timer Settings",
    font=(FONT_NAME, 16, "bold"),
    bootstyle="info"
)
settings_label.pack(pady=(0, 15))

# Work time adjustment
work_frame = ttk.Labelframe(main_frame, text="Work Duration", padding=15, bootstyle="success")
work_frame.pack(fill=X, pady=5)

work_inner_frame = ttk.Frame(work_frame)
work_inner_frame.pack(fill=X)

ttk.Label(work_inner_frame, text="1", font=(FONT_NAME, 9)).pack(side=LEFT, padx=(0, 5))

work_scale = ttk.Scale(
    work_inner_frame,
    from_=1,
    to=60,
    orient=HORIZONTAL,
    bootstyle="success",
    command=lambda v: update_work_time()
)
work_scale.set(WORK_MIN)
work_scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

ttk.Label(work_inner_frame, text="60", font=(FONT_NAME, 9)).pack(side=LEFT, padx=(5, 0))

work_value_label = ttk.Label(
    work_frame,
    text=f"{WORK_MIN} min",
    font=(FONT_NAME, 14, "bold"),
    bootstyle="success"
)
work_value_label.pack(pady=(10, 0))

# Break time adjustment
break_frame = ttk.Labelframe(main_frame, text="Break Duration", padding=15, bootstyle="warning")
break_frame.pack(fill=X, pady=5)

break_inner_frame = ttk.Frame(break_frame)
break_inner_frame.pack(fill=X)

ttk.Label(break_inner_frame, text="1", font=(FONT_NAME, 9)).pack(side=LEFT, padx=(0, 5))

break_scale = ttk.Scale(
    break_inner_frame,
    from_=1,
    to=30,
    orient=HORIZONTAL,
    bootstyle="warning",
    command=lambda v: update_break_time()
)
break_scale.set(SHORT_BREAK_MIN)
break_scale.pack(side=LEFT, fill=X, expand=YES, padx=5)

ttk.Label(break_inner_frame, text="30", font=(FONT_NAME, 9)).pack(side=LEFT, padx=(5, 0))

break_value_label = ttk.Label(
    break_frame,
    text=f"{SHORT_BREAK_MIN} min",
    font=(FONT_NAME, 14, "bold"),
    bootstyle="warning"
)
break_value_label.pack(pady=(10, 0))

long_break_label = ttk.Label(
    break_frame,
    text=f"(Long break: {LONG_BREAK_MIN} min)",
    font=(FONT_NAME, 9),
    bootstyle="secondary"
)
long_break_label.pack(pady=(5, 0))

window.mainloop()