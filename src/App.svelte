<script>
  import { chatState } from './state.svelte.js';
  import IosStatusBar from './lib/IosStatusBar.svelte';
  import IosHomeBar from './lib/IosHomeBar.svelte';
  import ChatHeader from './lib/ChatHeader.svelte';
  import MessageBubble from './lib/MessageBubble.svelte';
  import InputToolbar from './lib/InputToolbar.svelte';
  import ControlDeck from './lib/ControlDeck.svelte';
  import ProfileModal from './lib/ProfileModal.svelte';
  import MessageEditModal from './lib/MessageEditModal.svelte';
  import MediaAttachModal from './lib/MediaAttachModal.svelte';
  import FakeCallModal from './lib/FakeCallModal.svelte';

  let chatScrollRef;

  function scrollToBottom() {
    if (chatScrollRef) {
      chatScrollRef.scrollTop = chatScrollRef.scrollHeight;
    }
  }

  $effect(() => {
    // Scroll down whenever messages change
    chatState.messages.length;
    setTimeout(scrollToBottom, 60);
  });
</script>

<!-- Top Floating Admin Controls (Hidden in Snapshot Mode) -->
<ControlDeck />

<!-- Main Container -->
<main class="w-full h-[100dvh] flex items-center justify-center overflow-hidden sm:p-4 select-none">
  <!-- iPhone Realistic Frame (Full width on mobile, 400px on desktop) -->
  <div 
    id="phone-screen-frame"
    class="relative w-full h-full sm:w-[393px] sm:h-[852px] sm:max-h-[92vh] sm:rounded-[48px] sm:shadow-[0_25px_60px_-15px_rgba(0,0,0,0.7)] flex flex-col overflow-hidden sm:border-[8px] sm:border-[#1e293b] transition-colors duration-200"
    class:dark={chatState.isDarkMode}
    class:bg-[#18191a]={chatState.isDarkMode}
    class:bg-white={!chatState.isDarkMode}
  >
    <!-- iOS Dynamic Island & Status Bar -->
    <IosStatusBar />

    <!-- Messenger Chat Header -->
    <ChatHeader />

    <!-- Messages Scrollable Body -->
    <div 
      bind:this={chatScrollRef}
      class="flex-1 overflow-y-auto px-3.5 py-2.5 space-y-1 ios-scroll no-scrollbar"
      class:bg-[#18191a]={chatState.isDarkMode}
      class:bg-white={!chatState.isDarkMode}
    >
      <!-- Encrypted notice or top hint (discreet) -->
      <div class="text-center py-4 select-none">
        <img 
          src={chatState.partnerAvatar} 
          alt={chatState.partnerName} 
          class="w-16 h-16 rounded-full mx-auto object-cover shadow-sm mb-2 border border-black/5" 
        />
        <h3 
          class="font-bold text-[17px] leading-tight"
          class:text-white={chatState.isDarkMode}
          class:text-gray-900={!chatState.isDarkMode}
        >
          {chatState.partnerName}
        </h3>
        <p 
          class="text-xs mt-0.5"
          class:text-gray-400={chatState.isDarkMode}
          class:text-gray-500={!chatState.isDarkMode}
        >
          Các bạn đã kết nối trên Messenger
        </p>
      </div>

      <!-- Messages List -->
      {#each chatState.messages as msg, index (msg.id)}
        {@const isLastFromSender = (index === chatState.messages.length - 1) || (chatState.messages[index + 1]?.sender !== msg.sender)}
        {@const isLastOverall = index === chatState.messages.length - 1}
        <MessageBubble 
          message={msg} 
          {isLastFromSender} 
          {isLastOverall} 
        />
      {/each}
    </div>

    <!-- Messenger Bottom Input Bar -->
    <InputToolbar />

    <!-- iOS Home Indicator Bar -->
    <IosHomeBar />

    <!-- Interactive Overlays & Modals -->
    {#if chatState.activeModal === 'profile'}
      <ProfileModal />
    {:else if chatState.activeModal === 'edit_message'}
      <MessageEditModal />
    {:else if chatState.activeModal === 'attach'}
      <MediaAttachModal />
    {:else if chatState.activeModal === 'call'}
      <FakeCallModal />
    {/if}
  </div>
</main>
