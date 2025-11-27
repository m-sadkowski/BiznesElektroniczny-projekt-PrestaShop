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
{extends file=$layout}

{block name='content'}

  <section id="main">
    <div class="cart-grid row">
      <!-- Column 1: Account -->
      <div class="col-xs-12 col-lg-4">
        <div class="card">
          <div class="card-block">
            <h3 class="h3">{l s='Personal Information' d='Shop.Theme.Checkout'}</h3>
            
            <!-- Static Mockup for Personal Info -->
            <form>
              <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-control" placeholder="test@example.com">
              </div>
              <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control">
              </div>
              <div class="form-group">
                <label>First Name</label>
                <input type="text" class="form-control">
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input type="text" class="form-control">
              </div>
            </form>

          </div>
        </div>
      </div>

      <!-- Column 2: Shipping & Payment -->
      <div class="col-xs-12 col-lg-4">
        <div class="card">
          <div class="card-block">
            <h3 class="h3">{l s='Shipping Method' d='Shop.Theme.Checkout'}</h3>
            
            <!-- Static Mockup for Shipping -->
            <div class="delivery-options">
              <div class="delivery-option">
                <label>
                  <input type="radio" name="delivery_option" checked>
                  <span>Kurier Inpost Paczkomaty</span>
                </label>
              </div>
              <div class="delivery-option">
                <label>
                  <input type="radio" name="delivery_option">
                  <span>Kurier (po przedpłacie)</span>
                </label>
              </div>
            </div>

          </div>
        </div>
        
        <div class="card mt-2">
          <div class="card-block">
             <h3 class="h3">{l s='Payment Method' d='Shop.Theme.Checkout'}</h3>
             
             <!-- Static Mockup for Payment -->
             <div class="payment-options">
               <div class="payment-option">
                 <label>
                   <input type="radio" name="payment_option" checked>
                   <span>BLIK</span>
                 </label>
               </div>
               <div class="payment-option">
                 <label>
                   <input type="radio" name="payment_option">
                   <span>Pay by bank wire</span>
                 </label>
               </div>
             </div>

          </div>
        </div>
      </div>

      <!-- Column 3: Shopping Cart -->
      <div class="cart-grid-right col-xs-12 col-lg-4">
        <div class="card cart-container">
          <div class="card-block">
            <h1 class="h1">{l s='Shopping Cart' d='Shop.Theme.Checkout'}</h1>
          </div>
          <hr class="separator">
          
          {block name='cart_overview'}
            {include file='checkout/_partials/cart-detailed.tpl' cart=$cart}
          {/block}

          {block name='cart_summary'}
            <div class="cart-summary">
              {block name='hook_shopping_cart'}
                {hook h='displayShoppingCart'}
              {/block}

              {block name='cart_totals'}
                {include file='checkout/_partials/cart-detailed-totals.tpl' cart=$cart}
              {/block}

              {block name='cart_actions'}
                {include file='checkout/_partials/cart-detailed-actions.tpl' cart=$cart}
              {/block}
            </div>
          {/block}
        </div>

        {block name='hook_reassurance'}
          {hook h='displayReassurance'}
        {/block}
      </div>
    </div>
  </section>
{/block}
