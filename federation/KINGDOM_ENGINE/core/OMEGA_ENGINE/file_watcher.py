from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time, os

TARGET = Path(os.environ["HOME"]) / "KINGDOM_ENGINE" / "memory" / "all_files_raw"

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print("[WATCHER] modified:", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print("[WATCHER] created:", event.src_path)

def start_watcher():
    obs = Observer()
    obs.schedule(Handler(), str(TARGET), recursive=True)
    obs.start()
    print("[WATCHER] running…")
    return obs

if __name__ == "__main__":
    obs = start_watcher()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
