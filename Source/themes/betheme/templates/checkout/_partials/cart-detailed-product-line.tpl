{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
<div class="product-line-compact">
  <!-- Left: Image -->
  <div class="product-image-container">
    <span class="product-image media-middle">
      {if $product.default_image}
        <img src="{$product.default_image.bySize.cart_default.url}" alt="{$product.name|escape:'quotes'}" loading="lazy">
      {else}
        <img src="{$urls.no_picture_image.bySize.cart_default.url}" loading="lazy" />
      {/if}
    </span>
  </div>

  <!-- Right: Info & Actions -->
  <div class="product-info-container">
    <div class="product-line-info">
      <a class="product-name" href="{$product.url}" data-id_customization="{$product.id_customization|intval}">{$product.name}</a>
    </div>

    <!-- Delivery Time Placeholder (Orange Badge) -->
    <div class="product-delivery-info">
        <span class="delivery-badge">Order processing time from 1 to 2 days</span>
    </div>

    <!-- Actions Row: Qty, Price, Delete -->
    <div class="product-actions-row">
        <!-- Qty -->
        <div class="qty-container">
             {if !empty($product.is_gift)}
              <span class="gift-quantity">{$product.quantity}</span>
            {else}
              <input
                class="js-cart-line-product-quantity form-control"
                data-down-url="{$product.down_quantity_url}"
                data-up-url="{$product.up_quantity_url}"
                data-update-url="{$product.update_quantity_url}"
                data-product-id="{$product.id_product}"
                type="number"
                inputmode="numeric"
                pattern="[0-9]*"
                value="{$product.quantity}"
                name="product-quantity-spin"
                aria-label="{l s='%productName% product quantity field' sprintf=['%productName%' => $product.name] d='Shop.Theme.Checkout'}"
              />
            {/if}
        </div>

        <!-- Price -->
        <div class="price-container">
            <span class="product-price">
              <strong>
                {if !empty($product.is_gift)}
                  <span class="gift">{l s='Gift' d='Shop.Theme.Checkout'}</span>
                {else}
                  {$product.total}
                {/if}
              </strong>
            </span>
        </div>

        <!-- Delete -->
        <div class="delete-container">
             <a
              class                       = "remove-from-cart"
              rel                         = "nofollow"
              href                        = "{$product.remove_from_cart_url}"
              data-link-action            = "delete-from-cart"
              data-id-product             = "{$product.id_product|escape:'javascript'}"
              data-id-product-attribute   = "{$product.id_product_attribute|escape:'javascript'}"
              data-id-customization   	  = "{$product.id_customization|escape:'javascript'}"
          >
            {if empty($product.is_gift)}
              <i class="material-icons float-xs-left">delete</i>
            {/if}
          </a>
        </div>
    </div>
    
    {if $product.customizations|count}
      <div class="customizations-modal-trigger">
          {foreach from=$product.customizations item="customization"}
              <a href="#" data-toggle="modal" data-target="#product-customizations-modal-{$customization.id_customization}">{l s='Product customization' d='Shop.Theme.Catalog'}</a>
          {/foreach}
      </div>
    {/if}
  </div>
</div>
