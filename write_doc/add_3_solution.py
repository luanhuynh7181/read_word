from typing import List
from models.exercise.solution import Solution
from docx import Document
from write_doc.utils_write_doc import create_table, add_style_paragraph, write_list_section_number, add_style_cell, add_style_text

from docx.shared import RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT


def write_solution_exercise(doc: Document, solutionExercise: List[Solution], group_solutions: List[object]): # type: ignore
    header = doc.add_heading(f"Hướng dẫn giải", level=2)
    add_style_paragraph(header, {
            'rgb_color': RGBColor(255, 0, 0),
            'alignment': WD_PARAGRAPH_ALIGNMENT.CENTER,
            'bold': True,
            'font_size': 20,
            'line_spacing': 25
        })

    for i, exercise in enumerate(solutionExercise, 0):
        header = doc.add_heading(f"Bài {i}: {exercise.title}", level=3)
        add_style_paragraph(header, {
            'rgb_color': RGBColor(0, 111, 192),
            'alignment': WD_PARAGRAPH_ALIGNMENT.LEFT,
            'bold': True,
            'space_before':20
        })
        
        phantich = doc.add_paragraph("1. Phân tích:")
        add_style_paragraph(phantich, {
            'rgb_color': RGBColor(0, 111, 192),
            'alignment': WD_PARAGRAPH_ALIGNMENT.LEFT,
            'bold': True,
            'space_before':15
        })

        write_list_section_number(doc, exercise.solution_textes, {
            'alignment': WD_PARAGRAPH_ALIGNMENT.LEFT,
            'left_indent': 0.82
        })
        code = doc.add_paragraph("2. Code tham khảo:",  style="Normal")
        add_style_paragraph(code, {
            'rgb_color': RGBColor(0, 111, 192),
            'alignment': WD_PARAGRAPH_ALIGNMENT.LEFT,
            'bold': True
        })
        create_code_table(doc, group_solutions[i]["code_sample"]) # type: ignore
    pass

def create_code_table(doc: Document, code: List[str]): # type: ignore
    table = create_table(doc, 1, 1)
    table_style = {
        'alignment': WD_PARAGRAPH_ALIGNMENT.LEFT,
        'vertical_alignment': WD_CELL_VERTICAL_ALIGNMENT.TOP,
        'font_size': 14
    }
    for i in range(len(code)):
        if(i == 0):
            add_style_cell(table.cell(0, 0), code[i], table_style)
        else:
            add_style_text(table.cell(0, 0), code[i], table_style)
    return table