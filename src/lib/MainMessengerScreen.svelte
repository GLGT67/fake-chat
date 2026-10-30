<script>
  import { chatState, selectConversation, deleteConversation } from '../state.svelte.js';
  import OriginalIcon from './OriginalIcon.svelte';
  import { Trash2 } from '@lucide/svelte';

  let searchQuery = $state('');

  const filteredConversations = $derived(
    chatState.conversations.filter(c => 
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.lastMessage || '').toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  function openCreateContact() {
    chatState.currentScreen = 'create_contact';
  }

  function startCall(type) {
    chatState.callType = type;
    chatState.callStatus = 'incoming';
    chatState.callTimer = 0;
    chatState.activeModal = 'call';
  }
</script>

<div 
  class="w-full h-full flex flex-col select-none transition-colors duration-200"
  class:bg-[#18191a]={chatState.isDarkMode}
  class:bg-white={!chatState.isDarkMode}
>
  <!-- Top Bar: Avatar with Badge '2' | 'Đoạn chat' | Camera & Pencil Icons -->
  <div class="flex items-center justify-between px-4 pt-2 pb-2 shrink-0">
    <!-- User Avatar with Unread Badge -->
    <div class="flex items-center space-x-3">
      <button 
        type="button" 
        class="relative cursor-pointer active:scale-95 transition-transform p-0 border-0 bg-transparent text-left" 
        onclick={() => { chatState.activeModal = 'profile'; }}
      >
        <img 
          src={chatState.conversations[0]?.avatar || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=120"} 
          alt="My profile" 
          class="w-10 h-10 rounded-full object-cover shadow-2xs border border-black/5"
        />
        <!-- Red badge '2' from original APK -->
        <span class="absolute -top-1 -right-1 w-4 h-4 bg-[#ff3b30] text-white rounded-full flex items-center justify-center text-[10px] font-bold border border-white">
          2
        </span>
      </button>

      <!-- Title: Đoạn chat -->
      <h1 
        class="text-[24px] font-black tracking-tight"
        class:text-white={chatState.isDarkMode}
        class:text-black={!chatState.isDarkMode}
      >
        Đoạn chat
      </h1>
    </div>

    <!-- Right Icons: Camera & Pencil -->
    <div class="flex items-center space-x-2 text-gray-700 dark:text-gray-200">
      <button 
        type="button" 
        class="w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={() => startCall('video')}
        title="Mở camera / Video"
      >
        <OriginalIcon name="camera" size={19} />
      </button>

      <button 
        type="button" 
        class="w-9 h-9 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={openCreateContact}
        title="Tạo liên hệ / Đoạn chat giả mới"
      >
        <OriginalIcon name="pencil" size={19} />
      </button>
    </div>
  </div>

  <!-- Search Bar (Card with search icon & 'Tìm kiếm') -->
  <div class="px-4 py-1.5 shrink-0">
    <div 
      class="flex items-center px-3.5 py-2 rounded-2xl transition-colors space-x-2.5"
      class:bg-[#242526]={chatState.isDarkMode}
      class:text-gray-300={chatState.isDarkMode}
      class:bg-[#f0f2f5]={!chatState.isDarkMode}
      class:text-gray-700={!chatState.isDarkMode}
    >
      <OriginalIcon name="search" size={16} class="text-gray-400" />
      <input 
        type="text" 
        placeholder="Tìm kiếm"
        bind:value={searchQuery}
        class="w-full bg-transparent text-[15px] outline-none placeholder-gray-400 font-normal"
      />
    </div>
  </div>

  <!-- Scrollable Content: Stories Carousel + Conversations List -->
  <div class="flex-1 overflow-y-auto ios-scroll no-scrollbar">
    <!-- Active Users / Stories Carousel (Horizontal) -->
    <div class="flex items-center space-x-4 px-4 py-3 overflow-x-auto no-scrollbar border-b border-gray-100 dark:border-gray-800 shrink-0">
      <!-- Your Story -->
      <button 
        type="button" 
        class="flex flex-col items-center space-y-1 shrink-0 cursor-pointer active:scale-95 transition-transform bg-transparent border-0 p-0" 
        onclick={openCreateContact}
      >
        <div class="relative w-13 h-13 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600">
          <span class="text-2xl font-light text-gray-500 dark:text-gray-300">+</span>
        </div>
        <span class="text-[11px] font-medium text-gray-600 dark:text-gray-400 w-14 truncate text-center">Tin của bạn</span>
      </button>

      <!-- Online Contacts -->
      {#each chatState.conversations as c (c.id)}
        <button 
          type="button" 
          class="flex flex-col items-center space-y-1 shrink-0 cursor-pointer active:scale-95 transition-transform bg-transparent border-0 p-0 text-left"
          onclick={() => selectConversation(c.id)}
        >
          <div class="relative w-13 h-13">
            <img 
              src={c.avatar} 
              alt={c.name} 
              class="w-full h-full rounded-full object-cover border-2 {c.isOnline ? 'border-[#0084ff]' : 'border-transparent'}"
            />
            {#if c.isOnline}
              <span class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-[#31a24c] rounded-full border-2 border-white dark:border-[#18191a]"></span>
            {/if}
          </div>
          <span class="text-[11px] font-medium text-gray-700 dark:text-gray-300 w-14 truncate text-center">{c.name}</span>
        </button>
      {/each}
    </div>

    <!-- Conversation List -->
    <div class="divide-y divide-transparent">
      {#each filteredConversations as c (c.id)}
        <div class="w-full flex items-center px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group">
          <button 
            type="button" 
            class="flex items-center flex-1 min-w-0 cursor-pointer text-left bg-transparent border-0 p-0"
            onclick={() => selectConversation(c.id)}
          >
            <!-- Avatar with Online Dot -->
            <div class="relative shrink-0 mr-3.5">
              <img 
                src={c.avatar} 
                alt={c.name} 
                class="w-14 h-14 rounded-full object-cover shadow-2xs"
              />
              {#if c.isOnline}
                <span class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-[#31a24c] rounded-full border-2 border-white dark:border-[#18191a]"></span>
              {/if}
            </div>

            <!-- Name & Message Preview -->
            <div class="flex-1 min-w-0 pr-2">
              <div class="flex items-center justify-between">
                <h2 
                  class="text-[16px] leading-tight truncate {c.unreadCount > 0 ? 'font-black' : 'font-bold'}"
                  class:text-white={chatState.isDarkMode}
                  class:text-black={!chatState.isDarkMode}
                >
                  {c.name}
                </h2>
              </div>

              <div class="flex items-center space-x-1.5 mt-1 text-[13px] text-gray-500 dark:text-gray-400">
                <p class="truncate flex-1 {c.unreadCount > 0 ? 'font-bold text-black dark:text-white' : ''}">
                  {c.lastMessage || 'Chưa có tin nhắn'}
                </p>
                <span class="shrink-0">•</span>
                <span class="shrink-0 text-[12px]">{c.lastTime}</span>
              </div>
            </div>

            <!-- Unread Dot or Delivery Status -->
            <div class="shrink-0 pl-1 pr-2">
              {#if c.unreadCount > 0}
                <span class="w-3.5 h-3.5 bg-[#0084ff] rounded-full block"></span>
              {:else}
                <OriginalIcon name="like" size={14} class="text-[#0084ff] opacity-80" />
              {/if}
            </div>
          </button>

          <!-- Delete Conversation Button -->
          <button 
            type="button" 
            class="p-2 text-gray-400 hover:text-red-500 active:scale-90 transition-all cursor-pointer opacity-30 hover:opacity-100"
            onclick={(e) => {
              e.stopPropagation();
              if (confirm(`Xóa đoạn chat với "${c.name}"?`)) {
                deleteConversation(c.id);
              }
            }}
            title="Xóa đoạn chat này"
          >
            <Trash2 size={16} />
          </button>
        </div>
      {/each}
    </div>
  </div>

  <!-- Bottom Navigation Bar (4 tabs from original APK: Đoạn chat, Cuộc gọi, Danh bạ, Tin) -->
  <div 
    class="w-full flex items-center justify-around py-2 border-t shrink-0 select-none transition-colors"
    class:bg-[#18191a]={chatState.isDarkMode}
    class:border-[#2f3031]={chatState.isDarkMode}
    class:bg-white={!chatState.isDarkMode}
    class:border-gray-200={!chatState.isDarkMode}
  >
    <!-- Tab 1: Đoạn chat with badge '12' -->
    <button 
      type="button" 
      class="flex flex-col items-center space-y-1 relative cursor-pointer active:scale-95 transition-transform"
      class:text-[#0084ff]={chatState.activeNavTab === 'chats'}
      class:text-gray-400={chatState.activeNavTab !== 'chats'}
      onclick={() => { chatState.activeNavTab = 'chats'; }}
    >
      <div class="relative">
        <OriginalIcon name="chat_nav" size={22} />
        <!-- Badge 12 from APK -->
        <span class="absolute -top-1 -right-2 bg-[#ff3b30] text-white text-[9px] font-bold px-1 rounded-full">
          12
        </span>
      </div>
      <span class="text-[10px] font-bold">Đoạn chat</span>
    </button>

    <!-- Tab 2: Cuộc gọi -->
    <button 
      type="button" 
      class="flex flex-col items-center space-y-1 cursor-pointer active:scale-95 transition-transform"
      class:text-[#0084ff]={chatState.activeNavTab === 'calls'}
      class:text-gray-400={chatState.activeNavTab !== 'calls'}
      onclick={() => startCall('audio')}
    >
      <OriginalIcon name="call" size={21} />
      <span class="text-[10px] font-medium">Cuộc gọi</span>
    </button>

    <!-- Tab 3: Danh bạ -->
    <button 
      type="button" 
      class="flex flex-col items-center space-y-1 cursor-pointer active:scale-95 transition-transform"
      class:text-[#0084ff]={chatState.activeNavTab === 'people'}
      class:text-gray-400={chatState.activeNavTab !== 'people'}
      onclick={openCreateContact}
    >
      <OriginalIcon name="phone_book" size={21} />
      <span class="text-[10px] font-medium">Danh bạ</span>
    </button>

    <!-- Tab 4: Tin -->
    <button 
      type="button" 
      class="flex flex-col items-center space-y-1 cursor-pointer active:scale-95 transition-transform"
      class:text-[#0084ff]={chatState.activeNavTab === 'stories'}
      class:text-gray-400={chatState.activeNavTab !== 'stories'}
      onclick={() => { chatState.activeModal = 'profile'; }}
    >
      <OriginalIcon name="story" size={21} />
      <span class="text-[10px] font-medium">Tin</span>
    </button>
  </div>
</div>
