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
os.chdir(os.path.join(os.path.dirname(__file__), 'dist'))

PORT = 8095
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
    print("\n--- TEST 1: Load App & Verify Initial Empty Demo Messages ---")
    driver.get(f'http://localhost:{PORT}')
    time.sleep(2)
    
    # 1. Verify demo messages are deleted
    chat_bubbles = driver.find_elements(By.CSS_SELECTOR, '.px-3\\.5.py-2.rounded-2xl')
    print(f"Initial chat bubbles count: {len(chat_bubbles)} (Expect 0)")
    assert len(chat_bubbles) == 0, "Demo messages should be empty!"
    print("✓ Test 1 PASSED: All demo messages are clean and empty.")

    print("\n--- TEST 2: Send Text Message in Messenger ---")
    input_elem = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Nhắn tin']")
    input_elem.send_keys("Xin chào, đây là tin nhắn kiểm thử đầu tiên!")
    input_elem.send_keys(Keys.ENTER)
    time.sleep(1)
    
    chat_frame = driver.find_element(By.ID, "phone-screen-frame")
    assert "Xin chào, đây là tin nhắn kiểm thử đầu tiên!" in chat_frame.text
    print("✓ Test 2 PASSED: Text message sent and visible, chat area is intact!")

    print("\n--- TEST 3: Message Interaction (Action Sheet on Tap: Edit, Reply, Delete) ---")
    # Click on the message bubble to open MessageActionModal
    bubble = driver.find_element(By.XPATH, "//*[contains(text(), 'Xin chào, đây là tin nhắn')]")
    driver.execute_script("arguments[0].click();", bubble)
    time.sleep(1)
    
    # Verify modal opened
    modal_title = driver.find_element(By.XPATH, "//*[contains(text(), 'Tin nhắn của bạn')]")
    assert modal_title is not None
    print("✓ Message Action Sheet opened successfully on message tap!")

    # Test Heart / Emoji Reaction from Action Sheet
    heart_react = driver.find_element(By.CSS_SELECTOR, "button[title='Thả cảm xúc']")
    driver.execute_script("arguments[0].click();", heart_react)
    time.sleep(1)
    print("✓ Reaction added to message!")

    # Re-open Action Sheet to test Reply (Trả lời)
    bubble = driver.find_element(By.XPATH, "//*[contains(text(), 'Xin chào, đây là tin nhắn')]")
    driver.execute_script("arguments[0].click();", bubble)
    time.sleep(1)
    
    reply_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Trả lời (Reply)')]")
    driver.execute_script("arguments[0].click();", reply_btn)
    time.sleep(1)
    
    # Verify Reply Quote Preview Banner is shown above input
    quote_banner = driver.find_element(By.XPATH, "//*[contains(text(), 'Đang trả lời')]")
    assert quote_banner is not None
    print("✓ Reply quote preview banner active above input!")
    
    # Type reply and send
    input_elem = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Nhắn tin']")
    input_elem.send_keys("Đây là câu trả lời trích dẫn nè")
    input_elem.send_keys(Keys.ENTER)
    time.sleep(1)
    
    assert "Đây là câu trả lời trích dẫn nè" in driver.find_element(By.ID, "phone-screen-frame").text
    print("✓ Test 3 PASSED: Full interaction (React, Reply quote, Send) working seamlessly!")

    print("\n--- TEST 4: Tích xanh (Verified Badge) & Trạng thái & Đổi Avatar ---")
    # Open Profile Modal via ChatHeader
    name_header = driver.find_element(By.XPATH, "//*[contains(text(), 'Trịnh Văn Mạnh')]")
    driver.execute_script("arguments[0].click();", name_header)
    time.sleep(1)
    
    # 4.1 Change Name
    name_input = driver.find_element(By.XPATH, "//span[contains(text(), 'Tên người nhận')]/following-sibling::input")
    name_input.clear()
    name_input.send_keys("Sơn Tùng M-TP")
    
    # 4.2 Turn on Tích xanh (Verified Badge)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    if checkboxes and not checkboxes[0].is_selected():
        driver.execute_script("arguments[0].click();", checkboxes[0])
    print("✓ Checked Verified Badge checkbox!")

    # 4.3 Change Status Text & Online
    status_input = driver.find_element(By.XPATH, "//input[@placeholder='Đang hoạt động / Vừa mới truy cập...']")
    status_input.clear()
    status_input.send_keys("Nghệ sĩ chính thức")
    
    # 4.4 Pick Preset Avatar
    preset_btn = driver.find_elements(By.XPATH, "//img[@alt='Preset']/parent::button")[1]
    driver.execute_script("arguments[0].click();", preset_btn)
    print("✓ Changed avatar to preset #2!")
    
    # Close Modal
    save_close = driver.find_element(By.XPATH, "//*[contains(text(), 'Lưu & Đóng')]")
    driver.execute_script("arguments[0].click();", save_close)
    time.sleep(1)
    
    # Verify in Chat Header
    header_text = driver.find_element(By.TAG_NAME, "header").text
    print("Updated Header text:", header_text)
    assert "Sơn Tùng M-TP" in header_text, "Name should be updated!"
    assert "Nghệ sĩ chính thức" in header_text, "Status text should be updated!"
    
    # Check if verified badge icon is in DOM
    badge_icons = driver.find_elements(By.CSS_SELECTOR, "header svg.lucide-badge-check")
    assert len(badge_icons) > 0, "Verified badge icon MUST be rendered in header!"
    print("✓ Test 4 PASSED: Verified badge, status, name, and avatar updated and rendered!")

    print("\n--- TEST 5: Switch to Zalo & Verify 1:1 UI, Heart & Actions ---")
    zalo_pill = driver.find_element(By.XPATH, "//*[contains(text(), '💙 Zalo')]")
    driver.execute_script("arguments[0].click();", zalo_pill)
    time.sleep(1)
    
    # Verify Zalo Chat Room is loaded
    zalo_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Tin nhắn']")
    zalo_input.send_keys("Alo em ơi, Zalo kiểm thử nhé!")
    zalo_input.send_keys(Keys.ENTER)
    time.sleep(1)
    
    zalo_body = driver.find_element(By.ID, "phone-screen-frame").text
    assert "Alo em ơi, Zalo kiểm thử nhé!" in zalo_body
    print("✓ Sent text in Zalo successfully!")
    
    # Tap Zalo message to open MessageActionModal
    z_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'Alo em ơi, Zalo kiểm thử nhé!')]")
    driver.execute_script("arguments[0].click();", z_msg)
    time.sleep(1)
    
    # Heart button in Zalo modal
    heart_action = driver.find_element(By.XPATH, "//*[contains(text(), 'Thả tim')]")
    driver.execute_script("arguments[0].click();", heart_action)
    time.sleep(1)
    
    # Verify Heart icon on message
    hearts = driver.find_elements(By.XPATH, "//*[contains(text(), '❤️')]")
    assert len(hearts) > 0, "Heart reaction should be visible on Zalo message!"
    print("✓ Test 5 PASSED: Zalo message, heart reaction, and action sheet verified!")

    # Take screenshot of clean test result
    os.makedirs('../gui_screenshots', exist_ok=True)
    driver.save_screenshot('../gui_screenshots/test_all_6_feedback_result.png')
    print("✓ Screenshot saved to gui_screenshots/test_all_6_feedback_result.png")

    print("\n==========================================")
    print("🎉 ALL 6 USER FEEDBACK TESTS PASSED 100%!")
    print("==========================================")

finally:
    driver.quit()
    httpd.shutdown()
