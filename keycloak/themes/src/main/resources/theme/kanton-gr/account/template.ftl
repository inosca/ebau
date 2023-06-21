<#macro mainLayout active bodyClass>
<!doctype html>
<html<#if realm.internationalizationEnabled> lang="${locale.currentLanguageTag}"</#if>>
<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="robots" content="noindex, nofollow">

    <title>${msg("accountManagementTitle")}</title>
    <link rel="icon" href="${url.resourcesPath}/img/favicon.ico">
    <#if properties.stylesCommon?has_content>
        <#list properties.stylesCommon?split(' ') as style>
            <link href="${url.resourcesCommonPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
    <#if properties.styles?has_content>
        <#list properties.styles?split(' ') as style>
            <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
    <#if properties.scripts?has_content>
        <#list properties.scripts?split(' ') as script>
            <script type="text/javascript" src="${url.resourcesPath}/${script}"></script>
        </#list>
    </#if>
</head>
<body class="admin-console user ${bodyClass}">
  <div class="${properties.kcLoginClass!}">
    <div id="kc-header" class="${properties.kcHeaderClass!}">
      <div id="kc-header-wrapper" class="${properties.kcHeaderWrapperClass!}">
        <div class="gr-logo"></div>
        <ul class="nav navbar-nav navbar-utility uk-flex">
          <#if realm.internationalizationEnabled  && locale.supported?size gt 1>
              <div id="kc-locale">
                  <div id="kc-locale-wrapper" class="${properties.kcLocaleWrapperClass!}">
                      <div class="kc-dropdown" id="kc-locale-dropdown">
                          <a href="#" id="kc-current-locale-link">${locale.current}</a>
                          <ul>
                              <#list locale.supported as l>
                                  <li class="kc-dropdown-item"><a href="${l.url}">${l.label}</a></li>
                              </#list>
                          </ul>
                      </div>
                  </div>
              </div>
          </#if>
          <#if referrer?has_content && referrer.url?has_content><a href="${referrer.url}" class="uk-link-muted" id="referrer">Zurück zu eBau</a></#if>
        </ul>
      </div>
    </div>
    <div class="uk-container uk-container-small uk-flex uk-margin-xlarge-top kc-form-card account-container">
        <div class="uk-width-1-3 flex uk-flex-column sidebar">
            <ul class="uk-tab uk-tab-left uk-margin-right">
                <li class="<#if active=='account'>uk-active</#if>"><a href="${url.accountUrl}">${msg("account")}</a></li>
                <#if features.passwordUpdateSupported><li class="<#if active=='password'>uk-active</#if>"><a href="${url.passwordUrl}">${msg("password")}</a></li></#if>
                <li class="<#if active=='totp'>uk-active</#if>"><a href="${url.totpUrl}">${msg("authenticator")}</a></li>
                <#-- the following features are not needed in GR
                  <#if features.identityFederation><li class="<#if active=='social'>active</#if>"><a href="${url.socialUrl}">${msg("federatedIdentity")}</a></li></#if>
                  <li class="<#if active=='sessions'>active</#if>"><a href="${url.sessionsUrl}">${msg("sessions")}</a></li>
                  <li class="<#if active=='applications'>uk-active</#if>"><a href="${url.applicationsUrl}">${msg("applications")}</a></li>
                  <#if features.log><li class="<#if active=='log'>uk-active</#if>"><a href="${url.logUrl}">${msg("log")}</a></li></#if>
                  <#if realm.userManagedAccessAllowed && features.authorization><li class="<#if active=='authorization'>active</#if>"><a href="${url.resourceUrl}">${msg("myResources")}</a></li></#if>
                -->
            </ul>
        </div>

        <div class="uk-width-2-3 content-area">
            <#if message?has_content>
                <div class="alert uk-alert-${message.type}">
                    <#if message.type=='success' ><span class="pficon pficon-ok"></span></#if>
                    <#if message.type=='error' ><span class="pficon pficon-error-circle-o"></span></#if>
                    <span class="kc-feedback-text">${kcSanitize(message.summary)?no_esc}</span>
                </div>
            </#if>

            <#nested "content">
        </div>
    </div>
  </div>
</body>
</html>
</#macro>
