import aiohttp
import asyncio
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from group_creator import create_group_exercises
from utils import print_error, print_info
from models.exercise.group_exercise import GroupExercise
from file_reader import extract_exercises_from_docx
import json

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://localhost"
}






semaphore = asyncio.Semaphore(10)

async def ask_openrouter_async(content: str) -> str:
    messages = [
        {"role": "system", "content": "Bạn là một giáo viên lập trình"},
        {"role": "user", "content": content}
    ]
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages
    }

    async with semaphore:  # Giới hạn số luồng
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(API_URL, headers=HEADERS, json=data) as resp:
                    if resp.status != 200:
                        return f"[Lỗi {resp.status}]: {await resp.text()}"
                    response_json = await resp.json()
                    return response_json["choices"][0]["message"]["content"]
            except Exception as e:
                return f"[Lỗi]: {e}"


# Test với file "ĐỀ SỐ 05.docx"
def get_prompts():
    prompts = []
    filename = "../files/2_de.docx"
    exercises = extract_exercises_from_docx(filename)
    group_exercises = create_group_exercises(exercises)
    for exercise in group_exercises:
        if not check_group_exercise(exercise):
            continue
        prompt = generate_prompt(exercise)
        prompts.append(prompt)
        print(prompt)
        return prompts
    return prompts

async def main(prompts):
    result_prompts = []
    tasks = [ask_openrouter_async(prompt) for prompt in prompts]

    for i, coro in enumerate(asyncio.as_completed(tasks), 1):
        result = await coro
        try:
            result_prompts.append(json.loads(result))
        except Exception as e:
            print_error("Lỗi: " + str(e))
            print_error("result: " + result)
        print("result: " + str(len(result_prompts)) + "/" + str(len(prompts)))
    return result_prompts

# Chạy thử
if __name__ == "__main__":
    prompts = get_prompts()
    print_info("Tạo prompts length: " + str(len(prompts)))
    results = asyncio.run(main(prompts))
    print_info("Ghi ra file json")
    data = []
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
