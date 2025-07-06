import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from file_reader import extract_exercises_from_docx
from group_creator import create_group_exercises
from utils import print_info, print_error
import asyncio
import json
from models.exercise.group_exercise import GroupExercise
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
def setup_driver():
    options = Options()
    options.add_argument(r"--user-data-dir=C:/Users/admin/ChromeSeleniumProfile")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--no-sandbox")
    service = Service("C:/Users/admin/Downloads/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return driver
json_file = "data1.json"
def send_prompt_to_chatgpt(driver, prompt, title):
    try:
        # Find chat input
        chat_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#prompt-textarea"))
        )
        chat_input.clear()
        chat_input.send_keys(prompt)
        sleep(1)
        # Find and click send button
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']"))
        )
        send_button.click()
        print(f"Đã gửi prompt: {title}...")
        return True
    except Exception as e:
        print(f"Lỗi khi gửi prompt: {e}")
        return False

def get_latest_response(driver, search_text="Tìm số nguyên", timeout=30, poll_frequency=0.5):
    try:
        # Chờ cho đến khi có response chứa span với nội dung cần tìm
        WebDriverWait(driver, timeout, poll_frequency).until(
            lambda d: d.find_elements(By.XPATH, f"//span[contains(., '{search_text}')]")
        )
        
        # Tìm tất cả các span chứa nội dung
        spans = driver.find_elements(By.XPATH, f"//span[contains(., '{search_text}')]")
        
        if not spans:
            print(f"Không tìm thấy span chứa nội dung '{search_text}'")
            return None
            
        # Lấy span mới nhất (cuối cùng trong danh sách)
        last_span = spans[-1]
        
        # Scroll vào view để đảm bảo element sẵn sàng
        driver.execute_script("arguments[0].scrollIntoView(true);", last_span)
        
        # Kiểm tra lại nội dung sau khi scroll
        WebDriverWait(driver, 10).until(
            lambda d: search_text in last_span.text and len(last_span.text.strip()) > 0
        )
        
        return last_span.text
        
    except TimeoutException:
        print(f"Timeout khi chờ span chứa '{search_text}'")
        return None
    except NoSuchElementException:
        print("Không tìm thấy thẻ span")
        return None
    except StaleElementReferenceException:
        print("Element không còn tồn tại, thử lại...")
        return get_latest_response(driver, search_text, timeout)  # Retry
    except Exception as e:
        print(f"Lỗi không xác định: {str(e)}")
        return None

def process_prompts(prompts_list):
    driver = setup_driver()
    print_info("Tạo trình duyệt thành công")
    try:
        driver.get("https://chatgpt.com/c/686aa0e9-9128-800d-b71c-d70579a640f7")

        results = []
        
        for prompt in prompts_list:
            sleep(1)
            if send_prompt_to_chatgpt(driver, prompt["prompt"], prompt["title"]):
                sleep(12)  # Wait for response to start
                response = get_latest_response(driver, prompt["title"])
                results.append(response)
                write_data(response, prompt["title"])
                # Wait between prompts
        sleep(1)
        return results
       
    except Exception as e:
        print_error(f"Lỗi khi xử lý prompts: {e}")
    finally:
        input(">>> Nhấn Enter để đóng trình duyệt...")
        driver.quit()


def check_group_exercise(exercise):
        if exercise.baseExercise.title == "":
            print_info("Bài tập không có title: " + exercise.baseExercise.title)
            return False
        if exercise.baseExercise.description_section == []:
            print_info("Bài tập không có description: " + exercise.baseExercise.title)
            return False
        if exercise.baseExercise.input_section == []:
            print_info("Bài tập không có input: " + exercise.baseExercise.title)
            return False
        if exercise.baseExercise.output_section == []:
            print_info("Bài tập không có output: " + exercise.baseExercise.title)
            return False
        if exercise.solutionExercise.solution_textes == []:
            print_info("Bài tập không có solution: " + exercise.baseExercise.title)
            return False
        return True

