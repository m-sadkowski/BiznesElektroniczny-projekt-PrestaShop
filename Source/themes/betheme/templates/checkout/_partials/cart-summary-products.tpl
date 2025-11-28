{block name='cart_summary_product_list'}
  <div class="cart-summary-products js-cart-summary-products">
    
    <h4 class="h4" style="margin-bottom: 15px; font-weight: bold; text-transform: uppercase;">
        {l s='Shopping Cart' d='Shop.Theme.Checkout'} 
        <span style="color:#777; font-size: 0.8em;">({$cart.products_count})</span>
    </h4>

    {* PĘTLA PRODUKTÓW - ZAWSZE WIDOCZNA *}
    <div class="media-list">
      {foreach from=$cart.products item=product}
        <li class="media" style="border-bottom: 1px solid #eee; padding: 10px 0; display: flex; align-items: center;">
            
            {* MINIATURKA *}
            <div class="media-left" style="width: 60px; margin-right: 10px;">
                <a href="{$product.url}" title="{$product.name}">
                    <img class="media-object" src="{$product.cover.small.url}" alt="{$product.name}" style="max-width: 100%; height: auto;">
                </a>
            </div>

            {* NAZWA I ILOŚĆ *}
            <div class="media-body" style="flex: 1;">
                <span class="product-name" style="font-weight: bold; display: block; line-height: 1.2; font-size: 13px;">
                    {$product.name}
                </span>
                <span class="product-quantity" style="color: #777; font-size: 12px;">
                    Ilość: x{$product.quantity}
                </span>
            </div>

            {* CENA *}
            <div class="media-right" style="font-weight: bold; color: #333;">
                {$product.price}
            </div>

        </li>
        {include file='checkout/_partials/cart-summary-product-line.tpl' product=$product}
      {/foreach}
    </div>
  </div>
{/block}