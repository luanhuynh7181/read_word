from docx import Document
import os
import re
from models import ObjExercise, GroupExercise, Exercise, Solution, ExtendedExercise
from group_creator import create_group_exercises
from utils import print_info
import json

def extract_exercises_from_docx(filename):
    """
    Đọc file .docx và tách thành các ObjExercise dựa trên pattern "Bài x" hoặc "Bài x.y"
    """
    try:
        if not os.path.exists(filename):
            print(f"Lỗi: File '{filename}' không tồn tại!")
            return []
        
        # Đọc file .docx
        doc = Document(filename)
        
        # Lấy tất cả text
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text = paragraph.text.strip()
                if text.upper() in ["HƯỚNG DẪN VÀ CODE THAM KHẢO", "HẾT"]:
                    continue
                full_text.append(text)
        
        # Tách thành các ObjExercise
        exercises = []
        current_exercise = None
        current_content = []
        
        for line in full_text:
            # Kiểm tra pattern "Bài x" hoặc "Bài x.y" (có thể có khoảng trắng)
            match = re.match(r'^Bài\s*(\d+(?:\.\d+)*)', line)
            
            if match:
                # Lưu exercise trước đó nếu có
                if current_exercise:
                    current_exercise.content = '\n'.join(current_content)
                    exercises.append(current_exercise)
                
                # Tạo exercise mới
                exercise_name = f"Bài {match.group(1)}"
                # Xử lý title: bỏ pattern "Bài X:" hoặc "Bài X." và cắt khoảng trống thừa
                clean_title = re.sub(r'^Bài\s*\d+(?:\.\d+)*\s*[:.]\s*', '', line).strip()
                # Cắt hết khoảng trống thừa (nhiều khoảng trắng thành 1 khoảng trắng)
                clean_title = re.sub(r'\s+', ' ', clean_title).strip()
                current_exercise = ObjExercise(
                    name=exercise_name,
                    title=clean_title,
                    content=""
                )
                current_content = []
            else:
                # Thêm vào nội dung của exercise hiện tại
                if current_exercise:
                    current_content.append(line)
        
        # Lưu exercise cuối cùng
        if current_exercise:
            current_exercise.content = '\n'.join(current_content)
            exercises.append(current_exercise)
        
        return exercises
        
    except Exception as e:
        print(f"Lỗi khi đọc file: {str(e)}")
        return []

def check_group_error(group_exercises):
    print_info("Check error")
    for group in group_exercises:
        group.check_error()
    print_info("Check error done")

def log_group_exercises(group_exercises):
    for i, group in enumerate(group_exercises, 1):
      group.log_info()
