<script lang="ts">
  export let percentage = 0;
  export let parentWidth = 100;
  export let matrixTheme;
  let barWidth;
  let boxShadow;
  let pulseBoxShadow;

  $: {
    if (matrixTheme) {
      updateComponentStyling();
    } else {
      updateComponentStyling();
    }

    if (parentWidth) {
      updateComponentWidth();
    }
  }

  function updateComponentStyling() {
    const matrixColor = matrixTheme ? '0, 255, 0' : '117, 182, 255';
    boxShadow = `inset 0px 0px 10px 1px rgba(${matrixColor}, 0.4), 0px 0px 20px rgba(${matrixColor}, 0.1)`;
    pulseBoxShadow = `inset 0px 0px 10px 2px rgba(${matrixColor}, 0.5), 0px 0px 40px 2px rgba(${matrixColor}, 1)`;
  }

  function updateComponentWidth() {
    barWidth = Math.floor(parentWidth / 5 - 10);
  }
</script>

<ul class="glowing-bars">
  {#each Array(5) as _, index}
    <li
      class={percentage > index * 20 && percentage < (index + 1) * 20 ? 'pulse' : ''}
      style="width: {barWidth}px; background: rgba(255, 255, 255, {Math.min(1, Math.max(0, (percentage - index * 20) / 20))}); box-shadow: {percentage > index * 20 &&
      percentage < (index + 1) * 20
        ? pulseBoxShadow
        : boxShadow};"
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
