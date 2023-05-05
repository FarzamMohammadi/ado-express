<script>
  export let percentage = 0;
  export let parentWidth = 100;
  export let matrixTheme;
  let barWidth;
  let boxShadow;
  let pulseBoxShadow;

  $: {
    barWidth = Math.floor(parentWidth / 5 - 10);
    boxShadow = matrixTheme
      ? 'inset 0px 0px 10px 1px rgba(0, 255, 0, 0.4), 0px 0px 20px rgba(0, 255, 0, 0.1)'
      : 'inset 0px 0px 10px 1px rgba(117, 182, 255, 0.4), 0px 0px 20px rgba(117, 182, 255, 0.1)';
    pulseBoxShadow = matrixTheme
      ? 'inset 0px 0px 10px 2px rgba(0, 255, 0, 0.5), 0px 0px 40px 2px rgba(0, 255, 0, 1)'
      : 'inset 0px 0px 10px 2px rgba(117, 182, 255, 0.5), 0px 0px 40px 2px rgba(105, 135, 255, 1)';
  }
</script>

<ul class="glowing-bars">
  {#each Array(5) as _, index}
    <li
      class={percentage > index * 20 && percentage < (index + 1) * 20
        ? 'pulse'
        : ''}
      style="width: {barWidth}px; background: rgba(255, 255, 255, {Math.min(
        1,
        Math.max(0, (percentage - index * 20) / 20)
      )}); box-shadow: {percentage > index * 20 && percentage < (index + 1) * 20 ? pulseBoxShadow : boxShadow};"
    />
  {/each}
</ul>

<style>
  .glowing-bars {
    display: flex;
    align-items: center;
    list-style: none;
    padding: 20;
  }

  .glowing-bars li {
    width: 90px;
    height: 10px;
    margin-right: 10px;
    background: rgba(255, 255, 255, 0);
  }

  .glowing-bars li.pulse {
    animation: pulse 1s alternate infinite;
  }

  @keyframes pulse {
    0% {
      background: rgba(255, 255, 255, 1);
    }
    100% {
      background: rgba(255, 255, 255, 0);
    }
  }
</style>
