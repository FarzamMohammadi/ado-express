<script>
  export let text = 'Tooltip';
  export let position = 'top';

  let tooltipClasses = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-full ml-2',
    right: 'left-full mr-2',
  };
  let arrowClasses = {
    top: 'bottom-0 mb-1',
    bottom: 'top-0 mt-1',
    left: 'right-0 mr-1',
    right: 'left-0 ml-1',
  };
</script>

<div class="relative inline-block cursor-pointer">
  <slot></slot>
  <div
    class={`absolute z-10 invisible text-xs text-white bg-black rounded py-1 px-2 shadow-md opacity-0 whitespace-nowrap tooltip ${tooltipClasses[position]}`}
  >
    {text}
    <div
      class={`absolute w-0 h-0 border-4 border-transparent ${arrowClasses[position]} ${
        position === 'top' || position === 'bottom'
          ? 'border-' + position + '-black'
          : 'border-' + position + '-transparent'
      }`}
    ></div>
  </div>
</div>

<style>
  .tooltip {
    transition: opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
  }

  .cursor-pointer:hover .tooltip {
    opacity: 100;
    visibility: visible;
  }
</style>
