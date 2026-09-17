// Progressive enhancement: community content exists in the initial HTML.
(() => {
  const form = document.querySelector('#community-filters');
  const search = document.querySelector('#search');
  const state = document.querySelector('#state');
  const sort = document.querySelector('#sort');
  const grid = document.querySelector('#community-grid');
  const cards = Array.from(grid.querySelectorAll('.community-card'));
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty-state');
  const dialog = document.querySelector('#community-dialog');
  let opener;

  function update() {
    const term = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    const ordered = [...cards];
    if (sort.value !== 'featured') {
      ordered.sort((a, b) => a.dataset[sort.value].localeCompare(b.dataset[sort.value]) || a.dataset.name.localeCompare(b.dataset.name));
    }
    for (const card of ordered) {
      const matchesText = `${card.dataset.name} ${card.dataset.city}`.toLocaleLowerCase().includes(term);
      card.hidden = !matchesText || Boolean(state.value && card.dataset.state !== state.value);
      if (!card.hidden) visible++;
      grid.append(card);
    }
    count.textContent = `Showing ${visible} of ${cards.length} ${visible === 1 ? 'community' : 'communities'}`;
    empty.hidden = visible !== 0;
  }
  form.addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', update);
  state.addEventListener('change', update);
  sort.addEventListener('change', update);
  form.addEventListener('reset', () => { search.value = ''; state.value = ''; sort.value = 'featured'; update(); });
  document.querySelector('#clear-empty').addEventListener('click', () => { form.reset(); search.focus(); });

  document.querySelectorAll('.community-open').forEach(button => {
    button.addEventListener('click', () => {
      const card = button.closest('.community-card');
      opener = button;
      document.querySelector('#dialog-title').textContent = card.dataset.name;
      document.querySelector('#dialog-location').textContent = `${card.dataset.city}, ${card.dataset.state}`;
      document.querySelector('#dialog-description').textContent = card.querySelector('.community-body p').textContent;
      const website = document.querySelector('#dialog-website');
      website.href = card.dataset.website;
      website.setAttribute('aria-label', `Visit ${card.dataset.name} website`);
      dialog.showModal();
    });
  });
  document.querySelector('#dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => opener?.focus());
})();
