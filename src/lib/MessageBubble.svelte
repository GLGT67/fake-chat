<script>
  import { chatState, THEMES, getActiveConversation } from '../state.svelte.js';
  import { Play, Pause, PhoneCall, PhoneMissed, Check, CheckCheck } from '@lucide/svelte';
  import OriginalIcon from './OriginalIcon.svelte';

  const { message, isLastFromSender, isLastOverall } = $props();

  const conv = $derived(getActiveConversation());
  const theme = $derived(THEMES[conv.themeKey] || THEMES.classic);
  let isPlayingVoice = $state(false);
  let showTimestamp = $state(false);

  function toggleVoice() {
    isPlayingVoice = !isPlayingVoice;
    if (isPlayingVoice) {
      setTimeout(() => { isPlayingVoice = false; }, 3000);
    }
  }

  function handleMessageClick() {
    showTimestamp = !showTimestamp;
  }

  function handleMessageEdit(e) {
    e.stopPropagation();
    chatState.editingMessageId = message.id;
    chatState.activeModal = 'edit_message';
  }

  let pressTimer = null;

  function handleTouchStart(e) {
    pressTimer = setTimeout(() => {
      handleReactionClick(e);
    }, 450);
  }

  function handleTouchEnd() {
    if (pressTimer) {
      clearTimeout(pressTimer);
      pressTimer = null;
    }
  }

  function handleReactionClick(e) {
    if (e && e.stopPropagation) e.stopPropagation();
    chatState.reactingMessageId = message.id;
    chatState.activeModal = 'react';
  }
</script>

{#if message.type === 'timestamp_divider'}
  <!-- Timestamp Divider (@7F0D0090 / item_chat_time_message_messenger) -->
  <div 
    class="w-full flex justify-center my-3 select-none cursor-pointer"
    onclick={handleMessageEdit}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && handleMessageEdit(e)}
  >
    <span 
      class="text-[11px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full transition-colors"
      class:text-gray-400={chatState.isDarkMode}
      class:text-gray-500={!chatState.isDarkMode}
    >
      {message.content || message.timestamp}
    </span>
  </div>

