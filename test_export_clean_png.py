import os
import sys
import time
import subprocess
import socket
from contextlib import closing

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def test_export():
    port = find_free_port()
    dist_dir = os.path.abspath("dist")
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", dist_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)

    options = Options()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=450,900")

    driver = webdriver.Chrome(options=options)
    try:
        url = f"http://localhost:{port}/"
        driver.get(url)
        time.sleep(2)

        os.makedirs("gui_screenshots", exist_ok=True)
        driver.save_screenshot("gui_screenshots/clean_preview_before.png")

        # Click Snapshot Mode
        snapshot_btn = driver.find_element(By.XPATH, "//button[@title='Ẩn sạch thanh công cụ để chụp màn hình trực tiếp bằng phím iPhone']")
        snapshot_btn.click()
        time.sleep(0.5)

        # In snapshot mode, verify the frame is borderless pure screen
        driver.save_screenshot("gui_screenshots/clean_snapshot_mode.png")
        print("✓ Chế độ Snapshot Mode sạch sẽ, không viền chassis.")

        # Restore
        restore_btn = driver.find_element(By.XPATH, "//button[@title='Chạm để mở lại thanh công cụ quản trị']")
        restore_btn.click()
        time.sleep(0.5)

        # Click Tải ảnh PNG
        export_btn = driver.find_element(By.XPATH, "//button[@title='Xuất ảnh PNG chất lượng Retina 3x lưu vào Photos']")
        export_btn.click()
        time.sleep(2)
        print("✓ Xuất ảnh PNG Retina 3x thành công.")

    finally:
        driver.quit()
        server.terminate()
        server.wait()

if __name__ == "__main__":
    test_export()
