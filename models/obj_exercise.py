import re

class ObjExercise:
    def __init__(self, name="", title="", content=""):
        self.name = name
        self.title = title
        self.content = content
        # Tạo baseName từ name
        self.baseName = self._extract_base_name(name)
    
    def _extract_base_name(self, name):
        """Trích xuất tên cơ bản từ name (ví dụ: 'Bài 1.1' -> 'Bài 1')"""
        if not name:
            return ""
        
        # Tìm pattern số đầu tiên trong name
        match = re.match(r'^Bài\s*(\d+)', name)
        if match:
            return f"Bài {match.group(1)}"
        return name
    
    def __str__(self):
        return f"ObjExercise: {self.name} (baseName: {self.baseName}) title: {self.title} content: {self.content[:100]}..." 