<#-- Copied from https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/login-idp-link-email.ftl -->
<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
    <#if section = "header">
        <#-- Change: remove idpDisplayName argument -->
        ${msg("emailLinkIdpTitle")}
    <#elseif section = "form">
        <#-- Change: use custom texts & buttons -->
        <div class="${properties.kcFormGroupClass!}">
            <p id="instruction1" class="instruction">
                ${kcSanitize(msg("emailLinkIdpHint1", brokerContext.email))?no_esc}
            </p>
            <p id="instruction2" class="instruction">
                ${msg("emailLinkIdpHint2")}
            </p>
            <a href="${url.loginAction}" class="button secondary">${msg("emailLinkIdpHint2Button")}</a>
            <p id="instruction3" class="instruction">
                ${msg("emailLinkIdpHint3")}
            </p>
            <a href="${url.loginAction}" class="button secondary">${msg("emailLinkIdpHint3Button")}</a>
        </div>
    <#-- Change: add context column -->
    <#elseif section = "context">
        <ul class='box-beige open' data-accordion data-allow-all-closed='true' data-multi-expand='false'>
            <li class="default infobox-wrapper is-active" data-accordion-item>
                <h4 class="infobox-title">${msg("loginFaqHeading")}</h4>
                <div class="accordion-content" data-tab-content>
                    <hr class="accordion">
                    ${kcSanitize(msg("emailLinkIdpContextMessage"))?no_esc}
                    <div class='arrow-link'>
                        <span class='link-arrow'></span>
                        <a class='text-link-2' href="${msg('emailLinkIdpContextMessageLinkTarget')}">${msg("emailLinkIdpContextMessageLinkText")}</a>
                    </div>
                </div>
            </li>
        </ul>
    </#if>
</@layout.registrationLayout>
