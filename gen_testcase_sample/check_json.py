import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.exercise.group_exercise import GroupExercise
from models.obj_exercise import ObjExercise   
from typing import List
import json
from file_reader import extract_exercises_from_docx
from group_creator import create_group_exercises

def check_json(data, exercises :List[GroupExercise]):
    for exercise in exercises:
        if exercise.solution is None:
            print(exercise.title)
            return False
    return True


if __name__ == "__main__":
    data = json.load(open("data.json", "r"))
    exercises = extract_exercises_from_docx( "../files/2_de.docx")
    group_exercises = create_group_exercises(exercises)     
    check_json(data, group_exercises)
