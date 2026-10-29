<script>
  import { 
    chatState, 
    getActiveZaloConversation, 
    addZaloMessage, 
    toggleZaloHeart 
  } from '../../state.svelte.js';
  import ZaloIcon from '../ZaloIcon.svelte';
  import { Phone, MessageSquare, Send, CheckCheck, BadgeCheck, X, Reply } from '@lucide/svelte';

  const conv = $derived(getActiveZaloConversation());
  let inputText = $state('');
  let fileInputRef;
  let chatBodyRef = $state();

  function scrollToBottom() {
    if (chatBodyRef) {
      chatBodyRef.scrollTop = chatBodyRef.scrollHeight;
    }
  }

  $effect(() => {
    conv?.messages?.length;
    setTimeout(scrollToBottom, 60);
  });

  function resetViewport() {
    setTimeout(() => {
      window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
    }, 50);
  }

  function handleBack() {
    chatState.zaloScreen = 'zalo_chats_list';
  }

  function handleSend() {
    if (!inputText.trim()) return;
    addZaloMessage({
      type: 'text',
      content: inputText.trim(),
      sender: chatState.activeSender
    });
    inputText = '';
    resetViewport();
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

  function handleImageUpload(e) {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        addZaloMessage({
          type: 'image',
          imageUri: reader.result,
          content: 'Hình ảnh',
          sender: chatState.activeSender
        });
        resetViewport();
      };
      reader.readAsDataURL(file);
    }
    e.target.value = '';
  }

  function sendSampleContactCard() {
    addZaloMessage({
      type: 'contact_card',
      cardName: 'Thu Hướng',
      cardAvatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces',
      sender: chatState.activeSender,
      hasHeart: true
    });
  }

  function sendVoiceNote() {
    addZaloMessage({
      type: 'voice',
      voiceDuration: '0:14',
      sender: chatState.activeSender
    });
    resetViewport();
  }

  function startCall(type) {
    chatState.callType = type;
    chatState.callStatus = 'incoming';
    chatState.callTimer = 0;
    chatState.activeModal = 'call';
  }

  function openActionModal(msg) {
    chatState.selectedActionMessage = msg;
    chatState.activeModal = 'message_action';
  }

  function cancelReply() {
    chatState.replyingToMessage = null;
  }
</script>

