import datetime
import os

class AutoArchiver:
    def __init__(self):
        self.archive_dir = "/sdcard/Omnissiah_Workspace/copy_archive/"
        os.makedirs(self.archive_dir, exist_ok=True)
    
    def archive_text(self, text, source="unknown"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.archive_dir}/{timestamp}_{source}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Source: {source}\n")
            f.write(f"Time: {timestamp}\n")
            f.write("="*50 + "\n")
            f.write(text)
        return filename

archiver = AutoArchiver()
print("🔄 Auto-archiver ready - all copy-paste will be saved")
