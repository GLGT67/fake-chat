<script>
  import { chatState } from '../state.svelte.js';
  import { Wifi } from '@lucide/svelte';
</script>

{#if chatState.showIosStatusBar}
  <div 
    class="w-full flex items-center justify-between px-7 pt-3 pb-1 select-none text-[14.5px] font-semibold tracking-tight transition-colors duration-200 z-30"
    class:text-white={chatState.isDarkMode}
    class:text-black={!chatState.isDarkMode}
  >
    <!-- Left: Time -->
    <div class="flex items-center pl-1 font-semibold text-[15px]">
      <span>{chatState.currentTime}</span>
    </div>

    <!-- Center: Dynamic Island -->
    <div class="w-[124px] h-[35px] bg-black rounded-full flex items-center justify-between px-3 shadow-sm mx-auto -mt-1.5 transition-all">
      <div class="w-3 h-3 rounded-full bg-[#111] flex items-center justify-center">
        <div class="w-2 h-2 rounded-full bg-[#0a1128] ring-1 ring-[#1b264f]/40"></div>
      </div>
      <div class="w-2.5 h-2.5 rounded-full bg-[#050505] ring-1 ring-[#1a1a1a]"></div>
    </div>

    <!-- Right: Cellular, Wifi, Battery -->
    <div class="flex items-center space-x-1.5 pr-1 text-[13px]">
      <!-- Signal Bars -->
      <div class="flex items-end space-x-[2px] h-[11px] pb-[1px]">
        <div class="w-[3px] h-[3px] rounded-[1px] {chatState.signalBars >= 1 ? (chatState.isDarkMode ? 'bg-white' : 'bg-black') : 'bg-gray-400/40'}"></div>
        <div class="w-[3px] h-[5px] rounded-[1px] {chatState.signalBars >= 2 ? (chatState.isDarkMode ? 'bg-white' : 'bg-black') : 'bg-gray-400/40'}"></div>
        <div class="w-[3px] h-[8px] rounded-[1px] {chatState.signalBars >= 3 ? (chatState.isDarkMode ? 'bg-white' : 'bg-black') : 'bg-gray-400/40'}"></div>
        <div class="w-[3px] h-[11px] rounded-[1px] {chatState.signalBars >= 4 ? (chatState.isDarkMode ? 'bg-white' : 'bg-black') : 'bg-gray-400/40'}"></div>
      </div>

      <!-- Cellular Type -->
      <span class="text-[11px] font-bold tracking-tighter ml-0.5">{chatState.cellularType}</span>

      <!-- Wifi Icon -->
      {#if chatState.wifiEnabled}
        <Wifi size={14} strokeWidth={2.5} class="ml-0.5" />
      {/if}

      <!-- Battery Indicator -->
      <div class="flex items-center space-x-1 ml-1">
        <div class="relative w-[23px] h-[12px] border {chatState.isDarkMode ? 'border-white/90' : 'border-black/90'} rounded-[4px] p-[1.5px] flex items-center">
          <div 
            class="h-full rounded-[2px] transition-all duration-300 {chatState.batteryLevel <= 20 ? 'bg-red-500' : (chatState.isDarkMode ? 'bg-white' : 'bg-black')}"
            style="width: {Math.max(8, Math.min(100, chatState.batteryLevel))}%;"
          ></div>
          <div class="absolute -right-[3.5px] top-[2.8px] w-[2px] h-[4.5px] {chatState.isDarkMode ? 'bg-white/90' : 'bg-black/90'} rounded-r-[1px]"></div>
          {#if chatState.isCharging}
            <div class="absolute inset-0 flex items-center justify-center text-[8px] font-bold text-yellow-400">⚡</div>
          {/if}
        </div>
      </div>
    </div>
  </div>
{/if}

