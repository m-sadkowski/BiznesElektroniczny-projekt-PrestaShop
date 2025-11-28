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
{block name='header_banner'}
  <div class="header-banner">
    {hook h='displayBanner'}
  </div>
{/block}

{block name='header_nav'}
  <nav class="header-nav">
        <div class="container">
    
        <div class="row justify-content-between">
            <div class="col col-auto col-md left-nav">
                                            <div class="block-iqitlinksmanager block-iqitlinksmanager-2 block-links-inline d-inline-block">
            <ul>
                                                            <li>
                            <a href="https://localhost/sitemap" title="Zagubiłeś się? Znajdź to, czego szukasz!">
                                Mapa strony
                            </a>
                        </li>
                                                                                <li>
                            <a href="https://localhost/contact-us" title="Skorzystaj z formularza kontaktowego">
                                Skontaktuj się z nami
                            </a>
                        </li>
                                                </ul>
        </div>
    
            </div>
            <div class="col col-auto center-nav text-center">
                

                <i class="fa fa-mobile"></i>
                Zadzwoń do nas:
                <a href="tel:881204207">881 204 207</a> lub <a href="tel:669847232">669 847 232</a>

             </div>
            <div class="col col-auto col-md right-nav text-right">
                

<div id="language_selector" class="d-inline-block">
    <div class="language-selector-wrapper d-inline-block">
        <div class="language-selector dropdown js-dropdown">
            <a class="expand-more" data-toggle="dropdown" data-iso-code="pl"><img width="16" height="11" src="https://bikepart.pl/img/l/1.jpg" alt="Polski" class="img-fluid lang-flag"> Polski <i class="fa fa-angle-down fa-fw" aria-hidden="true"></i></a>
            <div class="dropdown-menu">
                <ul>
                                            <li class="current">
                            <a href="https://bikepart.pl/pl/" rel="alternate" hreflang="pl" class="dropdown-item"><img width="16" height="11" src="https://bikepart.pl/img/l/1.jpg" alt="Polski" class="img-fluid lang-flag" data-iso-code="pl"> Polski</a>
                        </li>
                                            <li>
                            <a href="https://bikepart.pl/en/" rel="alternate" hreflang="en" class="dropdown-item"><img width="16" height="11" src="https://bikepart.pl/img/l/2.jpg" alt="English" class="img-fluid lang-flag" data-iso-code="en"> English</a>
                        </li>
                                            <li>
                            <a href="https://bikepart.pl/cs/" rel="alternate" hreflang="cs" class="dropdown-item"><img width="16" height="11" src="https://bikepart.pl/img/l/3.jpg" alt="Čeština" class="img-fluid lang-flag" data-iso-code="cs"> Čeština</a>
                        </li>
                                    </ul>
            </div>
        </div>
    </div>
</div>
<div id="currency_selector" class="d-inline-block">
    <div class="currency-selector dropdown js-dropdown d-inline-block">
        <a class="expand-more" data-toggle="dropdown">PLN  zł <i class="fa fa-angle-down" aria-hidden="true"></i></a>
        <div class="dropdown-menu">
            <ul>
                                    <li>
                        <a title="Korona czeska" rel="nofollow" href="https://bikepart.pl/pl/?SubmitCurrency=1&amp;id_currency=3" class="dropdown-item">CZK  Kč</a>
                    </li>
                                    <li>
                        <a title="Euro" rel="nofollow" href="https://bikepart.pl/pl/?SubmitCurrency=1&amp;id_currency=2" class="dropdown-item">EUR  €</a>
                    </li>
                                    <li class="current">
                        <a title="Złoty polski" rel="nofollow" href="https://bikepart.pl/pl/?SubmitCurrency=1&amp;id_currency=1" class="dropdown-item">PLN  zł</a>
                    </li>
                            </ul>
        </div>
    </div>
</div>

             </div>
        </div>

                        </div>
            </nav>
{/block}

