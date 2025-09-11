<#import "footer.ftl" as footer>
    <#import "header.ftl" as header>
        <#macro registrationLayout pageId bodyClass="" displayInfo=false displayMessage=true displayRequiredFields=false
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
    <body class="login" data-page-id="login-${pageId}">
        <div class="box-content">
            <@header.content pageId></@header.content>
            <main class="content">
                <#nested "header">
                <div class="main-column">
                    <#if displayMessage && message?has_content>
                        <div class="feedback feedback-${message.type}">
                            <span class="feedback-icon"></span>
                            <span class="feedback-text">
                                ${kcSanitize(message.summary)?no_esc}
                            </span>
                        </div>
                    </#if>
                    <#if msg("feedbackbox-message") != "feedbackbox-message" && msg("feedbackbox-message")?has_content>
                        <div class="feedback feedback-${msg("feedbackbox-type")}">
                            <span class="feedback-icon"></span>
                            <span class="feedback-text">
                                ${kcSanitize(msg("feedbackbox-message"))?no_esc}
                            </span>
                        </div>
                    </#if>
                    <#nested "form">
                </div>
                <div class="context-column">
                    <#nested "context">
                </div>
            </main>
            <@footer.content></@footer.content>
        </div>
    </body>
</html>
</#macro>
