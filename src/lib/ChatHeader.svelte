<script>
  import { chatState, THEMES, getActiveConversation } from '../state.svelte.js';
  import { ChevronLeft, Info, BadgeCheck } from '@lucide/svelte';
  import OriginalIcon from './OriginalIcon.svelte';

  const conv = $derived(getActiveConversation());
  const theme = $derived(THEMES[conv.themeKey] || THEMES.classic);

  function openProfile() {
    chatState.activeModal = 'profile';
  }

  function handleBack() {
    chatState.currentScreen = 'chats_list';
  }

  function startCall(type) {
    chatState.callType = type;
    chatState.callStatus = 'incoming';
    chatState.callTimer = 0;
    chatState.activeModal = 'call';
  }
</script>

<header 
  class="w-full flex items-center justify-between px-2.5 py-2 border-b select-none transition-colors duration-200 z-20 shrink-0"
  class:bg-[#18191a]={chatState.isDarkMode}
  class:border-[#2f3031]={chatState.isDarkMode}
  class:bg-white={!chatState.isDarkMode}
  class:border-gray-100={!chatState.isDarkMode}
>
  <!-- Left: Back button & Partner Info -->
  <div class="flex items-center space-x-1.5 flex-1 min-w-0">
    <button 
      type="button"
      class="p-1 -ml-1 rounded-full active:opacity-60 transition-opacity cursor-pointer text-gray-700 dark:text-gray-200"
      onclick={handleBack}
      title="Trở về danh sách đoạn chat"
    >
      <ChevronLeft size={28} strokeWidth={2.8} />
    </button>

    <!-- Avatar with Online indicator -->
    <button 
      type="button" 
      class="relative shrink-0 text-left cursor-pointer group active:scale-95 transition-transform"
      onclick={openProfile}
    >
      <img 
        src={conv.avatar} 
        alt={conv.name} 
        class="w-10 h-10 rounded-full object-cover shadow-xs border border-black/5"
      />
      {#if conv.isOnline}
        <span 
          class="absolute bottom-0 right-0 w-3 h-3 bg-[#31a24c] rounded-full border-2 transition-colors"
          class:border-[#18191a]={chatState.isDarkMode}
          class:border-white={!chatState.isDarkMode}
        ></span>
      {/if}
    </button>

    <!-- Name & Status -->
    <button 
      type="button" 
      class="flex flex-col text-left min-w-0 flex-1 pl-1 cursor-pointer"
      onclick={openProfile}
    >
      <div class="flex items-center space-x-1">
        <span 
          class="font-bold text-[16px] leading-tight truncate"
          class:text-white={chatState.isDarkMode}
          class:text-black={!chatState.isDarkMode}
        >
          {conv.name}
        </span>
        {#if conv.hasVerifiedBadge}
          <BadgeCheck size={16} class="text-[#0084ff] shrink-0 fill-[#0084ff] text-white" />
        {/if}
      </div>
      <span 
        class="text-[12px] leading-tight truncate font-normal transition-colors"
        class:text-gray-400={chatState.isDarkMode}
        class:text-gray-500={!chatState.isDarkMode}
      >
        {conv.statusText}
      </span>
    </button>
  </div>

  <!-- Right Actions: Phone, Video, Info (using extracted APK vectors) -->
  <div class="flex items-center space-x-3.5 pl-2 shrink-0" style="color: {theme.primary};">
    <button 
      type="button"
      class="p-1 active:scale-90 transition-transform cursor-pointer"
      onclick={() => startCall('audio')}
      title="Giả lập cuộc gọi thoại"
    >
      <OriginalIcon name="call" size={20} />
    </button>

    <button 
      type="button"
      class="p-1 active:scale-90 transition-transform cursor-pointer"
      onclick={() => startCall('video')}
      title="Giả lập cuộc gọi video"
    >
      <OriginalIcon name="call_video" size={22} />
    </button>

    <button 
      type="button"
      class="p-1 active:scale-90 transition-transform cursor-pointer"
      onclick={openProfile}
      title="Tùy chỉnh & Giao diện"
    >
      <Info size={22} strokeWidth={2.4} />
    </button>
  </div>
</header>
