from models.obj_exercise import ObjExercise
from typing import Optional, List
from models.exercise.exercise import Exercise
from models.exercise.solution import Solution
from models.exercise.extended_exercise import ExtendedExercise
class GroupExercise:
    def __init__(self, baseExercise: Exercise, solutionExercise: Optional[Solution] = None, extendedExercises: Optional[List[ExtendedExercise]] = None):
        self.baseExercise = baseExercise
        self.solutionExercise = solutionExercise
        self.extendedExercises = extendedExercises or []
    
    def __str__(self):
        return f"GroupExercise:\n- Base: {self.baseExercise}\n- Solution: {self.solutionExercise}\n- Extended: {len(self.extendedExercises)} exercises"
