<#macro content pageId="">
  <header>
    <div class="inner">
      <div class="mobile-menu-nav">
        <button id="mobile-menu-toggle" alt="toggle menu">
          <i class="icon open-icon fa fa-bars"></i>
          <i class="icon close-icon fa fa-times"></i>
        </button>
        <div id="mobile-menu">
          <div class="mobile-menu-container sand">
            <ul class="mobile-menu-list">
              <li><a role='listitem' href="${url.loginUrl}" class="js-login-link item service-menue
              <#if pageId == 'login'>
                active
              </#if>">${msg("navLogin")}</a></li>
              <li><a role='listitem' href="#" class="js-contact-toggle item service-menue">${msg("navSupport")}</a></li>
            </ul>
            <#-- Change: This part is copied from the original template.ftl -->
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
        </div>
      </div>
      <div class='service-nav login' role='list'>
        <a role='listitem' href="${url.loginUrl}" class="js-login-link service-menue
            <#if pageId == 'login'>
              active
          </#if>">${msg("navLogin")}</a>
        <a role='listitem' href="#" class="js-contact-toggle service-menue">${msg("navSupport")}</a>
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
