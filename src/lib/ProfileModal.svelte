<script>
  import { chatState, THEMES, DEFAULT_AVATARS, getCurrentFormattedTime, getCurrentActiveChat } from '../state.svelte.js';
  import { X, Upload, Check, Moon, Sun, Smartphone, User, Palette, BadgeCheck } from '@lucide/svelte';

  const conv = $derived(getCurrentActiveChat());
  let activeTab = $state('user'); // 'user' | 'theme' | 'ios'

  function closeModal() {
    chatState.activeModal = null;
  }

  function handleAvatarUpload(e) {
    const file = e.target.files?.[0];
    if (file && conv) {
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          conv.avatar = reader.result;
        }
      };
      reader.readAsDataURL(file);
    }
  }

  function syncCurrentTime() {
    chatState.currentTime = getCurrentFormattedTime();
  }
</script>

<div class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-black/60 backdrop-blur-xs select-none animate-in fade-in duration-150">
  <div 
    class="w-full max-w-md rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] border transition-colors"
    class:bg-[#1e1e1e]={chatState.isDarkMode}
    class:border-[#333]={chatState.isDarkMode}
    class:text-white={chatState.isDarkMode}
    class:bg-white={!chatState.isDarkMode}
    class:border-gray-200={!chatState.isDarkMode}
    class:text-gray-900={!chatState.isDarkMode}
  >
    <!-- Modal Header -->
    <div class="flex items-center justify-between px-5 py-3.5 border-b shrink-0"
         class:border-[#2e2e2e]={chatState.isDarkMode}
         class:border-gray-100={!chatState.isDarkMode}
    >
      <div class="flex items-center space-x-2">
        <h2 class="text-[17px] font-bold">Cài đặt & Tùy biến</h2>
        <span class="text-xs px-2 py-0.5 rounded-full font-bold {chatState.currentApp === 'zalo' ? 'bg-[#0068ff] text-white' : 'bg-[#0084ff] text-white'}">
          {chatState.currentApp === 'zalo' ? 'Zalo' : 'Messenger'}
        </span>
      </div>
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-500 hover:text-gray-800 dark:hover:text-white active:scale-90 transition-transform cursor-pointer"
        onclick={closeModal}
      >
        <X size={18} />
      </button>
    </div>

    <!-- Tabs Navigation -->
    <div class="flex border-b px-2 shrink-0 text-[13px] font-semibold"
         class:border-[#2e2e2e]={chatState.isDarkMode}
         class:border-gray-100={!chatState.isDarkMode}
    >
      <button 
        type="button" 
        class="flex-1 py-2.5 flex items-center justify-center space-x-1.5 border-b-2 cursor-pointer transition-all"
        class:border-[#0084ff]={activeTab === 'user'}
        class:text-[#0084ff]={activeTab === 'user'}
        class:border-transparent={activeTab !== 'user'}
        class:text-gray-400={activeTab !== 'user'}
        onclick={() => { activeTab = 'user'; }}
      >
        <User size={15} />
        <span>Đối phương</span>
      </button>

      <button 
        type="button" 
        class="flex-1 py-2.5 flex items-center justify-center space-x-1.5 border-b-2 cursor-pointer transition-all"
        class:border-[#0084ff]={activeTab === 'theme'}
        class:text-[#0084ff]={activeTab === 'theme'}
        class:border-transparent={activeTab !== 'theme'}
        class:text-gray-400={activeTab !== 'theme'}
        onclick={() => { activeTab = 'theme'; }}
      >
        <Palette size={15} />
        <span>Giao diện</span>
      </button>

      <button 
        type="button" 
        class="flex-1 py-2.5 flex items-center justify-center space-x-1.5 border-b-2 cursor-pointer transition-all"
        class:border-[#0084ff]={activeTab === 'ios'}
        class:text-[#0084ff]={activeTab === 'ios'}
        class:border-transparent={activeTab !== 'ios'}
        class:text-gray-400={activeTab !== 'ios'}
        onclick={() => { activeTab = 'ios'; }}
      >
        <Smartphone size={15} />
        <span>iOS Status</span>
      </button>
    </div>

    <!-- Modal Body -->
    <div class="p-5 overflow-y-auto space-y-4 text-[14px]">
      {#if activeTab === 'user' && conv}
        <!-- Partner Name -->
        <div class="space-y-1.5">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Tên người nhận</span>
          <input 
            type="text" 
            bind:value={conv.name} 
            class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[16px] focus:ring-2 focus:ring-[#0084ff]/40 transition-all"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>

        <!-- Verified Badge Checkbox (TÍCH XANH) -->
        <div class="flex items-center justify-between p-3 rounded-2xl border transition-colors {conv.hasVerifiedBadge ? (chatState.isDarkMode ? 'bg-blue-950/40 border-blue-400' : 'bg-blue-50 border-blue-300') : (chatState.isDarkMode ? 'border-[#3a3b3c]' : 'border-gray-200')}">
          <div class="flex items-center space-x-2">
            <BadgeCheck size={20} class="text-[#0084ff] shrink-0 fill-[#0084ff] text-white" />
            <div>
              <span class="font-bold block text-[14px]">Tích xanh xác minh (Verified)</span>
              <span class="text-xs text-gray-500">Hiển thị huy hiệu tích xanh chính chủ cạnh tên</span>
            </div>
          </div>
          <input 
            type="checkbox" 
            bind:checked={conv.hasVerifiedBadge} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        <!-- Avatar Selection -->
        <div class="space-y-2">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Ảnh đại diện</span>
          <div class="flex items-center space-x-3">
            <img 
              src={conv.avatar} 
              alt="Avatar preview" 
              class="w-14 h-14 rounded-full object-cover border-2 border-[#0084ff] shadow-sm shrink-0" 
            />
            <label class="flex-1 flex items-center justify-center space-x-2 px-3 py-2.5 rounded-xl border border-dashed border-gray-400 hover:border-[#0084ff] cursor-pointer text-[13px] font-semibold transition-colors">
              <Upload size={16} />
              <span>Tải ảnh từ máy lên</span>
              <input type="file" accept="image/*" onchange={handleAvatarUpload} class="hidden" />
            </label>
          </div>

          <!-- Preset Avatars -->
          <div class="flex items-center space-x-2 pt-1">
            <span class="text-xs text-gray-400">Ảnh mẫu:</span>
            {#each DEFAULT_AVATARS as av}
              <button 
                type="button" 
                class="w-8 h-8 rounded-full overflow-hidden border-2 cursor-pointer transition-transform active:scale-95"
                class:border-[#0084ff]={conv.avatar === av}
                class:border-transparent={conv.avatar !== av}
                onclick={() => { conv.avatar = av; }}
              >
                <img src={av} alt="Preset" class="w-full h-full object-cover" />
              </button>
            {/each}
          </div>
        </div>

        <!-- Online Status & Text -->
        <div class="space-y-3 pt-2 border-t border-gray-100 dark:border-gray-800">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <span class="w-3 h-3 bg-[#31a24c] rounded-full inline-block"></span>
              <span class="font-medium">Bật chấm xanh Online</span>
            </div>
            <input 
              type="checkbox" 
              bind:checked={conv.isOnline} 
              class="w-5 h-5 accent-[#31a24c] rounded cursor-pointer"
            />
          </div>

          <div class="space-y-1">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Dòng chữ trạng thái</span>
            <input 
              type="text" 
              bind:value={conv.statusText} 
              placeholder="Đang hoạt động / Vừa mới truy cập..."
              class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[16px]"
              class:bg-[#2a2a2a]={chatState.isDarkMode}
              class:border-[#3a3b3c]={chatState.isDarkMode}
              class:bg-gray-50={!chatState.isDarkMode}
              class:border-gray-200={!chatState.isDarkMode}
            />
            <div class="flex flex-wrap gap-1.5 pt-1">
              {#each ['Đang hoạt động', 'Vừa mới truy cập', 'Hoạt động 5 phút trước', 'Hoạt động 1 giờ trước', 'Tài khoản chính thức'] as quickStatus}
                <button 
                  type="button" 
                  class="text-[11px] px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                  onclick={() => { conv.statusText = quickStatus; }}
                >
                  {quickStatus}
                </button>
              {/each}
            </div>
          </div>
        </div>

      {:else if activeTab === 'theme'}
        <!-- Dark Mode Toggle -->
        <div class="flex items-center justify-between p-3 rounded-2xl border"
             class:bg-[#242526]={chatState.isDarkMode}
             class:border-[#3a3b3c]={chatState.isDarkMode}
             class:bg-gray-50={!chatState.isDarkMode}
             class:border-gray-200={!chatState.isDarkMode}
        >
          <div class="flex items-center space-x-2.5">
            {#if chatState.isDarkMode}
              <Moon size={20} class="text-indigo-400" />
              <span class="font-semibold">Chế độ Tối (Dark Mode OLED)</span>
            {:else}
              <Sun size={20} class="text-amber-500" />
              <span class="font-semibold">Chế độ Sáng (Light Mode)</span>
            {/if}
          </div>
          <input 
            type="checkbox" 
            bind:checked={chatState.isDarkMode} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        {#if chatState.currentApp === 'messenger' && conv}
          <!-- Chat Bubble Color Theme (Messenger) -->
          <div class="space-y-2">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Chủ đề màu bong bóng (Messenger)</span>
            <div class="grid grid-cols-2 gap-2">
              {#each Object.values(THEMES) as th}
                <button 
                  type="button" 
                  class="flex items-center space-x-2.5 p-2.5 rounded-xl border text-left cursor-pointer transition-all {conv.themeKey === th.id ? (chatState.isDarkMode ? 'border-[#0084ff] bg-blue-950/40' : 'border-[#0084ff] bg-blue-50') : (chatState.isDarkMode ? 'border-[#3a3b3c]' : 'border-gray-200')}"
                  onclick={() => { conv.themeKey = th.id; }}
                >
                  <span class="w-5 h-5 rounded-full shadow-xs shrink-0" style="background-color: {th.primary};"></span>
                  <span class="text-[13px] font-semibold">{th.name}</span>
                </button>
              {/each}
            </div>
          </div>
        {/if}

      {:else if activeTab === 'ios'}
        <!-- Time setting -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Giờ trên thanh trạng thái</span>
            <button 
              type="button" 
              class="text-xs text-[#0084ff] font-semibold hover:underline cursor-pointer"
              onclick={syncCurrentTime}
            >
              Lấy giờ hiện tại
            </button>
          </div>
          <input 
            type="text" 
            bind:value={chatState.currentTime} 
            placeholder="09:41"
            class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[16px]"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>

        <!-- Battery level slider -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Phần trăm Pin</span>
            <span class="text-xs font-bold">{chatState.batteryLevel}%</span>
          </div>
          <input 
            type="range" 
            min="1" 
            max="100" 
            bind:value={chatState.batteryLevel} 
            class="w-full accent-[#34c759] cursor-pointer"
          />
        </div>

        <!-- Cellular Type -->
        <div class="space-y-1.5">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Kiểu mạng di động</span>
          <div class="flex space-x-2">
            {#each ['5G', '4G', 'LTE', '3G'] as net}
              <button 
                type="button" 
                class="flex-1 py-1.5 rounded-xl border text-xs font-bold cursor-pointer transition-all"
                class:bg-[#0084ff]={chatState.cellularType === net}
                class:text-white={chatState.cellularType === net}
                class:border-[#0084ff]={chatState.cellularType === net}
                class:border-gray-200={chatState.cellularType !== net && !chatState.isDarkMode}
                class:border-[#3a3b3c]={chatState.cellularType !== net && chatState.isDarkMode}
                onclick={() => { chatState.cellularType = net; }}
              >
                {net}
              </button>
            {/each}
          </div>
        </div>

        <!-- Dynamic Island Toggle -->
        <div class="flex items-center justify-between p-3 rounded-2xl border"
             class:bg-[#242526]={chatState.isDarkMode}
             class:border-[#3a3b3c]={chatState.isDarkMode}
             class:bg-gray-50={!chatState.isDarkMode}
             class:border-gray-200={!chatState.isDarkMode}
        >
          <div>
            <span class="font-semibold block text-[13.5px]">Đảo động (Dynamic Island)</span>
            <span class="text-xs text-gray-400">Tắt theo mặc định để ảnh chụp màn hình sạch như phím cứng iPhone</span>
          </div>
          <input 
            type="checkbox" 
            bind:checked={chatState.showDynamicIsland} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>
      {/if}
    </div>

    <!-- Modal Footer -->
    <div class="p-4 border-t flex justify-end shrink-0"
         class:border-[#2e2e2e]={chatState.isDarkMode}
         class:border-gray-100={!chatState.isDarkMode}
    >
      <button 
        type="button" 
        class="px-5 py-2 rounded-xl bg-[#0084ff] text-white font-bold text-[14px] hover:bg-[#0073e6] active:scale-95 transition-all cursor-pointer shadow-md"
        onclick={closeModal}
      >
        Lưu & Đóng
      </button>
    </div>
  </div>
</div>
