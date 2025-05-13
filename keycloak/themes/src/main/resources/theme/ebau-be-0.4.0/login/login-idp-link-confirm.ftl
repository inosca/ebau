<#import "template.ftl" as layout>
<#-- Copied from https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/login-idp-link-confirm.ftl -->
<@layout.registrationLayout; section>
    <#-- CHANGE: Moved optional header section into form section -->
    <#if section = "form">
        <form id="kc-register-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">
            <div class="${properties.kcFormGroupClass!} uk-button-group">
                <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="submitAction" id="updateProfile" value="updateProfile">${msg("confirmLinkIdpReviewProfile")}</button>
                <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="submitAction" id="linkAccount" value="linkAccount">${msg("confirmLinkIdpContinue", idpDisplayName)}</button>
            </div>
        </form>
        <div style="margin-top: 30px; margin-bottom: 30px">
            <div><p><b>${msg("loginIdpLinkConfirmTitle")}</b><p></div>
            <div>${msg("loginIdpLinkConfirmMessage",brokerContext.email)?no_esc}</div>
        </div>
    </#if>
</@layout.registrationLayout>
