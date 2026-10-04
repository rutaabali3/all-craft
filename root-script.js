document.addEventListener('DOMContentLoaded', () => {
  // Pre-cache DOM elements and pre-compute card metadata on initialization
  // to avoid repeated DOM dataset reads and string allocations during search/filter operations.
  const search = document.querySelector('#project-search');
  const empty = document.querySelector('#empty-state');
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
    const term = search.value.trim().toLowerCase();
    // Pre-evaluate loop invariants outside card iteration
    // to avoid redundant string equality/length checks on every card.
    const hasTerm = term.length > 0;
    const isAllFilter = activeFilter === 'all';
    let visible = 0;

    for (let i = 0; i < cardData.length; i++) {
      const card = cardData[i];
      // Short-circuit: skip card.haystack.includes() if term does not match or activeFilter is 'all'
      const matches = (!hasTerm || card.name.includes(term)) && (isAllFilter || card.haystack.includes(activeFilter));
      const hide = !matches;

      // Only mutate DOM if hidden state changes to eliminate unnecessary reflows and paints
      if (card.hidden !== hide) {
        card.el.hidden = hide;
        card.hidden = hide;
      }
      if (matches) visible++;
    }

    const emptyHidden = visible !== 0;
    if (empty.hidden !== emptyHidden) {
      empty.hidden = emptyHidden;
    }
  };

  search.addEventListener('input', applyFilters);
  filters.forEach((filter) => filter.addEventListener('click', () => {
    activeFilter = filter.dataset.filter;
    filters.forEach((button) => button.classList.toggle('active', button === filter));
    applyFilters();
  }));

  if (window.gsap) {
    gsap.from('.site-header', { y: -20, opacity: 0, duration: .7, ease: 'power2.out' });
    gsap.from('.reveal', { y: 24, opacity: 0, duration: .8, stagger: .11, delay: .18, ease: 'power3.out' });
    gsap.from('.hero-still-life > *', { scale: .7, opacity: 0, rotate: 'random(-20,20)', duration: 1, stagger: .08, delay: .25, ease: 'back.out(1.6)' });
    gsap.to('.sun-disc', { y: -12, scale: 1.04, duration: 3.4, repeat: -1, yoyo: true, ease: 'sine.inOut' });
    gsap.to('.paperclip', { rotation: 28, y: -7, duration: 2.8, repeat: -1, yoyo: true, ease: 'sine.inOut' });
    gsap.from('.project-card', { y: 20, opacity: 0, duration: .55, stagger: .025, delay: .45, ease: 'power2.out' });
  }
});
