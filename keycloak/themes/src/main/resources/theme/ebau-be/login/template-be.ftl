<#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="de" xml:lang="de">
<head>
    <title><#nested "title"></title>

    <link rel="icon" href="${url.resourcesPath}/img/favicon.ico" />

    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0" id="viewport" />
    <meta name="mobile-ready" content="yes" id="mobile-indicator" />

    <#if properties.meta?has_content>
      <#list properties.meta?split(' ') as meta>
        <meta name="${meta?split('==')[0]}" content="${meta?split('==')[1]}"/>
      </#list>
    </#if>

    <#if properties.styles?has_content>
      <#list properties.styles?split(' ') as style>
        <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
      </#list>
    </#if>

    <#if properties.scripts?has_content>
      <#list properties.scripts?split(' ') as script>
            <script src="${url.resourcesPath}/${script}" type="text/javascript"></script>
      </#list>
    </#if>
    <#if scripts??>
      <#list scripts as script>
            <script src="${script}" type="text/javascript"></script>
      </#list>
    </#if>
</head>
<body><a name="top" id="top"></a>
<div id="wrapper">

    <div class="header">

        <div id="div_header">
            <div id="identity">
                <div id="div-header-meta">
                    <h1 class="noOverwrite">
                        <a title="index" target="_blank" href="http://www.be.ch/portal/de/index.html">
                          ${msg("kantonBern")}
                            <span class="small">${msg("startseite")}</span>
                        </a>
                    </h1>
                </div>


                <div id="div_header-main">
                    <div id="div-header-main-logohomelink">
                        <a id="logo-be" title="${msg("startseite")}" href="/">
                        </a>
                        <h2 id="app-title">
                            <a title="${msg("startseite")}" href="/">${msg(realm.displayName!'')}</a>
                            <a title="${msg("startseite")}" href="/" class="small"><span class="hidden"></span>${msg("startseite")}</a>
                        </h2>
                    </div>
                </div>


            </div>

            <hr />

            <hr />

            <div class="header-meta">
                <#if realm.internationalizationEnabled>
                    <a name="anchor-nav-lang"></a>
                    <h2 class="hidden">${msg("andereSprachen")}</h2>
                    <div id="header-nav-lang">
                        <ul>
                            <#list locale.supported as l>
                              <#if l.label != locale.current>
                                <li><a href="${l.url}">${l.label}</a></li>
                              </#if>
                            </#list>
                        </ul>
                    </div>
                </#if>

            </div>

        </div>
    </div>

    <div id="global-nav"></div>
    <div class="clear"></div>

    <div id="content">

        <div id="content-col-nav">
            <p></p>
        </div>
        <hr />

        <a name="anchor-content"></a>
        <div id="content-col-main">

            <div class="content">

                <#if displayMessage && message?has_content>
                  <#if message.type = 'success'>
                    <div class="confirmbox buttonstyle">
                  <#elseif message.type = 'warning'>
                    <div class="warnbox buttonstyle">
                  <#elseif message.type = 'error'>
                    <div class="errorbox buttonstyle">
                  <#else>
                    <div class="hinweisbox buttonstyle">
                  </#if>

                    <span class="text kc-feedback-text">${message.summary?no_esc}</span>
                  </div>
                </#if>

                <#nested "form">

            </div>

        </div>

        <hr />

        <a name="anchor-context"></a>
        <div id="content-col-context">

        </div>
        <br class="clear" />

        <hr />

        <div class="clear"></div>

    </div>

    <hr />

</div>


<div id="footer">
    <div class="footer floatingComponent">
        <p class="half-width">
            <button id="footer-resize-text" style="display: none;"></button>
        </p>

        <p id="footer-classic-view" style="display: none;">
            <a href="#" class="footer-links switch-to-desktop" style="display: none;">Zur klassischen Ansicht wechseln</a>
        </p>

        <p id="footer-copyright-direction">
            <a title="${msg("startseite")}" class="footer-links" href="/"><span class="footer-links" id="icon-copyright">&copy;&nbsp;eBau BE</span></a>
        </p>
    </div>
</div>

<div class="mobileNavigation mobileNav">
    <div id="content-col-nav-mobile">
    </div>
</div>

</body>
</html>
</#macro>