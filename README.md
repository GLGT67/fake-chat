# 💬 Messenger Fake Chat (Mobile-First Web App)

> 🚀 **Dùng trực tiếp trên iPhone tại đây:** [**https://glgt67.github.io/fake-chat/**](https://glgt67.github.io/fake-chat/)

---

## 📱 Cài đặt lên iPhone như App Thật (PWA 0đ - Không cần App Store)
1. Mở link trên bằng trình duyệt **Safari** trên iPhone.
2. Bấm nút **Chia sẻ (Share)** (biểu tượng hình vuông có mũi tên chỉ lên ở đáy Safari).
3. Chọn **"Thêm vào Màn hình chính" (Add to Home Screen)**.
4. Xong! Ứng dụng sẽ xuất hiện như app Messenger thật trên màn hình, mở toàn màn hình (không có thanh địa chỉ Safari), chạy mượt 120Hz và lưu offline.

---

## 🛠️ Hướng dẫn Sử dụng Chi tiết

### 1. Soạn tin nhắn 2 chiều & Đổi người gửi siêu tốc
* Cạnh ô nhập tin nhắn có nút **`[Tôi gửi ➔]` / `[◀ Bạn gửi]`**: Chạm 1 lần để đảo chiều người gửi ngay lập tức mà không cần vào cài đặt.
* Gõ chữ và bấm **Gửi**, hoặc để trống bấm để gửi **biểu tượng Like xanh lớn 👍**.

### 2. Chỉnh sửa tin nhắn trực tiếp (In-Place Edit)
* **Chạm đúp (hoặc bấm vào)** bất kỳ tin nhắn nào trên màn hình để:
  - Sửa lại nội dung tin nhắn.
  - Sửa mốc thời gian gửi (VD: `09:41`).
  - Đổi chiều người gửi (Tôi ↔ Đối phương).
  - Đổi trạng thái tin nhắn: *Đã xem (Avatar nhỏ)*, *Đã nhận (Tích đầy)*, *Đã gửi (Tích rỗng)*, *Đang gửi*.
  - Chèn thêm tin nhắn lên trên / xuống dưới, hoặc xóa tin nhắn đó.

### 3. Thêm tin nhắn đặc biệt (Nút `+`)
* Bấm nút **`+`** ở góc trái thanh nhập liệu để:
  - Gửi ảnh chụp từ thiết bị.
  - Gửi tin nhắn ghi âm (Voice note sóng âm chân thực).
  - Chèn mốc thời gian (VD: `14:30 - HÔM NAY`).
  - Chèn thông báo cuộc gọi thoại / video hoặc cuộc gọi nhỡ.

### 4. Chụp màn hình sạch sẽ & Xuất ảnh Retina
* **Cách 1 (Chụp trực tiếp bằng phím iPhone)**:
  - Bấm nút **"Chế độ Chụp Ảnh"** trên thanh công cụ trên cùng. Toàn bộ menu công cụ sẽ ẩn sạch 100%, trả về màn hình Messenger iOS nguyên bản để bạn bấm phím cứng iPhone chụp trực tiếp không cần cắt cúp.
  - Chạm vào nút mờ góc dưới để bật lại công cụ khi cần.
* **Cách 2 (Tải ảnh sắc nét 3x)**:
  - Bấm nút **"Tải ảnh PNG"**: Hệ thống sẽ tự động xuất ảnh chụp màn hình độ phân giải Retina 3x lưu thẳng vào Photos.

### 5. Cài đặt Đối phương & Hệ thống iOS (Nút Cài đặt hoặc chạm vào Tên/Avatar)
* Đổi tên, tích xanh xác minh, đổi avatar (tải từ máy hoặc chọn mẫu).
* Bật/tắt chấm xanh Online, chỉnh dòng chữ trạng thái ("Đang hoạt động", "Hoạt động 5p trước"...).
* Đổi màu chủ đề (Classic Blue, Ocean, Berry Pink, Sunset, Mint) & Bật/tắt chế độ tối (Dark Mode OLED).
* Chỉnh thanh trạng thái iOS: Đồng hồ, mức pin %, đang sạc ⚡, cột sóng 5G/4G/Wifi.

### 6. Thả cảm xúc tin nhắn (Reactions)
* **Chạm giữ hoặc nhấn vào icon cảm xúc cạnh tin nhắn** để mở bảng Bottom Sheet với 6 biểu tượng nguyên bản từ APK gốc: Thích 👍, Yêu thích ❤️, Haha 😂, Wow 😮, Buồn 😢, Phẫn nộ 😡.
* Huy hiệu cảm xúc sẽ hiển thị đè ở góc dưới tin nhắn chuẩn 1:1 Messenger.

### 7. Điều hướng Đa Màn hình (Chuẩn APK 1:1)
* Bấm nút **`<`** trên thanh tiêu đề để quay về **Màn hình chính "Đoạn chat"** (`activity_main_messenger.xml`): Xem danh sách story, thanh tìm kiếm, và chuyển đổi giữa các cuộc trò chuyện.
* Bấm biểu tượng **Bút chì ✏️** ở góc trên phải để mở màn hình **"Tạo liên hệ giả"** (`activity_fake_contact_messenger.xml`): Nhập tên, tải ảnh đại diện, chỉnh trạng thái online và bấm **LƯU** để tạo hội thoại mới.

### 8. Giả lập Cuộc gọi thoại & Video
* Bấm icon **Điện thoại** hoặc **Máy quay** ở góc trên phải để giả lập cuộc gọi đến (chuông reo, avatar lớn, nút nghe/từ chối). Sau khi kết thúc, thời lượng cuộc gọi sẽ tự động được ghi log vào khung chat.
* Khi nghe máy sẽ có đồng hồ đếm giây thời gian thực và tự động ghi log vào đoạn chat khi cúp máy.
