<script>
  import { chatState, addZaloConversation, DEFAULT_AVATARS } from '../../state.svelte.js';
  import ZaloIcon from '../ZaloIcon.svelte';
  import { Camera, ChevronLeft } from '@lucide/svelte';

  let name = $state('Trần Huyền Trang');
  let avatar = $state(DEFAULT_AVATARS[0]);
  let isOnline = $state(true);
  let statusText = $state('Vừa mới truy cập');
  let unreadCount = $state(0);
  let isPinned = $state(false);

  function handleSave() {
    if (!name.trim()) return;
    addZaloConversation({
      name: name.trim(),
      avatar,
      isOnline,
      statusText: statusText.trim() || 'Vừa mới truy cập',
      unreadCount: parseInt(String(unreadCount)) || 0,
      isPinned
    });
  }

  function handleBack() {
    chatState.zaloScreen = 'zalo_chats_list';
  }

  function handleAvatarUpload(e) {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        avatar = reader.result;
      };
      reader.readAsDataURL(file);
    }
  }
</script>

<div class="w-full h-full flex flex-col bg-white select-none transition-colors duration-200 overflow-y-auto ios-scroll no-scrollbar">
  <!-- Top Bar: Back | Title | 'LƯU' -->
  <div class="flex items-center justify-between px-3 py-3 border-b border-gray-100 shrink-0 bg-white">
    <button 
      type="button" 
      class="p-1 rounded-full text-gray-700 active:scale-90 transition-transform cursor-pointer"
      onclick={handleBack}
    >
      <ChevronLeft size={28} />
    </button>

    <h2 class="text-[17px] font-bold text-gray-900">
      Tạo liên hệ Zalo mới
    </h2>

    <button 
      type="button" 
      class="text-[#0068ff] font-bold text-[16px] px-2 py-1 active:opacity-60 transition-opacity cursor-pointer uppercase"
      onclick={handleSave}
    >
      Lưu
    </button>
  </div>

  <!-- Body Content -->
  <div class="p-5 space-y-6 flex-1">
    <!-- Big Avatar with Camera Overlay -->
    <div class="flex flex-col items-center space-y-3">
      <div class="relative cursor-pointer group">
        <img 
          src={avatar} 
          alt="Avatar" 
          class="w-24 h-24 rounded-full object-cover border-2 border-gray-200 shadow-md"
        />
        <label class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-[#0068ff] text-white flex items-center justify-center shadow-lg cursor-pointer active:scale-90 transition-transform">
          <Camera size={18} />
          <input type="file" accept="image/*" onchange={handleAvatarUpload} class="hidden" />
        </label>
      </div>

      <!-- Preset Avatars -->
      <div class="flex items-center space-x-2 pt-1">
        {#each DEFAULT_AVATARS as av}
          <button 
            type="button"
            class="w-8 h-8 rounded-full overflow-hidden border-2 cursor-pointer transition-transform active:scale-95"
            class:border-[#0068ff]={avatar === av}
            class:border-transparent={avatar !== av}
            onclick={() => { avatar = av; }}
          >
            <img src={av} alt="Preset" class="w-full h-full object-cover" />
          </button>
        {/each}
      </div>
    </div>

    <!-- Name Field -->
    <div class="space-y-1.5">
      <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Tên người liên hệ Zalo</span>
      <input 
        type="text" 
        placeholder="Nhập tên hiển thị..." 
        bind:value={name}
        class="w-full px-4 py-2.5 rounded-xl border border-gray-200 bg-[#f0f2f5] outline-none font-semibold text-[16px] text-black"
      />
    </div>

    <!-- Active Status Switch & Input -->
    <div class="space-y-2 pt-2 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <div>
          <span class="font-bold text-[15px] block text-gray-900">Trạng thái hoạt động</span>
          <span class="text-xs text-gray-400">Hiển thị chấm xanh online</span>
        </div>
        <input 
          type="checkbox" 
          bind:checked={isOnline}
          class="w-6 h-6 accent-[#00c853] rounded cursor-pointer" 
        />
      </div>

      <div class="space-y-1">
        <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Dòng chữ trạng thái</span>
        <input 
          type="text" 
          bind:value={statusText}
          placeholder="Vừa mới truy cập / Truy cập 15 phút trước..."
          class="w-full px-4 py-2 rounded-xl border border-gray-200 bg-[#f0f2f5] outline-none text-sm text-black"
        />
      </div>
    </div>

    <!-- Pinned & Unread Settings -->
    <div class="space-y-3 pt-2 border-t border-gray-100">
      <div class="flex items-center justify-between">
        <div>
          <span class="font-bold text-[15px] block text-gray-900">Ghim hội thoại lên đầu</span>
          <span class="text-xs text-gray-400">Hiển thị biểu tượng ghim 📌 trong danh sách</span>
        </div>
        <input 
          type="checkbox" 
          bind:checked={isPinned}
          class="w-6 h-6 accent-[#0068ff] rounded cursor-pointer" 
        />
      </div>

      <div class="flex items-center justify-between">
        <div>
          <span class="font-bold text-[15px] block text-gray-900">Số tin nhắn chưa đọc</span>
          <span class="text-xs text-gray-400">0 là đã đọc, từ 1 trở lên sẽ hiện chấm đỏ</span>
        </div>
        <input 
          type="number" 
          min="0"
          max="99"
          bind:value={unreadCount}
          class="w-16 px-2 py-1 text-center font-bold text-sm rounded-lg border border-gray-200 bg-[#f0f2f5]"
        />
      </div>
    </div>
  </div>
</div>

