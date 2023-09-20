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
                    <#if referrer?has_content && referrer.url?has_content><a href="${referrer.url}" class="uk-link-muted" id="referrer">Zurück zu eBau</a></#if>
                </div>
                </div>

                <div class="${properties.kcFormCardClass}">
                    <div class="uk-grid uk-grid-small">
                        <div class="uk-width-1-3">
                            <ul class="uk-tab uk-tab-left">
                                <li class="<#if active=='account'>uk-active</#if>"><a href="${url.accountUrl}">${msg("account")}</a></li>
                                <#if features.passwordUpdateSupported><li class="<#if active=='password'>uk-active</#if>"><a href="${url.passwordUrl}">${msg("password")}</a></li></#if>
                                <li class="<#if active=='totp'>uk-active</#if>"><a href="${url.totpUrl}">${msg("authenticator")}</a></li>
                            </ul>
                        </div>

                        <div class="uk-width-2-3">
                            <#if message?has_content>
                                <div class="uk-alert uk-alert-${message.type} <#if message.type=='error'>uk-alert-danger</#if>">
                                    ${kcSanitize(message.summary)?no_esc}
                                </div>
                            </#if>

                            <#nested "content">
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>
</#macro>
