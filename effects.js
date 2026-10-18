// Touch screens have no hover, so a tap lights up every link near the finger
// with the same rainbow effect ("glow" class in style.css), then lets it fade.
(() => {
  const RADIUS = 90;   // px from the tap to the edge of a link
  const HOLD = 2000;   // ms before the glow starts fading back
  const timers = new WeakMap();

  document.addEventListener("pointerdown", (e) => {
    if (e.pointerType !== "touch") return;
    for (const link of document.querySelectorAll("a:not([aria-current])")) {
      const r = link.getBoundingClientRect();
      // Distance from the tap to the nearest point of the link's box
      const dx = Math.max(r.left - e.clientX, 0, e.clientX - r.right);
      const dy = Math.max(r.top - e.clientY, 0, e.clientY - r.bottom);
      if (dx * dx + dy * dy > RADIUS * RADIUS) continue;
      link.classList.add("glow");
      clearTimeout(timers.get(link));
      timers.set(link, setTimeout(() => link.classList.remove("glow"), HOLD));
    }
  }, { passive: true });
})();
