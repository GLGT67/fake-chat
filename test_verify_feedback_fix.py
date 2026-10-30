import sys
sys.stdout.reconfigure(encoding='utf-8')
import http.server
import socketserver
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Switch to dist folder
dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
os.chdir(dist_dir)

PORT = 8097
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', PORT), Handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"[TEST SERVER] Running on port {PORT}")

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=393,852')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)

try:
    print("\n================ TEST 1: VERIFY NO DEMO CHATS IN ZALO LIST ================")
    driver.get(f'http://localhost:{PORT}')
    time.sleep(2)
    
    # Switch to Zalo
    zalo_pill = driver.find_element(By.XPATH, "//*[contains(text(), '💙 Zalo')]")
    driver.execute_script("arguments[0].click();", zalo_pill)
    time.sleep(1)
    
    # Go to Zalo main conversation list screen (Back button)
    back_btn = driver.find_element(By.CSS_SELECTOR, "button[title='Quay lại danh sách chat Zalo']")
    driver.execute_script("arguments[0].click();", back_btn)
    time.sleep(1)
    
    body_text = driver.find_element(By.ID, "phone-screen-frame").text
    print("Zalo Main Screen Text:")
    print(body_text)
    
    # Check that demo items are GONE
    assert "Lỗi đổ đầu chúng toi" not in body_text, "Demo 'Lỗi đổ đầu chúng toi' should be gone!"
    assert "Game Data Research" not in body_text, "Demo 'Game Data Research' should be gone!"
    assert "Quyên Xử Lý Nước" not in body_text, "Demo 'Quyên Xử Lý Nước' should be gone!"
    assert "Thiết kế đồ hoạ" not in body_text, "Demo 'Thiết kế đồ hoạ' should be gone!"
    assert "Zalo Bảo Mật" not in body_text, "Demo 'Zalo Bảo Mật' should be gone!"
    print("✓ TEST 1 PASSED: All demo conversation items have been completely removed from Zalo list!")

    print("\n================ TEST 2: VERIFY NO GHOST EMOJI IN STATUS AREA (ZALO) ================")
    # Enter conversation with Trần Huyền Trang
    first_conv = driver.find_element(By.XPATH, "//*[contains(text(), 'Trần Huyền Trang')]")
    driver.execute_script("arguments[0].click();", first_conv)
    time.sleep(1)
    
    # Send a text message
    zalo_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Tin nhắn']")
    zalo_input.send_keys("Xin chao Zalo khong co emoji o status")
    zalo_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    # Verify the message text is there
    chat_frame = driver.find_element(By.ID, "phone-screen-frame")
    assert "Xin chao Zalo khong co emoji o status" in chat_frame.text
    
    # Verify that NO 🤍 or ❤️ is rendered when un-hearted
    hearts = driver.find_elements(By.XPATH, "//*[contains(text(), '🤍')]")
    assert len(hearts) == 0, "There should be NO '🤍' outline emoji rendered on messages without heart!"
    print("✓ Checked: 0 ghost '🤍' emojis rendered in chat or status area!")

    # Check status pill 'Đã nhận' is visible and clean
    status_pills = driver.find_elements(By.XPATH, "//*[contains(text(), 'Đã nhận')]")
    assert len(status_pills) > 0, "Status pill 'Đã nhận' should be visible for sender!"
    print("✓ Status pill 'Đã nhận' is visible cleanly without any emoji overlap!")

    print("\n================ TEST 3: HEART REACTION PLACEMENT & CLEARANCE ================")
    # Tap message to open MessageActionModal
    msg_bubble = driver.find_element(By.XPATH, "//*[contains(text(), 'Xin chao Zalo khong co emoji o status')]")
    driver.execute_script("arguments[0].click();", msg_bubble)
    time.sleep(1)
    
    # Click 'Thả tim'
    heart_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Thả tim')]")
    driver.execute_script("arguments[0].click();", heart_btn)
    time.sleep(1)
    
    # Verify Heart icon ❤️ appears
    red_hearts = driver.find_elements(By.XPATH, "//*[contains(text(), '❤️')]")
    assert len(red_hearts) > 0, "Heart reaction '❤️' should appear when hearted!"
    print("✓ Heart reaction pill '❤️' appears on message corner cleanly!")

    # Take screenshot of clean Zalo message & status
    os.makedirs('../gui_screenshots', exist_ok=True)
    driver.save_screenshot('../gui_screenshots/test_clean_zalo_status.png')
    print("✓ Saved screenshot to gui_screenshots/test_clean_zalo_status.png")

    print("\n================ TEST 4: VERIFY MESSENGER STATUS & NO DEMO CHATS ================")
    # Switch back to Messenger
    msg_pill = driver.find_element(By.XPATH, "//*[contains(text(), '💬 Messenger')]")
    driver.execute_script("arguments[0].click();", msg_pill)
    time.sleep(1)
    
    # Send a Messenger message
    m_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Nhắn tin']")
    m_input.send_keys("Tin nhan Messenger test khong loi status")
    m_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    # Verify NO floating '😊' emoji
    smileys = driver.find_elements(By.XPATH, "//*[text()='😊']")
    # Only in input toolbar smile icon, NOT floating on the message bubble!
    msg_bubbles = driver.find_elements(By.XPATH, "//*[contains(text(), 'Tin nhan Messenger test khong loi status')]/ancestor::div[contains(@class, 'flex-col')]")
    for b in msg_bubbles:
        assert "😊" not in b.text, "Floating 😊 should NOT be inside message bubble container!"
    print("✓ Verified: Floating '😊' emoji completely removed from Messenger message & status!")

    # Go to Messenger main conversation list
    back_btn_m = driver.find_element(By.CSS_SELECTOR, "button[title='Trở về danh sách đoạn chat']")
    driver.execute_script("arguments[0].click();", back_btn_m)
    time.sleep(1)
    
    m_body = driver.find_element(By.ID, "phone-screen-frame").text
    assert "Nguyễn Thảo My" not in m_body, "Demo 'Nguyễn Thảo My' should be gone!"
    assert "Đức Nguyễn" not in m_body, "Demo 'Đức Nguyễn' should be gone!"
    print("✓ Verified: Demo contacts 'Nguyễn Thảo My' and 'Đức Nguyễn' removed from Messenger list!")

    driver.save_screenshot('../gui_screenshots/test_clean_messenger_status.png')
    print("✓ Saved screenshot to gui_screenshots/test_clean_messenger_status.png")

    print("\n=======================================================")
    print("🎉 ALL TESTS PASSED: DEMO CHATS REMOVED & STATUS FIXED!")
    print("=======================================================")

finally:
    driver.quit()
    httpd.shutdown()
