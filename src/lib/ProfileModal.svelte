<script>
  import { chatState, THEMES, DEFAULT_AVATARS, getCurrentFormattedTime } from '../state.svelte.js';
  import { X, Upload, Check, Moon, Sun, Smartphone, User, Palette } from '@lucide/svelte';

  let activeTab = $state('user'); // 'user' | 'theme' | 'ios'

  function closeModal() {
    chatState.activeModal = null;
  }

  function handleAvatarUpload(e) {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        chatState.partnerAvatar = reader.result;
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
      <h2 class="text-[17px] font-bold">Cài đặt & Tùy biến</h2>
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
      {#if activeTab === 'user'}
        <!-- Partner Name -->
        <div class="space-y-1.5">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Tên người nhận</span>
          <input 
            type="text" 
            bind:value={chatState.partnerName} 
            class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[15px] focus:ring-2 focus:ring-[#0084ff]/40 transition-all"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>

        <!-- Verified Badge Checkbox -->
        <div class="flex items-center justify-between py-1">
          <span class="font-medium">Tích xanh xác minh (Verified)</span>
          <input 
            type="checkbox" 
            bind:checked={chatState.hasVerifiedBadge} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        <!-- Avatar Selection -->
        <div class="space-y-2">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Ảnh đại diện</span>
          <div class="flex items-center space-x-3">
            <img 
              src={chatState.partnerAvatar} 
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
                class:border-[#0084ff]={chatState.partnerAvatar === av}
                class:border-transparent={chatState.partnerAvatar !== av}
                onclick={() => { chatState.partnerAvatar = av; }}
              >
                <img src={av} alt="Preset" class="w-full h-full object-cover" />
              </button>
            {/each}
          </div>
        </div>

        <!-- Online Status & Text -->
        <div class="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-800">
          <div class="flex items-center justify-between">
            <span class="font-medium">Bật chấm xanh Online</span>
            <input 
              type="checkbox" 
              bind:checked={chatState.isOnline} 
              class="w-5 h-5 accent-[#31a24c] rounded cursor-pointer"
            />
          </div>

          <div class="space-y-1">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Dòng chữ trạng thái</span>
            <input 
              type="text" 
              bind:value={chatState.statusText} 
              placeholder="Đang hoạt động / Hoạt động 10 phút trước..."
              class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium text-[14px]"
              class:bg-[#2a2a2a]={chatState.isDarkMode}
              class:border-[#3a3b3c]={chatState.isDarkMode}
              class:bg-gray-50={!chatState.isDarkMode}
              class:border-gray-200={!chatState.isDarkMode}
            />
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
            class="w-6 h-6 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        <!-- Color Themes Palette -->
        <div class="space-y-2 pt-2">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Màu chủ đề Messenger</span>
          <div class="grid grid-cols-2 gap-2.5">
            {#each Object.values(THEMES) as th}
              <button 
                type="button"
                class="flex items-center space-x-2.5 p-2.5 rounded-xl border text-left cursor-pointer transition-all active:scale-95"
                class:ring-2={chatState.themeKey === th.id}
                class:ring-[#0084ff]={chatState.themeKey === th.id}
                class:border-[#3a3b3c]={chatState.isDarkMode}
                class:border-gray-200={!chatState.isDarkMode}
                onclick={() => { chatState.themeKey = th.id; }}
              >
                <div class="w-6 h-6 rounded-full shadow-xs shrink-0" style="background: {th.primary};"></div>
                <span class="font-semibold text-[13px] truncate">{th.name}</span>
                {#if chatState.themeKey === th.id}
                  <Check size={16} class="text-[#0084ff] ml-auto shrink-0" />
                {/if}
              </button>
            {/each}
          </div>
        </div>

      {:else if activeTab === 'ios'}
        <!-- iOS Status Bar Toggle -->
        <div class="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-800">
          <div>
            <span class="font-semibold block">Thanh Status Bar iPhone</span>
            <span class="text-xs text-gray-400">Ẩn nếu dùng PWA full màn hình trên iPhone</span>
          </div>
          <input 
            type="checkbox" 
            bind:checked={chatState.showIosStatusBar} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        <!-- Home Bar Toggle -->
        <div class="flex items-center justify-between pb-2 border-b border-gray-100 dark:border-gray-800">
          <span class="font-semibold">Thanh gạch đáy (Home Bar)</span>
          <input 
            type="checkbox" 
            bind:checked={chatState.showHomeBar} 
            class="w-5 h-5 accent-[#0084ff] rounded cursor-pointer"
          />
        </div>

        <!-- Time Settings -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Đồng hồ iPhone</span>
            <button 
              type="button" 
              class="text-xs text-[#0084ff] font-semibold underline cursor-pointer"
              onclick={syncCurrentTime}
            >
              Lấy giờ thực tế
            </button>
          </div>
          <input 
            type="text" 
            bind:value={chatState.currentTime} 
            class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>

        <!-- Battery Level Slider -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Dung lượng Pin ({chatState.batteryLevel}%)</span>
            <label class="flex items-center space-x-1 text-xs cursor-pointer">
              <input type="checkbox" bind:checked={chatState.isCharging} class="accent-yellow-400" />
              <span>Đang sạc ⚡</span>
            </label>
          </div>
          <input 
            type="range" 
            min="1" 
            max="100" 
            bind:value={chatState.batteryLevel} 
            class="w-full accent-[#0084ff] cursor-pointer"
          />
        </div>

        <!-- Signal & Network -->
        <div class="grid grid-cols-2 gap-3 pt-2">
          <div>
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Cột sóng ({chatState.signalBars}/4)</span>
            <input 
              type="range" 
              min="0" 
              max="4" 
              bind:value={chatState.signalBars} 
              class="w-full accent-[#0084ff] cursor-pointer"
            />
          </div>

          <div>
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Loại mạng</span>
            <select 
              bind:value={chatState.cellularType} 
              class="w-full px-3 py-1.5 rounded-xl border outline-none font-medium"
              class:bg-[#2a2a2a]={chatState.isDarkMode}
              class:border-[#3a3b3c]={chatState.isDarkMode}
              class:bg-gray-50={!chatState.isDarkMode}
              class:border-gray-200={!chatState.isDarkMode}
            >
              <option value="5G">5G</option>
              <option value="LTE">LTE</option>
              <option value="4G">4G</option>
              <option value="3G">3G</option>
            </select>
          </div>
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
        class="w-full py-2.5 rounded-xl bg-[#0084ff] hover:bg-[#0073e6] text-white font-bold shadow-md active:scale-98 transition-all cursor-pointer"
        onclick={closeModal}
      >
        Áp dụng & Đóng
      </button>
    </div>
  </div>
</div>

