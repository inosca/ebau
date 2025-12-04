<#-- COPIED FROM: https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/login-idp-link-confirm-override.ftl -->
<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
    <#if section = "header">
        ${msg("confirmOverrideIdpTitle")}
    <#elseif section = "form">
        <form id="kc-register-form" action="${url.loginAction}" method="post">
            <#-- Change: removed page expiered hint & restart link -->

            <div class="${properties.kcFormGroupClass!}">
                <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="submitAction" id="confirmOverride" value="confirmOverride">${msg("confirmOverrideIdpContinue", idpDisplayName)}</button>

                <#-- Change: move restart restart link and styled as button -->
                <a id="loginRestartLink" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" href="${url.loginRestartFlowUrl}">${msg("doCancel")}</a>
            </div>
        </form>
    <#-- Change: add context column -->
    <#elseif section = "context">
        <ul class='box-beige open' data-accordion data-allow-all-closed='true' data-multi-expand='false'>
            <li class="default infobox-wrapper is-active" data-accordion-item>
                <h4 class="infobox-title">${msg("loginFaqHeading")}</h4>
                <div class="accordion-content" data-tab-content>
                    <hr class="accordion">
                    ${kcSanitize(msg("loginIdpLinkConfirmOverrideContextMessage"))?no_esc}
                    <div class='arrow-link'>
                        <span class='link-arrow'></span>
                        <a class='text-link-2' href="${msg('loginIdpLinkConfirmOverrideContextMessageLinkTarget')}">${msg("loginIdpLinkConfirmOverrideContextMessageLinkText")}</a>
                    </div>
                </div>
            </li>
        </ul>
    </#if>
</@layout.registrationLayout>
