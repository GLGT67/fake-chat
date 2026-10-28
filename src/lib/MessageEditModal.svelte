<script>
  import { chatState, updateMessage, deleteMessage, insertMessageAt } from '../state.svelte.js';
  import { X, Trash2, ArrowUp, ArrowDown, Clock } from '@lucide/svelte';

  const editingMsg = $derived(chatState.messages.find(m => m.id === chatState.editingMessageId));

  function closeModal() {
    chatState.activeModal = null;
    chatState.editingMessageId = null;
  }

  function handleSave() {
    closeModal();
  }

  function handleDelete() {
    if (chatState.editingMessageId) {
      deleteMessage(chatState.editingMessageId);
      closeModal();
    }
  }

  function handleInsertBefore() {
    if (chatState.editingMessageId) {
      insertMessageAt(chatState.editingMessageId, {
        content: "Tin nhắn mới",
        sender: editingMsg?.sender || "me"
      }, "before");
      closeModal();
    }
  }

  function handleInsertAfter() {
    if (chatState.editingMessageId) {
      insertMessageAt(chatState.editingMessageId, {
        content: "Tin nhắn mới",
        sender: editingMsg?.sender || "me"
      }, "after");
      closeModal();
    }
  }
</script>

{#if editingMsg}
  <div class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-black/60 backdrop-blur-xs select-none animate-in fade-in duration-150">
    <div 
      class="w-full max-w-sm rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] border transition-colors"
      class:bg-[#1e1e1e]={chatState.isDarkMode}
      class:border-[#333]={chatState.isDarkMode}
      class:text-white={chatState.isDarkMode}
      class:bg-white={!chatState.isDarkMode}
      class:border-gray-200={!chatState.isDarkMode}
      class:text-gray-900={!chatState.isDarkMode}
    >
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-5 py-3.5 border-b shrink-0"
           class:border-[#2e2e2e]={chatState.isDarkMode}
           class:border-gray-100={!chatState.isDarkMode}
      >
        <h2 class="text-[16px] font-bold">Chỉnh sửa tin nhắn</h2>
        <button 
          type="button" 
          class="w-7 h-7 rounded-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-500 hover:text-gray-800 dark:hover:text-white active:scale-90 transition-transform cursor-pointer"
          onclick={closeModal}
        >
          <X size={16} />
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-5 overflow-y-auto space-y-4 text-[14px]">
        <!-- Sender Switch -->
        <div class="space-y-1.5">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Người gửi</span>
          <div class="grid grid-cols-2 gap-2">
            <button 
              type="button" 
              class="py-2 px-3 rounded-xl border font-semibold text-center cursor-pointer transition-all active:scale-95"
              class:bg-[#0084ff]={editingMsg.sender === 'me'}
              class:text-white={editingMsg.sender === 'me'}
              class:border-[#0084ff]={editingMsg.sender === 'me'}
              class:border-gray-300={editingMsg.sender !== 'me' && !chatState.isDarkMode}
              class:border-[#3a3b3c]={editingMsg.sender !== 'me' && chatState.isDarkMode}
              onclick={() => updateMessage(editingMsg.id, { sender: 'me' })}
            >
              Tôi gửi (Bên phải)
            </button>

            <button 
              type="button" 
              class="py-2 px-3 rounded-xl border font-semibold text-center cursor-pointer transition-all active:scale-95"
              class:bg-[#0084ff]={editingMsg.sender === 'them'}
              class:text-white={editingMsg.sender === 'them'}
              class:border-[#0084ff]={editingMsg.sender === 'them'}
              class:border-gray-300={editingMsg.sender !== 'them' && !chatState.isDarkMode}
              class:border-[#3a3b3c]={editingMsg.sender !== 'them' && chatState.isDarkMode}
              onclick={() => updateMessage(editingMsg.id, { sender: 'them' })}
            >
              {chatState.partnerName} gửi
            </button>
          </div>
        </div>

        <!-- Content Input -->
        {#if editingMsg.type === 'text' || editingMsg.type === 'timestamp_divider'}
          <div class="space-y-1.5">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Nội dung văn bản</span>
            <textarea 
              rows="3"
              value={editingMsg.content}
              oninput={(e) => updateMessage(editingMsg.id, { content: e.target.value })}
              class="w-full px-3.5 py-2 rounded-xl border outline-none font-normal text-[15px] focus:ring-2 focus:ring-[#0084ff]/40 transition-all resize-none"
              class:bg-[#2a2a2a]={chatState.isDarkMode}
              class:border-[#3a3b3c]={chatState.isDarkMode}
              class:bg-gray-50={!chatState.isDarkMode}
              class:border-gray-200={!chatState.isDarkMode}
            ></textarea>
          </div>
        {:else if editingMsg.type === 'voice'}
          <div class="space-y-1.5">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Thời lượng ghi âm</span>
            <input 
              type="text" 
              value={editingMsg.voiceDuration || '0:15'}
              oninput={(e) => updateMessage(editingMsg.id, { voiceDuration: e.target.value })}
              placeholder="VD: 0:45"
              class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium"
              class:bg-[#2a2a2a]={chatState.isDarkMode}
              class:border-[#3a3b3c]={chatState.isDarkMode}
              class:bg-gray-50={!chatState.isDarkMode}
              class:border-gray-200={!chatState.isDarkMode}
            />
          </div>
        {/if}

        <!-- Timestamp -->
        <div class="space-y-1.5">
          <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center space-x-1">
            <Clock size={13} />
            <span>Giờ gửi</span>
          </span>
          <input 
            type="text" 
            value={editingMsg.timestamp}
            oninput={(e) => updateMessage(editingMsg.id, { timestamp: e.target.value })}
            placeholder="VD: 09:41"
            class="w-full px-3.5 py-2 rounded-xl border outline-none font-medium"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>

        <!-- Delivery Status (for "me" messages) -->
        {#if editingMsg.sender === 'me'}
          <div class="space-y-1.5">
            <span class="block text-xs font-bold text-gray-400 uppercase tracking-wider">Trạng thái tin nhắn</span>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <button 
                type="button" 
                class="py-2 px-2.5 rounded-xl border font-medium cursor-pointer transition-all"
                class:bg-[#0084ff]={editingMsg.status === 'seen'}
                class:text-white={editingMsg.status === 'seen'}
                class:border-[#0084ff]={editingMsg.status === 'seen'}
                class:border-gray-200={editingMsg.status !== 'seen' && !chatState.isDarkMode}
                class:border-[#3a3b3c]={editingMsg.status !== 'seen' && chatState.isDarkMode}
                onclick={() => updateMessage(editingMsg.id, { status: 'seen' })}
              >
                Đã xem (Avatar)
              </button>

              <button 
                type="button" 
                class="py-2 px-2.5 rounded-xl border font-medium cursor-pointer transition-all"
                class:bg-[#0084ff]={editingMsg.status === 'delivered'}
                class:text-white={editingMsg.status === 'delivered'}
                class:border-[#0084ff]={editingMsg.status === 'delivered'}
                class:border-gray-200={editingMsg.status !== 'delivered' && !chatState.isDarkMode}
                class:border-[#3a3b3c]={editingMsg.status !== 'delivered' && chatState.isDarkMode}
                onclick={() => updateMessage(editingMsg.id, { status: 'delivered' })}
              >
                Đã nhận (Tích đầy)
              </button>

              <button 
                type="button" 
                class="py-2 px-2.5 rounded-xl border font-medium cursor-pointer transition-all"
                class:bg-[#0084ff]={editingMsg.status === 'sent'}
                class:text-white={editingMsg.status === 'sent'}
                class:border-[#0084ff]={editingMsg.status === 'sent'}
                class:border-gray-200={editingMsg.status !== 'sent' && !chatState.isDarkMode}
                class:border-[#3a3b3c]={editingMsg.status !== 'sent' && chatState.isDarkMode}
                onclick={() => updateMessage(editingMsg.id, { status: 'sent' })}
              >
                Đã gửi (Tích rỗng)
              </button>

              <button 
                type="button" 
                class="py-2 px-2.5 rounded-xl border font-medium cursor-pointer transition-all"
                class:bg-[#0084ff]={editingMsg.status === 'sending'}
                class:text-white={editingMsg.status === 'sending'}
                class:border-[#0084ff]={editingMsg.status === 'sending'}
                class:border-gray-200={editingMsg.status !== 'sending' && !chatState.isDarkMode}
                class:border-[#3a3b3c]={editingMsg.status !== 'sending' && chatState.isDarkMode}
                onclick={() => updateMessage(editingMsg.id, { status: 'sending' })}
              >
                Đang gửi (Vòng tròn)
              </button>
            </div>
          </div>
        {/if}

        <!-- Insert actions -->
        <div class="pt-2 border-t border-gray-100 dark:border-gray-800 grid grid-cols-2 gap-2 text-xs font-semibold">
          <button 
            type="button" 
            class="flex items-center justify-center space-x-1 py-2 px-3 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer active:scale-95 transition-all"
            onclick={handleInsertBefore}
          >
            <ArrowUp size={14} />
            <span>Chèn lên trên</span>
          </button>

          <button 
            type="button" 
            class="flex items-center justify-center space-x-1 py-2 px-3 rounded-xl border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer active:scale-95 transition-all"
            onclick={handleInsertAfter}
          >
            <ArrowDown size={14} />
            <span>Chèn xuống dưới</span>
          </button>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t flex items-center justify-between space-x-3 shrink-0"
           class:border-[#2e2e2e]={chatState.isDarkMode}
           class:border-gray-100={!chatState.isDarkMode}
      >
        <button 
          type="button" 
          class="flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:hover:bg-red-900/60 text-red-600 dark:text-red-400 font-semibold text-xs active:scale-95 transition-all cursor-pointer"
          onclick={handleDelete}
        >
          <Trash2 size={15} />
          <span>Xóa tin này</span>
        </button>

        <button 
          type="button" 
          class="flex-1 py-2.5 rounded-xl bg-[#0084ff] hover:bg-[#0073e6] text-white font-bold shadow-md active:scale-98 transition-all cursor-pointer"
          onclick={handleSave}
        >
          Hoàn tất
        </button>
      </div>
    </div>
  </div>
{/if}
