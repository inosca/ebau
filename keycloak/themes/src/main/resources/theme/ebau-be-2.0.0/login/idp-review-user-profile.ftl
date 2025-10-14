<#-- Copied from https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/idp-review-user-profile.ftl -->
<#import "template.ftl" as layout>
<#import "user-profile-commons.ftl" as userProfileCommons>
<@layout.registrationLayout displayMessage=messagesPerField.exists('global') displayRequiredFields=true; section>
    <#if section = "header">
        ${msg("loginIdpReviewProfileTitle")}
    <#elseif section = "form">
        <form id="kc-idp-review-profile-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">

            <@userProfileCommons.userProfileFormFields/>

            <div class="${properties.kcFormGroupClass!}">
                <div id="kc-form-options" class="${properties.kcFormOptionsClass!}">
                    <div class="${properties.kcFormOptionsWrapperClass!}">
                    </div>
                </div>

                <div id="kc-form-buttons" class="${properties.kcFormButtonsClass!}">
                    <input class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" type="submit" value="${msg("doSubmit")}" />
                </div>
            </div>
        </form>
    <#elseif section = "context">
        <ul class='box-beige open' data-accordion data-allow-all-closed='true' data-multi-expand='false'>
            <li class="default infobox-wrapper is-active" data-accordion-item>
                <h4 class="infobox-title">${msg("loginFaqHeading")}</h4>
                <div class="accordion-content" data-tab-content>
                    <hr class="accordion">
                    ${kcSanitize(msg("loginIdpReviewProfileContextMessage"))?no_esc}
                </div>
            </li>
        </ul>
    </#if>
</@layout.registrationLayout>
