import os
import time
import re
import yaml
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TailHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        # store last read offset per file
        self.positions = {}
        # precompile keyword regex (case-insensitive)
        kw = "|".join([re.escape(k) for k in config.get("keywords", [])])
        self.keyword_re = re.compile(rf"({kw})", re.IGNORECASE) if kw else None

        # initialize positions for existing files
        for f in config.get("files", []):
            try:
                self.positions[f] = os.path.getsize(f)
            except FileNotFoundError:
                self.positions[f] = 0

    def on_modified(self, event):
        # only handle file modifications
        if event.is_directory:
            return
        path = os.path.abspath(event.src_path)
        if path not in self.positions:
            return
        self._tail_and_scan(path)

    def _tail_and_scan(self, path):
        try:
            with open(path, "r", errors="ignore") as fh:
                fh.seek(self.positions.get(path, 0))
                new = fh.read()
                self.positions[path] = fh.tell()
        except Exception as e:
            print(f"⚠ Could not read {path}: {e}")
            return

        if not new:
            return

        for line in new.splitlines():
            print(f"{path}: {line}")
            if self.keyword_re and self.keyword_re.search(line):
                self._alert(path, line)

    def _alert(self, path, line):
        summary = self.config.get("notify_summary", "Log Alert")
        # Use notify-send for desktop notifications (Ubuntu)
        cmd = [self.config.get("notify_command", "notify-send"), summary, f"{os.path.basename(path)}: {line}"]
        try:
            subprocess.Popen(cmd)
        except Exception as e:
            print(f"Failed to send notification: {e}")

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def watch_loop(config):
    # create parent directories to watch (watchdog watches directories)
    watch_dirs = set()
    for f in config.get("files", []):
        watch_dirs.add(os.path.dirname(os.path.abspath(f)) or ".")

    event_handler = TailHandler(config)
    observer = Observer()
    for d in watch_dirs:
        observer.schedule(event_handler, path=d, recursive=False)
        print(f"Watching directory: {d}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    cfg = load_config()
    watch_loop(cfg)
