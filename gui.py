import tkinter as tk
from tkinter import messagebox, ttk, Toplevel, Label, Entry, Button
from models import Workout, Exercises
from storage import GymTracker
import datetime

tracker = GymTracker()
tracker.load_from_file()

root = tk.Tk()
root.title("Gym Tracker Pro")
root.geometry("500x800")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))

def display(text):
    output.delete(1.0, tk.END)
    output.insert(tk.END, text)

def refresh_exercises():
    exercises = sorted(list(set(ex.name for w in tracker.workouts for ex in w.exercises)))
    exercise_combo['values'] = exercises

def open_add_workout_window():
    add_win = Toplevel(root)
    add_win.title("Add Workout")
    add_win.geometry("300x400")

    today = str(datetime.date.today())
    current_workout = Workout(today)

    Label(add_win, text=f"Date: {today}", font=("Arial", 12, "bold")).pack(pady=10)

    Label(add_win, text="Exercise Name:").pack()
    ex_entry = Entry(add_win)
    ex_entry.pack()

    Label(add_win, text="Sets:").pack()
    sets_entry = Entry(add_win)
    sets_entry.pack()

    Label(add_win, text="Reps:").pack()
    reps_entry = Entry(add_win)
    reps_entry.pack()

    Label(add_win, text="Weight (kg):").pack()
    weight_entry = Entry(add_win)
    weight_entry.pack()

    def save_exercise():
        try:
            if not ex_entry.get():
                messagebox.showwarning("Input Error", "Exercise name cannot be empty")
                return

            new_ex = Exercises(
                ex_entry.get(),
                int(sets_entry.get()),
                int(reps_entry.get()),
                float(weight_entry.get())
            )

            current_workout.add_exercise(new_ex)

            ex_entry.delete(0, tk.END)
            sets_entry.delete(0, tk.END)
            reps_entry.delete(0, tk.END)
            weight_entry.delete(0, tk.END)

            messagebox.showinfo("Success", f"Added {new_ex.name} to today's logs")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def final_save():
        if not current_workout.exercises:
            messagebox.showwarning("Empty", "Add at least one exercise before saving")
            return

        prs = tracker.check_pr(current_workout)
        tracker.add_workout(current_workout)
        tracker.save_to_file()
        refresh_exercises()

        if prs:
            messagebox.showinfo("PR ALERT", "\n".join(prs))

        messagebox.showinfo("Saved", "Workout saved successfully!")
        add_win.destroy()

    Button(add_win, text="Add Exercise", command=save_exercise, bg="#3498db", fg="white").pack(pady=10)
    Button(add_win, text="Finish & Save", command=final_save, bg="#2ecc71", fg="white").pack(pady=10)

def showDashboard():
    display(tracker.dashboard())

def showBalance():
    display(tracker.muscle_balance())

def recommendation():
    display(tracker.recommend_workout())

def showHistory():
    name = exercise_combo.get()
    if not name:
        return
    history_result = tracker.show_exercise_history(name)
    plateau_msg = tracker.detect_plateau(name)
    if plateau_msg:
        history_result = plateau_msg + "\n" + "-" * 30 + "\n" + history_result
    display(history_result)

def show_stats():
    name = exercise_combo.get()
    if name:
        display(tracker.exercise_stats(name))

title = ttk.Label(root, text="Gym Tracker Pro", style="Header.TLabel")
title.pack(pady=15)

stats_frame = ttk.LabelFrame(root, text="General Insights", padding=10)
stats_frame.pack(fill="x", padx=20, pady=10)

ttk.Button(stats_frame, text="Dashboard", command=showDashboard).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(stats_frame, text="Muscle Balance", command=showBalance).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(stats_frame, text="Recommendation", command=recommendation).grid(row=1, column=0, columnspan=2, pady=5)

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=5)

graph_frame = ttk.LabelFrame(root, text="Visual Progress", padding=10)
graph_frame.pack(fill="x", padx=20, pady=10)

btn1 = ttk.Button(graph_frame, text="Exercise Frequency", command=tracker.plot_exercise_frequency)
btn2 = ttk.Button(graph_frame, text="Muscle Distribution", command=tracker.plot_muscle_distribution)

btn1.pack(side="left", expand=True, padx=10)
btn2.pack(side="right", expand=True, padx=10)

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=5)

ex_frame = ttk.LabelFrame(root, text="Exercise Analysis", padding=10)
ex_frame.pack(fill="x", padx=20, pady=10)

ttk.Label(ex_frame, text="Select Exercise:").pack()

existing_exercises = sorted(list(set(ex.name for w in tracker.workouts for ex in w.exercises)))

exercise_combo = ttk.Combobox(ex_frame, values=existing_exercises, width=30, state="readonly")
exercise_combo.pack(pady=5)

ttk.Button(ex_frame, text="Show History", command=showHistory).pack(pady=3)
ttk.Button(ex_frame, text="View Stats", command=show_stats).pack(pady=3)

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=5)

ttk.Button(root, text="+ Add New Workout", command=open_add_workout_window).pack(pady=10)

output_frame = ttk.Frame(root)
output_frame.pack(fill="both", expand=True, padx=20, pady=10)

output = tk.Text(output_frame, wrap="word", font=("Consolas", 10))
output.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=output.yview)
scrollbar.pack(side="right", fill="y")

output.config(yscrollcommand=scrollbar.set)

ttk.Button(root, text="Clear Output", command=lambda: output.delete(1.0, tk.END)).pack(pady=5)

display(tracker.dashboard())

root.mainloop()