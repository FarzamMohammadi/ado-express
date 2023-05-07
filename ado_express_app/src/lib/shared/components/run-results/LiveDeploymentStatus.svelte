<script>
  import GlowingBars from '../utils/GlowingBars.svelte';

  export let key = '';
  export let status = '';
  export let percentage = 0;
  export let parentWidth = 0;
  export let matrixTheme = true;
</script>

<div class="mb-4">
  <div
    class="flex {parentWidth < 400
      ? 'flex-col'
      : 'flex-row'} items-center justify-between"
  >
    <div>
      <strong class="text-xl">{key}</strong>
    </div>
    <div class="text-xl">
      {status}
    </div>
  </div>
  <div class="flex flex-row items-center justify-center">
    <div>
      <GlowingBars {percentage} {parentWidth} {matrixTheme} />
    </div>
    
    <div>
      {percentage.toFixed()}%
    </div>
  </div>
</div>
