<script>
  import { chatState, THEMES, addMessage } from '../state.svelte.js';
  import { Plus, Camera, Image as ImageIcon, Mic, Smile, Send } from '@lucide/svelte';

  const theme = $derived(THEMES[chatState.themeKey] || THEMES.classic);
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
        <span class="text-gray-600 dark:text-gray-300">Người gửi tiếp theo:</span>
        <button 
          type="button" 
          class="flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full transition-all active:scale-95 shadow-2xs cursor-pointer font-bold"
          class:bg-[#0084ff]={chatState.activeSender === 'me'}
          class:bg-gray-300={chatState.activeSender === 'them' && !chatState.isDarkMode}
          class:text-gray-800={chatState.activeSender === 'them' && !chatState.isDarkMode}
          class:bg-gray-700={chatState.activeSender === 'them' && chatState.isDarkMode}
          class:text-white={chatState.activeSender === 'me' || (chatState.activeSender === 'them' && chatState.isDarkMode)}
          onclick={toggleSender}
        >
          {#if chatState.activeSender === 'me'}
            <span>Tôi gửi ➔</span>
          {:else}
            <span>◀ {chatState.partnerName} gửi</span>
          {/if}
        </button>
      </div>

      <button 
        type="button" 
        class="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 text-[10px] underline cursor-pointer"
        onclick={toggleSender}
      >
        (Nhấn đổi)
      </button>
    </div>
  {/if}

  <!-- Main Messenger Input Bar -->
  <div class="flex items-center px-2 py-1.5 space-x-1.5">
    <!-- Left Tools -->
    <div class="flex items-center space-x-1" style="color: {theme.primary};">
      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={openAttach}
        title="Đính kèm tính năng"
      >
        <Plus size={22} strokeWidth={2.8} />
      </button>

      <button 
        type="button" 
        class="w-8 h-8 rounded-full flex items-center justify-center active:scale-90 transition-transform cursor-pointer"
        onclick={() => fileInputRef.click()}
        title="Chọn ảnh"
      >
        <ImageIcon size={21} strokeWidth={2.3} />
      </button>

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
        title="Gửi voice ghi âm"
      >
        <Mic size={21} strokeWidth={2.3} />
      </button>
    </div>

    <!-- Text Input Pill -->
    <div 
      class="flex-1 flex items-center rounded-full px-3 py-1.5 transition-colors"
      class:bg-[#f0f2f5]={!chatState.isDarkMode}
      class:text-black={!chatState.isDarkMode}
      class:bg-[#242526]={chatState.isDarkMode}
      class:text-white={chatState.isDarkMode}
    >
      <input 
        type="text" 
        placeholder="Aa"
        bind:value={inputText}
        onkeydown={handleKeyDown}
        class="w-full bg-transparent text-[15px] outline-none placeholder-gray-400 font-normal leading-normal"
      />
      <button 
        type="button" 
        class="text-gray-400 active:opacity-60 ml-1 shrink-0"
        onclick={() => { inputText += ' 😊'; }}
      >
        <Smile size={20} strokeWidth={2} />
      </button>
    </div>

    <!-- Right Action Button: Like or Send -->
    <div class="shrink-0 flex items-center justify-center">
      {#if inputText.trim().length > 0}
        <button 
          type="button" 
          class="w-9 h-9 rounded-full flex items-center justify-center text-white active:scale-90 transition-transform cursor-pointer shadow-xs"
          style="background-color: {theme.primary};"
          onclick={handleSend}
          title="Gửi tin nhắn"
        >
          <Send size={18} strokeWidth={2.5} class="ml-0.5" />
        </button>
      {:else}
        <button 
          type="button" 
          class="w-9 h-9 flex items-center justify-center text-[26px] active:scale-125 transition-transform cursor-pointer select-none"
          onclick={handleSend}
          title="Gửi Like"
        >
          👍
        </button>
      {/if}
    </div>
  </div>
</div>

