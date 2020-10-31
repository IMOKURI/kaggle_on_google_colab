import io
import os
import subprocess
import sys

from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class Setup:
    def __init__(self):
        auth.authenticate_user()

        drive_service = build("drive", "v3")
        results = (
            drive_service.files()
            .list(q="name = 'kaggle.json'", fields="files(id)")
            .execute()
        )
        kaggle_api_key = results.get("files", [])

        filename = "/root/.kaggle/kaggle.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        request = drive_service.files().get_media(fileId=kaggle_api_key[0]["id"])
        fh = io.FileIO(filename, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        os.chmod(filename, 600)

    def dirs(self, compete):
        dirs = [
            f"/content/zip",
            f"/content/{compete}/input/{compete}",
            f"/content/{compete}/output",
            f"/content/{compete}/working",
        ]
        for dir_ in dirs:
            os.makedirs(dir_, exist_ok=True)


def exec_get_lines(cmd):
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    while True:
        line = proc.stdout.readline()
        if line:
            yield line

        if not line and proc.poll() is not None:
            break
