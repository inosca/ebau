<#-- Based on https://raw.githubusercontent.com/keycloak/keycloak/refs/heads/release/26.5/themes/src/main/resources/theme/base/login/login.ftl -->
<#import "template.ftl" as layout>
<#import "passkeys.ftl" as passkeys>
<#-- CHANGE: set attributes isLogin=true and displayInfo=social.displayInfo and add displayWide. Removed displayMessage -->
<@layout.registrationLayout displayInfo=social.displayInfo isLogin=true displayWide=(realm.password && social.providers??); section>
    <#if section = "header">
        <#-- CHANGE: hide header
        ${msg("loginAccountTitle")}
        -->
    <#elseif section = "form">
        <#-- CHANGE:
            The form section is entirely custom and handles the social login part here instead of in its
            own section (See comment <#nested socialProviders> in template.ftl).

            The template includes unused sections from the base template to make it easier to review changes
            after keycloak upgrades.
        -->

        <#if realm.displayNameHtml != "master">
            <div id="info-messages">
                ${kcSanitize(msg((realm.displayNameHtml!'')))?no_esc}
            </div>
        </#if>

        <div id="kc-form" <#if realm.password && social.providers?has_content>class="${properties.kcContentWrapperClass!}"</#if>>
            <div id="kc-form-wrapper" <#if realm.password && social.providers?has_content>class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}"</#if>>
                <#if realm.password && social.providers??>
                    <div id="kc-social-providers" class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}">
                        <ul class="${properties.kcFormSocialAccountListClass!} <#if social.providers?size gt 4>${properties.kcFormSocialAccountDoubleListClass!}</#if>">
                            <#-- "pseudo"-IdP: local login, password reset and registration -->
                            <#if realm.password>
                                <form id="kc-form-login" class="uk-form-horizontal uk-width-xlarge uk-margin-auto" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                                    <h1>Anmeldung</h1>
                                    <p>Für Bürger, Gemeinden und lokale Benutzer</p>
                                    <div class="${properties.kcFormGroupClass!}">
                                        <label for="username" class="${properties.kcLabelClass!}"><#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if></label>

                                        <div class="uk-form-controls">
                                            <#if usernameEditDisabled??>
                                                <input tabindex="1" id="username" class="${properties.kcInputClass!}" name="username" value="${(login.username!'')}" type="text" disabled />
                                            <#else>
                                                <input tabindex="1" id="username" class="${properties.kcInputClass!}" name="username" value="${(login.username!'')}"  type="text" autofocus autocomplete="off" />
                                            </#if>
                                        </div>
                                    </div>

                                    <div class="${properties.kcFormGroupClass!}">
                                        <label for="password" class="${properties.kcLabelClass!}">${msg("password")}</label>
                                        <div class="uk-form-controls">
                                            <input tabindex="2" id="password" class="${properties.kcInputClass!}" name="password" type="password" autocomplete="off" />
                                        </div>
                                    </div>

                                    <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
                                        <div id="kc-form-options">
                                            <#if realm.rememberMe && !usernameEditDisabled??>
                                                <div class="checkbox">
                                                    <label>
                                                        <#if login.rememberMe??>
                                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                                                        <#else>
                                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                                                        </#if>
                                                    </label>
                                                </div>
                                            </#if>
                                            <div class="${properties.kcFormOptionsWrapperClass!}">
                                                <#if realm.resetPasswordAllowed>
                                                    <span><a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                                                </#if>
                                            </div>

                                        </div>

                                        <div id="kc-form-buttons" class="${properties.kcFormGroupClass!}">
                                            <input type="hidden" id="id-hidden-input" name="credentialId" <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>
                                            <input tabindex="4" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="login" id="kc-login" type="submit" value="${msg("doLogIn")}"/>
                                        </div>
                                    </div>
                                    <span>${msg("noAccount")} <a tabindex="6" href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                                </form>
                            </#if>
                            <#list social.providers as p>
                                <li class="${properties.kcFormSocialAccountListLinkClass!}"><a href="${p.loginUrl}" id="zocial-${p.alias}" class="${p.providerId}">
                                    <#-- show icons for IdPs -->
                                    <div class="icon icon-${p.alias}"></div>
                                    <span>${p.displayName}</span></a>
                                </li>
                            </#list>
                        </ul>
                    </div>
                </#if>
            </div>
        </div>

        <@passkeys.conditionalUIData />
        <script type="module" src="${url.resourcesPath}/js/passwordVisibility.js"></script>
    <#elseif section = "info" >
        <#if realm.displayNameHtml != "master">
            <div id="info-messages">
                ${kcSanitize(msg((realm.displayNameHtml!'')))?no_esc}
            </div>
        </#if>
        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div id="kc-registration-container">
                <div id="kc-registration">
                    <span>${msg("noAccount")} <a tabindex="8"
                                                 href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                </div>
            </div>
        </#if>
    <#elseif section = "socialProviders" >
        <#if realm.password && social?? && social.providers?has_content>
            <div id="kc-social-providers" class="${properties.kcFormSocialAccountSectionClass!}">
                <hr/>
                <h2>${msg("identity-provider-login-label")}</h2>

                <ul class="${properties.kcFormSocialAccountListClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountListGridClass!}</#if>">
                    <#list social.providers as p>
                        <li>
                            <a data-once-link data-disabled-class="${properties.kcFormSocialAccountListButtonDisabledClass!}" id="social-${p.alias}"
                                    class="${properties.kcFormSocialAccountListButtonClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountGridItem!}</#if>"
                                    type="button" href="${p.loginUrl}">
                                <#if p.iconClasses?has_content>
                                    <i class="${properties.kcCommonLogoIdP!} ${p.iconClasses!}" aria-hidden="true"></i>
                                    <span class="${properties.kcFormSocialAccountNameClass!} kc-social-icon-text">${p.displayName!}</span>
                                <#else>
                                    <span class="${properties.kcFormSocialAccountNameClass!}">${p.displayName!}</span>
                                </#if>
                            </a>
                        </li>
                    </#list>
                </ul>
            </div>
        </#if>
    </#if>

</@layout.registrationLayout>
