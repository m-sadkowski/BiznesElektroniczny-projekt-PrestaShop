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
{block name='product_miniature_item'}
<div class="js-product product{if !empty($productClasses)} {$productClasses}{/if}">
  <article class="product-miniature product-miniature-default product-miniature-grid product-miniature-layout-2 js-product-miniature" data-id-product="{$product.id_product}" data-id-product-attribute="{$product.id_product_attribute}">
    
    {* 1. CONTAINER OBRAZKA I FLAGEK *}
    <div class="thumbnail-container">
        <a href="{$product.url}" class="thumbnail product-thumbnail">
            <img src="{$product.cover.bySize.home_default.url}" alt="{$product.cover.legend}" width="{$product.cover.bySize.home_default.width}" height="{$product.cover.bySize.home_default.height}" class="img-fluid swiper-lazy lazy-product-image product-thumbnail-first">
            {* Dodaj warunek na obrazek 2, jeśli istnieje *}
            {if isset($product.images.1.bySize.home_default.url)}
                <img src="{$product.images.1.bySize.home_default.url}" alt="{$product.images.1.legend}" width="{$product.images.1.bySize.home_default.width}" height="{$product.images.1.bySize.home_default.height}" class="img-fluid swiper-lazy lazy-product-image product-thumbnail-second">
            {/if}
        </a>
        
        {block name='product_flags'}
            <ul class="product-flags js-product-flags">
                {foreach from=$product.flags item=flag}
                    <li class="product-flag {$flag.type}">{$flag.label}</li>
                {/foreach}
            </ul>
        {/block}
        
        {* Wymagane do działania quickview / funkcjonalnych przycisków *}
        <div class="product-functional-buttons product-functional-buttons-bottom">
            <div class="product-functional-buttons-links">
                {hook h='displayProductListFunctionalButtons' product=$product}
                <a class="js-quick-view-iqit" href="#" data-link-action="quickview" data-toggle="tooltip" title="{l s='Quick view' d='Shop.Theme.Actions'}">
                    <i class="fa fa-eye" aria-hidden="true"></i>
                </a>
            </div>
        </div>
        
        {* Wymagana informacja o dostępności (Czas realizacji zamówienia) *}
        <div class="product-availability d-block mt-2 pfix-fallback">
            {hook h='displayProductAvailability'}
        </div>
    </div>
    
    {* 2. CONTAINER OPISU, CENY I KOSZYKA *}
    <div class="product-description">
        <div class="row extra-small-gutters justify-content-end">
            <div class="col">
                <div class="product-category-name text-muted">{$product.category_name}</div>
                
                <h2 class="h3 product-title">
                    <a href="{$product.url}">{$product.name|truncate:50:'...'}</a>
                </h2>
                
                <div class="product-reference text-muted">{$product.reference}</div>
            </div>
            
            <div class="col col-auto product-miniature-right">
                <div class="product-price-and-shipping">
                    {if $product.has_discount}
                        {hook h='displayProductPriceBlock' product=$product type="old_price"}
                        <span class="regular-price">{$product.regular_price}</span>
                    {/if}
                    <span class="product-price" content="{$product.price_amount}" aria-label="{l s='Price' d='Shop.Theme.Catalog'}">
                        {$product.price}
                    </span>
                </div>
            </div>
        </div>

        {* Krótki opis (opcjonalny, ale był w Twoim kodzie) *}
        <div class="product-description-short text-muted">
             {$product.description_short|strip_tags:'UTF-8'|truncate:100:'...'}
        </div>
        
        {* PRZYCISK DO KOSZYKA (Najważniejszy element) *}
        <div class="product-add-cart js-product-add-cart-{$product.id_product}-{$product.id_product_attribute}">
    <form action="{$smarty.const._PS_BASE_URL_}{$smarty.const.__PS_BASE_URI__}koszyk" method="post">
        <input type="hidden" name="id_product" value="{$product.id_product}">
        <input type="hidden" name="token" value="{$static_token}">
        <input type="hidden" name="id_product_attribute" value="{$product.id_product_attribute}">
        
        <div class="input-group-add-cart">
            <div class="input-group bootstrap-touchspin">
                <input type="number" name="qty" value="1" class="form-control input-qty" min="1" style="display: block;">
                <span class="input-group-btn-vertical">
                    <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-up" type="button"><i class="fa fa-angle-up touchspin-up"></i></button>
                    <button class="btn btn-touchspin js-touchspin bootstrap-touchspin-down" type="button"><i class="fa fa-angle-down touchspin-down"></i></button>
                </span>
            </div>
            
            <button class="btn btn-product-list add-to-cart" data-button-action="add-to-cart" type="submit">
                <i class="fa fa-shopping-bag fa-fw bag-icon" aria-hidden="true"></i> 
                <i class="fa fa-circle-o-notch fa-spin fa-fw spinner-icon" aria-hidden="true"></i> 
                {l s='Do koszyka' d='Shop.Theme.Actions'}
            </button>
        </div>
    </form>
</div>
        
    </div>
    
    {* DODATKOWA INFORMACJA O DOSTĘPNOŚCI POD PRODUKTEM (dla pewności) *}
    <div class="product-availability d-block mt-2 pfix-fallback">
        {hook h='displayProductAvailability'}
    </div>

</article>
</div>
{/block}
