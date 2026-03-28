import subprocess
import time
import re
import sys


def run_tests(file_path="inputs.txt"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        return

    test_number = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"(.*?)\s+\((.*?)\)\s+\((.*?)\)", line)
        if not match:
            print(f"Test #{test_number}: Parse Error - Невірний формат рядка: {line}")
            test_number += 1
            continue

        script_path = match.group(1).strip()
        args = match.group(2).strip()
        expected = match.group(3).strip()

        start_time = time.perf_counter()
        result_status = ""

        try:
            process = subprocess.run(
                [sys.executable, script_path],
                input=args,
                text=True,
                capture_output=True,
                timeout=1.0
            )

            execution_time = time.perf_counter() - start_time

            if process.returncode != 0:
                result_status = "Runtime Error"
            else:
                output = process.stdout.strip()

                if output:
                    actual_result = output.split()[-1]
                else:
                    actual_result = ""

                if actual_result == expected:
                    result_status = "Accepted"
                else:
                    result_status = "Wrong Answer"

        except subprocess.TimeoutExpired:
            execution_time = time.perf_counter() - start_time
            result_status = "Time Limit Exceeded"
        except Exception:
            execution_time = time.perf_counter() - start_time
            result_status = "Runtime Error"

        print(f"Test #{test_number}: {result_status} ({execution_time:.3f}s)")
        test_number += 1


if __name__ == "__main__":
    run_tests()