<script>
  import { chatState, selectZaloConversation } from '../../state.svelte.js';
  import ZaloIcon from '../ZaloIcon.svelte';
  import { ChevronRight, Pin } from '@lucide/svelte';

  let searchQuery = $state('');

  const filteredConversations = $derived(
    chatState.zaloConversations.filter(c => 
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.lastMessage.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  function openCreateContact() {
    chatState.zaloScreen = 'zalo_create_contact';
  }
</script>

<div class="w-full h-full flex flex-col bg-white select-none transition-colors duration-200">
  <!-- Top Blue Gradient Header (1:1 from sample image 1) -->
  <div class="bg-gradient-to-r from-[#0068ff] via-[#007aff] to-[#008fe5] text-white px-3 pt-2 pb-2.5 flex items-center space-x-2 shrink-0 shadow-xs">
    <!-- Search Bar with Search Icon -->
    <div class="flex-1 flex items-center bg-transparent space-x-2.5 pl-1">
      <ZaloIcon name="search" size={20} class="text-white shrink-0" />
      <input 
        type="text" 
        placeholder="Tìm kiếm"
        bind:value={searchQuery}
        class="w-full bg-transparent text-white placeholder-white/70 text-[16px] outline-none font-normal"
      />
    </div>

    <!-- Right: QR Scanner & Plus Button -->
    <div class="flex items-center space-x-3.5 pr-1 text-white">
      <button 
        type="button" 
        class="active:scale-90 transition-transform cursor-pointer p-0.5" 
        title="Quét mã QR"
      >
        <ZaloIcon name="qr" size={22} />
      </button>

      <button 
        type="button" 
        class="active:scale-90 transition-transform cursor-pointer p-0.5" 
        onclick={openCreateContact}
        title="Tạo liên hệ Zalo mới"
      >
        <ZaloIcon name="plus" size={24} />
      </button>
    </div>
  </div>

  <!-- Body Content -->
  <div class="flex-1 overflow-y-auto ios-scroll no-scrollbar divide-y divide-gray-100">
    <!-- Profile update banner (From sample image 1) -->
    <div 
      class="flex items-center justify-between px-4 py-2.5 hover:bg-gray-50 active:bg-gray-100 transition-colors cursor-pointer border-b border-gray-100"
      onclick={() => { chatState.activeModal = 'profile'; }}
      role="button"
      tabindex="0"
      onkeydown={(e) => e.key === 'Enter' && (chatState.activeModal = 'profile')}
    >
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
          <ZaloIcon name="user" size={20} class="text-gray-500" />
        </div>
        <span class="text-[15px] font-normal text-gray-800">Cập nhật thông tin cá nhân</span>
      </div>
      <ChevronRight size={18} class="text-gray-400" />
    </div>

    <!-- Conversations List (1:1 identical to sample image 1) -->
    {#each filteredConversations as c (c.id)}
      <button 
        type="button" 
        class="w-full flex items-center px-4 py-3 hover:bg-gray-50 active:bg-gray-100 transition-colors cursor-pointer text-left border-0 bg-transparent"
        onclick={() => selectZaloConversation(c.id)}
      >
        <!-- Avatar with badges -->
        <div class="relative w-13 h-13 shrink-0 mr-3">
          <img 
            src={c.avatar} 
            alt={c.name} 
            class="w-full h-full rounded-full object-cover shadow-2xs border border-gray-100"
          />
          {#if c.hasVerifiedBadge}
            <span class="absolute bottom-0 right-0 w-4 h-4 bg-[#ff9800] text-white rounded-full flex items-center justify-center text-[10px] font-bold border-2 border-white shadow-xs">
              ✓
            </span>
          {:else if c.isOnline}
            <span class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-[#00c853] rounded-full border-2 border-white shadow-xs"></span>
          {/if}
        </div>

        <!-- Name & Message preview -->
        <div class="flex-1 min-w-0 pr-2">
          <div class="flex items-center justify-between mb-0.5">
            <h3 class="text-[15.5px] font-semibold text-gray-900 truncate">
              {c.name}
            </h3>
            
            <!-- Time & Pin -->
            <div class="flex items-center space-x-1 shrink-0 ml-2">
              {#if c.isPinned}
                <Pin size={13} class="text-gray-400 rotate-45" />
              {/if}
              <span class="text-[12px] text-gray-400 font-normal">
                {c.lastTime}
              </span>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <p class="text-[13.5px] text-gray-500 truncate font-normal leading-normal">
              {c.lastMessage}
            </p>

            <!-- Unread Badge -->
            {#if c.unreadCount > 0}
              <div class="flex items-center space-x-1 ml-2 shrink-0">
                {#if c.hasMention}
                  <span class="w-4 h-4 rounded-full bg-[#0084ff] text-white text-[10px] font-bold flex items-center justify-center">@</span>
                {/if}
                <span class="min-w-[18px] h-[18px] px-1 bg-[#ff3b30] text-white text-[11px] font-bold rounded-full flex items-center justify-center shadow-xs">
                  {c.unreadCount}
                </span>
              </div>
            {/if}
          </div>
        </div>
      </button>
    {/each}
  </div>

  <!-- Bottom Navigation (5 tabs from sample image 1) -->
  <nav class="w-full flex items-center justify-around bg-white border-t border-gray-200 py-1.5 shrink-0 z-20">
    <!-- Tab 1: Tin nhắn (Active) -->
    <button 
      type="button" 
      class="flex flex-col items-center justify-center text-[#0068ff] py-0.5 cursor-pointer flex-1"
      onclick={() => { chatState.zaloActiveTab = 'messages'; }}
    >
      <div class="relative">
        <ZaloIcon name="message_main" size={24} class="text-[#0068ff]" />
        <span class="absolute -top-1.5 -right-3 px-1 py-0.2 bg-[#ff3b30] text-white text-[9px] font-bold rounded-full border border-white">
          5+
        </span>
      </div>
      <span class="text-[10.5px] font-semibold mt-0.5">Tin nhắn</span>
    </button>

    <!-- Tab 2: Danh bạ -->
    <button 
      type="button" 
      class="flex flex-col items-center justify-center text-gray-500 py-0.5 cursor-pointer flex-1"
      onclick={() => { chatState.zaloActiveTab = 'contacts'; }}
    >
      <ZaloIcon name="phone_book" size={24} class="text-gray-500" />
      <span class="text-[10.5px] font-medium mt-0.5">Danh bạ</span>
    </button>

    <!-- Tab 3: Khám phá -->
    <button 
      type="button" 
      class="flex flex-col items-center justify-center text-gray-500 py-0.5 cursor-pointer flex-1"
      onclick={() => { chatState.zaloActiveTab = 'explore'; }}
    >
      <ZaloIcon name="explore" size={24} class="text-gray-500" />
      <span class="text-[10.5px] font-medium mt-0.5">Khám phá</span>
    </button>

    <!-- Tab 4: Tường nhà -->
    <button 
      type="button" 
      class="flex flex-col items-center justify-center text-gray-500 py-0.5 cursor-pointer flex-1"
      onclick={() => { chatState.zaloActiveTab = 'timeline'; }}
    >
      <div class="relative">
        <ZaloIcon name="timeline" size={24} class="text-gray-500" />
        <span class="absolute -top-1 -right-2 w-3.5 h-3.5 bg-[#ff3b30] text-white text-[9px] font-bold rounded-full flex items-center justify-center border border-white">
          N
        </span>
      </div>
      <span class="text-[10.5px] font-medium mt-0.5">Tường nhà</span>
    </button>

    <!-- Tab 5: Cá nhân -->
    <button 
      type="button" 
      class="flex flex-col items-center justify-center text-gray-500 py-0.5 cursor-pointer flex-1"
      onclick={() => { chatState.activeModal = 'profile'; }}
    >
      <ZaloIcon name="user" size={24} class="text-gray-500" />
      <span class="text-[10.5px] font-medium mt-0.5">Cá nhân</span>
    </button>
  </nav>
</div>

