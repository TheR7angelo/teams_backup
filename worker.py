import os
import datetime

from PySide6.QtCore import QObject, Signal, QRunnable

import datetime

import sqlite3
import time

import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from fonction import *


class WorkerSignals(QObject):
    start = Signal(bool)
    progress = Signal(int)
    data = Signal(dict)


class Worker(QRunnable):
    """
    Worker thread
    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    signals = WorkerSignals()

    def __init__(self, fonction):
        super().__init__()
        self.fonction = fonction

        self.is_killed = False

    def run(self):

        self.signals.start.emit(True)

        try:
            if self.fonction == 'tout':
                print('tout')
            else:
                print(f'Fonction {self.fonction} non trouver')

        except Exception as error:
            print(error)

            date = datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')
            file = os.path.basename(__file__).replace('.py', '')
            directory = 'crash-log\\'

            os.makedirs(directory, exist_ok=True)
            with open(f'{directory}{file}_{date}.txt', 'w') as crash_report:
                crash_report.write(str(error))

        self.signals.start.emit(False)

    def kill(self):
        self.is_killed = True
        return
