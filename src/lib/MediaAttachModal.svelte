<script>
  import { chatState, addMessage, getCurrentFormattedTime } from '../state.svelte.js';
  import { X, Image as ImageIcon, Mic, ThumbsUp, Calendar, PhoneCall, PhoneMissed } from '@lucide/svelte';

  let voiceDuration = $state('0:24');
  let dividerText = $state(getCurrentFormattedTime() + ' - HÔM NAY');
  let callDuration = $state('15 phút');

  function closeModal() {
    chatState.activeModal = null;
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
        closeModal();
      };
      reader.readAsDataURL(file);
    }
  }

  function insertVoice() {
    addMessage({
      type: 'voice',
      voiceDuration: voiceDuration.trim() || '0:15',
      sender: chatState.activeSender
    });
    closeModal();
  }

  function insertLike() {
    addMessage({
      type: 'like',
      content: '👍',
      sender: chatState.activeSender
    });
    closeModal();
  }

  function insertDivider() {
    addMessage({
      type: 'timestamp_divider',
      content: dividerText.trim() || 'HÔM NAY',
      sender: 'me'
    });
    closeModal();
  }

  function insertCallBanner(type, missed = false) {
    addMessage({
      type: 'call_event',
      sender: 'me',
      callInfo: {
        type,
        missed,
        duration: callDuration.trim() || '5 phút'
      }
    });
    closeModal();
  }
</script>

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
      <h2 class="text-[16px] font-bold">Thêm tin nhắn đặc biệt</h2>
      <button 
        type="button" 
        class="w-7 h-7 rounded-full flex items-center justify-center bg-gray-100 dark:bg-gray-800 text-gray-500 hover:text-gray-800 dark:hover:text-white active:scale-90 transition-transform cursor-pointer"
        onclick={closeModal}
      >
        <X size={16} />
      </button>
    </div>

    <!-- Modal Body -->
    <div class="p-5 overflow-y-auto space-y-4 text-[13px]">
      <!-- 1. Attach Image -->
      <label class="flex items-center space-x-3 p-3 rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 hover:border-[#0084ff] cursor-pointer transition-all active:scale-98">
        <div class="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-[#0084ff] flex items-center justify-center shrink-0">
          <ImageIcon size={22} />
        </div>
        <div class="flex-1">
          <span class="font-bold block text-[14px]">Gửi ảnh chụp</span>
          <span class="text-xs text-gray-400">Tải ảnh từ thư viện thiết bị</span>
        </div>
        <input type="file" accept="image/*" onchange={handleImageUpload} class="hidden" />
      </label>

      <!-- 2. Voice Note -->
      <div class="p-3 rounded-2xl border border-gray-200 dark:border-gray-800 space-y-2">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-purple-50 dark:bg-purple-950/40 text-purple-500 flex items-center justify-center shrink-0">
            <Mic size={18} />
          </div>
          <span class="font-bold text-[14px]">Tin nhắn ghi âm (Voice Note)</span>
        </div>
        <div class="flex items-center space-x-2">
          <input 
            type="text" 
            bind:value={voiceDuration} 
            placeholder="Thời lượng (VD: 0:24)" 
            class="flex-1 px-3 py-1.5 rounded-xl border outline-none font-medium text-xs"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
          <button 
            type="button" 
            class="px-3.5 py-1.5 rounded-xl bg-[#0084ff] text-white font-bold text-xs cursor-pointer active:scale-95"
            onclick={insertVoice}
          >
            Chèn
          </button>
        </div>
      </div>

      <!-- 3. Timestamp Divider -->
      <div class="p-3 rounded-2xl border border-gray-200 dark:border-gray-800 space-y-2">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-500 flex items-center justify-center shrink-0">
            <Calendar size={18} />
          </div>
          <span class="font-bold text-[14px]">Mốc thời gian (Divider)</span>
        </div>
        <div class="flex items-center space-x-2">
          <input 
            type="text" 
            bind:value={dividerText} 
            placeholder="VD: 14:20 - HÔM NAY" 
            class="flex-1 px-3 py-1.5 rounded-xl border outline-none font-medium text-xs"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
          <button 
            type="button" 
            class="px-3.5 py-1.5 rounded-xl bg-[#0084ff] text-white font-bold text-xs cursor-pointer active:scale-95"
            onclick={insertDivider}
          >
            Chèn
          </button>
        </div>
      </div>

      <!-- 4. Call Banners -->
      <div class="p-3 rounded-2xl border border-gray-200 dark:border-gray-800 space-y-2">
        <div class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-500 flex items-center justify-center shrink-0">
            <PhoneCall size={18} />
          </div>
          <span class="font-bold text-[14px]">Thông báo cuộc gọi</span>
        </div>
        <div class="flex items-center space-x-2 pb-1">
          <input 
            type="text" 
            bind:value={callDuration} 
            placeholder="Thời lượng (VD: 15 phút)" 
            class="w-full px-3 py-1.5 rounded-xl border outline-none font-medium text-xs"
            class:bg-[#2a2a2a]={chatState.isDarkMode}
            class:border-[#3a3b3c]={chatState.isDarkMode}
            class:bg-gray-50={!chatState.isDarkMode}
            class:border-gray-200={!chatState.isDarkMode}
          />
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs">
          <button 
            type="button" 
            class="py-1.5 px-2 rounded-xl bg-gray-100 dark:bg-gray-800 font-semibold cursor-pointer active:scale-95 transition-all text-center"
            onclick={() => insertCallBanner('audio', false)}
          >
            Đã gọi thoại
          </button>
          <button 
            type="button" 
            class="py-1.5 px-2 rounded-xl bg-gray-100 dark:bg-gray-800 font-semibold cursor-pointer active:scale-95 transition-all text-center"
            onclick={() => insertCallBanner('video', false)}
          >
            Đã gọi video
          </button>
          <button 
            type="button" 
            class="col-span-2 py-1.5 px-2 rounded-xl bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400 font-semibold cursor-pointer active:scale-95 transition-all text-center"
            onclick={() => insertCallBanner('audio', true)}
          >
            Cuộc gọi nhỡ
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

