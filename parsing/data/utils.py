import time
from threading import Thread


class EditThread(Thread):
    def __init__(self, message):
        super(EditThread, self).__init__()
        self.message = message
        self.stopped = False

    def run(self):
        max_count = self.message.text.count('.')
        count = max_count
        while not self.stopped:
            count = 1 + count % max_count
            time.sleep(0.5)
            self.message.edit_text('Начинаем поиск' + '.' * count)

    def stop(self):
        self.stopped = True