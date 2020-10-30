import io
import os

from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class Setup:
    def __init__(self, compete):
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

        dirs = [
            f"/content/{compete}/input/{compete}",
            f"/content/{compete}/output",
            f"/content/{compete}/working",
        ]
        for dir_ in dirs:
            os.makedirs(dir_, exist_ok=True)
