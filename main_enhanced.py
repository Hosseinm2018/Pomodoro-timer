from tkinter import *
import os, math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
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
    title_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0
    
    # Show start button, hide pause button
    start_button.grid(column=0, row=2)
    pause_button.grid_remove()
    
    # Enable time adjustment buttons
    work_plus_button.config(state=NORMAL)
    work_minus_button.config(state=NORMAL)
    break_plus_button.config(state=NORMAL)
    break_minus_button.config(state=NORMAL)

# ---------------------------- TIMER PAUSE ------------------------------- # 
def pause_timer():
    global is_paused, timer
    if timer:
        window.after_cancel(timer)
        timer = None
    is_paused = True
    pause_button.config(text="Resume")
    pause_button.config(command=resume_timer)

# ---------------------------- TIMER RESUME ------------------------------- # 
def resume_timer():
    global is_paused
    is_paused = False
    pause_button.config(text="Pause")
    pause_button.config(command=pause_timer)
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
    pause_button.grid(column=0, row=2)
    pause_button.config(text="Pause", command=pause_timer)
    
    # Disable time adjustment buttons once started
    work_plus_button.config(state=DISABLED)
    work_minus_button.config(state=DISABLED)
    break_plus_button.config(state=DISABLED)
    break_minus_button.config(state=DISABLED)

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- TIME ADJUSTMENT ------------------------------- #
def adjust_work_time(amount):
    global WORK_MIN
    WORK_MIN = max(1, WORK_MIN + amount)
    work_time_label.config(text=f"Work: {WORK_MIN} min")

def adjust_break_time(amount):
    global SHORT_BREAK_MIN
    SHORT_BREAK_MIN = max(1, SHORT_BREAK_MIN + amount)
    break_time_label.config(text=f"Break: {SHORT_BREAK_MIN} min")

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global remaining_time, timer
    remaining_time = count
    
    count_min = math.floor(count/60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
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
window = Tk()
window.title("Pomodoro")
window.config(padx=15, pady=5, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35))
title_label.grid(column=1, row=0)

# Time adjustment controls
time_control_frame = Frame(bg=YELLOW)
time_control_frame.grid(column=1, row=4, pady=10)

work_time_label = Label(time_control_frame, text=f"Work: {WORK_MIN} min", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 12, "bold"))
work_time_label.grid(column=0, row=0, padx=5)

work_minus_button = Button(time_control_frame, text="-", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 10, "bold"), 
                           command=lambda: adjust_work_time(-1), width=2)
work_minus_button.grid(column=1, row=0, padx=2)

work_plus_button = Button(time_control_frame, text="+", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 10, "bold"), 
                          command=lambda: adjust_work_time(1), width=2)
work_plus_button.grid(column=2, row=0, padx=2)

break_time_label = Label(time_control_frame, text=f"Break: {SHORT_BREAK_MIN} min", fg=PINK, bg=YELLOW, font=(FONT_NAME, 12, "bold"))
break_time_label.grid(column=3, row=0, padx=5)

break_minus_button = Button(time_control_frame, text="-", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 10, "bold"), 
                            command=lambda: adjust_break_time(-1), width=2)
break_minus_button.grid(column=4, row=0, padx=2)

break_plus_button = Button(time_control_frame, text="+", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 10, "bold"), 
                           command=lambda: adjust_break_time(1), width=2)
break_plus_button.grid(column=5, row=0, padx=2)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "tomato.png")
tomato_img = PhotoImage(file=image_path)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 15, "bold"), command=start_timer)
start_button.grid(column=0, row=2)

pause_button = Button(text="Pause", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 15, "bold"), command=pause_timer)
pause_button.grid(column=0, row=2)
pause_button.grid_remove()  # Hide initially

reset_button = Button(text="Reset", bg=YELLOW, highlightthickness=0, font=(FONT_NAME, 15, "bold"), command=reset_timer)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_marks.grid(column=1, row=3)

window.mainloop()