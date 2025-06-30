from pdb import line_prefix
from pickletools import decimalnl_long

from docx.shared import Length
from models.obj_exercise import ObjExercise
import re
from utils import remove_empty_items, print_error
class Exercise:
    def __init__(self, obj_exercise: ObjExercise):
        self.title = obj_exercise.title
        self.input_section = []
        self.output_section = []
        self.description_section = ""
        self.lines =  obj_exercise.content.split('\n')
        self._parse_description()
        self._parse_input()
        self._parse_output()
    
    def _parse_description(self):
        self.description_section = self.lines[0]
        self.lines.pop(0)


        pattern = re.search(r'Ví dụ\s*:?', self.lines[-1], re.IGNORECASE)
        if pattern:
            self.lines[-1] = self.lines[-1][:pattern.start()].strip()

        self.output_section = remove_empty_items(self.lines)
        # Kiểm tra dòng tiếp theo có phải là Input không
        if re.search(r'input\s*:?', self.lines[0], re.IGNORECASE):
            self.lines.pop(0)  # Bỏ dòng Input
        else:
            # Tìm pattern "input" trong description_section
            input_pattern = re.search(r'input\s*:?', self.description_section, re.IGNORECASE)
            if input_pattern:
                # Bỏ phần từ "input" trở đi
                self.description_section = self.description_section[:input_pattern.start()].strip()

 
    def _parse_input(self):
        while(len(self.lines) > 0 and not re.search(r'output\s*:?', self.lines[0], re.IGNORECASE)):
            self.input_section.append(self.lines[0])
            self.lines.pop(0)
        
        if(len(self.lines) == 0):
            return
        # Xem lines[0] có độ dài hơn 15 thì bỏ output đi và thêm vào input_section
        if len(self.lines[0]) > 15:
            str_output = self.lines[0]
            pattern = re.search(r'output\s*:?', str_output, re.IGNORECASE)
            if pattern:  # Kiểm tra pattern có tồn tại không
                self.input_section.append(str_output[:pattern.start()].strip())

        self.lines.pop(0)
        self.input_section = remove_empty_items(self.input_section)

    def _parse_output(self):

        if(len(self.lines) == 0):
            return     
        # Kiểm tra xem dòng cuối cùng có pattern "input" thì xóa input đi
        lastline = self.lines[-1]


    def check_error(self):
        if len(self.description_section) == 0:
            print_error(f"[Exercise]No description section found in {self.title}")
        if len(self.title) == 0:
            print_error(f"[Exercise]No title found in {self.title}")
        if len(self.input_section) == 0:
            print_error(f"[Exercise]No input section found in {self.title}")
        if len(self.output_section) == 0:
            print_error(f"[Exercise]No output section found in {self.title}")

    def __str__(self):
        return f"title: {self.title}\ndescription: {self.description_section}\ninput: {self.input_section}\noutput: {self.output_section}"



