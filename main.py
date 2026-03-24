from models import Exercises, Workout
from storage import GymTracker

tracker = GymTracker()

tracker.load_from_file()


def create_workout():
    date = input("Enter workout date (YYYY-MM-DD): ")
    new_workout = Workout(date)

    while True:
        name = input("Exercise name (type 'done' to finish): ")

        if name.lower() == "done":
            break

        sets = int(input("Sets: "))
        reps = int(input("Reps: "))
        weight = float(input("Weight: "))

        exercise = Exercises(name, sets, reps, weight)
        new_workout.add_exercise(exercise)

    return new_workout



while True:
    print("\n ========= Gym Tracker ===========")
    print("1. Add workout")
    print("2. View exercise  history")
    print("3. View exercise statistics")
    print("4. View strongest exercise")
    print("5. view workout summary by date")
    print("6. View dashboard")
    print("7. View Training frequency")
    print("8. Exercise frequency chart")
    print("9. Muscle distribution chart")
    print("!0. Get workut recommendation")
    print("11. Exit")
    print("===============================")


    choice = input ("Select an option: ")


    if choice == "1":
        new_workout = create_workout()

        print(f"Total workout volume {new_workout.total_volume()} kg")

        # CHECK PR before adding
        pr_results = tracker.check_pr(new_workout)

        for message in pr_results:
            print(message)


        tracker.add_workout(new_workout)
        for ex in new_workout.exercises:
            plateau_message = tracker.detect_plateau(ex.name)
            if plateau_message:
                print(plateau_message)


        for ex in new_workout.exercises:
            progress = tracker.analyze_progress(ex.name)

            if progress:
                print(progress)


        tracker.saveToFile()
        print("Workout saved successfully.")

    elif choice =="2":
        while True:
           check_exercise = input("Enter exercise to view stats (or press enter to return)").strip()

           if not check_exercise:
               break
           tracker.show_exercise_history(check_exercise)

    elif choice =="3":

          while True:

            stat_exercise= input("Enter exercise to view stats(or press enter to continue): ")

            if not stat_exercise:
                break     

            tracker.exercise_stats(stat_exercise)  


    elif choice=="4":
                  
        tracker.strongest_exercise()


    elif choice=="5":
        date = input("Enter workout date(YYYY-MM-DD): ")
        tracker.workout_summary_by_date(date)

    elif choice ==  "6":
        tracker.dashboard()  

    elif choice == "7":
        tracker.training_frequency()  

    elif choice == "8":
        tracker.plot_exercise_frequency()  

    elif choice == "9":
        tracker.plot_muscle_distribution()  

    elif choice == "10":
        tracker.recommend_workout()       

    elif choice == "11":

        tracker.saveToFile()
        print("Data saved. Goodbye.")
        break

    else:
        print("Invalid option. Please select 1–6.")    
        

     
         


                 