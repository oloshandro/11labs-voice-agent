import os

APP_DIR = os.path.join(os.path.abspath(os.curdir))
WORK_DIR = os.path.join(APP_DIR, "app")

LOG_DIR = os.path.join(os.sep, WORK_DIR, "chat_logs")
REC_DIR = os.path.join(WORK_DIR, "recordings")
PROMPTS_DIR = os.path.join(WORK_DIR, "prompts")
PROMPTS_FILE_PATH = os.path.join(PROMPTS_DIR, "prompts.yaml")