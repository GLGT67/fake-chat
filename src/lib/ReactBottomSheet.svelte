<script>
  import { chatState, setReaction } from '../state.svelte.js';
  import { X } from '@lucide/svelte';

  const REACTIONS = [
    { id: 'like', name: 'Thích (Like)', icon: './reacts/ic_react_like.png' },
    { id: 'heart', name: 'Yêu thích (Thả tim)', icon: './reacts/ic_react_heart.png' },
    { id: 'haha', name: 'Haha', icon: './reacts/ic_react_haha.png' },
    { id: 'wow', name: 'Wow', icon: './reacts/ic_react_wow.png' },
    { id: 'sad', name: 'Buồn (Sad)', icon: './reacts/ic_react_sad.png' },
    { id: 'angry', name: 'Phẫn nộ (Angry)', icon: './reacts/ic_react_angry.png' },
  ];

  function handleSelect(id) {
    if (chatState.reactingMessageId) {
      setReaction(chatState.reactingMessageId, id);
    }
  }

  function closeModal() {
    chatState.activeModal = null;
    chatState.reactingMessageId = null;
  }
</script>

<div class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-3 bg-black/60 backdrop-blur-xs select-none animate-in fade-in duration-150" onclick={closeModal} role="button" tabindex="0" onkeydown={(e) => e.key === 'Escape' && closeModal()}>
  <div 
    class="w-full max-w-sm rounded-3xl shadow-2xl p-4 border transition-colors flex flex-col items-center space-y-3"
    class:bg-[#1e1e1e]={chatState.isDarkMode}
    class:border-[#333]={chatState.isDarkMode}
    class:text-white={chatState.isDarkMode}
    class:bg-white={!chatState.isDarkMode}
    class:border-gray-200={!chatState.isDarkMode}
    onclick={(e) => e.stopPropagation()}
    onkeydown={(e) => e.stopPropagation()}
    role="dialog"
    tabindex="-1"
  >
    <div class="w-10 h-1 bg-gray-300 dark:bg-gray-700 rounded-full mb-1"></div>
    <span class="text-xs font-bold uppercase tracking-wider text-gray-400">Bày tỏ cảm xúc tin nhắn</span>

    <!-- 6 Reactions Bar from com.fakechat.apk -->
    <div class="flex items-center justify-around w-full py-2 px-1 bg-gray-50 dark:bg-gray-800/60 rounded-2xl border border-gray-100 dark:border-gray-700">
      {#each REACTIONS as r}
        <button 
          type="button" 
          class="flex flex-col items-center space-y-1 p-1.5 rounded-xl hover:scale-125 active:scale-95 transition-transform cursor-pointer"
          onclick={() => handleSelect(r.id)}
          title={r.name}
        >
          <img src={r.icon} alt={r.name} class="w-8 h-8 object-contain drop-shadow-xs" />
        </button>
      {/each}
    </div>

    <!-- Options below -->
    <div class="w-full flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold">
      <button 
        type="button" 
        class="text-red-500 hover:underline cursor-pointer"
        onclick={() => handleSelect(null)}
      >
        Gỡ cảm xúc
      </button>

      <button 
        type="button" 
        class="text-gray-500 hover:text-black dark:hover:text-white cursor-pointer"
        onclick={closeModal}
      >
        Đóng
      </button>
    </div>
  </div>
</div>

