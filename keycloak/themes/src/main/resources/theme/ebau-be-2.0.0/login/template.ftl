<#import "footer.ftl" as footer>
    <#import "header.ftl" as header>
        <#macro registrationLayout bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false
            hideOtherWays=false>
            <!DOCTYPE html
                PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <!DOCTYPE html>
            <html lang="en" class="login">

            <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="robots" content="noindex, nofollow">
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link
                    href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
                    rel="stylesheet">
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
        <div class="box-content">
            <@header.content />
            <main class="content">
                <div class="main-column">
                    <div class="title">
                        <h1>${msg("login")}</h1>
                    </div>
                    <#if displayMessage && message?has_content>
                        <div class="alert alert-${message.type}">
                            <#if message.type=' success'><span class="${properties.kcFeedbackSuccessIcon!}"></span>
                </#if>
                <#if message.type='warning'><span class="${properties.kcFeedbackWarningIcon!}"></span></#if>
                <#if message.type='error'><span class="${properties.kcFeedbackErrorIcon!}"></span></#if>
                <#if message.type='info'><span class="${properties.kcFeedbackInfoIcon!}"></span></#if>
                <span class="kc-feedback-text">
                    ${kcSanitize(message.summary)?no_esc}
                </span>
                </div>
                </#if>
                <#nested "form">
                    </div>
                    <div class="context-column">
                        <ul class='box-beige open' data-accordion data-allow-all-closed='true'
                            data-multi-expand='false'>
                            <li class="default infobox-wrapper is-active" data-accordion-item>
                                <h4 class="infobox-title">Fragen & Antworten</h4>
                                <div class="accordion-content" data-tab-content>
                                    <hr class="accordion">
                                    <h4>Welche Anmeldedienste wähle ich aus?</h4>
                                    <p>Nec fusce nullam tristique hac morbi. A dapibus metus sed tincidunt. Id placerat
                                        eu purus platea torquent tellus duis porttitor convallis volutpat.</p>
                                    <h4>Wo erhalte ich Hilfe?</h4>
                                    <p>Nec fusce nullam tristique hac morbi. A dapibus metus sed tincidunt. Id placerat
                                        eu purus platea torquent tellus duis porttitor convallis volutpat.</p>
                                    <div class='arrow-link'>
                                        <span class='link-arrow'></span>
                                        <a class='text-link-2'>Support Informationen</a>
                                    </div>
                                </div>
                            </li>
                    </div>
                    </main>
                    <@footer.content />
                    </div>
                    </body>

            </html>
        </#macro>
