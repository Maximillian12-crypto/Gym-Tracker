class Exercises:
    def __init__(self, name, sets, reps, weight):
        self.name= name
        self.sets=int(sets)
        self.reps=int(reps)
        self.weight=float(weight) 

    def calculate_volume(self):
        return self.sets*self.reps*self.weight
    def to_dict(self):
        return{
            "name":self.name,
            "sets":self.sets,
            "reps":self.reps,
            "weight":self.weight
        }    
    
class Workout:
    def __init__(self,date):
        self.date=date
        self.exercises = []

    def add_exercise(self,exercise):
        self.exercises.append(exercise)     
   
    def total_volume(self):
        total =0
        for exercise in self.exercises:
            total += exercise.calculate_volume()
        return total    
    
    
    def to_dict(self):
        return{
            "date":self.date,
            "exercises": [ex.to_dict() for ex in self.exercises]
        }   


class User:
    def __init__(self, name, age, weight, height):

        self.name=name
        self.age=age
        self.weight=weight
        self.height=height
        self.goals={
            "strength":False,
            "muscle gain": False,
            "fat loss":False
        }
            