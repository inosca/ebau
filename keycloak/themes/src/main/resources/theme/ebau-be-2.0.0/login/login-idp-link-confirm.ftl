<#-- Copied from https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/login-idp-link-confirm.ftl -->
<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
    <#if section = "header">
        ${msg("confirmLinkIdpTitle")}
    <#elseif section = "form">
        <form id="kc-register-form" action="${url.loginAction}" method="post">
            <div class="${properties.kcFormGroupClass!}">
                <#-- Change: removed "review profile" button since this should take place on the IdPs site -->

                <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="submitAction" id="linkAccount" value="linkAccount">${msg("confirmLinkIdpContinue", idpDisplayName)}</button>
            </div>
        </form>
    <#-- Change: add context column -->
    <#elseif section = "context">
        <ul class='box-beige open' data-accordion data-allow-all-closed='true' data-multi-expand='false'>
            <li class="default infobox-wrapper is-active" data-accordion-item>
                <h4 class="infobox-title">${msg("loginFaqHeading")}</h4>
                <div class="accordion-content" data-tab-content>
                    <hr class="accordion">
                    ${kcSanitize(msg("loginIdpLinkConfirmContextMessage"))?no_esc}
                    <div class='arrow-link'>
                        <span class='link-arrow'></span>
                        <a class='text-link-2' href="${msg('loginIdpLinkConfirmContextMessageLinkTarget')}">${msg("loginIdpLinkConfirmContextMessageLinkText")}</a>
                    </div>
                </div>
            </li>
        </ul>
    </#if>
</@layout.registrationLayout>
