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
<div id="js-product-list">
  <div class="products row products-grid justify-content-center">
    {foreach from=$listing.products item="product"}
      {block name='product_miniature'}
        {* Wymuszenie 4 kolumn (col-xl-3) *}
        <div class="js-product-miniature-wrapper col-6 col-md-4 col-lg-3 col-xl-3">
          {include file='catalog/_partials/miniatures/product.tpl' product=$product}
        </div>
      {/block}
    {/foreach}
  </div>

  {block name='pagination'}
    {include file='catalog/_partials/products-bottom.tpl' listing=$listing}
  {/block}
  
  {* Ten div jest kluczowy dla działania Infinite Scroll *}
  <div class="hidden-md-up text-xs-right up">
    <a href="#header" class="btn btn-secondary">
      {l s='Back to top' d='Shop.Theme.Actions'}
      <i class="material-icons">&#xE316;</i>
    </a>
  </div>
</div>
