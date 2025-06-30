from pdb import line_prefix
from pickletools import decimalnl_long
from models.obj_exercise import ObjExercise
import re
from utils import remove_empty_items
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
        
        # Kiểm tra dòng tiếp theo có phải là Input không
        if re.search(r'input\s*:', self.lines[0], re.IGNORECASE):
            self.lines.pop(0)  # Bỏ dòng Input
        else:
            # Tìm pattern "input" trong description_section
            input_pattern = re.search(r'input\s*:?', self.description_section, re.IGNORECASE)
            if input_pattern:
                # Bỏ phần từ "input" trở đi
                self.description_section = self.description_section[:input_pattern.start()].strip()
            else:
                print(f"No input section found in {self.title}")

 
    def _parse_input(self):
        while(not re.search(r'output\s*:?', self.lines[0], re.IGNORECASE)):
            self.input_section.append(self.lines[0])
            self.lines.pop(0)
        
        # Xem lines[0] có độ dài hơn 15 thì bỏ output đi và thêm vào input_section
        if len(self.lines[0]) > 15:
            str_output = self.lines[0]
            pattern = re.search(r'output\s*:?', str_output, re.IGNORECASE)
            if pattern:  # Kiểm tra pattern có tồn tại không
                self.input_section.append(str_output[:pattern.start()].strip())

        self.lines.pop(0)
        self.input_section = remove_empty_items(self.input_section)

    def _parse_output(self):
     
        # Kiểm tra xem dòng cuối cùng có pattern "input" thì xóa input đi
        last_line = self.lines[-1]
        pattern = re.search(r'Ví dụ\s*:?', last_line, re.IGNORECASE)
        if pattern:
            self.lines[-1] = last_line[:pattern.start()].strip()
        self.output_section = remove_empty_items(self.lines)

    def __str__(self):
        return f"title: {self.title}\ndescription: {self.description_section}\ninput: {self.input_section}\noutput: {self.output_section}"



