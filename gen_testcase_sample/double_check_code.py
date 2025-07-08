import json
from io import StringIO
from sys import stdout

def lamdata_check(data):
    inputs = data["input_sample"].copy()

    def mock_input():
        return inputs.pop(0)

    code = "\n".join(data["code_sample"])

    # Ghi lại output nếu muốn
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    # Thực thi
    exec(code, {"input": mock_input})

    # Trả lại output
    sys.stdout = old_stdout
    output = buffer.getvalue().strip().splitlines()

    return output


if __name__ == "__main__":
    json_file = "data1.json"
    with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

    
    for item in data:
        res = lamdata_check(item)
        if not res == item["output_sample"]:
            item["output_sample"] = res

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, 
                ensure_ascii=False, 
                indent=2,
                sort_keys=True,
                separators=(',', ': '))
