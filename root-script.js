document.addEventListener('DOMContentLoaded', () => {
  // Pre-cache DOM elements and pre-compute card metadata on initialization
  // to avoid repeated DOM dataset reads and string allocations during search/filter operations.
  const search = document.querySelector('#project-search');
  const empty = document.querySelector('#empty-state');
  const filtersContainer = document.querySelector('.filters');
  const filters = [...document.querySelectorAll('.filter')];
  const cardData = [...document.querySelectorAll('.project-card')].map((el) => {
    const name = (el.dataset.name || '').toLowerCase();
    const category = (el.dataset.category || '').toLowerCase();
    return {
      el,
      name,
      haystack: `${name} ${category}`,
      hidden: el.hidden
    };
  });
  let activeFilter = 'all';

  const applyFilters = () => {
    const term = search ? search.value.trim().toLowerCase() : '';
    let visible = 0;

    for (let i = 0; i < cardData.length; i++) {
      const card = cardData[i];
      const matchesTerm = !term || card.name.includes(term);
      const matchesFilter = activeFilter === 'all' || card.haystack.includes(activeFilter);
      const show = matchesTerm && matchesFilter;
      const hide = !show;

      // Only mutate DOM if hidden state changes to eliminate unnecessary reflows and paints
      if (card.hidden !== hide) {
        card.el.hidden = hide;
        card.hidden = hide;
      }
      if (show) visible++;
    }

    const emptyHidden = visible !== 0;
    if (empty && empty.hidden !== emptyHidden) {
      empty.hidden = emptyHidden;
    }
  };

  // Debounce search input via requestAnimationFrame to batch input updates into single animation
  // frames, avoiding synchronous card iterations on every keystroke during rapid typing.
  let searchAnimationFrame = null;
  const onSearchInput = () => {
    if (searchAnimationFrame) cancelAnimationFrame(searchAnimationFrame);
    searchAnimationFrame = requestAnimationFrame(() => {
      searchAnimationFrame = null;
      applyFilters();
    });
  };

  if (search) {
    search.addEventListener('input', onSearchInput);
  }

  // Use event delegation on filter container to avoid attaching per-button event listeners
  // and skip work when re-clicking the already active filter.
  if (filtersContainer) {
    filtersContainer.addEventListener('click', (e) => {
      const filterBtn = e.target.closest('.filter');
      if (!filterBtn) return;
      const targetFilter = filterBtn.dataset.filter;
      if (activeFilter === targetFilter) return;

      activeFilter = targetFilter;
      for (let i = 0; i < filters.length; i++) {
        filters[i].classList.toggle('active', filters[i] === filterBtn);
      }

      if (searchAnimationFrame) {
        cancelAnimationFrame(searchAnimationFrame);
        searchAnimationFrame = null;
      }
      applyFilters();
    });
  }

  if (window.gsap) {
    gsap.from('.site-header', { y: -20, opacity: 0, duration: .7, ease: 'power2.out' });
    gsap.from('.reveal', { y: 24, opacity: 0, duration: .8, stagger: .11, delay: .18, ease: 'power3.out' });
    gsap.from('.hero-still-life > *', { scale: .7, opacity: 0, rotate: 'random(-20,20)', duration: 1, stagger: .08, delay: .25, ease: 'back.out(1.6)' });
    gsap.to('.sun-disc', { y: -12, scale: 1.04, duration: 3.4, repeat: -1, yoyo: true, ease: 'sine.inOut' });
    gsap.to('.paperclip', { rotation: 28, y: -7, duration: 2.8, repeat: -1, yoyo: true, ease: 'sine.inOut' });
    gsap.from('.project-card', { y: 20, opacity: 0, duration: .55, stagger: .025, delay: .45, ease: 'power2.out' });
  }
});
