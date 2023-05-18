<script lang="ts">
  let arrowClasses = {
    bottom: 'top-0 mt-1',
    left: 'right-0 mr-1',
    right: 'left-0 ml-1',
    top: 'bottom-0 mb-1',
  };

  let tooltipClasses = {
    bottom: 'top-full mt-2',
    left: 'right-full ml-2',
    right: 'left-full mr-2',
    top: 'bottom-full mb-2',
  };

  export let position = 'top';
  export let text = 'Tooltip';
</script>

<div class="cursor-pointer inline-block relative">
  <slot />
  <div class={`absolute bg-black opacity-0 invisible px-2 py-1 rounded shadow-md text-xs text-white tooltip whitespace-nowrap z-10 ${tooltipClasses[position]}`}>
    {text}
    <div
      class={`absolute border-4 border-transparent h-0 w-0 ${arrowClasses[position]} ${
        position === 'top' || position === 'bottom' ? 'border-' + position + '-black' : 'border-' + position + '-transparent'
      }`}
    />
  </div>
</div>

<style>
  .tooltip {
    transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
  }

  .cursor-pointer:hover .tooltip {
    opacity: 1;
    visibility: visible;
  }
</style>
