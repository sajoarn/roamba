# Multi-Line print test
import time

def move_up_char(num):
    return f"\033[{num}A"

print("Line1: abc\nLine2: def")
time.sleep(1)
print(f"{move_up_char(2)}Line3: hij\nLine4: klm")