<div class="w-full h-full flex flex-col bg-[#eef0f4] select-none transition-colors duration-200">
  <!-- Hidden file input for image attachment -->
  <input 
    type="file" 
    accept="image/*" 
    bind:this={fileInputRef} 
    onchange={handleImageUpload} 
    class="hidden" 
  />

  <!-- Top Blue Header (1:1 from sample image 2) -->
  <div class="bg-[#0068ff] text-white px-3 py-2.5 flex items-center justify-between shrink-0 shadow-xs z-20">
    <!-- Left: Back Button & Name -->
    <div class="flex items-center space-x-2 min-w-0 flex-1">
      <button 
        type="button" 
        class="p-1 -ml-1 text-white active:scale-90 transition-transform cursor-pointer"
        onclick={handleBack}
        title="Quay lại danh sách chat Zalo"
      >
        <ZaloIcon name="back" size={24} class="text-white" />
      </button>

      <button 
        type="button"
        class="flex flex-col min-w-0 text-left cursor-pointer active:opacity-80"
        onclick={() => { chatState.activeModal = 'profile'; }}
        title="Nhấn để đổi tên, ảnh, tích xanh và trạng thái"
      >
        <div class="flex items-center space-x-1.5">
          <h2 class="text-[17px] font-semibold text-white leading-tight truncate">
            {conv.name}
          </h2>
          {#if conv.hasVerifiedBadge}
            <BadgeCheck size={16} class="text-[#0068ff] shrink-0 fill-white text-[#0068ff]" />
          {/if}
        </div>
        {#if conv.statusText}
          <span class="text-[11.5px] text-white/80 leading-tight truncate">
            {conv.statusText}
          </span>
        {/if}
      </button>
    </div>

    <!-- Right Actions: Voice Call, Video Call, 3-Line Menu -->
    <div class="flex items-center space-x-4 pr-1 text-white shrink-0">
      <button 
        type="button" 
        class="active:scale-90 transition-transform cursor-pointer p-0.5"
        onclick={() => startCall('audio')}
        title="Gọi thoại Zalo"
      >
        <ZaloIcon name="voice_call" size={22} class="text-white" />
      </button>

      <button 
        type="button" 
        class="active:scale-90 transition-transform cursor-pointer p-0.5"
        onclick={() => startCall('video')}
        title="Gọi video Zalo"
      >
        <ZaloIcon name="video_call" size={22} class="text-white" />
      </button>

      <button 
        type="button" 
        class="active:scale-90 transition-transform cursor-pointer p-0.5"
        onclick={() => { chatState.activeModal = 'profile'; }}
        title="Tùy chọn đoạn chat Zalo"
      >
        <ZaloIcon name="menu_3line" size={22} class="text-white" />
      </button>
    </div>
  </div>

  <!-- Messages Scroll Area (1:1 identical to sample image 2) -->
  <div 
    bind:this={chatBodyRef}
    class="flex-1 overflow-y-auto px-3.5 py-3 space-y-3 ios-scroll no-scrollbar bg-[#eef0f4]"
  >
    <!-- Empty State Greeting if no messages -->
    {#if conv.messages.length === 0}
      <div class="text-center py-8 select-none">
        <img 
          src={conv.avatar} 
          alt={conv.name} 
          class="w-16 h-16 rounded-full mx-auto object-cover shadow-sm mb-2 border border-black/5"
        />
        <div class="flex items-center justify-center space-x-1">
          <h3 class="font-bold text-[17px] text-gray-800 leading-tight">
            {conv.name}
          </h3>
          {#if conv.hasVerifiedBadge}
            <BadgeCheck size={16} class="text-[#0068ff] shrink-0 fill-[#0068ff] text-white" />
          {/if}
        </div>
        <p class="text-xs text-gray-500 mt-1">
          {conv.statusText || 'Bắt đầu cuộc trò chuyện Zalo mới'}
        </p>
      </div>
    {/if}

    {#each conv.messages as msg, i (msg.id)}
      {@const isThem = msg.sender === 'them'}
      <div 
        class="flex flex-col select-none"
        class:items-end={!isThem}
        class:items-start={isThem}
      >
        <div class="flex items-end max-w-[82%] space-x-1.5 group relative">
          <!-- Them Avatar on the left -->
          {#if isThem}
            <div class="w-7 h-7 shrink-0 -mb-1">
              <img 
                src={conv.avatar} 
                alt={conv.name} 
                class="w-7 h-7 rounded-full object-cover border border-black/5 shadow-2xs"
              />
            </div>
          {/if}

          <!-- Message Container (Tap to open full actions) -->
          <div 
            class="relative flex flex-col cursor-pointer active:scale-[0.98] transition-transform" 
            class:items-end={!isThem} 
            class:items-start={isThem}
            onclick={() => openActionModal(msg)}
            role="button"
            tabindex="0"
            onkeydown={(e) => e.key === 'Enter' && openActionModal(msg)}
            title="Nhấn để tương tác: Thả tim, Trả lời, Sửa, Đổi người gửi, Xóa"
          >
            {#if msg.type === 'text'}
              <!-- Standard Text Bubble -->
              <div 
                class="px-3.5 py-2 rounded-2xl text-[15px] text-black leading-relaxed break-words shadow-2xs tracking-tight {isThem ? 'bg-white' : 'bg-[#d5f1ff]'}"
              >
                <!-- Quote text inside text bubble if any -->
                {#if msg.quoteText}
                  <div class="mb-1.5 pl-2 border-l-3 border-[#0068ff] text-left">
                    <span class="block text-[11px] font-bold text-gray-700">{msg.quoteSender || 'Người gửi'}</span>
                    <p class="text-[11px] text-gray-500 truncate">{msg.quoteText}</p>
                  </div>
                {/if}
                {msg.content}
              </div>

            {:else if msg.type === 'contact_card'}
              <!-- Zalo Contact Card (1:1 from sample image 2) -->
              <div class="w-[240px] rounded-2xl overflow-hidden shadow-2xs border border-blue-200">
                <!-- Top Blue Header -->
                <div class="bg-gradient-to-r from-[#0068ff] to-[#008fe5] p-3 flex items-center space-x-2.5 text-white">
                  <img 
                    src={msg.cardAvatar || conv.avatar} 
                    alt="Contact" 
                    class="w-10 h-10 rounded-full object-cover border-2 border-white/40 shadow-xs"
                  />
                  <span class="font-bold text-[15px] truncate text-white">{msg.cardName || 'Danh thiếp'}</span>
                </div>
                <!-- Bottom Action Split -->
                <div class="bg-white flex items-center divide-x divide-gray-100 text-[#0068ff] font-semibold text-[13.5px]">
                  <button type="button" class="flex-1 py-2 text-center hover:bg-gray-50 active:bg-gray-100 cursor-pointer">
                    Gọi điện
                  </button>
                  <button type="button" class="flex-1 py-2 text-center hover:bg-gray-50 active:bg-gray-100 cursor-pointer">
                    Nhắn tin
                  </button>
                </div>
              </div>

            {:else if msg.type === 'reply_quote'}
              <!-- Zalo Reply Quote Bubble (1:1 from sample image 2) -->
              <div class="p-3 rounded-2xl bg-white shadow-2xs max-w-[240px] space-y-1.5 border border-gray-100">
                <!-- Quoted Block with blue vertical bar -->
                <div class="pl-2.5 border-l-3 border-[#0068ff] text-left">
                  <span class="block text-[13px] font-bold text-gray-800">{msg.quoteSender || 'Người gửi'}</span>
                  <p class="text-[12px] text-gray-500 truncate">{msg.quoteText || 'Nội dung trích dẫn'}</p>
                </div>
                <!-- Main reply text -->
                <p class="text-[15px] font-normal text-black pt-0.5 leading-snug">{msg.content}</p>
              </div>

            {:else if msg.type === 'image'}
              <!-- Image Attachment -->
              <div class="rounded-2xl overflow-hidden shadow-2xs max-w-[220px] border border-gray-200">
                <img src={msg.imageUri || msg.content} alt="Ảnh Zalo" class="w-full h-auto object-cover max-h-[280px]" />
              </div>

            {:else if msg.type === 'voice'}
              <!-- Voice Note Waveform -->
              <div 
                class="px-3.5 py-2 rounded-2xl flex items-center space-x-2 min-w-[150px] shadow-2xs"
                class:bg-white={isThem}
                class:bg-[#d5f1ff]={!isThem}
              >
                <div class="w-6 h-6 rounded-full bg-[#0068ff] text-white flex items-center justify-center text-xs">▶</div>
                <div class="flex-1 flex items-center space-x-0.5 h-4">
                  {#each [4, 10, 16, 8, 14, 18, 6, 12, 10, 14] as h}
                    <div class="w-[2px] bg-[#0068ff] rounded-full" style="height: {h}px;"></div>
                  {/each}
                </div>
                <span class="text-xs text-gray-500 font-medium">{msg.voiceDuration || '0:14'}</span>
              </div>
            {/if}

            <!-- Attached Heart Reaction Pill (White circle with heart) -->
            {#if msg.hasHeart}
              <button 
                type="button" 
                class="absolute -bottom-2.5 {isThem ? 'right-0' : 'left-0'} w-6 h-6 bg-white rounded-full shadow-md border border-gray-200 flex items-center justify-center text-red-500 cursor-pointer active:scale-125 transition-transform"
                onclick={(e) => { e.stopPropagation(); toggleZaloHeart(msg.id); }}
                title="Bỏ thích"
              >
                <span class="text-[12px] leading-none">❤️</span>
              </button>
            {:else}
              <button 
                type="button" 
                class="opacity-60 hover:opacity-100 absolute -bottom-2 {isThem ? 'right-0' : 'left-0'} w-5 h-5 bg-white/90 rounded-full flex items-center justify-center text-gray-400 hover:text-red-500 transition-all cursor-pointer shadow-xs border border-gray-100"
                onclick={(e) => { e.stopPropagation(); toggleZaloHeart(msg.id); }}
                title="Thả tim Zalo"
              >
                <span class="text-[10px]">🤍</span>
              </button>
            {/if}

            <!-- Timestamp underneath (Zalo Style) -->
            <span class="text-[11px] text-gray-400 mt-0.5 px-1 font-normal">
              {msg.timestamp}
            </span>

            <!-- Status Pill for Sender (e.g. '✓✓ Đã nhận') -->
            {#if !isThem && i === conv.messages.length - 1}
              <div class="mt-0.5 px-2 py-0.5 bg-[#d8e0ea] rounded-full flex items-center space-x-1 text-[10px] text-gray-600 font-medium shadow-2xs">
                <CheckCheck size={12} strokeWidth={2.5} class="text-gray-500" />
                <span>{msg.status === 'seen' ? 'Đã xem' : 'Đã nhận'}</span>
              </div>
            {/if}
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Bottom Input Bar (1:1 from sample image 2) -->
  <div class="w-full flex flex-col bg-white border-t border-gray-200 shrink-0 z-20">
    <!-- Active Quote Reply Preview Banner for Zalo -->
    {#if chatState.replyingToMessage}
      <div class="flex items-center justify-between px-3.5 py-1.5 bg-gray-50 border-b border-gray-200 text-[12px] animate-in fade-in duration-150">
        <div class="flex items-center space-x-2 min-w-0 flex-1 border-l-3 border-[#0068ff] pl-2">
          <Reply size={14} class="text-[#0068ff] shrink-0" />
          <div class="truncate">
            <span class="font-bold text-gray-800">
              Đang trả lời {chatState.replyingToMessage.sender === 'me' ? 'chính bạn' : conv.name}:
            </span>
            <span class="text-gray-500 italic ml-1 truncate">
              {chatState.replyingToMessage.content || 'Tin nhắn thoại / Hình ảnh'}
            </span>
          </div>
        </div>
        <button 
          type="button" 
          class="w-5 h-5 rounded-full flex items-center justify-center text-gray-400 hover:text-gray-600 cursor-pointer active:scale-90 ml-2 shrink-0"
          onclick={cancelReply}
          title="Hủy trả lời"
        >
          <X size={14} />
        </button>
      </div>
    {/if}

    <!-- Quick Switcher Bar (Hidden in snapshot mode) -->
    {#if !chatState.isSnapshotMode}
      <div class="flex items-center justify-between px-3.5 py-1 text-[11px] font-semibold bg-gray-50 border-b border-gray-100">
        <div class="flex items-center space-x-2">
          <span class="text-gray-500">Người gửi tiếp theo:</span>
          <button 
            type="button" 
            class="px-2 py-0.5 rounded-full text-white font-bold transition-transform active:scale-95 cursor-pointer shadow-2xs"
            class:bg-[#0068ff]={chatState.activeSender === 'me'}
            class:bg-gray-600={chatState.activeSender === 'them'}
            onclick={toggleSender}
          >
            {chatState.activeSender === 'me' ? 'Tôi gửi ➔' : `◀ ${conv.name} gửi`}
          </button>
        </div>

        <div class="flex items-center space-x-2">
          <button 
            type="button" 
            class="text-[#0068ff] font-medium hover:underline text-[11px] cursor-pointer"
            onclick={sendSampleContactCard}
          >
            + Chèn Danh thiếp
          </button>
        </div>
      </div>
    {/if}

    <!-- Zalo Input Toolbar -->
    <div class="flex items-center px-3 py-2 space-x-2">
      <!-- Left: Zalo Smile Face Sticker Icon -->
      <button 
        type="button" 
        class="text-gray-600 active:scale-90 transition-transform cursor-pointer p-0.5"
        title="Mở nhãn dán Zalo"
      >
        <ZaloIcon name="open_icon" size={26} class="text-gray-700" />
      </button>

      <!-- Center: Text Input Field (16px to stop iOS auto-zoom) -->
      <input 
        type="text" 
        placeholder="Tin nhắn"
        bind:value={inputText}
        onkeydown={handleKeyDown}
        onblur={resetViewport}
        class="flex-1 bg-transparent text-[16px] outline-none text-black placeholder-gray-400 font-normal py-1"
      />

      <!-- Right Action Icons: 3 Dots, Mic, Image, or Send -->
      {#if inputText.trim().length > 0}
        <button 
          type="button" 
          class="w-8 h-8 rounded-full bg-[#0068ff] text-white flex items-center justify-center active:scale-90 transition-transform cursor-pointer shadow-xs"
          onclick={handleSend}
          title="Gửi tin nhắn Zalo"
        >
          <Send size={16} strokeWidth={2.5} class="ml-0.5" />
        </button>
      {:else}
        <!-- 3 dots menu -->
        <button 
          type="button" 
          class="text-gray-600 active:scale-90 transition-transform cursor-pointer p-1"
          onclick={sendSampleContactCard}
          title="Tùy chọn mở rộng Zalo"
        >
          <ZaloIcon name="menu" size={20} class="text-gray-600" />
        </button>

        <!-- Mic voice note -->
        <button 
          type="button" 
          class="text-gray-600 active:scale-90 transition-transform cursor-pointer p-1"
          onclick={sendVoiceNote}
          title="Gửi ghi âm Zalo"
        >
          <ZaloIcon name="mic" size={20} class="text-gray-600" />
        </button>

        <!-- Gallery Image (orange photo icon) -->
        <button 
          type="button" 
          class="text-[#ff9800] active:scale-90 transition-transform cursor-pointer p-1"
          onclick={() => fileInputRef.click()}
          title="Gửi hình ảnh Zalo"
        >
          <ZaloIcon name="open_image" size={22} class="text-[#ff9800]" />
        </button>
      {/if}
    </div>
  </div>
</div>
