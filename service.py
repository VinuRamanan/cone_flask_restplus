
import ctypes
import os
import random
import socket
import threading

import servicemanager
import win32event
import win32service
import win32serviceutil
from waitress import serve
from app import app


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('thread start\n')
        serve(app, listen='*:5000')  # blocking
        print('thread done\n')

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def exit(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


class SMWinservice(win32serviceutil.ServiceFramework):
    _svc_name_ = 'WaitressService'
    _svc_display_name_ = 'Waitress server'
    _svc_description_ = 'Python waitress WSGI service'

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stopEvt = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stopEvt)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        print('main start')
        self.server = ServerThread()
        self.server.start()
        print('waiting on win32event')
        win32event.WaitForSingleObject(self.stopEvt, win32event.INFINITE)
        self.server.exit()  # raise SystemExit in inner thread
        print('waiting on thread')
        self.server.join()
        print('main done')


if __name__ == '__main__':
    SMWinservice.parse_command_line()
