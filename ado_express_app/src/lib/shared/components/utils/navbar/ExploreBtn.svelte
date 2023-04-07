<!-- SOURCE:
<span>
  See the Pen <a href="https://codepen.io/jh3y/pen/eYPYKep">
  CSS Galaxy Button 🚀</a> 
  by Jhey (<a href="https://codepen.io/jh3y">@jh3y</a>)
  on <a href="https://codepen.io">CodePen</a>.
</span> 
-->

<script lang="ts">
  import { onMount } from 'svelte';

  onMount(() => {
    const initParticles = () => {
      const RANDOM = (min: number, max: number): number =>
        Math.floor(Math.random() * (max - min + 1) + min);
      const PARTICLES = document.querySelectorAll('.star');

      PARTICLES.forEach((P) => {
        P.setAttribute(
          'style',
          `
            --angle: ${RANDOM(0, 360)};
            --duration: ${RANDOM(6, 20)};
            --delay: ${RANDOM(1, 10)};
            --alpha: ${RANDOM(40, 90) / 100};
            --size: ${RANDOM(2, 6)};
            --distance: ${RANDOM(40, 200)};
          `
        );
      });
    };

    initParticles();
  });
</script>

<a
target="_blank"
href="https://github.com/FarzamMohammadi"
>
  <button class="text-xl">
    <span class="spark" />
    <span class="backdrop" />
    <span class="galaxy__container">
      <span class="star star--static" />
      <span class="star star--static" />
      <span class="star star--static" />
      <span class="star star--static" />
    </span>
    <span class="galaxy">
      <span class="galaxy__ring">
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
        <span class="star" />
      </span>
    </span>
    <span class="text">Explore Other Projects</span>
  </button>
  <div class="bodydrop" />
</a>

<style lang="scss">
  *,
  *:after,
  *:before {
    box-sizing: border-box;
  }

  :root {
    --transition: 0.25s;
    --spark: 1.8s;
    --hue: 245;
  }

  button {
    --cut: 0.12em;
    --active: 0;
    --bg: radial-gradient(
          100% 120% at 126% 126%,
          hsl(
              var(--hue) calc(var(--active) * 97%) 98% /
                calc(var(--active) * 0.9)
            )
            40%,
          transparent 50%
        )
        calc(100px - (var(--active) * 100px)) 0 / 100% 100% no-repeat,
      radial-gradient(
          120% 120% at 120% 120%,
          hsl(
              var(--hue) calc(var(--active) * 97%) 70% / calc(var(--active) * 1)
            )
            30%,
          transparent 70%
        )
        calc(100px - (var(--active) * 100px)) 0 / 100% 100% no-repeat,
      hsl(
        var(--hue) calc(var(--active) * 100%) calc(12% - (var(--active) * 8%))
      );
    background: var(--bg);
    font-weight: 500;
    border: 0;
    cursor: pointer;
    padding: 0.9em 1.3em;
    display: flex;
    align-items: center;
    gap: 0.25em;
    white-space: nowrap;
    border-radius: 2rem;
    position: relative;
    box-shadow: 0 0 calc(var(--active) * 6em) calc(var(--active) * 1em)
        hsl(var(--hue) 97% 61% / 0.5),
      0 0.05em 0 0
        hsl(
          var(--hue) calc(var(--active) * 97%) calc((var(--active) * 50%) + 30%)
        )
        inset,
      0 -0.05em 0 0 hsl(
          var(--hue) calc(var(--active) * 97%) calc(var(--active) * 10%)
        ) inset;
    transition: box-shadow var(--transition), scale var(--transition),
      background var(--transition);
    scale: calc(1 + (var(--active) * 0.1));
    transform-style: preserve-3d;
    perspective: 100vmin;
    overflow: hidden;
  }

  button:active {
    scale: 1;
  }

  .star {
    height: calc(var(--size) * 1px);
    aspect-ratio: 1;
    background: white;
    border-radius: 50%;
    position: absolute;
    opacity: var(--alpha);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(10deg) rotate(0deg)
      translateY(calc(var(--distance) * 1px));
    animation: orbit calc(var(--duration) * 1s) calc(var(--delay) * -1s)
      infinite linear;
  }

  @keyframes orbit {
    to {
      transform: translate(-50%, -50%) rotate(10deg) rotate(360deg)
        translateY(calc(var(--distance) * 1px));
    }
  }

  .galaxy {
    position: absolute;
    width: 100%;
    aspect-ratio: 1;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    overflow: hidden;
    opacity: var(--active);
    transition: opacity var(--transition);
  }

  .galaxy__ring {
    height: 200%;
    width: 200%;
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 50%;
    transform: translate(-28%, -40%) rotateX(-24deg) rotateY(-30deg)
      rotateX(90deg);
    transform-style: preserve-3d;
  }

  .galaxy__container {
    position: absolute;
    inset: 0;
    opacity: var(--active);
    transition: opacity var(--transition);
    mask: radial-gradient(white, transparent);
  }

  .star--static {
    animation: none;
    top: 50%;
    left: 50%;
    transform: translate(0, 0);
    max-height: 4px;
    filter: brightness(4);
    opacity: 0.9;
    animation: move-x calc(var(--duration) * 0.1s) calc(var(--delay) * -0.1s)
        infinite linear,
      move-y calc(var(--duration) * 0.2s) calc(var(--delay) * -0.2s) infinite
        linear;
  }

  button:hover .star--static {
    animation-play-state: paused;
  }

  @keyframes move-x {
    0% {
      translate: -100px 0;
    }
    100% {
      translate: 100px 0;
    }
  }

  @keyframes move-y {
    0% {
      transform: translate(0, -50px);
    }
    100% {
      transform: translate(0, 50px);
    }
  }

  .spark {
    position: absolute;
    inset: 0;
    border-radius: 2rem;
    rotate: 0deg;
    overflow: hidden;
    mask: linear-gradient(white, transparent 50%);
    animation: flip calc(var(--spark) * 2) infinite steps(2, end);
  }

  @keyframes flip {
    to {
      rotate: 360deg;
    }
  }

  .spark:before {
    content: '';
    position: absolute;
    width: 200%;
    aspect-ratio: 1;
    top: 0%;
    left: 50%;
    z-index: -1;
    translate: -50% -15%;
    rotate: 0;
    transform: rotate(-90deg);
    opacity: calc((var(--active)) + 0.4);
    background: conic-gradient(from 0deg, transparent 0 340deg, white 360deg);
    transition: opacity var(--transition);
    animation: rotate var(--spark) linear infinite both;
  }

  .spark:after {
    content: '';
    position: absolute;
    inset: var(--cut);
    border-radius: 22rem;
  }

  .backdrop {
    position: absolute;
    inset: var(--cut);
    background: var(--bg);
    border-radius: 2rem;
    transition: background var(--transition);
  }

  @keyframes rotate {
    to {
      transform: rotate(90deg);
    }
  }

  @supports (selector(:has(:is(+ *)))) {
    body:has(button:is(:hover, :focus-visible)) {
      --active: 1;
      --play-state: running;
    }
  }

  button:is(:hover, :focus-visible) ~ :is(.particle-pen) {
    --active: 1;
    --play-state: running;
  }

  button:is(:hover, :focus-visible) {
    --active: 1;
    --play-state: running;
  }

  @keyframes float-out {
    to {
      rotate: 360deg;
    }
  }

  .text {
    font-size: medium;
    translate: 2% -6%;
    letter-spacing: 0.01ch;
    color: hsl(0 0% calc(60% + (var(--active) * 26%)));
  }
</style>
