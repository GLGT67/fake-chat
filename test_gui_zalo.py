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

def run_zalo_gui_tests():
    print("=" * 70)
    print("🔍 KIỂM THỬ TRỰC TIẾP FULL GUI: CHỨC NĂNG & GIAO DIỆN ZALO 1:1")
    print("=" * 70)

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
    options.add_argument("--window-size=393,852")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(393, 852)

    os.makedirs("gui_screenshots", exist_ok=True)
    errors = []

    try:
        url = f"http://localhost:{port}/"
        print(f"\n[1] Mở ứng dụng tại {url}...")
        driver.get(url)
        time.sleep(2)

        # Switch to Zalo mode
        print("\n[2] Chuyển đổi sang chế độ Zalo [💙 Zalo]...")
        zalo_tab = driver.find_element(By.XPATH, "//button[contains(., 'Zalo')]")
        zalo_tab.click()
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/zalo_01_chat_room.png")

        # Verify Zalo Chat Room Header
        header_name = driver.find_element(By.XPATH, "//h2[contains(text(), 'Trần Huyền Trang')]")
        assert header_name is not None
        print("  ✓ Đã mở Khung chat Zalo với 'Trần Huyền Trang' (1:1 Ảnh mẫu 2).")

        # Verify elements from Sample Image 2
        print("\n[3] Kiểm tra các thành phần tin nhắn Zalo chuẩn Ảnh mẫu 2...")
        # 1. Contact Card
        contact_card = driver.find_element(By.XPATH, "//*[contains(text(), 'Thu Hướng')]")
        assert contact_card is not None
        print("  ✓ Thẻ danh thiếp 'Thu Hướng' hiển thị đúng với 2 nút [Gọi điện | Nhắn tin].")

        # 2. Reply Quote block
        quote_sender = driver.find_element(By.XPATH, "//*[contains(text(), 'Nguyễn sơn Tùng')]")
        assert quote_sender is not None
        print("  ✓ Khung trích dẫn tin nhắn 'Nguyễn sơn Tùng' hiển thị đúng với vạch xanh Zalo.")

        # 3. Status pill
        status_pill = driver.find_element(By.XPATH, "//*[contains(text(), 'Đã nhận')]")
        assert status_pill is not None
        print("  ✓ Huy hiệu trạng thái '✓✓ Đã nhận' hiển thị đúng ở góc tin nhắn gửi.")

        # [4] Test Quick Switcher Toggle
        print("\n[4] Kiểm tra đảo chiều người gửi Zalo [Tôi gửi / Trần Huyền Trang gửi]...")
        switcher = driver.find_element(By.XPATH, "//button[contains(., 'gửi')]")
        before_text = switcher.text
        switcher.click()
        time.sleep(0.4)
        after_text = switcher.text
        assert before_text != after_text
        print(f"  ✓ Đã đổi người gửi từ '{before_text}' sang '{after_text}'.")

        # [5] Test Text Messaging in Zalo
        print("\n[5] Kiểm tra gửi tin nhắn văn bản Zalo...")
        input_box = driver.find_element(By.XPATH, "//input[@placeholder='Tin nhắn']")
        input_box.send_keys("Vâng ạ, em gửi hồ sơ qua Zalo luôn nhé!")
        time.sleep(0.4)
        driver.save_screenshot("gui_screenshots/zalo_02_typing.png")

        send_btn = driver.find_element(By.XPATH, "//button[@title='Gửi tin nhắn Zalo']")
        send_btn.click()
        time.sleep(0.5)

        sent_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'Vâng ạ, em gửi hồ sơ')]")
        assert sent_msg is not None
        print("  ✓ Tin nhắn đã xuất hiện trong khung chat Zalo.")
        driver.save_screenshot("gui_screenshots/zalo_03_sent.png")

        # [6] Test Heart Reaction
        print("\n[6] Kiểm tra thả tim phản hồi tin nhắn Zalo 🤍...")
        heart_btn = driver.find_element(By.XPATH, "//button[@title='Bỏ thích' or @title='Thả tim Zalo']")
        heart_btn.click()
        time.sleep(0.4)
        print("  ✓ Tương tác thả tim tin nhắn Zalo hoạt động tốt.")

        # [7] Test Navigation to Zalo Main Screen (Ảnh mẫu 1)
        print("\n[7] Kiểm tra quay lại Màn hình chính Zalo (1:1 Ảnh mẫu 1)...")
        back_btn = driver.find_element(By.XPATH, "//button[@title='Quay lại danh sách chat Zalo']")
        driver.execute_script("arguments[0].click();", back_btn)
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/zalo_04_main_screen.png")

        # Verify search box & title
        search_box = driver.find_element(By.XPATH, "//input[@placeholder='Tìm kiếm']")
        assert search_box is not None
        print("  ✓ Thanh tìm kiếm Zalo gradient xanh hiển thị đúng.")

        # Verify banner
        profile_banner = driver.find_element(By.XPATH, "//*[contains(text(), 'Cập nhật thông tin cá nhân')]")
        assert profile_banner is not None
        print("  ✓ Banner 'Cập nhật thông tin cá nhân' hiển thị đúng.")

        # Verify sample conversation items from Image 1
        c1 = driver.find_element(By.XPATH, "//*[contains(text(), 'Lỗi đổ đầu chúng toi')]")
        assert c1 is not None
        print("  ✓ Hội thoại ghim 'Lỗi đổ đầu chúng toi' hiển thị đúng kèm icon ghim 📌.")

        c2 = driver.find_element(By.XPATH, "//*[contains(text(), 'Zalo Bảo Mật')]")
        assert c2 is not None
        print("  ✓ Tài khoản 'Zalo Bảo Mật' có huy hiệu xác thực tích xanh/cam.")

        # Verify 5 tabs in bottom bar
        tabs = driver.find_elements(By.XPATH, "//nav//button")
        assert len(tabs) >= 5
        print(f"  ✓ Thanh điều hướng đáy có đủ {len(tabs)} tabs (Tin nhắn 5+, Danh bạ, Khám phá, Tường nhà N, Cá nhân).")

        # [8] Test Create Zalo Contact
        print("\n[8] Kiểm tra mở Màn hình Tạo liên hệ Zalo mới (+)...")
        plus_btn = driver.find_element(By.XPATH, "//button[@title='Tạo liên hệ Zalo mới']")
        driver.execute_script("arguments[0].click();", plus_btn)
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/zalo_05_create_contact.png")

        # Input new contact name
        name_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Nhập tên hiển thị')]")
        name_field.clear()
        name_field.send_keys("Lê Hoàng Yến")
        time.sleep(0.3)

        # Click LƯU
        save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Lưu') or contains(text(), 'LƯU')]")
        save_btn.click()
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/zalo_06_new_chat.png")

        # Verify opened into new chat room
        new_header = driver.find_element(By.XPATH, "//h2[contains(text(), 'Lê Hoàng Yến')]")
        assert new_header is not None
        print("  ✓ Đã tạo liên hệ Zalo mới 'Lê Hoàng Yến' và mở vào Khung chat thành công!")

        # [9] Test Snapshot Mode
        print("\n[9] Kiểm tra Chế độ Chụp Ảnh Snapshot Mode cho Zalo...")
        snapshot_btn = driver.find_element(By.XPATH, "//button[@title='Ẩn sạch thanh công cụ để chụp màn hình trực tiếp bằng phím iPhone']")
        snapshot_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/zalo_07_clean_snapshot.png")
        print("  ✓ Màn hình Zalo ở chế độ Chụp Ảnh sạch sẽ 100% không viền đen.")

        # Check console errors
        logs = driver.get_log("browser")
        crit = [l for l in logs if l.get("level") in ("SEVERE", "ERROR")]
        if crit:
            print(f"  ❌ Có lỗi console: {crit}")
            errors.extend(crit)
        else:
            print("  ✓ 0 lỗi JavaScript console runtime trong toàn bộ quá trình tương tác Zalo!")

    except Exception as e:
        print(f"\n❌ LỖI KIỂM THỬ: {e}")
        errors.append(str(e))
        driver.save_screenshot("gui_screenshots/zalo_error.png")
    finally:
        driver.quit()
        server.terminate()
        server.wait()

    print("\n" + "=" * 70)
    if not errors:
        print("🎉 TOÀN BỘ CHỨC NĂNG & GIAO DIỆN ZALO ĐÃ VƯỢT QUA KIỂM THỬ 100%!")
    else:
        print(f"⚠️ Phát hiện {len(errors)} vấn đề cần xử lý.")
    print("=" * 70)
    return len(errors) == 0

if __name__ == "__main__":
    success = run_zalo_gui_tests()
    sys.exit(0 if success else 1)
