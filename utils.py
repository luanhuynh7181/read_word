import re
from colorama import Fore, Style

def remove_empty_items(list):
    result = []
    for item in list:
        if item.strip() != "":
            result.append(remove_extra_whitespace(item))
    return result

def remove_extra_whitespace(text):
    """
    Xóa khoảng trắng thừa: ở đầu, cuối và giữa các từ
    """
    if not text:
        return ""
    
    # Xóa khoảng trắng ở đầu và cuối
    text = text.strip()
    
    # Thay thế nhiều khoảng trắng liên tiếp bằng một khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    
    return text



def print_error(message):
    print(Fore.RED + f"{message}" + Style.RESET_ALL)


def print_info(message):
    print(Fore.GREEN +  f"{message}" + Style.RESET_ALL)


