import subprocess
import datetime
import logging
import os

logging.basicConfig(
    filename='logs/automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_task(script_path, task_name):
    print(f"Starting {task_name}...")
    try:
        result = subprocess.run(['python3', script_path], check=True, capture_output=True, text=True)
        logging.info(f"SUCCESS: {task_name}")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"FAILED: {task_name}. ERROR: {e.stderr}")
        print(f"Error during {task_name}. Check logs/automation.log for details.")
        return False
    
def main():
    print(f"--- Automation Triggered: {datetime.datetime.now()} ---")
    if run_task('src/scraper.py', 'Web Scraper'):
        run_task('src/reporter.py', 'Data Reporter')

    print("---Automation Cycle Complete---")

if __name__ == "__main__":
    main()
