document.addEventListener('DOMContentLoaded', () => {
  const search = document.querySelector('#project-search');
  const empty = document.querySelector('#empty-state');
  const filters = [...document.querySelectorAll('.filter')];
  let activeFilter = 'all';

  // Performance Optimization: Cache card metadata and visibility state upfront.
  // This avoids dataset DOM attribute accesses, string interpolations, and redundant DOM mutations on every search keystroke/filter click.
  const cardData = [...document.querySelectorAll('.project-card')].map((el) => {
    const name = el.dataset.name || '';
    const category = el.dataset.category || '';
    return {
      el,
      name,
      haystack: `${name} ${category}`,
      isHidden: el.hidden || false
    };
  });

  const applyFilters = () => {
    const term = search.value.trim().toLowerCase();
    let visible = 0;
    const isAllFilter = activeFilter === 'all';

    cardData.forEach((item) => {
      const matchesTerm = !term || item.name.includes(term);
      const matchesFilter = isAllFilter || item.haystack.includes(activeFilter);
      const show = matchesTerm && matchesFilter;
      const shouldHide = !show;

      if (item.isHidden !== shouldHide) {
        item.isHidden = shouldHide;
        item.el.hidden = shouldHide;
      }
      if (show) visible += 1;
    });

    const emptyStateHidden = visible !== 0;
    if (empty.hidden !== emptyStateHidden) {
      empty.hidden = emptyStateHidden;
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
