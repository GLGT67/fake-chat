<script>
  import { chatState, THEMES, addMessage, getActiveConversation } from '../state.svelte.js';
  import { Smile, Send } from '@lucide/svelte';
  import OriginalIcon from './OriginalIcon.svelte';

  const conv = $derived(getActiveConversation());
  const theme = $derived(THEMES[conv.themeKey] || THEMES.classic);
  let inputText = $state('');
  let fileInputRef;

  function handleSend() {
    if (!inputText.trim()) {
      // Send Like Thumbs Up if empty
      addMessage({
        type: 'like',
        content: '👍',
        sender: chatState.activeSender
      });
      return;
    }

    addMessage({
      type: 'text',
      content: inputText.trim(),
      sender: chatState.activeSender
    });
    inputText = '';
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  }

  function toggleSender() {
    chatState.activeSender = chatState.activeSender === 'me' ? 'them' : 'me';
  }

  function openAttach() {
    chatState.activeModal = 'attach';
  }

  function handleImageUpload(e) {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        addMessage({
          type: 'image',
          imageUri: reader.result,
          content: 'Hình ảnh',
          sender: chatState.activeSender
        });
      };
      reader.readAsDataURL(file);
    }
    e.target.value = '';
  }
</script>

<div 
  class="w-full flex flex-col border-t select-none transition-colors duration-200 z-20 shrink-0"
  class:bg-[#18191a]={chatState.isDarkMode}
  class:border-[#2f3031]={chatState.isDarkMode}
  class:bg-white={!chatState.isDarkMode}
  class:border-gray-100={!chatState.isDarkMode}
>
  <!-- Hidden File Input for fast image attachment -->
  <input 
    type="file" 
    accept="image/*" 
    bind:this={fileInputRef} 
    onchange={handleImageUpload} 
    class="hidden" 
  />

  <!-- Quick Switcher Bar (Toggled off in snapshot mode) -->
  {#if !chatState.isSnapshotMode}
    <div 
      class="flex items-center justify-between px-4 py-1.5 text-[11px] font-semibold border-b transition-colors"
      class:bg-[#242526]={chatState.isDarkMode}
      class:border-[#3a3b3c]={chatState.isDarkMode}
      class:bg-gray-50={!chatState.isDarkMode}
      class:border-gray-100={!chatState.isDarkMode}
    >
      <div class="flex items-center space-x-2">
        <span class="text-gray-700 dark:text-gray-300">Người gửi tiếp theo:</span>
        <button 
          type="button" 
          class="flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full transition-all active:scale-95 shadow-2xs cursor-pointer font-bold"
          class:bg-[#0084ff]={chatState.activeSender === 'me'}
          class:bg-gray-300={chatState.activeSender === 'them' && !chatState.isDarkMode}
          class:text-gray-900={chatState.activeSender === 'them' && !chatState.isDarkMode}
          class:bg-gray-700={chatState.activeSender === 'them' && chatState.isDarkMode}
          class:text-white={chatState.activeSender === 'me' || (chatState.activeSender === 'them' && chatState.isDarkMode)}
          onclick={toggleSender}
        >
          {#if chatState.activeSender === 'me'}
            <span>Tôi gửi ➔</span>
          {:else}
            <span>◀ {conv.name} gửi</span>
          {/if}
        </button>
      </div>

      <button 
        type="button" 
        class="text-gray-700 hover:text-black dark:text-gray-300 dark:hover:text-white text-[10px] font-semibold underline cursor-pointer"
        onclick={toggleSender}
      >
        (Nhấn đổi)
      </button>
    </div>
  {/if}

  <!-- Main Messenger Input Bar (HUD 100% matched to activity_messenger_contact_message.xml) -->
  <div class="flex items-center px-2 py-1.5 space-x-2">
    <!-- Left Tools: 4-dot, Camera, Gallery, Mic (Using original APK vector drawables) -->
    <div class="flex items-center space-x-1.5" style="color: {theme.primary};">
      <!-- 4-dot menu (@7F0A0168 / ic_4_dot) -->
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={openAttach}
        title="Menu tính năng (4 chấm)"
      >
        <OriginalIcon name="4_dot" size={19} />
      </button>

      <!-- Camera (@7F0A0187 / ic_camera) -->
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={() => fileInputRef.click()}
        title="Chụp ảnh"
      >
        <OriginalIcon name="camera" size={19} />
      </button>

      <!-- Gallery / Image (@7F0A01BF / ic_add_image) -->
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={() => fileInputRef.click()}
        title="Thư viện ảnh"
      >
        <OriginalIcon name="image" size={19} />
      </button>

      <!-- Mic (@7F0A01B3 / ic_mic) -->
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={() => {
          addMessage({
            type: 'voice',
            voiceDuration: '0:22',
            sender: chatState.activeSender
          });
        }}
        title="Ghi âm giọng nói"
      >
        <OriginalIcon name="mic" size={19} />
      </button>
    </div>

    <!-- Text Input Pill (@7F0A0105 with hint 'Nhắn tin' & smiley emoji @7F0A01C0) -->
    <div 
      class="flex-1 flex items-center rounded-full px-3 py-1.5 transition-colors"
      class:bg-[#f0f2f5]={!chatState.isDarkMode}
      class:text-black={!chatState.isDarkMode}
      class:bg-[#242526]={chatState.isDarkMode}
      class:text-white={chatState.isDarkMode}
    >
      <input 
        type="text" 
        placeholder="Nhắn tin"
        bind:value={inputText}
        onkeydown={handleKeyDown}
        class="w-full bg-transparent text-[15px] outline-none placeholder-gray-400 font-normal leading-normal"
      />
      <button 
        type="button" 
        class="text-gray-400 active:opacity-60 ml-1 shrink-0"
        onclick={() => { inputText += ' 😊'; }}
      >
        <Smile size={19} strokeWidth={2} />
      </button>
    </div>

    <!-- Right Action Button: Like or Send -->
    <div class="shrink-0 flex items-center justify-center" style="color: {theme.primary};">
      {#if inputText.trim().length > 0}
        <button 
          type="button" 
          class="w-8 h-8 rounded-full flex items-center justify-center text-white active:scale-90 transition-transform cursor-pointer shadow-xs"
          style="background-color: {theme.primary};"
          onclick={handleSend}
          title="Gửi tin nhắn"
        >
          <Send size={17} strokeWidth={2.5} class="ml-0.5" />
        </button>
      {:else}
        <!-- Original ic_like (@7F0A01A4) -->
        <button 
          type="button" 
          class="w-8 h-8 flex items-center justify-center active:scale-125 transition-transform cursor-pointer select-none"
          onclick={handleSend}
          title="Gửi Like"
        >
          <OriginalIcon name="like" size={24} />
        </button>
      {/if}
    </div>
  </div>
</div>
