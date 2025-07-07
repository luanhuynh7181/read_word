from itertools import count
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docx.shared import Pt, RGBColor
from file_reader import extract_exercises_from_docx, check_group_error, log_group_exercises
from group_creator import create_group_exercises
from utils import print_error, print_info
from models.exercise.group_exercise import GroupExercise
from models.exercise.exercise import Exercise
from models.exercise.solution import Solution
from models.exercise.extended_exercise import ExtendedExercise
from typing import List
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from write_doc.add_1_header import add_1_header 
from write_doc.add_2_excercise import write_exercise
from write_doc.add_4_extendExcercise import write_extend_exercise
from write_doc.add_3_solution import write_solution_exercise
from write_doc.utils_write_doc import create_table, write_list_section
from docx2pdf import convert
import json
docFile = "output.docx"
doc = Document()

def write_doc(groupExercises: List[GroupExercise]):
    # split by 3 exercises
    count = 0

    for i in range(0, len(groupExercises), 4):
        count += 1
        
        write_group_exercise(groupExercises[i:i+4], count)
        print(f"Đã xử lý {count}/30 nhóm")
    doc.save(docFile)
        
def write_group_exercise(groupExercise: List[GroupExercise], count: int):
    add_1_header(doc, [group.baseExercise for group in groupExercise], count)
    write_exercise(doc, [group.baseExercise for group in groupExercise])
    write_solution_exercise(doc, [group.solutionExercise for group in groupExercise])
    write_extend_exercise(doc, [group.extendedExercises for group in groupExercise])
    pass

def setup_document_styles():
    heading2_style = doc.styles['Heading 1']
    heading2_style.font.bold = True           # type: ignore
    heading2_style.font.size = Pt(16)         # type: ignore
    heading2_style.font.name = 'Arial'        # type: ignore
    heading2_style.font.color.rgb = RGBColor(0, 0, 139)  # type: ignore




def write_extended_exercises(extendedExercises: List[List[ExtendedExercise]]):
    doc.add_heading("Bài tập mở rộng", level=1)
    # for i, exercise in enumerate(extendedExercises, 1):
        # write_base_exercise(exercise, f"{i}.")



if __name__ == "__main__":
    print_info("running...")
    exercises = extract_exercises_from_docx( "../files/2_de.docx")
    group_exercises = create_group_exercises(exercises)
    write_doc(group_exercises)
    # convert("output.docx", "output.pdf")