import json
import matplotlib.pyplot as plt
from models import Workout, Exercises
from collections import Counter
import os
import sys


class GymTracker:
    def __init__(self):
        self.workouts = []
        self.exercise_db = self.load_exercise_database()

    def add_workout(self, workout=None):
        """Add a workout to the tracker."""
        if workout:
            self.workouts.append(workout)

    def save_to_file(self, filename="data.json"):
        """Save all workouts to a JSON file."""
        with open(filename, "w") as f:
            json.dump([w.to_dict() for w in self.workouts], f, indent=4)

    def load_from_file(self, filename="data.json"):
        """Load workouts from a JSON file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for workout_data in data:
                    workout = Workout(workout_data["date"])
                    for ex_data in workout_data["exercises"]:
                        exercise = Exercises(
                            ex_data["name"],
                            int(ex_data["sets"]),
                            int(ex_data["reps"]),
                            float(ex_data["weight"])
                        )
                        workout.add_exercise(exercise)
                    self.workouts.append(workout)
            return "Data loaded successfully."
        except FileNotFoundError:
            return "No previous data found."

    def check_pr(self, new_workout):
        """Check for personal records in a new workout."""
        pr_messages = []
        for new_ex in new_workout.exercises:
            previous_best = 0
            for workout in self.workouts:
                for ex in workout.exercises:
                    if ex.name.strip().lower() == new_ex.name.strip().lower():
                        if ex.weight > previous_best:
                            previous_best = ex.weight

            if new_ex.weight > previous_best:
                pr_messages.append(
                    f"🔥 New PR for {new_ex.name}! Previous: {previous_best} kg | New: {new_ex.weight} kg"
                )
        return pr_messages

    def show_exercise_history(self, exercise_name):
        """Display history for a specific exercise."""
        found = False
        full_output = f"--- History for {exercise_name} ---\n"

        for workout in self.workouts:
            for ex in workout.exercises:
                if ex.name.strip().lower() == exercise_name.strip().lower():
                    volume = ex.calculate_volume()
                    full_output += f"{workout.date} --> Weight: {ex.weight} || {ex.sets} x {ex.reps} --> Volume: {volume}\n"
                    found = True

        if not found:
            return f"No history found for '{exercise_name}'"
        return full_output

    def detect_plateau(self, exercise_name):
        """Detect if an exercise has plateaued over the last 3 sessions."""
        history = []
        for workout in self.workouts:
            for exercise in workout.exercises:
                if exercise.name.strip().lower() == exercise_name.strip().lower():
                    history.append(exercise)

        if len(history) < 3:
            return None

        last_three = history[-3:]
        first = last_three[0]
        plateau = True

        for ex in last_three[1:]:
            if ex.weight > first.weight:
                plateau = False
                break

        if plateau:
            return f"⚠️ {exercise_name} has plateaued for 3 sessions."
        return None

    def analyze_progress(self, exercise_name):
        """Analyze progress trend for an exercise."""
        history = []
        for workout in self.workouts:
            for ex in workout.exercises:
                if ex.name.strip().lower() == exercise_name.strip().lower():
                    history.append(ex)

        if len(history) < 3:
            return None

        last_three = history[-3:]
        w1, w2, w3 = last_three[0].weight, last_three[1].weight, last_three[2].weight

        if w1 < w2 < w3:
            return f"{exercise_name} -> 📈 Improving"
        elif w1 == w2 == w3:
            return f"{exercise_name} -> ⚠️ Plateau"
        elif w1 > w2 > w3:
            return f"{exercise_name} -> 📉 Regressing"
        else:
            return f"{exercise_name} -> Mixed Progress"

    def exercise_stats(self, exercise_name):
        """Get statistics for a specific exercise."""
        volumes = []
        weights = []
        session_count = 0

        for workout in self.workouts:
            for ex in workout.exercises:
                if ex.name.strip().lower() == exercise_name.strip().lower():
                    session_count += 1
                    weights.append(ex.weight)
                    volumes.append(ex.calculate_volume())

        if session_count == 0:
            return "No data found for that exercise"

        best_weight = max(weights)
        avg_weight = sum(weights) / len(weights)
        total_volume = sum(volumes)

        output = f"\nExercise Statistics for {exercise_name}\n"
        output += "-" * 30
        output += f"\nTotal sessions: {session_count}\n"
        output += f"Best weight: {best_weight} kg\n"
        output += f"Average weight: {avg_weight:.2f} kg\n"
        output += f"Total volume lifted: {total_volume} kg\n"
        return output

    def strongest_exercise(self):
        """Find the strongest exercises based on max weight."""
        best_lifts = {}
        for workout in self.workouts:
            for ex in workout.exercises:
                name = ex.name.strip().lower()
                weight = float(ex.weight)
                if name not in best_lifts or weight > best_lifts[name]:
                    best_lifts[name] = weight

        if not best_lifts:
            return "No workout data available"

        sorted_lifts = sorted(best_lifts.items(), key=lambda x: x[1], reverse=True)

        output = "Strongest exercises\n"
        output += "-" * 30 + "\n"
        for i, (exercise, weight) in enumerate(sorted_lifts[:5], start=1):
            output += f"{i}. {exercise.title()} --> {weight} kg\n"
        return output

    def workout_summary_by_date(self, date):
        """Get summary for a specific workout date."""
        for workout in self.workouts:
            if workout.date == date:
                output = f"Workout summary - {workout.date}\n"
                output += "-" * 40 + "\n"
                total_volume = 0

                for ex in workout.exercises:
                    volume = ex.calculate_volume()
                    total_volume += volume
                    output += f"{ex.name.title()} {ex.sets} x {ex.reps} @ {ex.weight} kg\n"
                output += f"Total volume lifted: {total_volume} kg\n"
                return output

        return "No workout found for that date"

    def dashboard(self):
        """Display overall workout statistics."""
        total_workouts = len(self.workouts)
        total_exercises = 0
        total_volume = 0
        exercise_count = {}

        for workout in self.workouts:
            for ex in workout.exercises:
                total_exercises += 1
                total_volume += ex.sets * ex.reps * ex.weight
                name = ex.name
                exercise_count[name] = exercise_count.get(name, 0) + 1

        most_performed = max(exercise_count, key=exercise_count.get) if exercise_count else "None"

        output = "\n============= DASHBOARD =================\n"
        output += f"\nTotal workouts logged: {total_workouts}\n"
        output += f"Total Exercises performed: {total_exercises}\n"
        output += f"Total volume lifted: {total_volume} KG\n"
        output += f"Most performed exercise: {most_performed}\n"
        output += "\n========================================\n"
        return output

    def training_frequency(self):
        """Display frequency of each exercise."""
        all_exercises = [ex.name for workout in self.workouts for ex in workout.exercises]
        exercise_count = Counter(all_exercises)

        if not exercise_count:
            return "No workout data available"

        output = "\n======= TRAINING FREQUENCY =======\n"
        for name, count in exercise_count.items():
            output += f"{name}: {count} sessions\n"
        output += "=================================\n"
        return output

    def get_db_path(self):
        """Get the path to the exercise database file."""
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "exercise_database.json")

    def load_exercise_database(self):
        try:
            current_dir = os.path.dirname(__file__)
            db_path = os.path.join(current_dir, "exercise_database.json")

            with open(db_path, "r") as f:
                data = json.load(f)

            # Normalize everything to lowercase keys
            normalized = {}
            for muscle, exercises in data.items():
                for ex in exercises:
                    normalized[ex.strip().lower()] = muscle.lower()

            return normalized  # now { "bench press": "chest" }

        except:
            return {}

    def get_muscle_group(self, exercise_name):
        key = exercise_name.strip().lower()
        return self.exercise_db.get(key, "Unknown")

    def muscle_balance(self):
        """Analyze muscle group balance in training."""
        muscle_counter = Counter()
        for workout in self.workouts:
            for ex in workout.exercises:
                muscle = self.get_muscle_group(ex.name)
                muscle_counter[muscle] += 1

        if not muscle_counter:
            return "No workout data available for muscle balance analysis"

        output = "\n======== MUSCLE BALANCE ANALYSIS =======\n"
        for muscle, count in muscle_counter.items():
            output += f"{muscle.capitalize()}: {count} exercises\n"

        if "Legs" in muscle_counter and muscle_counter["Legs"] < muscle_counter.get("Chest", 0):
            output += "\n⚠ Legs appear undertrained.\n"
        if "Back" in muscle_counter and muscle_counter["Back"] < muscle_counter.get("Chest", 0):
            output += "⚠ Back training appears low.\n"

        output += "========================================\n"
        return output

    def plot_exercise_frequency(self):
        """Plot exercise frequency as a bar chart."""
        all_exercise_names = [ex.name for workout in self.workouts for ex in workout.exercises]

        if not all_exercise_names:
            print("No data to plot!")
            return

        exercise_count = Counter(all_exercise_names)
        names = list(exercise_count.keys())
        counts = list(exercise_count.values())

        plt.figure(figsize=(10, 6))
        plt.bar(names, counts, color='skyblue')
        plt.title("Exercise Frequency")
        plt.xlabel("Exercise")
        plt.ylabel("Number of sessions")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_muscle_distribution(self):
        """Plot muscle group distribution as a pie chart."""
        muscle_counter = Counter()
        for workout in self.workouts:
            for ex in workout.exercises:
                muscle = self.get_muscle_group(ex.name)
                muscle_counter[muscle] += 1

        if not muscle_counter:
            print("No muscle data to plot!")
            return

        labels = list(muscle_counter.keys())
        sizes = list(muscle_counter.values())

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Muscle Group Distribution")
        plt.show()

    def recommend_workout(self):
        """Recommend exercises based on training balance."""
        muscle_counter = Counter()
        for workout in self.workouts:
            for ex in workout.exercises:
                muscle = self.get_muscle_group(ex.name)
                muscle_counter[muscle] += 1

        if not muscle_counter:
            return "No workout data available for recommendations"

        weakest_muscle = min(muscle_counter, key=muscle_counter.get)

        output = "\n============= WORKOUT RECOMMENDATION ================\n"
        output += f"Focus: {weakest_muscle.capitalize()} (undertrained)\n"

        exercises = self.exercise_db.get(weakest_muscle, [])
        if exercises:
            output += "Suggested Exercises:\n"
            for ex in exercises[:5]:
                output += f"  - {ex}\n"
        else:
            output += "No exercises found for this muscle group\n"

        output += "===================================================\n"
        return output