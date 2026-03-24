import json
import matplotlib.pyplot as plt
from models import Workout, Exercises  
from collections import Counter


class GymTracker:
    def __init__(self):
        self.workouts = []
        self.exercise_db = self.load_exercise_database()

    def add_workout(self, workout = None):
        self.workouts.append(workout)

    def saveToFile(self, filename="data.json"):
        with open(filename, "w") as f:
            json.dump([w.to_dict() for w in self.workouts], f, indent=4)

    def load_from_file(self, filename="data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

                for workout_data in data:
                    workout = Workout(workout_data["date"])

                    for ex_data in workout_data["exercises"]:
                        exercise = Exercises(
                            ex_data["name"],
                           int (ex_data["sets"]),
                           int (ex_data["reps"]),
                           float(ex_data["weight"])
                        )
                        workout.add_exercise(exercise)

                    self.workouts.append(workout)

            output = "Data loaded successfully."
            return output

        except FileNotFoundError:
            output = "No previous data found."
            return output


    def check_pr(self, new_workout):
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
        found = False
        # 1. Initialize an empty string to hold all history lines
        full_output = f"--- History for {exercise_name} ---\n"
        
        for workout in self.workouts:
            for ex in workout.exercises:
                if ex.name.strip().lower() == exercise_name.strip().lower():
                    volume = ex.calculate_volume()
                    # 2. Use += to APPEND each new line to the string
                    full_output += f"{workout.date} --> Weight:{ex.weight} || {ex.sets} x {ex.reps} --> Volume: {volume}\n"
                    found = True

        # 3. Only return AFTER the loops are completely finished
        if not found:
            return f"No history found for '{exercise_name}'"
            
        return full_output          


    def detect_plateau(self, exercise_name):
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
            # If any workout has a higher weight than the first one, it's not a plateau
            if ex.weight > first.weight: 
                plateau = False
                break  # We can stop checking once we find an increase

        # --- MOVED OUTSIDE THE LOOP ---
        if plateau:
            return f"⚠️ {exercise_name} has plateaued for 3 sessions."
        
        return None


    def analyze_progress(self, exercise_name):
        history=[]

        for workout in self.workouts:
            for ex in workout.exercises:
             if ex.name.strip().lower() == exercise_name.strip().lower():
                history.append(ex)

        if len(history) < 3:
            return None

        last_three = history [-3:]
         
        w1 = last_three[0].weight
        w2 = last_three[1].weight
        w3 = last_three[2].weight

        if w1 < w2 < w3:
            return f"{exercise_name} -> 📈 Improving" 
        elif w1 == w2 == w3:
            return f"{exercise_name} ->  ⚠️ Plateau"
        elif w1 > w2 > w3:
            return f"{exercise_name} -> 📉 Regressing"
        else:
            return f"{exercise_name} -> Mixed Progress"
    


    def exercise_stats(self, exercise_name):
        volumes=[]
        weights=[]
        session_count= 0

        for workout in self.workouts:
            for ex in workout.exercises:
                if ex.name.strip().lower() == exercise_name.strip().lower():
                    session_count +=1 
                    weights.append(ex.weight)
                    volumes.append(ex.calculate_volume())

        if session_count == 0:
            print("No data found for that exercise")
            return

        best_weight=max(weights)
        avg_weight= sum(weights) / len(weights)
        total_volume= sum(volumes)

        output = f"\n Exercise Statistics for {exercise_name}\n"
        output += "-"*30
        output += f"\nTotal sessions: {session_count}\n"
        output += f"Best weight: {best_weight} kg\n"
        output += f"Average weight: {avg_weight:.2f} kg\n"  
        output += f"Total volume lifted: {total_volume} kg\n"
        return output          


    def strongest_exercise(self):
        best_lifts={}

        for workout in self.workouts:
            for ex in workout.exercises:
                name=ex.name.strip().lower()
                weight= float(ex.weight)
                if name not in best_lifts:
                    best_lifts[name]= weight
                else:
                    if weight > best_lifts[name]:
                        best_lifts[name] = weight

        if not best_lifts:
            output += "No wrorkout data available"
            return output
        
        sorted_lifts=sorted(best_lifts.items(), key=lambda x: x[1], reverse=True)

        output +="Strongest exercises"
        output +="-" *30

        for i ,(exercise,weight) in enumerate (sorted_lifts[:5], start=1):
            output += f"{i}. {exercise.title()} --> {weight} kg"   
            return output       



    def workout_summary_by_date(self, date):
        for workout in self.workouts:
            if workout.date == date:
                output +=f"Workout summary - {workout.date}"
                output +="-"*40

                total_volume = 0

                for ex in workout.exercises:
                    volume = ex.calculate_volume()

                    total_volume += volume
                    output +=f"{ex.name.title()}  {ex.sets} x {ex.reps} @ {ex.weight} kg" 
                output+= f"Total volume lifted: ", total_volume, "kg" 
                return output

        output += "No workout found for that date"
        return output      


    def dashboard(self):
        total_workouts= len(self.workouts)
        total_exercises=0
        total_volume=0
        exercise_count={}

        for workout in self.workouts:
            for ex in workout.exercises:
                total_exercises +=1
                total_volume += ex.sets * ex.reps * ex.weight
                name = ex.name

                if name not in exercise_count:
                    exercise_count[name] =0
                exercise_count[name] +=1 

        if exercise_count:
            most_performed= max(exercise_count, key=exercise_count.get)

        else:
            most_performed= "None"

        output = "\n=============DASHBOARD=================\n"
        output += f"\nTotal workouts logged: {total_workouts}\n"
        output +=f"\nTotal Exercises performed: {total_exercises}\n"
        output +=f"\nTotal volume lifted: {total_volume} KG\n"
        output += f"\nMost performed exercise: {most_performed}\n"
        output += "\n==============================\n"                  
        
        return output



    def training_frequency(self):

        all_exercises = [ex.name for workout in self.workouts for ex in workout.exercises]

        exercise_count = Counter(all_exercises)

        output +="\n======= TRAINING FREQUENCY ======="

        for name, count in exercise_count.items():
            output += f"{name} : {count} sessions"
            return output

        output +="\n===============================\n"
        
    
        self.exercise_db = self.load_exercise_database()
        return output

    def load_exercise_database(self):
        try:
            with open("exercise_database.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            data = {"exercises" : []}
            with open ("exercise_database.json", "w ") as file:
                json.dump(data, file, indent=4) 
            
            return data

    def get_muscle_group(self, exercise_name):
        for muscle, exercises in self.exercise_db.items():
             if exercise_name.lower() in [e.lower() for e in exercises]:
                 return muscle
             

    def muscle_balance(self):
        muscle_counter =Counter()
        for workout in self.workouts:
            for ex in workout.exercises:
                muscle =   self.get_muscle_group(ex.name)
                label = muscle if muscle else "unknown"
                muscle_counter[label] += 1

        output ="\n========MUSCLE BALANCE ANALYSIS=======\n"
        for muscle, count in muscle_counter.items():
            output+=f"{muscle.capitalize()} : {count} exercises"

        if "legs" in muscle_counter and muscle_counter["legs"] < muscle_counter["chest"]:
            output+="\n⚠ Legs appear undertrained."

        if "back" in muscle_counter and muscle_counter["back"] < muscle_counter["chest"]:
            output+="⚠ Back training appears low."

        output +="\n=====================================\n"
        return output


    def plot_exercise_frequency(self):
        # FIX: We need to count names from WORKOUTS, not the database
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
        muscle_counter = Counter()

        for workout in self.workouts:
            # FIX: changed self.exercise to workout.exercises
            for ex in workout.exercises:
                muscle = self.get_muscle_group(ex.name)
                # Handle cases where muscle might be None if not in DB
                label = muscle if muscle else "Unknown"
                muscle_counter[label] += 1
                
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
        from collections import Counter    
        muscle_counter = Counter()

        for workout in self.workouts:
            for ex in workout.exercises:
                muscle=  self.get_muscle_group(ex.name)
                muscle_counter[muscle] += 1

        if not muscle_counter:
            output+="No wrokout data available"
            return output

        weakest_muscle= min(muscle_counter, key=muscle_counter.get)

        output="\n============= WORKOUT RECOMMENDATION================\n"
        output +=f"Focus: {weakest_muscle.capitalize()} (undertrained)\n"

        exercises = self.exercise_db.get( weakest_muscle, [])
        

        if exercises:
            output+="Suggested Exercises: "
            for ex in exercises[:5] :
                output+=f"-{ex}"  

        else:
            output+="No exercises found for this muscle group"  

        output+="===================================="
        return output               