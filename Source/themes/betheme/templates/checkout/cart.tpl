{extends file='layouts/layout-full-width.tpl'}

{block name='content'}

  <section id="main">
    <div class="cart-grid row">

      <div class="cart-grid-body col-xs-12 col-lg-8">
        <div class="card cart-container">
          <div class="card-block">
            <h1 class="h1">{l s='Shopping Cart' d='Shop.Theme.Checkout'}</h1>
          </div>
          <hr class="separator">
          
          {include file='checkout/_partials/cart-detailed.tpl' cart=$cart}
        </div>

        {hook h='displayShoppingCartFooter'}
      </div>

      <div class="cart-grid-right col-xs-12 col-lg-4">
        <div class="card cart-summary">
          
          {block name='cart_summary_totals'}
            {include file='checkout/_partials/cart-detailed-totals.tpl' cart=$cart}
          {/block}

          {block name='cart_summary_actions'}
            {include file='checkout/_partials/cart-detailed-actions.tpl' cart=$cart}
          {/block}

        </div>
        
        {hook h='displayReassurance'}
      </div>

    </div>
  </section>
{/block}