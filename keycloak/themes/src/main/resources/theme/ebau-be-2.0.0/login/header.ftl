<#macro content>
  <header>
    <div class="inner">
      <div class='service-nav login' role='list'>
        <a class='service-menue active' href='#' role='listitem'>Login</a>
        <a class='service-menue' href='https://www.belogin.apps.be.ch/phfrontend/contact' role='listitem'>Support</a>
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
    </div>
  </header>
</#macro>