def generate_prompt(exercise: GroupExercise):       
    prompts = ""
    data_input = {
        "id": "Số nguyên tố lớn nhất",
        "des": "Cho dãy số nguyên (a1, a2, ... , an), 1 ≤n ≤ 10000; với mọi i sao cho ai ≤ 10^8. Hãy tìm số nguyên tố lớn nhất trong dãy trên",
        "input": ["Dòng thứ nhất chứa số nguyên dương n", "Dòng thứ hai chứa n số nguyên a1, a2, ... , an"],
        "output": ["Dòng thứ nhất ghi số nguyên tố lớn nhất", "Dòng thứ hai ghi các chỉ số trong dãy mà giá trị của nó là số nguyên tố lớn nhất"],
        "solution": ["Sắp xếp dãy số theo thứ tự giảm dần", "Phép nhân lớn nhất sẽ là phép nhân của hai số đầu tiên trong dãy."],
    }
    data_output = {
    "id": 2,
    "short_name": "MAXPRIME",
    "point":"10",
  "input_sample": ["6", "2 4 5 7 9 7"],
  "output_sample": ["7", "4 6"],
  "code_sample": [
    "import math",
    "",
    "def is_prime(n):",
    "    if n < 2:",
    "        return False",
    "    for i in range(2, int(math.sqrt(n)) + 1):",
    "        if n % i == 0:",
    "            return False",
    "    return True",
    "",
    "n = int(input())",
    "arr = list(map(int, input().split()))",
    "max_prime = -1",
    "indices = []",
    "for idx, num in enumerate(arr):",
    "    if is_prime(num) and num > max_prime:",
    "        max_prime = num",
    "        indices = [idx + 1]",
    "    elif is_prime(num) and num == max_prime:",
    "        indices.append(idx + 1)",
    "print(max_prime)",
    "print(' '.join(map(str, indices)))"
  ]
}

    data_exercise = {
        "id": exercise.baseExercise.title,
        "des": ".".join(exercise.baseExercise.description_section),
        "input": exercise.baseExercise.input_section,
        "output": exercise.baseExercise.output_section,
        "solution": "\n".join(exercise.solutionExercise.solution_textes)
    }
    prompts = f"tôi cho bạn 1 description và lời giải, hãy viết cho tôi testcase mẫu và code python trả về theo json"
    prompts += f".Ví dụ: input: {data_input} và output: {data_output}."
    prompts += f'Đề: input: {data_exercise}.'
    prompts += 'Kết quả trả về là json (id, input_sample, output_sample, code_sample, short_name,point)'
    prompts += 'với short_name là tên viết tắt của id tối đa 10 kí tự, point là điểm của bài tập, tính short_name'
    prompts += ': point  = tổng dòng code *10 + function * 20  +  (map, list, set, dict, tuple, ...)* 20 + for, while,* 20' 
    prompts += 'để trong code tôi chuyển thành json qua hàm json.loads. kết quả trả về 1 dòng json string duy nhất'
    prompts += f".Hãy xài cú pháp đơn giản thôi cho học sinh dễ hiểu. Không xài class, regex"
    return prompts

def get_prompts():
    prompts = []
    filename = "../files/sach.docx"
    exercises = extract_exercises_from_docx(filename)
    group_exercises = create_group_exercises(exercises)
    for exercise in group_exercises:
        check_group_exercise(exercise)
        prompt = generate_prompt(exercise)
        prompts.append({
            "prompt": prompt,
            "title": exercise.baseExercise.title
        })
    return prompts

def write_data(response, title):
    try:
        data = []
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        # Kiểm tra trùng title
        # Parse response và thêm vào data
        new_item = json.loads(json.loads(response))
        list_field = ["id", "input_sample", "output_sample", "code_sample", "short_name"]
        for field in list_field:
            if field not in new_item:
                print_info(f"new_item khong có field {field}: {new_item}")
                return
     
        data.append(new_item)
        print_info(f"progress: {len(data)}/120")
        
        # Ghi file với định dạng đẹp
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, 
                     ensure_ascii=False, 
                     indent=2,
                     sort_keys=True,
                     separators=(',', ': '))
            
    except Exception as e:
        print(f"Lỗi khi ghi data: {title} - {str(e)}")

def retry():
    data = []
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    prompts = []
    filename = "../files/sach.docx"
    exercises = extract_exercises_from_docx(filename)
    group_exercises = create_group_exercises(exercises)
    print_info(f"retry: data:{ len(group_exercises)- len(data)}  / exercises:{len(group_exercises)}")
    for exercise in group_exercises:
        if exercise.baseExercise.title  in [item["id"] for item in data]:
            continue
        prompt = generate_prompt(exercise)
        prompts.append({
            "prompt": prompt,
            "title": exercise.baseExercise.title
        })
    return prompts


if __name__ == "__main__":
    # prompts = get_prompts()
    prompts = retry()
    data =process_prompts(prompts)
