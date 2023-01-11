import time
import psutil
import threading
import sys

RUNNING = True
CPU_COUNT = psutil.cpu_count()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def input_thread():
    global RUNNING
    input()
    RUNNING = False


def is_float(element: any) -> bool:
    # If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def display_usage1(cpu_usage, memmory_usage, bars=30):
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = "█" * int(cpu_percent * bars) + "-" * (bars - int(cpu_percent * bars))
    mem_percent = (memmory_usage / 100.0)
    mem_bar = "█" * int(mem_percent * bars) + "-" * (bars - int(mem_percent * bars))

    print(f"\rCPU Usage : |{cpu_bar}| {cpu_usage:.2f}%   ", end="")
    print(f"MEM Usage : |{mem_bar}| {mem_percent:.2f}%   ", end="\r")


def display_usage2(cpu_usage, memmory_usage, cpu_core_usage, bars=30):
    global CPU_COUNT
    if cpu_usage < 80:
        cpu_color = bcolors.OKGREEN
    else:
        cpu_color = bcolors.FAIL
    if memmory_usage < 80:
        memmory_color = bcolors.OKGREEN
    else:
        memmory_color = bcolors.FAIL
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = "█" * int(cpu_percent * bars) + "-" * (bars - int(cpu_percent * bars))
    mem_percent = (memmory_usage / 100.0)
    mem_bar = "█" * int(mem_percent * bars) + "-" * (bars - int(mem_percent * bars))
    print(f"{cpu_color}CPU Usage : |{cpu_bar}| {cpu_usage:.2f}%   {bcolors.ENDC}", end="")
    print(f"{memmory_color}MEM Usage : |{mem_bar}| {mem_percent:.2f}%   {bcolors.ENDC}")
    counter = 1
    for core in cpu_core_usage:
        core_percent = (core / 100.0)
        core_bar = "█" * int(core_percent * bars * 2) + "-" * (bars * 2 - int(core_percent * bars * 2))
        if counter < 10:
            counter_show = str(counter) + " "
        else:
            counter_show = counter
        print(f"Core{counter_show} Usage : |{core_bar}| {core:.2f}%   ")
        counter += 1
    sys.stdout.write(f"\033[{CPU_COUNT + 1}F")


def main():
    global RUNNING
    while RUNNING:
        mode = input("simple or pro ? ").lower()
        if mode == "simple" or mode == "s":
            threading.Thread(target=input_thread, args=(), name="input_capture_thread").start()
            while RUNNING:
                display_usage1(psutil.cpu_percent(), psutil.virtual_memory().percent)
                time.sleep(1)
        elif mode == "pro" or mode == "p":
            while RUNNING:
                refrresh_time = input("refresh time (in seccond) : ")
                if is_float(refrresh_time):
                    refrresh_time = float(refrresh_time)
                    break
            threading.Thread(target=input_thread, args=(), name="input_capture_thread").start()
            while RUNNING:
                display_usage2(cpu_usage=psutil.cpu_percent(), memmory_usage=psutil.virtual_memory().percent,
                               cpu_core_usage=psutil.cpu_percent(percpu=True))
                time.sleep(refrresh_time)


if __name__ == "__main__":
    main()
