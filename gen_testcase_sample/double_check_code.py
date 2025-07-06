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

def send_prompt_to_chatgpt(driver, prompt):
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
        print(f"Đã gửi prompt: {prompt[:50]}...")
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
        driver.get("https://chatgpt.com/c/686aa684-1a4c-800d-9d95-c740679c41a3")

        results = []
        
        for prompt in prompts_list:
            sleep(3)
            if send_prompt_to_chatgpt(driver, prompt["prompt"]):
                sleep(6)  # Wait for response to start
                response = get_latest_response(driver, prompt["title"])
                results.append(response)
                return results
                # Wait between prompts
        return results
    except Exception as e:
        print_error(f"Lỗi khi xử lý prompts: {e}")
    finally:
        input(">>> Nhấn Enter để đóng trình duyệt...")
        driver.quit()

def generate_prompt(data):     
    prompts =  "Bạn hãy chạy đoạn code python sau và kết quả trả về kết quả"
    prompts += f"\ncode:{'\n'.join(data['code_sample'])}"
    prompts += f"\ninput ={'\n'.join(data['input_sample'])}"
    prompts += f"\noutput={'\n'.join(data['output_sample'])}"
    prompts += f"\nKết quả sai rồi, hãy sửa lại"
    prompts += f'Hãy trả về json string có dạng json to string, để trong code tôi chuyển thành json qua hàm json.loads,' 
    prompts += f'kết quả trả về là json có 2 field: "result là array of string" và "title {data["id"]}"' 
    prompts += f"Trả về trong cùng 1 dòng và không nói gì thêm"
    return prompts

def get_prompts():
    prompts = []
    filename = "data.json"
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item["id"] != "Đếm số lượng từ có độ dài lẻ":
            continue
        prompt = generate_prompt(item)
        prompts.append({
            "prompt": prompt,
            "title": item["id"]
        })
    return prompts

if __name__ == "__main__":
    prompts = get_prompts()
    data =process_prompts(prompts)
