// Animaciones vinculadas a la posición real del scroll, sin dependencias ni bucle en reposo.
(function initScrollMotion() {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const hero = document.querySelector('.hero');
  const heroLayer = document.getElementById('heroVideoLayer');
  const heroContent = document.getElementById('heroMainContent');
  const heroTitle = heroContent.querySelector('h1');
  const heroLead = heroContent.querySelector('.hero-lead-text');
  const heroChips = [...heroContent.querySelectorAll('.stat-chip')];
  const video = document.getElementById('heroVideo');
  const bar = document.getElementById('siteTopBar');
  const journey = document.querySelector('.journey');
  const stage = journey.querySelector('.journey-stage');
  const frame = journey.querySelector('.journey-window');
  const scenes = [...journey.querySelectorAll('.journey-scene')].map(el => ({
    el, image: el.querySelector('img'), word: el.querySelector('.journey-word'), caption: el.querySelector('.journey-caption')
  }));
  const tracks = [...journey.querySelectorAll('.journey-steps i')];
  const counter = journey.querySelector('.journey-count');
  const clamp = (n, a = 0, b = 1) => Math.max(a, Math.min(b, n));
  const ease = n => n * n * (3 - 2 * n);
  let pending = 0, dirty = true, heroVisible = true, currentScene = -1;
  let metrics = {};
  const near = new Set();
  const photos = [...document.querySelectorAll('.day-photo-wrap, .hotel-photo-holder')];
  const cards = [...document.querySelectorAll('.day-card-single, .hotel-card-item, .clean-panel, .timeline-card, .route-card-toggle')];
  const headings = [...document.querySelectorAll('.section-head')];
  const records = new Map();

  // Las fotos ya están embebidas y verificadas en las fichas. Reutilizamos sus datos.
  scenes.forEach(scene => {
    const source = document.querySelector('#' + scene.el.dataset.photo + ' .day-photo-wrap img');
    if (source) scene.image.src = source.src;
  });

  function schedule() {
    if (!pending && !document.hidden) pending = requestAnimationFrame(paint);
  }
  function refresh() { dirty = true; schedule(); }
  window.refreshScrollMotion = refresh;

  // Offset geométrico sin las transformaciones visuales: evita realimentación al animar.
  function layoutTop(el) {
    let top = 0;
    for (let node = el; node; node = node.offsetParent) top += node.offsetTop;
    return top;
  }
  function measure() {
    metrics = {
      heroTop: layoutTop(hero), heroHeight: hero.offsetHeight,
      journeyTop: layoutTop(journey), journeyLength: Math.max(1, journey.offsetHeight - stage.offsetHeight),
      height: window.innerHeight, mobile: window.innerWidth <= 920
    };
    records.forEach((record, el) => {
      record.top = layoutTop(el);
      record.height = el.offsetHeight;
      record.visible = el.getClientRects().length > 0;
    });
    dirty = false;
  }
  function updateVideo() {
    if (!video) return;
    if (reduced.matches || document.hidden || !heroVisible || !hero.offsetHeight) video.pause();
    else { const play = video.play(); if (play) play.catch(() => {}); }
  }
  function paint() {
    pending = 0;
    if (dirty) measure();
    const y = window.scrollY;
    const { heroTop, heroHeight, journeyTop, journeyLength, height, mobile } = metrics;
    bar.classList.toggle('bar-solid', y > Math.max(80, heroHeight * .7));
    if (reduced.matches) return;

    const hp = clamp((y - heroTop) / Math.max(1, heroHeight));
    const distance = Math.min(Math.max(0, y - heroTop), heroHeight);
    heroLayer.style.transform = `translate3d(0,${distance * (mobile ? .15 : .32)}px,0) scale(${1 + hp * .14})`;
    heroContent.style.opacity = String(1 - ease(clamp(hp / .8)));
    heroTitle.style.transform = `translate3d(0,${-hp * (mobile ? 28 : 80)}px,0) scale(${1 + hp * .09})`;
    heroLead.style.transform = `translate3d(0,${-hp * 30}px,0)`;
    heroChips.forEach((chip, i) => {
      chip.style.transform = `translate3d(${(i - 1) * hp * (mobile ? 12 : 65)}px,${hp * (12 + i * 12)}px,0)`;
    });

    if (journey.offsetHeight && y + height >= journeyTop && y <= journeyTop + journey.offsetHeight) {
      const progress = clamp((y - journeyTop) / journeyLength);
      const open = ease(clamp(progress / .2));
      frame.style.clipPath = `inset(${(1 - open) * 8}% ${(1 - open) * (mobile ? 4 : 8)}% round ${(1 - open) * 28}px)`;
      // Dos fundidos y tres pausas de lectura, todos reversibles con el scroll.
      const blend1 = ease(clamp((progress - .26) / .15));
      const blend2 = ease(clamp((progress - .62) / .15));
      const alphas = [1, blend1, blend2];
      const captionAlphas = [
        1 - ease(clamp((progress - .26) / .075)),
        ease(clamp((progress - .335) / .075)) * (1 - ease(clamp((progress - .62) / .075))),
        ease(clamp((progress - .695) / .075))
      ];
      const selected = blend2 >= .5 ? 2 : blend1 >= .5 ? 1 : 0;
      scenes.forEach((scene, i) => {
        const local = clamp((progress - [0, .26, .62][i]) / .4);
        scene.el.style.opacity = String(alphas[i]);
        scene.image.style.transform = `scale(${1.15 - local * .12}) translate3d(${(local - .5) * (mobile ? -1 : -2)}%,${(local - .5) * 2}%,0)`;
        scene.word.style.transform = `translate3d(${(local - .5) * -14}%,0,0)`;
        scene.caption.style.transform = `translate3d(0,${(1 - local) * (mobile ? 32 : 65)}px,0)`;
        scene.caption.style.opacity = String(captionAlphas[i]);
      });
      if (selected !== currentScene) {
        currentScene = selected;
        counter.textContent = `0${selected + 1} / 03`;
        scenes.forEach((scene, i) => scene.el.setAttribute('aria-hidden', String(i !== selected)));
      }
      tracks.forEach((track, i) => track.style.transform = `scaleX(${clamp((progress - i / 3) * 3)})`);
    }

    // Solo se pintan las tarjetas y fotos próximas a la ventana visible.
    near.forEach(el => {
      const record = records.get(el);
      if (!record || !record.visible) return;
      const top = record.top - y;
      if (record.kind === 'photo') {
        const progress = clamp((height - top) / (height + record.height));
        el.style.setProperty('--photo-y', `${((progress - .5) * (mobile ? 40 : 68)).toFixed(2)}px`);
      } else if (record.kind === 'card') {
        const entrance = ease(clamp((height - top) / (height * .28)));
        el.style.setProperty('--enter-opacity', String(.3 + entrance * .7));
        el.style.setProperty('--enter-y', `${(1 - entrance) * (mobile ? 28 : 62)}px`);
        el.style.setProperty('--enter-scale', String(.965 + entrance * .035));
        el.style.setProperty('--enter-tilt', `${(1 - entrance) * record.direction * (mobile ? .35 : 1.2)}deg`);
      } else {
        el.style.setProperty('--heading-fill', `${clamp((height - top) / (height * .45)) * 100}%`);
      }
    });
  }

  photos.forEach(el => { el.classList.add('scroll-photo'); records.set(el, { kind: 'photo' }); });
  cards.forEach((el, i) => { el.classList.add('scroll-enter'); records.set(el, { kind: 'card', direction: i % 2 ? 1 : -1 }); });
  headings.forEach(el => records.set(el, { kind: 'heading' }));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(({ target, isIntersecting }) => {
        if (isIntersecting) near.add(target); else near.delete(target);
        if (records.get(target).kind === 'photo') target.classList.toggle('motion-near', isIntersecting);
      });
      schedule();
    }, { rootMargin: '180px 0px' });
    records.forEach((record, el) => observer.observe(el));
    new IntersectionObserver(entries => {
      heroVisible = entries[0].isIntersecting;
      updateVideo();
    }).observe(hero);
  } else {
    records.forEach((record, el) => near.add(el));
  }
  if ('ResizeObserver' in window) {
    const resize = new ResizeObserver(refresh);
    resize.observe(document.querySelector('main'));
    resize.observe(hero);
  }
  function applyPreference() {
    document.documentElement.classList.toggle('motion-ready', !reduced.matches);
    journey.classList.toggle('journey-ready', !reduced.matches && scenes.every(scene => scene.image.hasAttribute('src')));
    updateVideo();
    refresh();
  }
  reduced.addEventListener('change', applyPreference);
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', refresh, { passive: true });
  window.addEventListener('pageshow', refresh);
  document.addEventListener('visibilitychange', () => { updateVideo(); if (!document.hidden) refresh(); });
  document.fonts.ready.then(refresh);
  applyPreference();
})();
