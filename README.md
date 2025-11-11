# 🍅 Pomodoro Timer - Enhanced Versions

A collection of Pomodoro Timer applications built with Python and Tkinter, ranging from a basic implementation to modern, feature-rich versions with advanced UI.

## 📋 Overview

This repository contains three versions of the Pomodoro Timer technique implementation:

1. **Basic Pomodoro** (`basic_pomodoro.py`) - Original implementation from Angela Yu's 100 Days of Code course
2. **Enhanced Pomodoro** (`enhanced_pomodoro.py`) - Added pause/resume and time customization features
3. **Modern Pomodoro** (`modern_pomodoro.py`) - Complete redesign with ttkbootstrap, notifications, and sliders

## ✨ Features Comparison

| Feature | Basic | Enhanced | Modern |
|---------|-------|----------|--------|
| Work/Break Timer | ✅ | ✅ | ✅ |
| Visual Checkmarks | ✅ | ✅ | ✅ |
| Pause/Resume | ❌ | ✅ | ✅ |
| Time Customization | ❌ | ✅ (Buttons) | ✅ (Sliders) |
| Modern UI | ❌ | ❌ | ✅ |
| Progress Bar | ❌ | ❌ | ✅ |
| Notifications | ❌ | ❌ | ✅ |
| Responsive Design | ❌ | ❌ | ✅ |

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)
- ttkbootstrap (for modern version only)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
```

2. Install dependencies (for modern version):
```bash
pip install -r requirements.txt
```

3. Make sure you have `tomato.png` in the same directory

### Running the Applications

**Basic Version:**
```bash
python basic_pomodoro.py
```

**Enhanced Version:**
```bash
python enhanced_pomodoro.py
```

**Modern Version:**
```bash
python modern_pomodoro.py
```

## 📖 Code Explanations

### Basic Pomodoro (`basic_pomodoro.py`)

**Key Components:**
- **Timer Mechanism**: Uses `window.after()` for non-blocking countdown
- **Pomodoro Cycle**: 
  - Work sessions (25 min default)
  - Short breaks (5 min) after each work session
  - Long break (20 min) after 4 work sessions
- **Visual Feedback**: Checkmarks (✓) accumulate after each work session
- **Color Coding**: Different colors for work (green), short break (pink), long break (red)

**Core Functions:**
```python
start_timer()    # Initiates the pomodoro cycle
count_down()     # Recursive countdown mechanism
reset_timer()    # Resets everything to initial state
```

### Enhanced Pomodoro (`enhanced_pomodoro.py`)

**New Features:**
- **Pause/Resume Functionality**: 
  - Saves current time when paused
  - Resumes from saved position
  - Button text changes dynamically
- **Time Customization**:
  - Plus/minus buttons for work duration (1-60 min)
  - Plus/minus buttons for break duration (1-30 min)
  - Adjustments disabled during active session
- **State Management**: Tracks `is_paused` and `remaining_time` globally

**Additional Functions:**
```python
pause_timer()          # Pauses the current session
resume_timer()         # Resumes from paused state
adjust_work_time()     # Modifies work duration
adjust_break_time()    # Modifies break duration
```

**State Flow:**
```
Initial → Start (buttons disabled) → Pause → Resume → Complete
   ↓                                                      ↓
   ←←←←←←←←←←←←← Reset ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

### Modern Pomodoro (`modern_pomodoro.py`)

**Major Enhancements:**

1. **ttkbootstrap Integration**:
   - Modern, flat design with "flatly" theme
   - Consistent styling with bootstrap-inspired components
   - Better color schemes and visual hierarchy

2. **UI Components**:
   - **Sliders**: Smooth range selection (1-60 min work, 1-30 min break)
   - **Progress Bar**: Visual representation of time remaining
   - **Labelframes**: Organized settings sections
   - **Emojis**: Enhanced visual communication (🍅 💼 ☕ 🎉)

3. **Advanced Features**:
   - **Toast Notifications**: Desktop notifications for session changes
   - **Scrollable Interface**: Accommodates all controls without crowding
   - **Mouse Wheel Support**: Scroll through settings easily
   - **Dynamic Long Break**: Automatically 4x the short break duration

4. **Improved UX**:
   - Real-time slider updates with value display
   - Disabled states are more visually obvious
   - Better spacing and padding throughout
   - Fallback handling if tomato.png is missing

**Key Technical Improvements:**

```python
# Progress bar calculation
progress = ((total_time - count) / total_time) * 100
progress_bar['value'] = progress

# Scrollable canvas for responsive design
canvas_container = Canvas(window, highlightthickness=0)
scrollbar = ttk.Scrollbar(window, orient="vertical")
scrollable_frame = ttk.Frame(canvas_container)

# Notification system
toast = ToastNotification(
    title=title,
    message=message,
    duration=3000,
    bootstyle=INFO
)
```

**Architecture Pattern:**
- **Separation of Concerns**: Settings, timer, and controls are visually separated
- **Event-Driven**: All interactions trigger callbacks
- **Graceful Degradation**: Works even if notifications fail or image is missing

## 🎯 The Pomodoro Technique

The Pomodoro Technique is a time management method:

1. Work for 25 minutes (1 Pomodoro)
2. Take a 5-minute break
3. After 4 Pomodoros, take a longer 15-20 minute break

This technique helps maintain focus and prevent burnout.

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter**: Standard Python GUI framework
- **ttkbootstrap**: Modern themed widgets for Tkinter
- **Math module**: For time calculations

## 📝 Credits

- Basic implementation inspired by Angela Yu's [100 Days of Code: Python Course](https://www.udemy.com/course/100-days-of-code/)
- Enhanced and modernized by Hossein Mosaffa
- Pomodoro Technique developed by Francesco Cirillo

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📧 Contact

Hossein Mosaffa - [LİNKEDİN](https://www.linkedin.com/in/hossein-mosaffa-087975163)

Project Link: [https://github.com/Hosseinm2018/pomodoro-timer](https://github.com/Hossein-Mosaffa/pomodoro-timer)

---

⭐ If you found this helpful, please give it a star!