{block name='header_top'}
  <div class="header-top">
    {* Przywracamy klasę container, żeby marginesy boczne wróciły *}
    <div id="desktop-header-container" class="container">
        
        {* align-items-center: centruje elementy w pionie *}
        {* justify-content-between: rozpycha elementy (lewo/środek/prawo) *}
        <div class="row align-items-center justify-content-between">
            
            {* LEWA STRONA: LOGO *}
            {* col-auto: zajmuje tylko tyle miejsca ile ma obrazek *}
            <div class="col-auto col-header-left">
                <div id="desktop_logo">
                    <a href="{$urls.base_url}">
                        <img class="logo img-fluid" src="https://bikepart.pl/img/logo-1677874955.jpg" alt="{$shop.name}" width="350" height="94">
                    </a>
                </div>
            </div>

            {* ŚRODEK: WYSZUKIWARKA *}
            {* col: zajmuje CAŁĄ wolną przestrzeń między logo a koszykiem *}
            {* text-center: centruje wyszukiwarkę wewnątrz tej przestrzeni *}
            <div class="col col-header-center text-center">
                <div id="search_widget_custom_wrapper" style="display:inline-block; width: 100%; max-width: 600px;">
                    {widget name='ps_searchbar'}
                </div>
            </div>

            {* PRAWA STRONA: KOSZYK I LOGOWANIE *}
            {* col-auto: zajmuje tylko tyle miejsca ile treść *}
            <div class="col-auto col-header-right text-right">
                
                {* Koszyk *}
                <div id="_desktop_cart_styled" style="margin-bottom: 5px; display: inline-block;">
                    {widget name='ps_shoppingcart'}
                </div>

                {* Logowanie *}
                <div class="user-info-custom" style="font-size: 13px; color: #777; text-align: right; margin-top: 5px;">
                    {if $customer.is_logged}
                        <i class="fa fa-user" style="margin-right:3px;"></i> 
                        <a href="{$urls.pages.my_account}" style="font-weight:bold; color:#555;">{$customer.firstname}</a> / 
                        <a href="{$urls.actions.logout}" style="color:#999;">Wyloguj się</a>
                    {else}
                        <a href="{$urls.pages.my_account}" style="color:#555; text-decoration:none;">
                            <i class="fa fa-user" style="margin-right:3px;"></i> Zaloguj się
                        </a>
                    {/if}
                </div>
            </div>

        </div>
    </div>
</div>
{/block}



{block name='header_top'}
{* --- STYLIZACJA I SKRYPTY --- *}
<style>
    /* --- POPRAWKA WYSZUKIWARKI (Z-INDEX) --- */
    /* To sprawia, że wyniki wyszukiwania są zawsze na wierzchu */
    .ui-autocomplete, 
    .search-widget .dropdown-menu, 
    .iqit-search-results { 
        z-index: 99999 !important; 
    }
    
    /* Upewniamy się, że kontener nagłówka nie przycina wyników */
    .header-top {
        position: relative;
        z-index: 1001; /* Wyżej niż menu */
    }

    /* --- STYL MENU --- */
    
    /* 1. Podstawowy wygląd paska menu (przed przewinięciem) */
    #custom-sticky-menu-container {
        width: 100%;
        background: #fff; /* Domyślnie białe */
        border-bottom: 1px solid #e1e1e1;
        height: 60px;
        z-index: 999; /* Niżej niż wyszukiwarka */
        transition: background-color 0.3s ease, top 0.3s ease, transform 0.3s ease;
    }

    /* 2. Style guzików (pełna wysokość) */
    #iqitmegamenu-horizontal .cbp-hrmenu {
        height: 60px;
        background: transparent !important;
    }
    
    #iqitmegamenu-horizontal .cbp-hrmenu > ul {
        height: 100%;
        display: flex;
        align-items: center;
    }

    #iqitmegamenu-horizontal .cbp-hrmenu > ul > li {
        height: 100%;
        display: flex;
        align-items: center;
    }

    /* Wygląd linków (tekst) */
    #iqitmegamenu-horizontal .cbp-hrmenu > ul > li > a {
        height: 100%;
        display: flex !important;
        align-items: center;
        padding: 0 20px !important;
        margin: 0 !important;
        border-radius: 0 !important;
        font-weight: 600; /* Pogrubienie tekstu */
        color: #333; /* Domyślny kolor tekstu (ciemny) */
        transition: color 0.3s ease, background-color 0.3s ease;
    }

    /* Efekt najechania (Hover) - Czerwone tło, biały tekst */
    #iqitmegamenu-horizontal .cbp-hrmenu > ul > li:hover > a,
    #iqitmegamenu-horizontal .cbp-hrmenu > ul > li.cbp-hrmenu-tab:hover > a {
        background-color: #ee152a !important;
        color: #fff !important;
    }

    /* --- STYL PRZYKLEJONEGO MENU (SCROLL) --- */
    
    /* 3. Gdy menu jest przyklejone (klasa .is-sticky) */
    #custom-sticky-menu-container.is-sticky {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #000000 !important; /* CZARNE TŁO */
        border-bottom: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        animation: slideDown 0.3s ease forwards;
    }

    /* Zmiana koloru tekstu na biały, gdy tło jest czarne */
    #custom-sticky-menu-container.is-sticky .cbp-hrmenu > ul > li > a {
        color: #ffffff !important;
    }

    /* Hover w trybie przyklejonym (nadal czerwony, ale upewniamy się co do tekstu) */
    #custom-sticky-menu-container.is-sticky .cbp-hrmenu > ul > li:hover > a {
        background-color: #ee152a !important;
        color: #ffffff !important;
    }

    /* Animacja wysuwania */
    @keyframes slideDown {
        from { transform: translateY(-100%); }
        to { transform: translateY(0); }
    }

    /* Placeholder zapobiegający skakaniu */
    .menu-placeholder {
        display: none;
        height: 60px;
    }
    .menu-placeholder.active {
        display: block;
    }
