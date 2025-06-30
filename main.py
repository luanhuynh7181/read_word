from file_reader import extract_exercises_from_docx, check_group_error
from group_creator import create_group_exercises
from utils import print_info
# Test với file "ĐỀ SỐ 05.docx"
if __name__ == "__main__":
    print_info("Tạo nhóm bài tập")
    filename = "files/sach.docx"
    exercises = extract_exercises_from_docx(filename)
    group_exercises = create_group_exercises(exercises)
    check_group_error(group_exercises)
    # log_group_exercises(group_exercises)
    