{:else if message.type === 'call_event'}
  <!-- Call Event Notification Banner -->
  <div 
    class="w-full flex flex-col items-center justify-center my-2 select-none cursor-pointer"
    onclick={handleMessageEdit}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && handleMessageEdit(e)}
  >
    <div 
      class="flex items-center space-x-1.5 px-3 py-1 rounded-full text-[12px] font-medium shadow-2xs border transition-colors"
      class:bg-[#242526]={chatState.isDarkMode}
      class:border-[#3a3b3c]={chatState.isDarkMode}
      class:text-gray-300={chatState.isDarkMode}
      class:bg-gray-100={!chatState.isDarkMode}
      class:border-gray-200={!chatState.isDarkMode}
      class:text-gray-600={!chatState.isDarkMode}
    >
      {#if message.callInfo?.missed}
        <PhoneMissed size={14} class="text-red-500" />
        <span>Cuộc gọi nhỡ</span>
      {:else}
        <PhoneCall size={14} style="color: {theme.primary};" />
        <span>Cuộc gọi {message.callInfo?.type === 'video' ? 'video' : 'thoại'} kết thúc • {message.callInfo?.duration || '10 phút'}</span>
      {/if}
    </div>
    <span class="text-[10px] text-gray-400 mt-0.5">{message.timestamp}</span>
  </div>

{:else}
  <!-- Standard Message Bubble (Me or Them) -->
  <div 
    class="flex flex-col my-[2.5px] transition-all select-none"
    class:items-end={message.sender === 'me'}
    class:items-start={message.sender === 'them'}
  >
    <div class="flex items-end max-w-[80%] space-x-1.5 group relative">
      <!-- Them Avatar on the left side of the last message in a group -->
      {#if message.sender === 'them'}
        <div class="w-7 h-7 shrink-0 -mb-0.5">
          {#if isLastFromSender}
            <img 
              src={conv.avatar} 
              alt={conv.name} 
              class="w-7 h-7 rounded-full object-cover border border-black/5 shadow-2xs"
            />
          {/if}
        </div>
      {/if}

      <!-- Message Content Container -->
      <div 
        class="relative cursor-pointer active:scale-[0.98] transition-transform"
        onclick={handleMessageClick}
        ondblclick={handleMessageEdit}
        ontouchstart={handleTouchStart}
        ontouchend={handleTouchEnd}
        oncontextmenu={(e) => { e.preventDefault(); handleReactionClick(e); }}
        role="button"
        tabindex="0"
        onkeydown={(e) => e.key === 'Enter' && handleMessageEdit(e)}
      >
        {#if message.type === 'text'}
          <!-- Text Bubble -->
          <div 
            class="px-3.5 py-2 rounded-2xl text-[15px] leading-snug break-words tracking-tight transition-colors shadow-2xs"
            class:bg-[#e4e6eb]={message.sender === 'them' && !chatState.isDarkMode}
            class:text-[#050505]={message.sender === 'them' && !chatState.isDarkMode}
            class:bg-[#303030]={message.sender === 'them' && chatState.isDarkMode}
            class:text-[#e4e6eb]={message.sender === 'them' && chatState.isDarkMode}
            class:rounded-bl-[4px]={message.sender === 'them' && isLastFromSender}
            class:rounded-br-[4px]={message.sender === 'me' && isLastFromSender}
            style={message.sender === 'me' ? `background-color: ${theme.primary}; color: white;` : ''}
          >
            {message.content}
          </div>

        {:else if message.type === 'image'}
          <!-- Attached Image Bubble -->
          <div class="rounded-2xl overflow-hidden shadow-xs border max-w-[220px]"
               class:border-[#3a3b3c]={chatState.isDarkMode}
               class:border-gray-200={!chatState.isDarkMode}
          >
            <img src={message.imageUri || message.content} alt="Đính kèm" class="w-full h-auto object-cover max-h-[300px]" />
          </div>

        {:else if message.type === 'voice'}
          <!-- Voice Note Waveform Bubble -->
          <div 
            class="flex items-center space-x-2.5 px-3 py-2 rounded-2xl min-w-[170px] shadow-2xs"
            class:bg-[#e4e6eb]={message.sender === 'them' && !chatState.isDarkMode}
            class:bg-[#303030]={message.sender === 'them' && chatState.isDarkMode}
            class:text-black={message.sender === 'them' && !chatState.isDarkMode}
            class:text-white={message.sender === 'them' && chatState.isDarkMode}
            style={message.sender === 'me' ? `background-color: ${theme.primary}; color: white;` : ''}
          >
            <!-- Play/Pause Button -->
            <button 
              type="button" 
              class="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center shrink-0 active:scale-90 transition-transform"
              onclick={(e) => { e.stopPropagation(); toggleVoice(); }}
            >
              {#if isPlayingVoice}
                <Pause size={14} class="fill-current" />
              {:else}
                <Play size={14} class="fill-current ml-0.5" />
              {/if}
            </button>

            <!-- Waveform bars -->
            <div class="flex items-center space-x-[2px] h-5 flex-1">
              {#each [6, 12, 18, 10, 16, 8, 14, 20, 12, 6, 14, 18, 8, 12, 6] as h, i}
                <div 
                  class="w-[2.5px] rounded-full transition-all duration-200 {isPlayingVoice && (i % 3 === 0) ? 'scale-y-125' : ''}" 
                  style="height: {h}px; background-color: currentColor; opacity: {i < 7 ? 0.95 : 0.45};"
                ></div>
              {/each}
            </div>

            <!-- Voice duration -->
            <span class="text-[12px] font-semibold shrink-0 opacity-90">{message.voiceDuration || '0:15'}</span>
          </div>

        {:else if message.type === 'like'}
          <!-- Messenger Like Thumbs Up Icon (using original APK vector) -->
          <div class="w-10 h-10 select-none active:scale-125 transition-transform" style="color: {theme.primary};">
            <OriginalIcon name="like" size={38} />
          </div>
        {/if}

        <!-- Reaction Badge Overlay (@7F0A009E / ic_react_*) -->
        {#if message.react}
          <button 
            type="button" 
            class="absolute -bottom-2 {message.sender === 'me' ? 'left-1' : 'right-1'} bg-white dark:bg-[#242526] rounded-full px-1 py-0.5 shadow-md border border-gray-200 dark:border-gray-700 flex items-center space-x-0.5 active:scale-125 transition-transform cursor-pointer"
            onclick={handleReactionClick}
          >
            <img src="./reacts/ic_react_{message.react}.png" alt={message.react} class="w-4 h-4 object-contain" />
          </button>
        {/if}
      </div>

      <!-- Quick Reaction Trigger Button on Hover / Side -->
      <button 
        type="button" 
        class="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-yellow-500 transition-opacity cursor-pointer shrink-0"
        onclick={handleReactionClick}
        title="Thả cảm xúc"
      >
        😊
      </button>
    </div>

    <!-- Subtitle: Timestamp & Status (when tapped or last message) -->
    <div 
      class="text-[11px] px-1 mt-0.5 flex items-center space-x-1 transition-opacity duration-200 select-none"
      class:text-gray-400={chatState.isDarkMode}
      class:text-gray-500={!chatState.isDarkMode}
    >
      {#if showTimestamp || isLastOverall}
        <span>{message.timestamp}</span>
      {/if}

      {#if message.sender === 'me' && isLastOverall}
        {#if message.status === 'seen'}
          <!-- Mini Avatar for Seen -->
          <img 
            src={conv.avatar} 
            alt="Đã xem" 
            class="w-3.5 h-3.5 rounded-full object-cover ml-1 shadow-2xs border border-white"
            title="Đã xem"
          />
        {:else if message.status === 'delivered'}
          <div class="w-3.5 h-3.5 rounded-full bg-gray-400 text-white flex items-center justify-center text-[8px] ml-0.5">
            <Check size={9} strokeWidth={3} />
          </div>
        {:else if message.status === 'sent'}
          <div class="w-3.5 h-3.5 rounded-full border border-gray-400 text-gray-400 flex items-center justify-center text-[8px] ml-0.5">
            <Check size={9} strokeWidth={3} />
          </div>
        {/if}
      {/if}
    </div>
  </div>
{/if}
