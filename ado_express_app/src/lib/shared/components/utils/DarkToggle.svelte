<!-- SOURCE: 
  https://codepen.io/aaroniker/pen/PoNewGe Day & Night Toggle
  by Aaron Iker https://codepen.io/aaroniker
-->

<script lang="ts">
  import gsap from 'gsap';
  import { onMount } from 'svelte';

  let darkMode = false;

  function toggleDarkMode() {
    darkMode = !darkMode;
    localStorage.setItem('darkMode', darkMode.toString());
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  onMount(() => {
    darkMode = localStorage.getItem('darkMode') === 'true';

    document.querySelectorAll('.day-night').forEach((dayNight: HTMLElement) => {
      if (darkMode) {
        dayNight.classList.add('night');
        dayNight.style.setProperty('--moon-y', '0px');
        dayNight.style.setProperty('--sun-y', '60px');
        dayNight.style.setProperty('--line', 'var(--night-line)');
        document.documentElement.classList.add('dark');
      } else {
        dayNight.classList.remove('night');
        dayNight.style.setProperty('--moon-y', '60px');
        dayNight.style.setProperty('--sun-y', '0px');
        dayNight.style.setProperty('--line', 'var(--day-line)');
        document.documentElement.classList.remove('dark');
      }

      let toggle = dayNight.querySelector('.toggle') as HTMLElement,
        svgLine = dayNight.querySelector('.line') as HTMLElement;

      let svgLineProxy = new Proxy(
        { y: null },
        {
          set(target, key, value) {
            target[key] = value;
            if (target.y !== null) {
              svgLine.innerHTML = getPath(target.y, 0.1925);
            }
            return true;
          },
          get(target, key) {
            return target[key];
          },
        }
      );

      svgLineProxy.y = 18;

      toggle.addEventListener('click', (e) => {
        e.preventDefault();

        if (dayNight.classList.contains('animate')) {
          return;
        }

        dayNight.classList.add('animate');

        let night = dayNight.classList.contains('night');

        gsap.to(dayNight, {
          keyframes: [
            {
              ['--' + (night ? 'moon-y' : 'sun-y')]: '-4px',
              duration: 0.25,
            },
            {
              ['--' + (night ? 'moon-y' : 'sun-y')]: '60px',
              duration: 0.2,
            },
            {
              ['--' + (night ? 'sun-y' : 'moon-y')]: '-4px',
              duration: 0.25,
              delay: 0.275,
              onStart() {
                gsap.to(dayNight, {
                  '--new-percent': '100%',
                  '--line': night ? 'var(--day-line)' : 'var(--night-line)',
                  '--background': night
                    ? 'var(--day-background)'
                    : 'var(--night-background)',
                  '--new-background': night
                    ? 'var(--day-background)'
                    : 'var(--night-background)',
                  duration: 0.5,
                });
              },
            },
            {
              ['--' + (night ? 'sun-y' : 'moon-y')]: '0px',
              duration: 0.5,
              ease: 'elastic.out(1, .5)',
              clearProps: '--sun-y,--moon-y',
              onComplete() {
                if (night) {
                  dayNight.classList.remove('night');
                  dayNight.style.setProperty('--moon-y', '60px');
                  dayNight.style.setProperty('--sun-y', '0px');
                } else {
                  dayNight.classList.add('night');
                  dayNight.style.setProperty('--moon-y', '0px');
                  dayNight.style.setProperty('--sun-y', '60px');
                }
                dayNight.classList.remove('animate');
                dayNight.style.setProperty('--new-percent', '0%');
                toggleDarkMode();
              },
            },
          ],
        });

        gsap.to(svgLineProxy, {
          keyframes: [
            {
              y: 24,
              delay: 0.25,
              duration: 0.2,
            },
            {
              y: 12,
              duration: 0.2,
            },
            {
              y: 24,
              duration: 0.25,
            },
            {
              y: 18,
              duration: 0.5,
              ease: 'elastic.out(1, .5)',
            },
          ],
        });
      });
    });
  });

  function getPoint(
    point: number[],
    i: number,
    a: number[][],
    smoothing: number
  ) {
    let cp = (
      current: number[],
      previous: number[] | null,
      next: number[] | null,
      reverse: boolean
    ) => {
      let p = previous || current,
        n = next || current,
        o = {
          length: Math.sqrt(
            Math.pow(n[0] - p[0], 2) + Math.pow(n[1] - p[1], 2)
          ),
          angle: Math.atan2(n[1] - p[1], n[0] - p[0]),
        },
        angle = o.angle + (reverse ? Math.PI : 0),
        length = o.length * smoothing;
      return [
        current[0] + Math.cos(angle) * length,
        current[1] + Math.sin(angle) * length,
      ];
    };
    const cps = cp(a[i - 1], a[i - 2], point, false);
    const cpe = cp(point, a[i - 1], a[i + 1], true);

    return `C ${cps[0]},${cps[1]} ${cpe[0]},${cpe[1]} ${point[0]},${point[1]}`;
  }

  function getPath(update: number, smoothing: number) {
    let points = [
      [4, 18],
      [26, update],
      [48, 18],
    ];
    let d = points.reduce(
      (acc, point, i, a) =>
        i === 0
          ? `M ${point[0]},${point[1]}`
          : `${acc} ${getPoint(point, i, a, smoothing)}`,
      ''
    );
    return `<path d="${d}" />`;
  }
</script>

<div class="day-night">
  <button class="toggle">
    <div>
      <svg class="sun" viewBox="0 0 24 24">
        <g class="lines">
          <line x1="1" y1="12" x2="2" y2="12" />
          <line x1="4.2" y1="4.2" x2="4.9" y2="4.9" />
          <line x1="12" y1="1" x2="12" y2="2" />
          <line x1="19.8" y1="4.2" x2="19.1" y2="4.9" />
          <line x1="23" y1="12" x2="22" y2="12" />
          <line x1="19.8" y1="19.8" x2="19.1" y2="19.1" />
          <line x1="12" y1="23" x2="12" y2="22" />
          <line x1="4.2" y1="19.8" x2="4.9" y2="19.1" />
        </g>
        <circle cx="12" cy="12" r="6" />
      </svg>
      <svg class="moon" viewBox="0 0 24 24">
        <path
          d="M18,16C12.5,16,8,11.5,8,6 c0-0.9,0.1-1.8,0.4-2.6C4.1,4.5,1,8.4,1,13c0,5.5,4.5,10,10,10c4.6,0,8.5-3.1,9.6-7.4C19.8,15.9,18.9,16,18,16z"
        />
        <g class="star-1">
          <line x1="15" y1="1" x2="15" y2="5" />
          <line x1="13" y1="3" x2="17" y2="3" />
        </g>
        <g class="star-2">
          <line x1="21" y1="7" x2="21" y2="11" />
          <line x1="19" y1="9" x2="23" y2="9" />
        </g>
      </svg>
    </div>
    <svg class="line" viewBox="0 0 52 36" />
  </button>
</div>

<style lang="scss">

  .day-night {
    --sun: #f0c644;
    --day-background: #eeeeee;
    --day-line: #3bb6c3;
    --moon: #fdd47e;
    --moon-stars: #ddeafb;
    --night-background: #1a1e24;
    --night-line: #73a1bb;
    --sun-lines: 1;
    --sun-lines-r: 0deg;
    --sun-y: 0;
    --moon-y: 60px;
    --new-percent: 0%;
    --background: var(--day-background);
    --line: var(--day-line);
    --new-background: var(--night-background);
    display: grid;
    place-items: center;
    &:before {
      content: '';
      display: block;
      position: fixed;
      left: 0;
      top: 0;
      right: 0;
      bottom: 0;
      background: var(--new-background);
      clip-path: circle(var(--new-percent) at 50% 50%);
      z-index: 40;
    }
    .toggle {
      outline: none;
      border: none;
      background: none;
      position: relative;
      cursor: pointer;
      z-index: 50;
      padding: 0;
      margin: 0;
      display: block;
      width: 100px;
      height: 34px;
      svg {
        display: block;
        pointer-events: none;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
        position: absolute;
        left: var(--left, -2px);
        top: var(--top, 14px);
        stroke-width: var(--stroke-width, 2px);
        stroke: var(--stroke, var(--line));
        &.line {
          --stroke-width: 2px;
          stroke-width: 1.5px;
        }
      }
      div {
        width: 102px;
        height: 45px;
        overflow: hidden;
        position: absolute;
        left: 30.5px;
        top: 10px;
        border-radius: 0 0 9px 9px;
        svg {
          --left: 2px;
          --top: 6px;
          width: 31px;
          height: 26px;
          &.sun {
            --stroke: var(--sun);
            transform: translateY(var(--sun-y)) translateZ(0);
            .lines {
              transform-origin: 12px 12px;
              animation: sun 20s linear infinite;
            }
          }
          &.moon {
            left: 3px;
            --stroke: var(--moon);
            transform: translateY(var(--moon-y)) scale(0.75) translateZ(0);
            .star-1,
            .star-2 {
              stroke: var(--moon-stars);
            }
            .star-1 {
              transform-origin: 15px 3px;
              animation: star 5s linear infinite;
            }
            .star-2 {
              transform-origin: 21px 9px;
              animation: star2 5s linear infinite;
            }
          }
        }
      }
    }
  }

  @keyframes sun {
    to {
      transform: rotate(360deg) translateZ(0);
    }
  }

  @keyframes star {
    5%,
    20% {
      opacity: 0;
      transform: scale(0) rotate(90deg) translateZ(0);
    }
    25%,
    100% {
      opacity: 1;
      transform: scale(1) rotate(180deg) translateZ(0);
    }
  }

  @keyframes star2 {
    0%,
    60% {
      opacity: 1;
      transform: scale(1) rotate(0) translateZ(0);
    }
    65%,
    70% {
      opacity: 0;
      transform: scale(0) rotate(90deg) translateZ(0);
    }
    75%,
    100% {
      opacity: 1;
      transform: scale(1) rotate(180deg) translateZ(0);
    }
  }

  * {
    box-sizing: inherit;
    &:before,
    &:after {
      box-sizing: inherit;
    }
  }
</style>
