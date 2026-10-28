<script>
  import { chatState } from '../state.svelte.js';
</script>

{#if chatState.showHomeBar}
  <div class="w-full h-7 flex items-center justify-center select-none shrink-0 pointer-events-none pb-1">
    <div 
      class="w-36 h-[4.5px] rounded-full transition-colors duration-200"
      class:bg-white={chatState.isDarkMode}
      class:bg-black={!chatState.isDarkMode}
    ></div>
  </div>
{/if}

