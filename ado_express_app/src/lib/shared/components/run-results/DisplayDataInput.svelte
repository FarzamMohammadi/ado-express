<script>
  export let data = '';
  export let showIdleDots = false;
  export let dotText = '';
</script>

<span>
  {data}
  {#if showIdleDots}{dotText}{/if}
</span>
