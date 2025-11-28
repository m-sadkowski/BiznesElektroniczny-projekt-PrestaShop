<div id="_desktop_cart_styled">
  <div class="blockcart cart-preview {if $cart.products_count > 0}active{else}inactive{/if}" data-refresh-url="{$refresh_url}">
    
    {* NAGŁÓWEK (CZARNY PASEK) *}
    <a href="{$cart_url}" rel="nofollow">
      <div class="header">
        <i class="fa fa-shopping-bag"></i>
        <span>Koszyk</span>
        <span class="cart-products-count">({$cart.products_count})</span>
        {* Cena jest opcjonalna, zalezy czy chcesz ja widziec na czarnym pasku *}
        <span class="value">{$cart.totals.total.value}</span>
      </div>
    </a>

    {* ROZWIJANA LISTA *}
    <div class="cart-dropdown">
        
        {* Lista produktów *}
        <ul>
          {foreach from=$cart.products item=product}
            <li class="cart-product-line">
              <div class="product-image-container">
                            <span class="product-image">
                                {if $product.cover}
                                    <a href="{$product.url}">
                                        <img src="{$product.cover.bySize.cart_default.url}" alt="{$product.name|escape:'quotes'}" class="img-fluid">
                                    </a>
                                {else}
                                    <a href="{$product.url}">
                                        <img src="{$urls.no_picture_image.bySize.cart_default.url}" class="img-fluid" />
                                    </a>
                                {/if}
                            </span>
                        </div>
              <span class="product-quantity">{$product.quantity}x</span>
              <span class="product-name">{$product.name}</span>
              <span class="product-price">{$product.price}</span>
              <a  class="remove-from-cart"
                  rel="nofollow"
                  href="{$product.remove_from_cart_url}"
                  data-link-action="delete-from-cart"
                  title="{l s='remove from cart' d='Shop.Theme.Actions'}"
              >
                  <i class="fa fa-trash-o" aria-hidden="true"></i>
              </a>
            </li>
          {/foreach}
        </ul>

        <div class="cart-subtotals">
            <div class="products">
                <span class="label">Suma produktów:</span>
                <span class="value" style="color: black">{$cart.subtotals.products.value}</span>
            </div>
            <div class="shipping">
                <span class="label">Wysyłka:</span>
                <span class="value">{$cart.subtotals.shipping.value}</span>
            </div>
        </div>

        <div class="cart-total">
            <span class="label">Łącznie (brutto):</span>
            <span class="value">{$cart.totals.total.value}</span>
        </div>

        <div class="cart-buttons">
             <a href="{$cart_url}?action=show" class="btn btn-primary">Do kasy</a>
        </div>
    </div>

  </div>
</div>