{extends file='layouts/layout-full-width.tpl'}

{block name='content'}
  <section id="content">
    <div class="row">
      
      {* --- LEWA KOLUMNA: KROKI (DANE, ADRES, DOSTAWA, PŁATNOŚĆ) --- *}
      <div class="col-md-8">
        <div class="checkout-process-wrapper">
          {render file='checkout/checkout-process.tpl' ui=$checkout_process}
        </div>
      </div>

      {* --- PRAWA KOLUMNA: PODSUMOWANIE KOSZYKA --- *}
      <div class="col-md-4">
        <div class="cart-summary-wrapper">
          {include file='checkout/_partials/cart-summary.tpl' cart=$cart}
        </div>
      </div>

    </div>
  </section>
{/block}