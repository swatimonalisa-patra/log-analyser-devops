#!/usr/bin/env python3
"""
Log Monitor Script
Monitors a folder for new log files and automatically runs the log analyser on them.
"""

import time
import os
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogFileHandler(FileSystemEventHandler):
    """Handler for log file events."""

    def __init__(self, analyser_script):
        self.analyser_script = analyser_script

    def on_created(self, event):
        """Called when a new file is created."""
        if not event.is_directory and event.src_path.endswith('.log'):
            print(f"New log file detected: {event.src_path}")
            self.analyze_log(event.src_path)

    def on_modified(self, event):
        """Called when a file is modified."""
        if not event.is_directory and event.src_path.endswith('.log'):
            print(f"Log file modified: {event.src_path}")
            self.analyze_log(event.src_path)

    def analyze_log(self, log_path):
        """Run the log analyser on the given log file."""
        try:
            # Run the analyser script
            result = subprocess.run([
                sys.executable, self.analyser_script,
                log_path, '--output', f"{os.path.splitext(log_path)[0]}_analysis"
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"Analysis completed successfully for {log_path}")
            else:
                print(f"Analysis failed for {log_path}")
                print(f"Error: {result.stderr}")

        except subprocess.TimeoutExpired:
            print(f"Analysis timed out for {log_path}")
        except Exception as e:
            print(f"Error analyzing {log_path}: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python log_monitor.py <folder_to_monitor>")
        sys.exit(1)

    folder_to_monitor = sys.argv[1]

    if not os.path.isdir(folder_to_monitor):
        print(f"Error: {folder_to_monitor} is not a valid directory")
        sys.exit(1)

    # Path to the analyser script (assume it's in the same directory)
    analyser_script = os.path.join(os.path.dirname(__file__), 'log_analyser.py')

    if not os.path.exists(analyser_script):
        print(f"Error: Analyser script not found at {analyser_script}")
        sys.exit(1)

    print(f"Monitoring folder: {folder_to_monitor}")
    print("Press Ctrl+C to stop monitoring")

    # Set up the observer
    event_handler = LogFileHandler(analyser_script)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=False)

    # Start monitoring
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()