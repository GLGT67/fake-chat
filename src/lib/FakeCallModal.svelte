<script>
  import { chatState, addMessage } from '../state.svelte.js';
  import { Phone, PhoneOff, Mic, MicOff, Volume2, Video, VideoOff } from '@lucide/svelte';

  let callSeconds = $state(0);
  let timerInterval = null;
  let isMuted = $state(false);
  let isSpeaker = $state(true);
  let isVideoOn = $state(chatState.callType === 'video');

  function startTimer() {
    callSeconds = 0;
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
      callSeconds++;
    }, 1000);
  }

  function formatDuration(sec) {
    const mins = Math.floor(sec / 60);
    const s = sec % 60;
    return `${String(mins).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  function acceptCall() {
    chatState.callStatus = 'connected';
    startTimer();
  }

  function declineCall() {
    if (timerInterval) clearInterval(timerInterval);
    addMessage({
      type: 'call_event',
      sender: 'them',
      callInfo: {
        type: chatState.callType,
        missed: true,
        duration: '0:00'
      }
    });
    chatState.activeModal = null;
  }

  function endCall() {
    if (timerInterval) clearInterval(timerInterval);
    const durationStr = callSeconds > 60 
      ? `${Math.floor(callSeconds / 60)} phút ${callSeconds % 60}s` 
      : `${callSeconds} giây`;

    addMessage({
      type: 'call_event',
      sender: 'them',
      callInfo: {
        type: chatState.callType,
        missed: false,
        duration: durationStr
      }
    });
    chatState.activeModal = null;
  }
</script>

<div class="absolute inset-0 z-40 flex flex-col justify-between items-center text-white p-6 overflow-hidden select-none animate-in fade-in duration-200">
  <!-- Blurred background image -->
  <div 
    class="absolute inset-0 bg-cover bg-center filter blur-2xl scale-125 opacity-40 -z-10"
    style="background-image: url('{chatState.partnerAvatar}');"
  ></div>
  <div class="absolute inset-0 bg-black/60 -z-10"></div>

  <!-- Top Info -->
  <div class="flex flex-col items-center mt-12 space-y-2 text-center">
    <!-- Big Avatar -->
    <div class="relative">
      <img 
        src={chatState.partnerAvatar} 
        alt={chatState.partnerName} 
        class="w-24 h-24 rounded-full object-cover shadow-2xl border-2 border-white/20 {chatState.callStatus === 'incoming' ? 'animate-pulse' : ''}" 
      />
    </div>

    <h2 class="text-[24px] font-bold tracking-tight">{chatState.partnerName}</h2>

    {#if chatState.callStatus === 'incoming'}
      <span class="text-[14px] text-white/80 font-medium">Messenger {chatState.callType === 'video' ? 'Cuộc gọi video...' : 'Cuộc gọi thoại...'}</span>
    {:else}
      <span class="text-[15px] font-semibold tracking-wider text-emerald-400 font-mono">{formatDuration(callSeconds)}</span>
    {/if}
  </div>

  <!-- Bottom Actions -->
  {#if chatState.callStatus === 'incoming'}
    <!-- Incoming Call Buttons (Red & Green) -->
    <div class="w-full flex items-center justify-around px-8 mb-10">
      <!-- Decline -->
      <div class="flex flex-col items-center space-y-2">
        <button 
          type="button" 
          class="w-16 h-16 rounded-full bg-red-600 hover:bg-red-500 text-white flex items-center justify-center shadow-xl active:scale-90 transition-transform cursor-pointer"
          onclick={declineCall}
        >
          <PhoneOff size={28} />
        </button>
        <span class="text-xs font-semibold text-white/90">Từ chối</span>
      </div>

      <!-- Accept -->
      <div class="flex flex-col items-center space-y-2">
        <button 
          type="button" 
          class="w-16 h-16 rounded-full bg-emerald-500 hover:bg-emerald-400 text-white flex items-center justify-center shadow-xl active:scale-90 transition-transform cursor-pointer animate-bounce"
          onclick={acceptCall}
        >
          <Phone size={28} />
        </button>
        <span class="text-xs font-semibold text-white/90">Trả lời</span>
      </div>
    </div>
  {:else}
    <!-- Connected In-Call Action Grid -->
    <div class="w-full flex flex-col items-center space-y-6 mb-8">
      <div class="grid grid-cols-3 gap-6">
        <!-- Mute -->
        <button 
          type="button" 
          class="w-14 h-14 rounded-full flex items-center justify-center cursor-pointer transition-all active:scale-90 {isMuted ? 'bg-white text-black' : 'bg-white/20 text-white'}"
          onclick={() => { isMuted = !isMuted; }}
        >
          {#if isMuted}
            <MicOff size={24} />
          {:else}
            <Mic size={24} />
          {/if}
        </button>

        <!-- Speaker -->
        <button 
          type="button" 
          class="w-14 h-14 rounded-full flex items-center justify-center cursor-pointer transition-all active:scale-90 {isSpeaker ? 'bg-white text-black' : 'bg-white/20 text-white'}"
          onclick={() => { isSpeaker = !isSpeaker; }}
        >
          <Volume2 size={24} />
        </button>

        <!-- Video Toggle -->
        <button 
          type="button" 
          class="w-14 h-14 rounded-full flex items-center justify-center cursor-pointer transition-all active:scale-90 {isVideoOn ? 'bg-white text-black' : 'bg-white/20 text-white'}"
          onclick={() => { isVideoOn = !isVideoOn; }}
        >
          {#if isVideoOn}
            <Video size={24} />
          {:else}
            <VideoOff size={24} />
          {/if}
        </button>
      </div>

      <!-- End Call Button -->
      <button 
        type="button" 
        class="w-16 h-16 rounded-full bg-red-600 hover:bg-red-500 text-white flex items-center justify-center shadow-2xl active:scale-90 transition-transform cursor-pointer"
        onclick={endCall}
      >
        <PhoneOff size={30} />
      </button>
    </div>
  {/if}
</div>

