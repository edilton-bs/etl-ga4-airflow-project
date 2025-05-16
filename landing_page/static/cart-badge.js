// static/js/cart-badge.js
(function(){
  // Atualiza o badge de contagem do carrinho
  function updateCartBadge() {
    const count = JSON.parse(localStorage.getItem('cartItems') || '[]').length;
    document.querySelectorAll('.cart-count-badge').forEach(el => {
      if (count > 0) {
        el.textContent = count;
        el.style.display = 'inline-block';
      } else {
        el.style.display = 'none';
      }
    });
  }

  // Dispara ao carregar a página
  document.addEventListener('DOMContentLoaded', () => {
    updateCartBadge();

    // Sempre que clicar em “Add ao carrinho”, atualiza o badge
    document.body.addEventListener('click', e => {
      if (e.target.classList.contains('btn-alugar')) {
        // O addToCart já salvou o item em localStorage
        updateCartBadge();
      }
    });
  });

  // Sincroniza em múltiplas abas
  window.addEventListener('storage', event => {
    if (event.key === 'cartItems') {
      updateCartBadge();
    }
  });
})();
