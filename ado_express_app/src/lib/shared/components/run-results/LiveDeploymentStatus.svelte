<script>
  import { onMount } from 'svelte';

  import GlowingBars from '../utils/GlowingBars.svelte';

  const lgMediaQuery = window.matchMedia('(min-width: 1024px)');

  export let key = '';
  export let matrixTheme = true;
  export let percentage = 0;
  export let status = '';
  let isLgViewport;
  let parentWidth;

  $: updateContainerWidth();

  function attachResizeListener() {
    window.addEventListener('resize', updateContainerWidth);

    return () => {
      window.removeEventListener('resize', updateContainerWidth);
    };
  }

  function attachViewPortListener() {
    lgMediaQuery.addEventListener('change', setViewPort);

    return () => {
      lgMediaQuery.removeEventListener('change', setViewPort);
    };
  }

  function setViewPort() {
    if (lgMediaQuery.matches) isLgViewport = true;
    else isLgViewport = false;
  }

  function updateContainerWidth() {
    parentWidth = Math.min((window.innerWidth / 2) * 0.60);

    if (parentWidth < 400) {
      parentWidth = parentWidth * 0.9;
    }
  }

  onMount(() => {
    attachResizeListener();
    attachViewPortListener();
  });
</script>

<div class="flex flex-col my-5">
  <div class={`flex ${parentWidth < 400 ? 'flex-col' : 'flex-row'} items-center justify-between`}>
    <div>
      <strong class="text-xl">{key}</strong>
    </div>
    <div class="text-xl">
      {status}
    </div>
  </div>
  <div class="flex flex-row items-center justify-between">
    <div>
      <GlowingBars matrixTheme={matrixTheme} parentWidth={parentWidth} percentage={percentage} />
    </div>
    <div>
      {percentage.toFixed()}%
    </div>
  </div>
</div>
