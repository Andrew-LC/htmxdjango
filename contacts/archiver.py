import time
from threading import Thread
from random import random
import json
from .models import Contact

class Archiver:
    archive_status = "Waiting"
    archive_progress = 0
    thread = None

    def status(self):
        return Archiver.archive_status

    def progress(self):
        return Archiver.archive_progress

    def run(self):
        if Archiver.archive_status == "Waiting":
            Archiver.archive_status = "Running"
            Archiver.archive_progress = 0
            Archiver.thread = Thread(target=self.run_impl)
            Archiver.thread.start()

    def run_impl(self):
        data = self.fetch_model_data()  # Fetch model data
        self.save_to_file(data, 'contacts.json')  # Save data to contacts.json

        for i in range(10):
            time.sleep(1 * random())
            if Archiver.archive_status != "Running":
                return
            Archiver.archive_progress = (i + 1) / 10
            print("Here... " + str(Archiver.archive_progress))
        time.sleep(1)
        if Archiver.archive_status != "Running":
            return
        Archiver.archive_status = "Complete"

    def fetch_model_data(self):
        model_data = Contact.objects.values()
        return list(model_data)

    def save_to_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def archive_file(self):
        return 'contacts.json'

    def reset(self):
        Archiver.archive_status = "Waiting"

    @classmethod
    def get(cls):
        return Archiver()
