{extends file=$layout}

{block name='head_microdata_special'}
  {include file='_partials/microdata/product-list-jsonld.tpl' listing=$listing}
{/block}

{block name='product_list'}
  
  {* Używamy klas, które motyw rozpoznaje jako siatkę produktów i włączamy CSS Layout 2 *}
  <div class="products-grid products">
    <div class="products row">
      
      {* Włączamy główną miniaturę i dodajemy KLASĘ LAYOUTU 2,
         która ostyluje produkt tak jak na stronie głównej. *}
      {include file='catalog/_partials/products.tpl' 
        listing=$listing 
        productClass="product-miniature-layout-2 col-xs-12 col-sm-6 col-md-6 col-lg-4 col-xl-3"}
        
    </div>
  </div>
{/block}

{block name='content'}
  <section id="main">

    {block name='product_list_header'}
      <h1 id="js-product-list-header" class="h2">{$listing.label}</h1>
    {/block}

    {block name='subcategory_list'}
      {if isset($subcategories) && $subcategories|@count > 0}
        {include file='catalog/_partials/subcategories.tpl' subcategories=$subcategories}
      {/if}
    {/block}

    {hook h="displayHeaderCategory"}

    <section id="products">
      {if $listing.products|count}

        {block name='product_list_top'}
          {include file='catalog/_partials/products-top.tpl' listing=$listing}
        {/block}

        {block name='product_list_active_filters'}
          <div class="hidden-sm-down">
            {$listing.rendered_active_filters nofilter}
          </div>
        {/block}

        {* ---------------- START: ZMIENIONY BLOK product_list ---------------- *}
        {block name='product_list'}
        <div class="products-grid products">
          <div class="products row">
            {include file='catalog/_partials/products.tpl' 
              listing=$listing 
              productClass="product-miniature-layout-2 col-xs-12 col-sm-6 col-md-6 col-lg-4 col-xl-3"}
          </div>
        </div>
      {/block}
        {* ---------------- END: ZMIENIONY BLOK product_list ---------------- *}

       

      {else}
        <div id="js-product-list-top"></div>

        <div id="js-product-list">
          {capture assign="errorContent"}
            <h4>{l s='No products available yet' d='Shop.Theme.Catalog'}</h4>
            <p>{l s='Stay tuned! More products will be shown here as they are added.' d='Shop.Theme.Catalog'}</p>
          {/capture}

          {include file='errors/not-found.tpl' errorContent=$errorContent}
        </div>

        <div id="js-product-list-bottom"></div>
      {/if}
    </section>

    {hook h="displayFooterCategory"}

  </section>
{/block}
