from models import GroupExercise
from models.exercise import Exercise
from models.exercise.solution import Solution
from models.exercise.extended_exercise import ExtendedExercise
from utils import print_error
import json

def find_solution(obj_exercises, base_exercise):
    for exercise in obj_exercises:
        if exercise.baseName == base_exercise.baseName and exercise != base_exercise:
            obj_exercises.remove(exercise)
            return Solution(exercise)
    print_error(f"No solution found for {base_exercise.title}")
    return None

def find_extended(obj_exercises, base_exercise):
    extended_exercises = []
    i = 0
    lastIndex = -1
    # print(f"obj_exercises: {base_exercise.baseName}")
    while i < len(obj_exercises):
        if obj_exercises[i].baseName == base_exercise.baseName and (lastIndex == -1 or i == lastIndex ):
            extended = ExtendedExercise(obj_exercises[i])
            extended_exercises.append(extended)
            lastIndex = i
            obj_exercises.pop(i)  # Xóa phần tử đã thêm
            # Không cần i++ vì sau khi pop(), phần tử tiếp theo sẽ ở vị trí i
        else:
            if lastIndex != -1:
                break  # Dừng khi đã tìm được ít nhất 1 phần tử và gặp phần tử khác
            i += 1  # Chỉ tăng i khi không tìm thấy phần tử phù hợp
    return extended_exercises

def create_group_exercise(obj_exercises, map_solution, map_extended):
    base_exercise = obj_exercises[0]
    obj_exercises.remove(base_exercise)

    # Tìm solution và extended
    solution = find_solution(obj_exercises, base_exercise)
    extendedes = find_extended(obj_exercises, base_exercise)
    
    # Tạo GroupExercise
    group = GroupExercise(
        baseExercise=Exercise(base_exercise),
        solutionExercise=solution if solution else Solution(base_exercise),
        extendedExercises=extendedes
    )

    base_solution = map_solution[base_exercise.title]

    try:
        group.baseExercise.set_solution(base_solution)
        group.solutionExercise.set_solution(base_solution)
        for extended in group.extendedExercises:
            extended.set_solution(map_extended[extended.title])
    except Exception as e:
        print_error(f"Error: {e}")

   
    return group

def create_group_exercises(obj_exercises):
    group_exercises = []
    
    # Tạo bản sao để không ảnh hưởng đến list gốc
    exercises_copy = obj_exercises.copy()
    map_solution = {}
    with open("../gen_testcase_sample/data1.json", "r", encoding="utf-8") as f:
        solutions = json.load(f)
        for solution in solutions:
            map_solution[solution["id"]] = solution
    
    map_extended = {}
    with open("../gen_testcase_sample/data_extend.json", "r", encoding="utf-8") as f:
        extendeds = json.load(f)
        for extended in extendeds:
            map_extended[extended["id"]] = extended
    
    # Nhóm các bài tập theo baseName
    while len(exercises_copy) > 0:
        group = create_group_exercise(exercises_copy, map_solution, map_extended)
        group_exercises.append(group)
    
    group_exercises.sort(key=lambda x: x.baseExercise.point, reverse=True)
    return group_exercises 