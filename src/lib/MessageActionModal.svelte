<script>
  import { 
    chatState, 
    setReaction, 
    deleteMessage, 
    toggleMessageSender, 
    getCurrentActiveChat 
  } from '../state.svelte.js';
  import { 
    X, 
    Reply, 
    Edit3, 
    Repeat, 
    Trash2, 
    Copy, 
    Check, 
    Heart 
  } from '@lucide/svelte';

  const message = $derived(chatState.selectedActionMessage);
  const conv = $derived(getCurrentActiveChat());
  let isEditing = $state(false);
  let editText = $state('');
  let editTime = $state('');
  let editStatus = $state('seen'); // 'seen' | 'delivered' | 'sent'
  let copied = $state(false);

  $effect(() => {
    if (message) {
      editText = message.content || '';
      editTime = message.timestamp || '';
      editStatus = message.status || 'seen';
      isEditing = false;
      copied = false;
    }
  });

  function close() {
    chatState.activeModal = null;
    chatState.selectedActionMessage = null;
  }

  function handleBackdropClick(/** @type {any} */ e) {
    if (e.target === e.currentTarget) {
      close();
    }
  }

  function handleReact(reaction) {
    if (message) {
      setReaction(message.id, reaction);
    }
    close();
  }

  function handleReply() {
    if (message) {
      chatState.replyingToMessage = message;
    }
    close();
  }

  function handleToggleSender() {
    if (message) {
      toggleMessageSender(message.id);
    }
    close();
  }

  function handleDelete() {
    if (message) {
      deleteMessage(message.id);
    }
    close();
  }

  function handleCopy() {
    if (message && message.content) {
      navigator.clipboard?.writeText(message.content);
      copied = true;
      setTimeout(close, 600);
    }
  }

  function handleSaveEdit() {
    if (message) {
      message.content = editText.trim();
      message.timestamp = editTime.trim() || message.timestamp;
      message.status = editStatus;
    }
    close();
  }
</script>

