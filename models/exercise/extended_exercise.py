from pdb import line_prefix
from pickletools import decimalnl_long
from models.obj_exercise import ObjExercise
import re
from utils import remove_empty_items, print_error
class ExtendedExercise:
    def __init__(self, obj_exercise: ObjExercise):
        self.title = obj_exercise.title
        self.input_section = []
        self.output_section = []
        self.description_section = []
        self.lines =  obj_exercise.content.split('\n')

        input_pattern = re.search(r'input\s*:?', self.title, re.IGNORECASE)
        if input_pattern:
            self.title = self.title[:input_pattern.start()].strip()
            
        self._parse_description()
        self._parse_input()
        self.description_section = remove_empty_items(self.description_section)
        self.input_section = remove_empty_items(self.input_section)
        self.output_section = remove_empty_items(self.lines)
    
    def _parse_description(self):
        # remove Ví dụ:
        pattern = re.search(r'Ví dụ\s*:?', self.lines[-1], re.IGNORECASE)
        if pattern:
            self.lines[-1] = self.lines[-1][:pattern.start()].strip()

        while(len(self.lines) > 0 and not re.search(r'input\s*:?', self.lines[0], re.IGNORECASE)):
            self.description_section.append(self.lines[0])
            self.lines.pop(0)
        
        if(len(self.lines) == 0):
            return

        self.description_section.append(self.lines[0])
        self.lines.pop(0)
        
        input_pattern = re.search(r'input\s*:?', self.description_section[-1], re.IGNORECASE)
        if input_pattern:
            self.description_section[-1] = self.description_section[-1][:input_pattern.start()].strip()
 
    def _parse_input(self):
        while(len(self.lines) > 0 and not re.search(r'output\s*:?', self.lines[0], re.IGNORECASE)):
            self.input_section.append(self.lines[0])
            self.lines.pop(0)
        
        if(len(self.lines) == 0):
            return

        self.input_section.append(self.lines[0])
        self.lines.pop(0)

        output_pattern = re.search(r'output\s*:?', self.input_section[-1], re.IGNORECASE)
        if output_pattern:
            self.input_section[-1] = self.input_section[-1][:output_pattern.start()].strip()

    def set_solution(self, solution):
        # check if input_sample is a list and not empty print_error
        if not isinstance(solution["input_sample"], list) or len(solution["input_sample"]) == 0:
            print_error(f"input_sample is not a list or empty in {self.title}")
        if not isinstance(solution["output_sample"], list) or len(solution["output_sample"]) == 0:
            print_error(f"output_sample is not a list or empty in {self.title}")
        self.input_sample = solution["input_sample"]
        self.output_sample = solution["output_sample"]

    def check_error(self):
        if len(self.title) == 0:
            print_error(f"[ExtendedExercise]No title found in {self.title}")    
        if len(self.input_section) == 0:
            print_error(f"[ExtendedExercise]No input section found in {self.title}")
        if len(self.output_section) == 0:
            print_error(f"[ExtendedExercise]No output section found in {self.title}")

    def __str__(self):
        return f"title: {self.title}\ninput: {self.input_section}\noutput: {self.output_section}"



