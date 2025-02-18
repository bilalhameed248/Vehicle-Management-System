import sys
from PyQt5.QtWidgets import QApplication
from templates.login import LoginPage

def main():
    app = QApplication(sys.argv)
    
    # Create and show the login window
    login_window = LoginPage()
    login_window.show()
    
    # Execute the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


# import sys
# import os
# import time
# import multiprocessing
# from PyQt5.QtWidgets import QApplication
# from templates.login import LoginPage
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# # Function to start the application
# def start_app():
#     app = QApplication(sys.argv)
#     login_window = LoginPage()
#     login_window.show()
#     sys.exit(app.exec_())

# # File Watcher Event Handler
# class ReloadHandler(FileSystemEventHandler):
#     def __init__(self, restart_event):
#         self.restart_event = restart_event

#     def on_any_event(self, event):
#         if event.is_directory:
#             return
#         print(f"File changed: {event.src_path}. Restarting...")
#         self.restart_event.set()  # Trigger restart

# # Function to monitor file changes
# def monitor_changes(process):
#     restart_event = multiprocessing.Event()
#     observer = Observer()
#     event_handler = ReloadHandler(restart_event)

#     observer.schedule(event_handler, path=".", recursive=True)
#     observer.start()

#     try:
#         while True:
#             time.sleep(1)
#             if restart_event.is_set():
#                 print("Restarting application...")
#                 process.terminate()
#                 process.join()
#                 process = multiprocessing.Process(target=start_app)
#                 process.start()
#                 restart_event.clear()
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

# if __name__ == "__main__":
#     process = multiprocessing.Process(target=start_app)
#     process.start()
#     monitor_changes(process)
