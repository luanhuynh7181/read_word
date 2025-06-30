from file_reader import extract_exercises_from_docx, log_exercises, log_group_exercises
from group_creator import create_group_exercises
from utils import print_info
# Test với file "ĐỀ SỐ 05.docx"
if __name__ == "__main__":
    print_info("Tạo nhóm bài tập")
    filename = "files/ĐỀ SỐ 05.docx"
    exercises = extract_exercises_from_docx(filename)
    group_exercises = create_group_exercises(exercises)
    log_group_exercises(group_exercises)
    
    
