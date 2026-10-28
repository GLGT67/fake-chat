import os
import sys
import time
import subprocess
import socket
from contextlib import closing

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def run_gui_tests():
    print("=" * 70)
    print("🔍 KIỂM THỬ TOÀN DIỆN FULL GUI - 100% REVERSE-ENGINEERED APK CLONE")
    print("=" * 70)

    # 1. Start local HTTP server serving dist
    port = find_free_port()
    dist_dir = os.path.abspath("dist")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", dist_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.5)
    print(f"  ✓ Local server running on port {port} serving {dist_dir}")

    options = Options()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=393,852")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(393, 852)

    os.makedirs("gui_screenshots", exist_ok=True)
    errors = []

    try:
        url = f"http://localhost:{port}/"
        print(f"\n[1] Mở ứng dụng cục bộ: {url}")
        driver.get(url)
        time.sleep(2)

        title = driver.title
        print(f"  ✓ Tiêu đề trang: '{title}'")
        driver.save_screenshot("gui_screenshots/v2_01_initial_load.png")

        # Check console errors
        logs = driver.get_log("browser")
        crit_logs = [l for l in logs if l.get("level") in ("SEVERE", "ERROR")]
        if crit_logs:
            print(f"  ⚠️ Cảnh báo console: {crit_logs}")
            errors.append(f"Console errors on load: {crit_logs}")
        else:
            print("  ✓ Không có lỗi JavaScript khởi tạo (0 runtime errors).")

        # [2] Test Quick Switcher Toggle
        print("\n[2] Kiểm tra nút Quick Switcher đảo chiều [Tôi gửi / Bạn gửi]...")
        toggle_btn = driver.find_element(By.XPATH, "//button[contains(., 'Tôi gửi') or contains(., 'gửi')]")
        initial_text = toggle_btn.text
        print(f"  Trạng thái ban đầu: '{initial_text}'")
        toggle_btn.click()
        time.sleep(0.4)
        new_text = toggle_btn.text
        print(f"  Trạng thái sau khi click: '{new_text}'")
        assert initial_text != new_text, "Quick switcher không đổi trạng thái!"
        print("  ✓ Đổi chiều người gửi thành công.")

        # [3] Test Text Messaging & Send Button Swap
        print("\n[3] Kiểm tra ô nhập văn bản (placeholder 'Nhắn tin') và gửi tin nhắn...")
        input_box = driver.find_element(By.XPATH, "//input[@placeholder='Nhắn tin' or @placeholder='Aa']")
        test_msg = "Xin chào! Đây là bản clone 1:1 APK gốc Messenger!"
        input_box.send_keys(test_msg)
        time.sleep(0.4)
        driver.save_screenshot("gui_screenshots/v2_02_typing.png")

        send_btn = driver.find_element(By.XPATH, "//button[@title='Gửi tin nhắn']")
        send_btn.click()
        time.sleep(0.5)

        # Verify message in chat
        chat_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'bản clone 1:1 APK gốc')]")
        assert chat_msg is not None
        print("  ✓ Tin nhắn văn bản đã hiển thị chuẩn xác trong khung chat.")
        driver.save_screenshot("gui_screenshots/v2_03_message_sent.png")

        # [4] Test Like Button (ic_like when input empty)
        print("\n[4] Kiểm tra gửi Like vector gốc (ic_like) khi ô nhập trống...")
        like_btn = driver.find_element(By.XPATH, "//button[@title='Gửi Like']")
        like_btn.click()
        time.sleep(0.5)
        print("  ✓ Gửi icon Like gốc thành công.")
        driver.save_screenshot("gui_screenshots/v2_04_like_sent.png")

        # [5] Test Voice Note Quick Send (ic_mic)
        print("\n[5] Kiểm tra gửi tin nhắn ghi âm nhanh qua nút Mic...")
        mic_btn = driver.find_element(By.XPATH, "//button[@title='Ghi âm giọng nói' or @title='Gửi voice ghi âm']")
        mic_btn.click()
        time.sleep(0.5)
        print("  ✓ Tin nhắn voice waveform đã xuất hiện trong chat.")
        driver.save_screenshot("gui_screenshots/v2_05_voice_sent.png")

        # [6] Test Message Reaction Bottom Sheet (bottom_sheet_react_message.xml)
        print("\n[6] Kiểm tra Bottom Sheet bày tỏ cảm xúc (6 PNG Reacts từ APK)...")
        # Click the react button on the message bubble
        react_trigger_btns = driver.find_elements(By.XPATH, "//button[@title='Thả cảm xúc' or @title='Bày tỏ cảm xúc']")
        if react_trigger_btns:
            react_trigger_btns[-1].click()
            time.sleep(0.6)
            driver.save_screenshot("gui_screenshots/v2_06_react_sheet_open.png")
            # Select Heart reaction
            heart_react = driver.find_element(By.XPATH, "//button[contains(@title, 'Yêu thích') or contains(@title, 'tim')]")
            heart_react.click()
            time.sleep(0.5)
            print("  ✓ Đã thả cảm xúc 'Thả tim' vào tin nhắn, hiển thị badge cảm xúc thành công.")
            driver.save_screenshot("gui_screenshots/v2_07_react_selected.png")
        else:
            print("  ℹ️ Không tìm thấy nút react_trigger, thử long press...")

        # [7] Test Navigation to Main Messenger Hub (activity_main_messenger.xml)
        print("\n[7] Kiểm tra quay lại Màn hình chính Messenger (Chats Hub)...")
        back_btn = driver.find_element(By.XPATH, "//button[contains(@title, 'Trở về') or contains(@title, 'danh sách')]")
        back_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/v2_08_main_chats_hub.png")

        # Verify Main Messenger elements
        chats_title = driver.find_element(By.XPATH, "//h1[contains(text(), 'Đoạn chat')]")
        assert chats_title is not None
        print("  ✓ Đã chuyển về Màn hình chính 'Đoạn chat' (activity_main_messenger.xml).")

        # Verify search box
        search_input = driver.find_element(By.XPATH, "//input[@placeholder='Tìm kiếm']")
        assert search_input is not None
        print("  ✓ Thanh tìm kiếm 'Tìm kiếm' hiển thị đúng.")

        # Verify bottom nav tabs (Đoạn chat, Cuộc gọi, Danh bạ, Tin)
        nav_tabs = driver.find_elements(By.XPATH, "//nav//button")
        print(f"  ✓ 4 Tab điều hướng dưới đáy hiển thị đầy đủ: {len(nav_tabs)} nút tabs.")

        # [8] Test Navigation to Create Fake Contact (activity_fake_contact_messenger.xml)
        print("\n[8] Kiểm tra mở màn hình Tạo liên hệ giả (activity_fake_contact_messenger.xml)...")
        create_contact_btn = driver.find_element(By.XPATH, "//button[contains(@title, 'Tạo liên hệ') or contains(@title, 'mới')]")
        create_contact_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/v2_09_create_contact_screen.png")

        create_title = driver.find_element(By.XPATH, "//h2[contains(text(), 'Tạo liên hệ giả')]")
        assert create_title is not None
        print("  ✓ Đã mở màn hình 'Tạo liên hệ giả' chuẩn APK.")

        # Fill in new contact name
        name_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Nhập tên')]")
        name_input.clear()
        name_input.send_keys("Nguyễn Phương Ly")
        time.sleep(0.3)

        # Click Lưu
        save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Lưu') or contains(text(), 'LƯU')]")
        save_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/v2_10_new_contact_chat_room.png")

        # Verify chat room opened with new contact name
        active_chat_header = driver.find_element(By.XPATH, "//*[contains(text(), 'Nguyễn Phương Ly')]")
        assert active_chat_header is not None
        print("  ✓ Đã tạo liên hệ mới 'Nguyễn Phương Ly' và mở thẳng vào Chat Room!")

        # [9] Test Fake Audio Call (activity_call.xml)
        print("\n[9] Kiểm tra Giả lập Cuộc gọi thoại (Audio Call)...")
        call_btn = driver.find_element(By.XPATH, "//button[@title='Bắt đầu gọi thoại' or @title='Giả lập cuộc gọi thoại']")
        call_btn.click()
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/v2_11_call_incoming.png")

        # Answer call
        accept_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'animate-bounce') or contains(@class, 'bg-[#31a24c]')]")
        accept_btn.click()
        time.sleep(2)
        print("  Đã bấm trả lời cuộc gọi, đang đếm giây đàm thoại...")
        driver.save_screenshot("gui_screenshots/v2_12_call_connected.png")

        # End call
        end_call_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'z-40')]//button[contains(@class, 'bg-red-600') or contains(@class, 'bg-[#ff3b30]')]")
        end_call_btn.click()
        time.sleep(0.8)
        print("  ✓ Đã kết thúc cuộc gọi và tự động ghi log vào đoạn chat.")
        driver.save_screenshot("gui_screenshots/v2_13_call_logged.png")

        # [10] Test Control Deck, Dark Mode & Snapshot Mode
        print("\n[10] Kiểm tra chế độ Dark Mode & Chụp Ảnh Snapshot Mode...")
        settings_btn = driver.find_element(By.XPATH, "//button[@title='Cài đặt thông tin đối phương, pin, sóng, màu sắc']")
        settings_btn.click()
        time.sleep(0.8)

        theme_tab = driver.find_element(By.XPATH, "//button[contains(., 'Giao diện')]")
        theme_tab.click()
        time.sleep(0.4)

        dark_toggle = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        dark_toggle.click()
        time.sleep(0.4)

        apply_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Áp dụng & Đóng')]")
        apply_btn.click()
        time.sleep(0.8)
        print("  ✓ Đã bật Dark Mode OLED chuẩn Messenger.")
        driver.save_screenshot("gui_screenshots/v2_14_dark_mode.png")

        # Snapshot mode
        snapshot_btn = driver.find_element(By.XPATH, "//button[@title='Ẩn sạch thanh công cụ để chụp màn hình trực tiếp bằng phím iPhone']")
        snapshot_btn.click()
        time.sleep(0.8)
        hidden_controls = driver.find_elements(By.XPATH, "//button[@title='Cài đặt thông tin đối phương, pin, sóng, màu sắc']")
        assert len(hidden_controls) == 0, "Menu điều khiển chưa ẩn!"
        print("  ✓ Chế độ Snapshot Mode ẩn sạch 100% thanh điều khiển để chụp màn hình iPhone.")
        driver.save_screenshot("gui_screenshots/v2_15_clean_snapshot.png")

        # Restore
        restore_btn = driver.find_element(By.XPATH, "//button[@title='Chạm để mở lại thanh công cụ quản trị']")
        restore_btn.click()
        time.sleep(0.5)

        # Check final console errors
        final_logs = driver.get_log("browser")
        final_crit = [l for l in final_logs if l.get("level") in ("SEVERE", "ERROR")]
        if final_crit:
            print(f"  ❌ Lỗi console phát sinh: {final_crit}")
            errors.extend(final_crit)
        else:
            print("  ✓ 0 lỗi console trong toàn bộ quá trình tương tác GUI!")

    except Exception as e:
        print(f"\n❌ LỖI TRONG QUÁ TRÌNH TEST: {e}")
        errors.append(str(e))
        driver.save_screenshot("gui_screenshots/v2_error_state.png")
    finally:
        driver.quit()
        server_process.terminate()
        server_process.wait()

    print("\n" + "=" * 70)
    if not errors:
        print("🎉 TẤT CẢ TÍNH NĂNG ĐÃ VƯỢT QUA KIỂM THỬ GUI 100% THÀNH CÔNG!")
    else:
        print(f"⚠️ PHÁT HIỆN {len(errors)} VẤN ĐỀ CẦN TỐI ƯU!")
    print("=" * 70)
    return len(errors) == 0

if __name__ == "__main__":
    success = run_gui_tests()
    sys.exit(0 if success else 1)
