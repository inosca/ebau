<#macro content>
  <header>
    <div class="header-container">
      <div class='service-nav login' role='list'>
        <a class='service-menue i1' href='#' role='listitem'>Benutzungshinweise</a>
        <a class='service-menue login' href='#' role='listitem'>BE-Login</a>
        <#if realm.internationalizationEnabled && locale.supported?size gt 1>
          <div class="${properties.kcLocaleMainClass!}" id="kc-locale">
            <div id="kc-locale-wrapper" class="${properties.kcLocaleWrapperClass!}">
              <div id="kc-locale-dropdown" class="${properties.kcLocaleDropDownClass!}">
                <ul class="${properties.kcLocaleListClass!}">
                  <#list locale.supported as l>
                    <li class="${properties.kcLocaleListItemClass!}">
                      <a class="${properties.kcLocaleItemClass} ${(l.languageTag == locale.currentLanguageTag)?then('active', '')}"
                        href="${l.url}">
                        ${l.languageTag}
                      </a>
                    </li>
                  </#list>
                </ul>
              </div>
            </div>
          </div>
        </#if>

      </div>
      <div class="header-logo"></div>
      <p class="logo-caption">
        ${kcSanitize(msg("realmInfo",(realm.displayNameHtml!'')))?no_esc}
      </p>
      <hr>
      <div class="title">
        <h1>${msg("login")}</h1>
        <#nested "header">
      </div>
    </div>
  </header>
</#macro>
