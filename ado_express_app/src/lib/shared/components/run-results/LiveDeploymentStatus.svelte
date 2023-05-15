<script>
  import { onMount } from 'svelte';
  import GlowingBars from '../utils/GlowingBars.svelte';

  export let key = '';
  export let status = '';
  export let percentage = 0;
  export let matrixTheme = true;
  let parentWidth;

  function updateContainerWidth(){
    parentWidth = Math.min((window.innerWidth / 2) * 0.6); // Adjust the multiplier (0.8) as needed to match the parent div's width

    if (parentWidth < 400 ) {
      parentWidth = parentWidth * 0.90;
    }
  }

  onMount(() => {
    window.addEventListener('resize', updateContainerWidth);

    return () => {
      window.removeEventListener('resize', updateContainerWidth);
    };
  });

  $: {
    updateContainerWidth();
  }

</script>

<div class="flex flex-col my-5">
  <div class="flex {parentWidth < 400 ? 'flex-col': 'flex-row'} items-center justify-between">
    <div>
      <strong class="text-xl">{key}</strong>
    </div>
    <div class="text-xl">
      {status}
    </div>
  </div>
  <div class="flex flex-row items-center justify-between">
    <div>
      <GlowingBars {percentage} {parentWidth} {matrixTheme} />
    </div>
    
    <div>
      {percentage.toFixed()}%
    </div>
  </div>
</div>
