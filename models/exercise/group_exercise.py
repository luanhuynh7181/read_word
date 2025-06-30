from models.obj_exercise import ObjExercise
from typing import Optional, List
from models.exercise.exercise import Exercise
from models.exercise.solution import Solution
from models.exercise.extended_exercise import ExtendedExercise
from utils import print_error, print_info

class GroupExercise:
    def __init__(self, baseExercise: Exercise, solutionExercise:Solution, extendedExercises: Optional[List[ExtendedExercise]] = None):
        self.baseExercise = baseExercise
        self.solutionExercise = solutionExercise
        self.extendedExercises = extendedExercises or []
    
    def __str__(self):
        return f"GroupExercise:\n- Base: {self.baseExercise}\n- Solution: {self.solutionExercise}\n- Extended: {len(self.extendedExercises)} exercises"

    def check_error(self):
        if(len(self.extendedExercises) != 3):
            print_error(f"[GroupExercise]No extended exercises found" + str(self.baseExercise.title) + " " + str(len(self.extendedExercises)))
        self.baseExercise.check_error()
        self.solutionExercise.check_error()
        for extendedExercise in self.extendedExercises:
            extendedExercise.check_error()
    
    def log_info(self):
        print_info(f"GroupExercise:\nTitle:{self.baseExercise.title}\nextended{len(self.extendedExercises)} exercises") 

