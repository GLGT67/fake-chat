<script>
  import { chatState, addConversation, DEFAULT_AVATARS, THEMES } from '../state.svelte.js';
  import { ChevronLeft, Camera, Upload } from '@lucide/svelte';

  let name = $state('Trịnh Văn Mạnh');
  let avatar = $state(DEFAULT_AVATARS[0]);
  let isOnline = $state(true);
  let statusText = $state('Đang hoạt động');
  let hasVerifiedBadge = $state(false);
  let hasUnread = $state(false);
  let themeKey = $state('classic');

  function handleSave() {
    if (!name.trim()) return;
    addConversation({
      name: name.trim(),
      avatar,
      isOnline,
      statusText: statusText.trim() || 'Đang hoạt động',
      hasVerifiedBadge,
      unreadCount: hasUnread ? 1 : 0,
      themeKey
    });
  }

  function handleBack() {
    chatState.currentScreen = 'chats_list';
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

<div 
  class="w-full h-full flex flex-col select-none transition-colors duration-200 overflow-y-auto ios-scroll no-scrollbar"
  class:bg-[#18191a]={chatState.isDarkMode}
  class:bg-white={!chatState.isDarkMode}
>
  <!-- Top Bar: Back | Title | 'LƯU' Button (From activity_fake_contact_messenger.xml) -->
  <div class="flex items-center justify-between px-3 py-3 border-b border-gray-100 dark:border-gray-800 shrink-0">
    <button 
      type="button" 
      class="p-1 rounded-full text-gray-700 dark:text-gray-200 active:scale-90 transition-transform cursor-pointer"
      onclick={handleBack}
    >
      <ChevronLeft size={28} />
    </button>

    <h2 
      class="text-[17px] font-bold"
      class:text-white={chatState.isDarkMode}
      class:text-black={!chatState.isDarkMode}
    >
      Tạo liên hệ giả
    </h2>

    <button 
      type="button" 
      class="text-[#0084ff] font-bold text-[16px] px-2 py-1 active:opacity-60 transition-opacity cursor-pointer uppercase"
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
          class="w-24 h-24 rounded-full object-cover border-2 border-gray-200 dark:border-gray-700 shadow-md"
        />
        <label class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-[#0084ff] text-white flex items-center justify-center shadow-lg cursor-pointer active:scale-90 transition-transform">
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
            class:border-[#0084ff]={avatar === av}
            class:border-transparent={avatar !== av}
            onclick={() => { avatar = av; }}
          >
            <img src={av} alt="Preset" class="w-full h-full object-cover" />
          </button>
        {/each}
      </div>
    </div>

    <!-- Name Field (@7F0A0103) -->
    <div class="space-y-1.5">
      <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Tên người liên hệ</span>
      <input 
        type="text" 
        placeholder="Nhập tên..." 
        bind:value={name}
        class="w-full px-4 py-2.5 rounded-xl border outline-none font-semibold text-[16px] transition-colors"
        class:bg-[#242526]={chatState.isDarkMode}
        class:border-[#3a3b3c]={chatState.isDarkMode}
        class:text-white={chatState.isDarkMode}
        class:bg-[#f0f2f5]={!chatState.isDarkMode}
        class:border-gray-200={!chatState.isDarkMode}
        class:text-black={!chatState.isDarkMode}
      />
    </div>

    <!-- Active Status Switch & Input (@7F0A02DD & @7F0A010B) -->
    <div class="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-800">
      <div class="flex items-center justify-between">
        <div>
          <span class="font-bold text-[15px] block text-gray-900 dark:text-white">Trạng thái hoạt động</span>
          <span class="text-xs text-gray-400">Hiển thị chấm xanh online</span>
        </div>
        <input 
          type="checkbox" 
          bind:checked={isOnline}
          class="w-6 h-6 accent-[#31a24c] rounded cursor-pointer" 
        />
      </div>

      <div class="space-y-1">
        <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Dòng chữ trạng thái</span>
        <input 
          type="text" 
          bind:value={statusText}
          placeholder="Đang hoạt động / Hoạt động 10 phút trước..."
          class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[14px]"
          class:bg-[#242526]={chatState.isDarkMode}
          class:border-[#3a3b3c]={chatState.isDarkMode}
          class:text-white={chatState.isDarkMode}
          class:bg-[#f0f2f5]={!chatState.isDarkMode}
          class:border-gray-200={!chatState.isDarkMode}
          class:text-black={!chatState.isDarkMode}
        />
      </div>
    </div>

    <!-- Verified Badge Switch -->
    <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800">
      <div>
        <span class="font-bold text-[15px] block text-gray-900 dark:text-white">Tích xanh xác minh (Verified)</span>
        <span class="text-xs text-gray-400">Hiện huy hiệu tích xanh chính chủ cạnh tên</span>
      </div>
      <input 
        type="checkbox" 
        bind:checked={hasVerifiedBadge}
        class="w-6 h-6 accent-[#0084ff] rounded cursor-pointer" 
      />
    </div>

    <!-- Unread Message Switch (@7F0A02E0) -->
    <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800">
      <div>
        <span class="font-bold text-[15px] block text-gray-900 dark:text-white">Đánh dấu chưa đọc</span>
        <span class="text-xs text-gray-400">Hiện chấm tròn xanh chưa đọc ở danh sách</span>
      </div>
      <input 
        type="checkbox" 
        bind:checked={hasUnread}
        class="w-6 h-6 accent-[#0084ff] rounded cursor-pointer" 
      />
    </div>

    <!-- Theme Color Spinner (@7F0A02BE) -->
    <div class="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-800">
      <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Chủ đề màu cuộc trò chuyện</span>
      <div class="grid grid-cols-2 gap-2">
        {#each Object.values(THEMES) as th}
          <button 
            type="button"
            class="flex items-center space-x-2 p-2.5 rounded-xl border cursor-pointer active:scale-95 transition-all"
            class:ring-2={themeKey === th.id}
            class:ring-[#0084ff]={themeKey === th.id}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
            onclick={() => { themeKey = th.id; }}
          >
            <div class="w-5 h-5 rounded-full" style="background: {th.primary};"></div>
            <span class="text-[13px] font-semibold text-gray-800 dark:text-gray-200 truncate">{th.name}</span>
          </button>
        {/each}
      </div>
    </div>
  </div>

  <!-- Bottom Save Bar -->
  <div class="p-4 border-t border-gray-100 dark:border-gray-800 shrink-0">
    <button 
      type="button" 
      class="w-full py-3 rounded-2xl bg-[#0084ff] hover:bg-[#0073e6] text-white font-bold text-[16px] shadow-md active:scale-98 transition-all cursor-pointer"
      onclick={handleSave}
    >
      LƯU LIÊN HỆ & VÀO CHAT
    </button>
  </div>
</div>

