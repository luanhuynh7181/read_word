from pdb import line_prefix
from pickletools import decimalnl_long
from models.obj_exercise import ObjExercise
import re
from utils import remove_empty_items, print_error
class ExtendedExercise:
    def __init__(self, obj_exercise: ObjExercise):
        self.title = obj_exercise.title
        self.description_section = ""
        self.output_section = []
        self.input_section = []
        self.lines =  obj_exercise.content.split('\n')
        self.remove_input_text()
        self._parse_input()

        self._parse_output()
    
    def remove_input_text(self):
        
        # Kiểm tra dòng tiếp theo có phải là Input không
        if re.search(r'input\s*:', self.lines[0], re.IGNORECASE):
            self.lines.pop(0)  # Bỏ dòng Input
        else:
            # Tìm pattern "input" trong description_section
            input_pattern = re.search(r'input\s*:?', self.title, re.IGNORECASE)
            if input_pattern:
                # Bỏ phần từ "input" trở đi
                self.title = self.title[:input_pattern.start()].strip()

        last_line = self.lines[-1]
        pattern = re.search(r'Ví dụ\s*:?', last_line, re.IGNORECASE)
        if pattern:
            self.lines[-1] = last_line[:pattern.start()].strip()
        self.lines = remove_empty_items(self.lines)

 
    def _parse_input(self):
        while(len(self.lines) > 0 and not re.search(r'output\s*:?', self.lines[0], re.IGNORECASE)):
            self.input_section.append(self.lines[0])
            self.lines.pop(0)
        
        # Xem lines[0] có độ dài hơn 15 thì bỏ output đi và thêm vào input_section
        if len(self.lines) > 0 and len(self.lines[0]) > 15:
            str_output = self.lines[0]
            pattern = re.search(r'output\s*:?', str_output, re.IGNORECASE)
            if pattern:  # Kiểm tra pattern có tồn tại không
                self.input_section.append(str_output[:pattern.start()].strip())

        if len(self.lines) > 0:
            self.lines.pop(0)
        self.input_section = remove_empty_items(self.input_section)

    def _parse_output(self):
        if(len(self.lines) == 0):
            return

        self.output_section = remove_empty_items(self.lines)
        
    def check_error(self):
        if len(self.title) == 0:
            print_error(f"[ExtendedExercise]No title found in {self.title}")    
        if len(self.input_section) == 0:
            print_error(f"[ExtendedExercise]No input section found in {self.title}")
        if len(self.output_section) == 0:
            print_error(f"[ExtendedExercise]No output section found in {self.title}")

    def __str__(self):
        return f"title: {self.title}\ninput: {self.input_section}\noutput: {self.output_section}"