{#if message}
  <div 
    class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/60 backdrop-blur-xs select-none animate-in fade-in duration-150"
    onclick={handleBackdropClick}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Escape' && close()}
  >
    <!-- Modal Sheet Container -->
    <div 
      class="w-full sm:max-w-sm rounded-t-3xl sm:rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh] border transition-colors bg-white dark:bg-[#202124] text-gray-900 dark:text-white border-gray-200 dark:border-gray-800"
      role="region"
      aria-label="Tùy chọn tin nhắn"
    >
      <!-- Top Drag Handle for Mobile -->
      <div class="w-full flex justify-center pt-2.5 pb-1 sm:hidden">
        <div class="w-10 h-1 bg-gray-300 dark:bg-gray-600 rounded-full"></div>
      </div>

      <!-- Quick Emoji Reactions Bar -->
      <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-800 flex items-center justify-around bg-gray-50/80 dark:bg-gray-800/40">
        {#if chatState.currentApp === 'zalo'}
          <!-- Zalo Reactions -->
          <button 
            type="button" 
            class="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-white dark:bg-gray-700 shadow-xs border border-gray-200 dark:border-gray-600 active:scale-125 transition-transform cursor-pointer"
            onclick={() => handleReact('heart')}
          >
            <span class="text-xl">❤️</span>
            <span class="text-xs font-bold text-red-500">{message.hasHeart ? 'Bỏ tim' : 'Thả tim'}</span>
          </button>

          {#each ['👍', '😂', '😮', '😭', '😡'] as emo}
            <button 
              type="button" 
              class="text-2xl hover:scale-125 active:scale-130 transition-transform cursor-pointer p-1"
              onclick={() => handleReact('heart')}
            >
              {emo}
            </button>
          {/each}
        {:else}
          <!-- Messenger 6 Reactions -->
          {#each [
            { type: 'heart', emo: '❤️' },
            { type: 'haha', emo: '😆' },
            { type: 'wow', emo: '😮' },
            { type: 'sad', emo: '😢' },
            { type: 'angry', emo: '😡' },
            { type: 'like', emo: '👍' }
          ] as r}
            <button 
              type="button" 
              class="w-10 h-10 rounded-full flex items-center justify-center hover:bg-gray-200 dark:hover:bg-gray-700 active:scale-130 transition-transform cursor-pointer"
              onclick={() => handleReact(r.type)}
              title="Thả cảm xúc"
            >
              <img src="./reacts/ic_react_{r.type}.png" alt={r.type} class="w-7 h-7 object-contain" />
            </button>
          {/each}
        {/if}
      </div>

      <!-- Message Content Preview -->
      <div class="px-5 py-3 border-b border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
        <span class="text-[11px] font-bold text-gray-400 uppercase tracking-wider block mb-1">
          {message.sender === 'me' ? 'Tin nhắn của bạn' : `Tin nhắn của ${conv.name}`} • {message.timestamp}
        </span>
        <p class="text-[14px] text-gray-800 dark:text-gray-200 line-clamp-2 italic">
          "{message.content || (message.type === 'voice' ? 'Tin nhắn thoại' : 'Tập tin đính kèm')}"
        </p>
      </div>

      <!-- Body: Edit Mode or Actions List -->
      {#if isEditing}
        <!-- In-line Edit Form -->
        <div class="p-4 space-y-3 overflow-y-auto">
          <div class="space-y-1">
            <span class="text-xs font-bold text-gray-500">Nội dung tin nhắn</span>
            <textarea 
              bind:value={editText} 
              rows="3"
              class="w-full p-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent text-[16px] outline-none focus:ring-2 focus:ring-[#0084ff]"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div class="space-y-1">
              <span class="text-xs font-bold text-gray-500">Giờ gửi</span>
              <input 
                type="text" 
                bind:value={editTime} 
                class="w-full p-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-transparent text-[16px] outline-none"
              />
            </div>

            <div class="space-y-1">
              <span class="text-xs font-bold text-gray-500">Trạng thái</span>
              <select 
                bind:value={editStatus}
                class="w-full p-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-[14px] outline-none font-medium"
              >
                <option value="seen">Đã xem (Seen)</option>
                <option value="delivered">Đã nhận (Delivered)</option>
                <option value="sent">Đã gửi (Sent)</option>
              </select>
            </div>
          </div>

          <div class="flex space-x-2 pt-2">
            <button 
              type="button" 
              class="flex-1 py-2 rounded-xl bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 font-bold text-xs cursor-pointer active:scale-95"
              onclick={() => { isEditing = false; }}
            >
              Hủy
            </button>
            <button 
              type="button" 
              class="flex-1 py-2 rounded-xl bg-[#0084ff] text-white font-bold text-xs cursor-pointer active:scale-95 shadow-xs"
              onclick={handleSaveEdit}
            >
              Lưu thay đổi
            </button>
          </div>
        </div>
      {:else}
        <!-- Action Options List -->
        <div class="p-2 space-y-1 overflow-y-auto text-[14.5px] font-medium">
          <!-- 1. Reply (Trả lời) -->
          <button 
            type="button" 
            class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-800/80 active:scale-98 transition-all cursor-pointer text-left"
            onclick={handleReply}
          >
            <div class="w-8 h-8 rounded-full bg-blue-50 dark:bg-blue-900/40 text-[#0084ff] flex items-center justify-center shrink-0">
              <Reply size={18} />
            </div>
            <div>
              <span class="block font-bold">Trả lời (Reply)</span>
              <span class="text-xs text-gray-400">Trích dẫn tin nhắn này vào câu trả lời tiếp theo</span>
            </div>
          </button>

          <!-- 2. Edit (Chỉnh sửa) -->
          <button 
            type="button" 
            class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-800/80 active:scale-98 transition-all cursor-pointer text-left"
            onclick={() => { isEditing = true; }}
          >
            <div class="w-8 h-8 rounded-full bg-amber-50 dark:bg-amber-900/40 text-amber-500 flex items-center justify-center shrink-0">
              <Edit3 size={18} />
            </div>
            <div>
              <span class="block font-bold">Chỉnh sửa nội dung & giờ gửi</span>
              <span class="text-xs text-gray-400">Sửa chữ, đổi giờ hoặc trạng thái đã xem</span>
            </div>
          </button>

          <!-- 3. Toggle Sender (Đổi người gửi Tôi <-> Bạn) -->
          <button 
            type="button" 
            class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-800/80 active:scale-98 transition-all cursor-pointer text-left"
            onclick={handleToggleSender}
          >
            <div class="w-8 h-8 rounded-full bg-emerald-50 dark:bg-emerald-900/40 text-emerald-500 flex items-center justify-center shrink-0">
              <Repeat size={18} />
            </div>
            <div>
              <span class="block font-bold">Đổi chiều người gửi</span>
              <span class="text-xs text-gray-400">Chuyển thành "{message.sender === 'me' ? conv.name : 'Tôi'}" gửi</span>
            </div>
          </button>

          <!-- 4. Copy text (Sao chép) -->
          <button 
            type="button" 
            class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-800/80 active:scale-98 transition-all cursor-pointer text-left"
            onclick={handleCopy}
          >
            <div class="w-8 h-8 rounded-full bg-purple-50 dark:bg-purple-900/40 text-purple-500 flex items-center justify-center shrink-0">
              {#if copied}
                <Check size={18} class="text-green-500" />
              {:else}
                <Copy size={18} />
              {/if}
            </div>
            <div>
              <span class="block font-bold">{copied ? 'Đã sao chép vào bộ nhớ tạm!' : 'Sao chép nội dung'}</span>
              <span class="text-xs text-gray-400">Copy tin nhắn văn bản</span>
            </div>
          </button>

          <!-- 5. Delete (Xóa tin nhắn) -->
          <button 
            type="button" 
            class="w-full flex items-center space-x-3 px-4 py-2.5 rounded-2xl hover:bg-red-50 dark:hover:bg-red-950/40 text-red-600 dark:text-red-400 active:scale-98 transition-all cursor-pointer text-left"
            onclick={handleDelete}
          >
            <div class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/40 text-red-500 flex items-center justify-center shrink-0">
              <Trash2 size={18} />
            </div>
            <div>
              <span class="block font-bold">Xóa tin nhắn này</span>
              <span class="text-xs opacity-70">Xóa vĩnh viễn khỏi đoạn hội thoại</span>
            </div>
          </button>
        </div>
      {/if}

      <!-- Bottom Close Button -->
      <div class="p-3 border-t border-gray-100 dark:border-gray-800">
        <button 
          type="button" 
          class="w-full py-2.5 rounded-2xl bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 font-bold text-[14px] cursor-pointer transition-colors active:scale-98"
          onclick={close}
        >
          Đóng
        </button>
      </div>
    </div>
  </div>
{/if}
