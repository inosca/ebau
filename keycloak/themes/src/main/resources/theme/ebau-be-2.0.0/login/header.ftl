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
              <#list ["Login","Support"] as site>
                <#if msg("nav"+site) !="nav" + site && msg("nav"+site)?has_content>
                  <li><a role='listitem' href="${msg('nav'+site+'Link')}" class="item service-menue
              <#if pageId == msg('nav' + site + 'Id')>
                active
              </#if>">${msg("nav"+site)}</a></li>
                </#if>
              </#list>
            </ul>
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
        <#list ["Login","Support"] as site>
          <#if msg("nav"+site) !="nav" + site && msg("nav"+site)?has_content>
            <a role='listitem' href="${msg('nav'+site+'Link')}" class="service-menue
              <#if pageId == msg('nav' + site + 'Id')>
                active
              </#if>">${msg("nav"+site)}</a>
          </#if>
        </#list>
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
