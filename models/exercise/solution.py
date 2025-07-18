from pdb import line_prefix
from pickletools import decimalnl_long
from models.obj_exercise import ObjExercise
import re
from utils import print_error, remove_empty_items

class Solution:
    def __init__(self, obj_exercise: ObjExercise):
        self.solution_textes = []
        self.title = obj_exercise.title
        lines = obj_exercise.content.split('\n')
        if(len(lines) < 2):
            print_error(f"No solution found for {obj_exercise.title}")
            return
        lines.pop(0)
        while(not re.search(r'Code tham khảo\s*:?', lines[0], re.IGNORECASE)):
            self.solution_textes.append(lines[0])
            lines.pop(0)
        self.solution_textes = remove_empty_items(self.solution_textes)

    def set_solution(self, solution):
        if not isinstance(solution["code_sample"], list) or len(solution["code_sample"]) == 0:
            print_error(f"code_sample is not a list or empty in {self.title}")
        self.code_sample = solution["code_sample"]

    def check_error(self):
        if len(self.solution_textes) == 0:
            print_error(f"[Solution]No solution textes found" + str(self.title))

    def __str__(self):
        return f"solution_textes: {self.solution_textes}"
