<script>
  import { chatState, getActiveConversation } from "./state.svelte.js";
  import IosStatusBar from "./lib/IosStatusBar.svelte";
  import IosHomeBar from "./lib/IosHomeBar.svelte";
  import ChatHeader from "./lib/ChatHeader.svelte";
  import MessageBubble from "./lib/MessageBubble.svelte";
  import InputToolbar from "./lib/InputToolbar.svelte";
  import ControlDeck from "./lib/ControlDeck.svelte";
  import ProfileModal from "./lib/ProfileModal.svelte";
  import MessageEditModal from "./lib/MessageEditModal.svelte";
  import MediaAttachModal from "./lib/MediaAttachModal.svelte";
  import FakeCallModal from "./lib/FakeCallModal.svelte";
  import MainMessengerScreen from "./lib/MainMessengerScreen.svelte";
  import CreateContactScreen from "./lib/CreateContactScreen.svelte";
  import ReactBottomSheet from "./lib/ReactBottomSheet.svelte";

  const conv = $derived(getActiveConversation());
  /** @type {HTMLDivElement | undefined} */
  let ảchatScrollRef = $state();

  function scrollToBottom() {
    if (chatScrollRef) {
      chatScrollRef.scrollTop = chatScrollRef.scrollHeight;
    }
  }

  $effect(() => {
    // Scroll down whenever messages change in active conversation
    conv?.messages?.length;
    setTimeout(scrollToBottom, 60);
  });
</script>

<!-- Top Floating Admin Controls (Hidden in Snapshot Mode) -->
<ControlDeck />

<!-- Main Container -->
<main
  class="w-full h-[100dvh] flex items-center justify-center overflow-hidden select-none transition-all"
  class:sm:p-4={!chatState.isSnapshotMode}
  class:p-0={chatState.isSnapshotMode}
>
  <!-- Desktop Simulator Phone Chassis (Outer Casing - Hidden in Snapshot Mode) -->
  <div 
    class="relative w-full h-full flex items-center justify-center transition-all"
    class:sm:w-[397px]={!chatState.isSnapshotMode}
    class:sm:h-[856px]={!chatState.isSnapshotMode}
    class:sm:max-h-[92vh]={!chatState.isSnapshotMode}
    class:sm:p-2={!chatState.isSnapshotMode}
    class:sm:rounded-[52px]={!chatState.isSnapshotMode}
    class:sm:bg-[#1e293b]={!chatState.isSnapshotMode}
    class:sm:shadow-[0_25px_60px_-15px_rgba(0,0,0,0.7)]={!chatState.isSnapshotMode}
  >
    <!-- Pure Phone Screen Frame (The ACTUAL screen to capture!) -->
    <div
      id="phone-screen-frame"
      class="relative w-full h-full flex flex-col overflow-hidden transition-colors duration-200 border-0"
      class:sm:w-[393px]={chatState.isSnapshotMode}
      class:sm:h-[852px]={chatState.isSnapshotMode}
      class:sm:rounded-[44px]={!chatState.isSnapshotMode}
      class:rounded-none={chatState.isSnapshotMode}
      class:dark={chatState.isDarkMode}
      class:bg-[#18191a]={chatState.isDarkMode}
      class:bg-white={!chatState.isDarkMode}
    >
    <!-- iOS Dynamic Island & Status Bar -->
    <IosStatusBar />

    <!-- Screen Routing (100% clone of APK screens) -->
    {#if chatState.currentScreen === "chats_list"}
      <!-- Screen 1: Main Messenger Hub (activity_main_messenger.xml) -->
      <MainMessengerScreen />
    {:else if chatState.currentScreen === "create_contact"}
      <!-- Screen 2: Create Fake Contact (activity_fake_contact_messenger.xml) -->
      <CreateContactScreen />
    {:else}
      <!-- Screen 3: Chat Room HUD (activity_messenger_contact_message.xml) -->
      <ChatHeader />

      <!-- Messages Scrollable Body -->
      <div
        bind:this={chatScrollRef}
        class="flex-1 overflow-y-auto px-3.5 py-2.5 space-y-1 ios-scroll no-scrollbar"
        class:bg-[#18191a]={chatState.isDarkMode}
        class:bg-white={!chatState.isDarkMode}
      >
        <!-- Encrypted notice or top contact greeting -->
        <div class="text-center py-4 select-none">
          <img
            src={conv.avatar}
            alt={conv.name}
            class="w-16 h-16 rounded-full mx-auto object-cover shadow-sm mb-2 border border-black/5"
          />
          <h3
            class="font-bold text-[17px] leading-tight"
            class:text-white={chatState.isDarkMode}
            class:text-gray-900={!chatState.isDarkMode}
          >
            {conv.name}
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
        {#each conv.messages as msg, index (msg.id)}
          {@const isLastFromSender =
            index === conv.messages.length - 1 ||
            conv.messages[index + 1]?.sender !== msg.sender}
          {@const isLastOverall = index === conv.messages.length - 1}
          <MessageBubble message={msg} {isLastFromSender} {isLastOverall} />
        {/each}
      </div>

      <!-- Messenger Bottom Input Bar -->
      <InputToolbar />
    {/if}

    <!-- iOS Home Indicator Bar -->
    <IosHomeBar />

    <!-- Interactive Overlays & Modals -->
    {#if chatState.activeModal === "react"}
      <ReactBottomSheet />
    {:else if chatState.activeModal === "profile"}
      <ProfileModal />
    {:else if chatState.activeModal === "edit_message"}
      <MessageEditModal />
    {:else if chatState.activeModal === "attach"}
      <MediaAttachModal />
    {:else if chatState.activeModal === "call"}
      <FakeCallModal />
    {/if}
    </div>
  </div>
</main>
