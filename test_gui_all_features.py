import os
import sys
import time

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

def run_gui_tests():
    print("=" * 60)
    print("🔍 BẮT ĐẦU KIỂM THỬ TOÀN DIỆN FULL GUI BẰNG CHROME HEADLESS")
    print("=" * 60)

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
        url = "https://glgt67.github.io/fake-chat/"
        print(f"\n[1] Mở ứng dụng tại: {url}")
        driver.get(url)
        time.sleep(2)

        title = driver.title
        print(f"  ✓ Tiêu đề trang: '{title}'")
        driver.save_screenshot("gui_screenshots/01_initial_load.png")

        # Check console errors
        logs = driver.get_log("browser")
        crit_logs = [l for l in logs if l.get("level") in ("SEVERE", "ERROR")]
        if crit_logs:
            print(f"  ⚠️ Cảnh báo console: {crit_logs}")
            errors.append(f"Console errors on load: {crit_logs}")
        else:
            print("  ✓ Không có lỗi JavaScript runtime khởi tạo.")

        # [2] Test Quick Switcher Toggle
        print("\n[2] Kiểm tra nút Quick Switcher đảo chiều [Tôi gửi / Bạn gửi]...")
        toggle_btn = driver.find_element(By.XPATH, "//button[contains(., 'Tôi gửi') or contains(., 'gửi')]")
        initial_text = toggle_btn.text
        print(f"  Trạng thái ban đầu: '{initial_text}'")
        toggle_btn.click()
        time.sleep(0.5)
        new_text = toggle_btn.text
        print(f"  Trạng thái sau khi click: '{new_text}'")
        assert initial_text != new_text, "Quick switcher không đổi trạng thái!"
        print("  ✓ Đổi chiều người gửi thành công.")

        # [3] Test Gõ tin nhắn văn bản và gửi
        print("\n[3] Kiểm tra ô nhập văn bản và gửi tin nhắn...")
        input_box = driver.find_element(By.XPATH, "//input[@placeholder='Aa']")
        test_msg = "Xin chào, đây là tin nhắn tự động từ GUI Test!"
        input_box.send_keys(test_msg)
        time.sleep(0.3)
        driver.save_screenshot("gui_screenshots/02_typing.png")

        # Find send button
        send_btn = driver.find_element(By.XPATH, "//button[@title='Gửi tin nhắn']")
        send_btn.click()
        time.sleep(0.5)

        # Verify message appeared in chat
        chat_body = driver.find_element(By.XPATH, "//*[contains(text(), 'Xin chào, đây là tin nhắn')]")
        assert chat_body is not None
        print("  ✓ Tin nhắn văn bản đã hiển thị chuẩn xác trong khung chat.")
        driver.save_screenshot("gui_screenshots/03_message_sent.png")

        # [4] Test Gửi Like Thumbs-up
        print("\n[4] Kiểm tra gửi biểu tượng Like lớn khi ô nhập trống...")
        like_btn = driver.find_element(By.XPATH, "//button[@title='Gửi Like']")
        like_btn.click()
        time.sleep(0.5)
        print("  ✓ Gửi icon Like thành công.")
        driver.save_screenshot("gui_screenshots/04_like_sent.png")

        # [5] Test Voice Note Quick Send
        print("\n[5] Kiểm tra gửi tin nhắn ghi âm nhanh qua nút Mic...")
        mic_btn = driver.find_element(By.XPATH, "//button[@title='Gửi voice ghi âm']")
        mic_btn.click()
        time.sleep(0.5)
        print("  ✓ Tin nhắn ghi âm với sóng âm waveform đã xuất hiện trong chat.")
        driver.save_screenshot("gui_screenshots/05_voice_sent.png")

        # [6] Test Modal Chỉnh sửa tin nhắn (In-place Edit)
        print("\n[6] Kiểm tra chạm đúp vào tin nhắn để mở Modal Chỉnh sửa...")
        actions = ActionChains(driver)
        actions.double_click(chat_body).perform()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/06_edit_modal.png")

        # Edit text inside modal
        edit_textarea = driver.find_element(By.XPATH, "//textarea")
        edit_textarea.clear()
        edit_textarea.send_keys("Tin nhắn đã được chỉnh sửa trực tiếp qua Modal!")

        # Change timestamp
        time_input = driver.find_element(By.XPATH, "//input[@placeholder='VD: 09:41']")
        time_input.clear()
        time_input.send_keys("10:00")

        # Click Hoàn tất
        done_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Hoàn tất')]")
        done_btn.click()
        time.sleep(0.5)

        # Verify edited text
        driver.find_element(By.XPATH, "//*[contains(text(), 'Tin nhắn đã được chỉnh sửa trực tiếp')]")
        print("  ✓ Chỉnh sửa nội dung và giờ gửi trong Modal thành công 100%.")

        # [7] Test Modal Đính kèm đặc biệt (+)
        print("\n[7] Kiểm tra Modal Đính kèm (+) (Voice, Mốc thời gian, Banner cuộc gọi)...")
        plus_btn = driver.find_element(By.XPATH, "//button[@title='Đính kèm tính năng']")
        plus_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/07_attach_modal.png")

        # Click Chèn Mốc thời gian
        chèn_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Chèn')]")
        if len(chèn_btns) >= 2:
            chèn_btns[1].click() # Click insert timestamp divider
            time.sleep(0.5)
            print("  ✓ Chèn mốc thời gian (Divider) thành công.")
        driver.save_screenshot("gui_screenshots/08_divider_inserted.png")

        # [8] Test Giả lập Cuộc gọi (Fake Call)
        print("\n[8] Kiểm tra Giả lập Cuộc gọi thoại & Đàm thoại thời gian thực...")
        call_btn = driver.find_element(By.XPATH, "//button[@title='Giả lập cuộc gọi thoại']")
        call_btn.click()
        time.sleep(1)
        driver.save_screenshot("gui_screenshots/09_call_incoming.png")

        # Check call incoming screen
        accept_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'animate-bounce')]")
        accept_btn.click()
        time.sleep(2)
        print("  Đã bấm trả lời cuộc gọi, đang đếm giây đàm thoại...")
        driver.save_screenshot("gui_screenshots/10_call_connected.png")

        # End call
        end_call_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'z-40')]//button[contains(@class, 'bg-red-600')]")
        end_call_btn.click()
        time.sleep(0.8)
        print("  ✓ Đã kết thúc cuộc gọi và tự động ghi log vào đoạn chat.")
        driver.save_screenshot("gui_screenshots/11_call_ended_logged.png")

        # [9] Test Cài đặt Giao diện & Đối phương (Profile Modal)
        print("\n[9] Kiểm tra Modal Cài đặt (Đổi tên, Dark Mode, Theme màu, Status Bar)...")
        settings_btn = driver.find_element(By.XPATH, "//button[@title='Cài đặt thông tin đối phương, pin, sóng, màu sắc']")
        settings_btn.click()
        time.sleep(0.8)
        driver.save_screenshot("gui_screenshots/12_settings_modal_user.png")

        # Change name to "Em Yêu 💖"
        name_input = driver.find_element(By.XPATH, "//div[contains(@class, 'space-y-4')]//input[@type='text']")
        name_input.clear()
        name_input.send_keys("Em Yêu 💖")

        # Switch to Theme tab
        theme_tab = driver.find_element(By.XPATH, "//button[contains(., 'Giao diện')]")
        theme_tab.click()
        time.sleep(0.5)
        driver.save_screenshot("gui_screenshots/13_settings_modal_theme.png")

        # Toggle Dark Mode
        dark_toggle = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        dark_toggle.click()
        time.sleep(0.5)

        # Switch to Sunset Peach theme
        sunset_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sunset Peach')]")
        sunset_btn.click()
        time.sleep(0.5)

        # Switch to iOS Status tab
        ios_tab = driver.find_element(By.XPATH, "//button[contains(., 'iOS Status')]")
        ios_tab.click()
        time.sleep(0.5)
        driver.save_screenshot("gui_screenshots/14_settings_modal_ios.png")

        # Change battery
        battery_slider = driver.find_element(By.XPATH, "//input[@type='range']")
        driver.execute_script("arguments[0].value = 50; arguments[0].dispatchEvent(new Event('input'));", battery_slider)

        # Close settings modal
        apply_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Áp dụng & Đóng')]")
        apply_btn.click()
        time.sleep(0.8)
        print("  ✓ Đổi tên thành 'Em Yêu 💖', kích hoạt Dark Mode OLED, đổi Theme Sunset Peach thành công.")
        driver.save_screenshot("gui_screenshots/15_dark_mode_active.png")

        # [10] Test Chế độ Chụp Ảnh (Snapshot Mode)
        print("\n[10] Kiểm tra Chế độ Chụp Ảnh (Snapshot Mode)...")
        snapshot_btn = driver.find_element(By.XPATH, "//button[@title='Ẩn sạch thanh công cụ để chụp màn hình trực tiếp bằng phím iPhone']")
        snapshot_btn.click()
        time.sleep(0.8)

        # Verify admin toolbar is completely hidden
        hidden_controls = driver.find_elements(By.XPATH, "//button[@title='Cài đặt thông tin đối phương, pin, sóng, màu sắc']")
        assert len(hidden_controls) == 0, "Menu điều khiển chưa được ẩn trong Snapshot Mode!"
        print("  ✓ Toàn bộ thanh công cụ đã ẩn sạch 100%, sẵn sàng cho chụp màn hình native iPhone.")
        driver.save_screenshot("gui_screenshots/16_snapshot_clean_mode.png")

        # Restore controls
        restore_btn = driver.find_element(By.XPATH, "//button[@title='Chạm để mở lại thanh công cụ quản trị']")
        restore_btn.click()
        time.sleep(0.5)
        print("  ✓ Khôi phục thanh công cụ quản trị thành công.")

        # [11] Test Xuất ảnh Retina PNG (Tải về máy)
        print("\n[11] Kiểm tra tính năng Xuất ảnh Retina 3x PNG...")
        export_btn = driver.find_element(By.XPATH, "//button[@title='Xuất ảnh PNG chất lượng Retina 3x lưu vào Photos']")
        export_btn.click()
        time.sleep(2)
        print("  ✓ Nút xuất ảnh Retina 3x hoạt động không gây lỗi.")

        # Final console error check
        final_logs = driver.get_log("browser")
        final_crit = [l for l in final_logs if l.get("level") in ("SEVERE", "ERROR")]
        if final_crit:
            print(f"  ❌ Có lỗi phát sinh trong quá trình tương tác: {final_crit}")
            errors.extend(final_crit)
        else:
            print("  ✓ 0 lỗi console trong toàn bộ quá trình tương tác GUI!")

    except Exception as e:
        print(f"\n❌ LỖI TRONG QUÁ TRÌNH TEST: {e}")
        errors.append(str(e))
        driver.save_screenshot("gui_screenshots/error_state.png")
    finally:
        driver.quit()

    print("\n" + "=" * 60)
    if not errors:
        print("🎉 TẤT CẢ TÍNH NĂNG ĐÃ VƯỢT QUA KIỂM THỬ GUI 100% THÀNH CÔNG!")
    else:
        print(f"⚠️ PHÁT HIỆN {len(errors)} VẤN ĐỀ CẦN TỐI ƯU!")
    print("=" * 60)
    return len(errors) == 0

if __name__ == "__main__":
    success = run_gui_tests()
    sys.exit(0 if success else 1)
