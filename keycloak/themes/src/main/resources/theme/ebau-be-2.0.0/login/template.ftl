<#import "footer.ftl" as footer>
<#import "header.ftl" as header>
    <#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false hideOtherWays=false>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <!DOCTYPE html>
        <html lang="en" class="login">

        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="robots" content="noindex, nofollow">
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <#-- import google Roboto font w/ all font-weights: -->
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
                <#if properties.meta?has_content>
                    <#list properties.meta?split(' ') as meta>
                <meta name="${meta?split('==')[0]}" content="${meta?split('==')[1]}"/>
            </#list>
        </#if>
            <title>
                ${msg("loginTitle",(realm.displayName!''))}
            </title>
        <link rel="icon" href="${url.resourcesPath}/img/favicon.ico" />
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
                <script src="${url.resourcesPath}/${script}" type="text/javascript"></script>
            </#list>
        </#if>
        <#if scripts??>
            <#list scripts as script>
                <script src="${script}" type="text/javascript"></script>
            </#list>
        </#if>
    </head>
    <body class="login">
        <@header.content />
        <main>
            <div class="login-box">
                <div class="box-content">
                    <div class="header">
                    <div class="header-container">
                        <div class="header-logo"></div>
                        <p>
                            ${kcSanitize(msg("loginTitleHtml",(realm.displayNameHtml!'')))?no_esc}
                        </p>
                    </div>
                    <div class="title">
                        <h1>
                            <span class="german-text">Anmelden</span>
                            <span class="french-text">/ Inscription</span>
                        </h1>
                        <div style="display: none">
                            <#nested "header">
                        </div>
                        <#if realm.internationalizationEnabled  && locale.supported?size gt 1>
                            <div class="${properties.kcLocaleMainClass!}" id="kc-locale">
                                <div id="kc-locale-wrapper" class="${properties.kcLocaleWrapperClass!}">
                                    <div id="kc-locale-dropdown" class="${properties.kcLocaleDropDownClass!}">
                                        <a href="#" id="kc-current-locale-link">
                                            ${locale.current}
                                        </a>
                                        <ul class="${properties.kcLocaleListClass!}">
                                            <#list locale.supported as l>
                                                <li class="${properties.kcLocaleListItemClass!}">
                                                    <a class="${properties.kcLocaleItemClass!}" href="${l.url}">
                                                        ${l.label}
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
                    <div class="content">
                    <#nested "socialProviders">
                    <#nested "form">
                </div>
                    <#if auth?has_content && auth.showTryAnotherWayLink() && !hideOtherWays>
                    <form id="kc-select-try-another-way-form" action="${url.loginAction}" method="post">
                        <div class="${properties.kcFormGroupClass!}">
                            <input type="hidden" name="tryAnotherWay" value="on"/>
                            <a href="#" id="try-another-way" onclick="document.forms[' kc-select-try-another-way-form'].submit();return false;">
                        ${msg("doTryAnotherWay")}
                        </a>
                        </div>
                        </form>
                </#if>
                <#if message?has_content && (message.type !='warning' || !isAppInitiatedAction??)>
                    <div class="alert alert-${message.type}">
                        <#if message.type='success'><span class="${properties.kcFeedbackSuccessIcon!}"></span></#if>
                        <#if message.type='warning'><span class="${properties.kcFeedbackWarningIcon!}"></span></#if>
                        <#if message.type='error'><span class="${properties.kcFeedbackErrorIcon!}"></span></#if>
                        <#if message.type='info'><span class="${properties.kcFeedbackInfoIcon!}"></span></#if>
                        <span class="kc-feedback-text">
                            ${kcSanitize(message.summary)?no_esc}
                        </span>
                    </div>
                </#if>
                <#nested "supportProvider">
                    <@footer.content />
                    </div>
                    </div>
                    </main>
                    </body>

        </html>
    </#macro>
