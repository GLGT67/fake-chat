<script>
  import { chatState, clearAllMessages } from '../state.svelte.js';
  import { Camera, Download, Settings, PhoneCall, Trash2, Eye, EyeOff } from '@lucide/svelte';
  import { toPng } from 'html-to-image';

  let isExporting = $state(false);

  function toggleSnapshotMode() {
    chatState.isSnapshotMode = !chatState.isSnapshotMode;
  }

  async function exportRetinaImage() {
    const node = document.getElementById('phone-screen-frame');
    if (!node) return;

    try {
      isExporting = true;
      const wasSnapshot = chatState.isSnapshotMode;
      chatState.isSnapshotMode = true; // hide controls before capture

      // allow DOM update
      await new Promise(r => setTimeout(r, 100));

      const dataUrl = await toPng(node, {
        pixelRatio: 3, // 3x Retina resolution
        quality: 0.98,
        skipFonts: true,
      });

      const link = document.createElement('a');
      link.download = `messenger_fake_${Date.now()}.png`;
      link.href = dataUrl;
      link.click();

      chatState.isSnapshotMode = wasSnapshot;
    } catch (err) {
      console.error('Export error:', err);
      alert('Không thể xuất ảnh: ' + err.message);
    } finally {
      isExporting = false;
    }
  }

  function handleClear() {
    if (confirm('Bạn có chắc chắn muốn xóa toàn bộ tin nhắn để bắt đầu đoạn chat mới không?')) {
      clearAllMessages();
    }
  }
</script>

{#if !chatState.isSnapshotMode}
  <!-- Desktop / Mobile Floating Control Bar -->
  <div class="fixed top-2 left-1/2 -translate-x-1/2 z-50 flex items-center bg-[#1e293b]/90 backdrop-blur-md text-white px-3 py-1.5 rounded-full shadow-2xl border border-white/10 space-x-2 text-[12px] font-medium transition-all max-w-[95vw] overflow-x-auto no-scrollbar">
    <!-- Snapshot Mode Button -->
    <button 
      type="button"
      class="flex items-center space-x-1 px-3 py-1 rounded-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold shadow-xs active:scale-95 transition-all cursor-pointer whitespace-nowrap"
      onclick={toggleSnapshotMode}
      title="Ẩn sạch thanh công cụ để chụp màn hình trực tiếp bằng phím iPhone"
    >
      <Camera size={14} strokeWidth={2.5} />
      <span>Chế độ Chụp Ảnh</span>
    </button>

    <!-- Retina Export Button -->
    <button 
      type="button"
      class="flex items-center space-x-1 px-2.5 py-1 rounded-full bg-blue-600 hover:bg-blue-500 text-white active:scale-95 transition-all cursor-pointer whitespace-nowrap"
      onclick={exportRetinaImage}
      disabled={isExporting}
      title="Xuất ảnh PNG chất lượng Retina 3x lưu vào Photos"
    >
      <Download size={14} />
      <span>{isExporting ? 'Đang xuất...' : 'Tải ảnh PNG'}</span>
    </button>

    <!-- Settings Button -->
    <button 
      type="button"
      class="flex items-center space-x-1 px-2.5 py-1 rounded-full bg-slate-700 hover:bg-slate-600 text-white active:scale-95 transition-all cursor-pointer whitespace-nowrap"
      onclick={() => { chatState.activeModal = 'profile'; }}
      title="Cài đặt thông tin đối phương, pin, sóng, màu sắc"
    >
      <Settings size={14} />
      <span>Cài đặt</span>
    </button>

    <!-- Fake Call Button -->
    <button 
      type="button"
      class="flex items-center space-x-1 px-2.5 py-1 rounded-full bg-slate-700 hover:bg-slate-600 text-white active:scale-95 transition-all cursor-pointer whitespace-nowrap"
      onclick={() => {
        chatState.callType = 'audio';
        chatState.callStatus = 'incoming';
        chatState.callTimer = 0;
        chatState.activeModal = 'call';
      }}
      title="Giả lập cuộc gọi thoại chuông reo"
    >
      <PhoneCall size={14} />
      <span>Giả lập Gọi</span>
    </button>

    <!-- Clear Chat Button -->
    <button 
      type="button"
      class="p-1 rounded-full text-slate-400 hover:text-red-400 active:scale-90 transition-transform cursor-pointer"
      onclick={handleClear}
      title="Xóa trắng cuộc trò chuyện"
    >
      <Trash2 size={15} />
    </button>
  </div>
{:else}
  <!-- In Snapshot Mode: A subtle translucent exit pill at the bottom edge -->
  <button 
    type="button"
    class="fixed bottom-2 left-2 z-50 bg-black/40 hover:bg-black/70 backdrop-blur-sm text-white/70 hover:text-white px-2.5 py-1 rounded-full text-[11px] font-medium border border-white/20 shadow-lg active:scale-95 transition-all cursor-pointer flex items-center space-x-1 opacity-40 hover:opacity-100"
    onclick={toggleSnapshotMode}
    title="Chạm để mở lại thanh công cụ quản trị"
  >
    <EyeOff size={13} />
    <span>Hiện lại công cụ</span>
  </button>
{/if}