</style>

<script>
document.addEventListener("DOMContentLoaded", function() {
    var menu = document.getElementById("custom-sticky-menu-container");
    var placeholder = document.getElementById("menu-placeholder");
    
    // Obliczamy pozycję menu
    var menuOffset = menu.offsetTop;
    var menuHeight = menu.offsetHeight;

    window.addEventListener("scroll", function() {
        // Logika: Menu znika i pojawia się przyklejone dopiero jak zjedziesz niżej
        if (window.scrollY > (menuOffset + menuHeight + 100)) {
            if (!menu.classList.contains("is-sticky")) {
                menu.classList.add("is-sticky");
                placeholder.classList.add("active");
            }
        } 
        // Powrót do oryginału jak wrócisz na górę
        else if (window.scrollY < menuOffset) {
            if (menu.classList.contains("is-sticky")) {
                menu.classList.remove("is-sticky");
                placeholder.classList.remove("active");
            }
        }
    });
});
</script>

{* --- STRUKTURA HTML MENU (Full Width + Sticky) --- *}

<div id="menu-placeholder" class="menu-placeholder"></div>

<div id="custom-sticky-menu-container">
    <div class="container iqit-megamenu-container" style="height: 100%;">
        <div class="sticky-desktop-wrapper" style="height: 100%;">
            <div id="iqitmegamenu-wrapper" class="iqitmegamenu-wrapper iqitmegamenu-all" style="height: 100%;">
                <div class="container container-iqitmegamenu" style="height: 100%;">
                    <div id="iqitmegamenu-horizontal" class="iqitmegamenu clearfix" role="navigation" style="height: 100%;">
                        
                        <nav id="cbp-hrmenu" class="cbp-hrmenu cbp-horizontal cbp-hrsub-narrow">
                            <ul>
                                <li id="cbp-hrmenu-tab-1" class="cbp-hrmenu-tab cbp-hrmenu-tab-1 cbp-onlyicon ">
                                    <a href="https://localhost/" class="nav-link">
                                        <span class="cbp-tab-title"> <i class="icon fa fa-home cbp-mainlink-icon"></i></span>
                                    </a>
                                </li>
                                <li id="cbp-hrmenu-tab-2" class="cbp-hrmenu-tab cbp-hrmenu-tab-2 ">
                                    <a href="https://localhost/8-motocykle-honda" class="nav-link">
                                        <span class="cbp-tab-title">CZĘŚCI DO MOTOCYKLI HONDA</span>
                                    </a>
                                </li>
                                <li id="cbp-hrmenu-tab-3" class="cbp-hrmenu-tab cbp-hrmenu-tab-3 ">
                                    <a href="https://localhost/362-skutery-honda" class="nav-link">
                                        <span class="cbp-tab-title">CZĘSCI DO SKUTERÓW HONDA</span>
                                    </a>
                                </li>
                                <li id="cbp-hrmenu-tab-4" class="cbp-hrmenu-tab cbp-hrmenu-tab-4 ">
                                    <a href="https://localhost/311-quady-honda" class="nav-link">
                                        <span class="cbp-tab-title">CZĘSCI DO QUADÓW HONDA</span>
                                    </a>
                                </li>
                                <li id="cbp-hrmenu-tab-5" class="cbp-hrmenu-tab cbp-hrmenu-tab-5 pull-right cbp-pulled-right">
                                    <a href="https://localhost/contact-us" class="nav-link">
                                        <span class="cbp-tab-title"> <i class="icon fa fa-phone cbp-mainlink-icon"></i> KONTAKT</span>
                                    </a>
                                </li>
                            </ul>
                        </nav>

                    </div>
                </div>
                <div id="sticky-cart-wrapper"></div>
            </div>
        </div>

        {* WERSJA MOBILNA *}
        <div id="_desktop_iqitmegamenu-mobile">
            <div id="iqitmegamenu-mobile" class="mobile-menu js-mobile-menu h-100 d-flex flex-column">
                <div class="mm-panel__header mobile-menu__header-wrapper px-2 py-2">
                    <div class="mobile-menu__header js-mobile-menu__header">
                        <button type="button" class="mobile-menu__back-btn js-mobile-menu__back-btn btn">
                            <span aria-hidden="true" class="fa fa-angle-left align-middle mr-4"></span>
                            <span class="mobile-menu__title js-mobile-menu__title paragraph-p1 align-middle"></span>
                        </button>
                    </div>
                    <button type="button" class="btn btn-icon mobile-menu__close js-mobile-menu__close" aria-label="Close" data-toggle="dropdown">
                        <span aria-hidden="true" class="fa fa-times"></span>
                    </button>
                </div>

                <div class="position-relative mobile-menu__content flex-grow-1 mx-c16 my-c24 ">
                    <ul class="position-absolute h-100 w-100 m-0 mm-panel__scroller mobile-menu__scroller px-4 py-4">
                        <li class="mobile-menu__above-content"></li>
                        <li class="d-flex align-items-center mobile-menu__tab mobile-menu__tab--id-1 js-mobile-menu__tab">
                            <a class="flex-fill mobile-menu__link" href="https://localhost/">
                                <i class="icon fa fa-home mobile-menu__tab-icon"></i>
                                <span class="js-mobile-menu__tab-title">Home</span>
                            </a>
                        </li>
                        <li class="d-flex align-items-center mobile-menu__tab mobile-menu__tab--id-2 js-mobile-menu__tab">
                            <a class="flex-fill mobile-menu__link" href="https://localhost/8-motocykle-honda">
                                <span class="js-mobile-menu__tab-title">CZĘŚCI DO MOTOCYKLI HONDA</span>
                            </a>
                        </li>
                        <li class="d-flex align-items-center mobile-menu__tab mobile-menu__tab--id-3 js-mobile-menu__tab">
                            <a class="flex-fill mobile-menu__link" href="https://localhost/362-skutery-honda">
                                <span class="js-mobile-menu__tab-title">CZĘSCI DO SKUTERÓW HONDA</span>
                            </a>
                        </li>
                        <li class="d-flex align-items-center mobile-menu__tab mobile-menu__tab--id-4 js-mobile-menu__tab">
                            <a class="flex-fill mobile-menu__link" href="https://localhost/311-quady-honda">
                                <span class="js-mobile-menu__tab-title">CZĘSCI DO QUADÓW HONDA</span>
                            </a>
                        </li>
                        <li class="d-flex align-items-center mobile-menu__tab mobile-menu__tab--id-5 js-mobile-menu__tab">
                            <a class="flex-fill mobile-menu__link" href="https://localhost/contact-us">
                                <i class="icon fa fa-phone mobile-menu__tab-icon"></i>
                                <span class="js-mobile-menu__tab-title">KONTAKT</span>
                            </a>
                        </li>
                        <li class="mobile-menu__below-content"> </li>
                    </ul>
                </div>

                <div class="js-top-menu-bottom mobile-menu__footer justify-content-between px-4 py-4">
                    <div class="d-flex align-items-start mobile-menu__language-currency js-mobile-menu__language-currency">
                        <div class="mobile-menu__language-selector d-inline-block mr-4">
                            Polski
                            <div class="mobile-menu__language-currency-dropdown">
                                <ul>
                                    <li class="my-3"><a href="https://bikepart.pl/en/" rel="alternate" class="text-reset" hreflang="en">English</a></li>
                                    <li class="my-3"><a href="https://bikepart.pl/cs/" rel="alternate" class="text-reset" hreflang="cs">Čeština</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="mobile-menu__currency-selector d-inline-block">
                            PLN zł
                            <div class="mobile-menu__language-currency-dropdown">
                                <ul>
                                    <li class="my-3"><a title="Korona czeska" rel="nofollow" href="https://bikepart.pl/pl/?SubmitCurrency=1&amp;id_currency=3" class="text-reset">CZK Kč</a></li>
                                    <li class="my-3"><a title="Euro" rel="nofollow" href="https://bikepart.pl/pl/?SubmitCurrency=1&amp;id_currency=2" class="text-reset">EUR €</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="mobile-menu__user">
                        <a href="https://localhost/login" class="text-reset"><i class="fa fa-user" aria-hidden="true"></i> Zaloguj się</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{/block}