<#-- adapted from https://github.com/keycloak/keycloak/blob/main/themes/src/main/resources/theme/base/login/login.ftl -->
<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=social.displayInfo isLogin=true displayWide=(realm.password && social.providers??); section>
    <#if section = "form">
    <#if realm.displayNameHtml != "master">
        <div id="info-messages">
            ${kcSanitize(msg((realm.displayNameHtml!'')))?no_esc}
        </div>
    </#if>
    <div id="kc-form" <#if realm.password>class="${properties.kcContentWrapperClass!}"</#if>>
      <div id="kc-form-wrapper" <#if realm.password>class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}"</#if>>
        <#-- Custom order: social providers appear later in DOM in base theme -->
        <#if realm.password??>
            <div id="kc-social-providers" class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}">
                <ul class="${properties.kcFormSocialAccountListClass!}">
                    <#-- "pseudo"-IdP: local login -->
                    <#if realm.password>
                        <div class="kc-form-card is-login-form uk-form-horizontal uk-width-xlarge uk-margin-small-right">
                            <h2 class="uk-margin-top">
                                ${msg("welcomeHeader")}
                            </h2>
                            <p>
                                ${msg("welcomeText")?no_esc}
                            </p>
                            <p>
                                <strong>${msg("infoHeader")?no_esc}</strong>
                                ${msg("infoText")?no_esc}
                            </p>
                        </div>
                        <form id="kc-form-login" class="kc-form-card is-login-form uk-form-horizontal uk-width-xlarge uk-margin-auto" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                            <h2 class="uk-margin-top">Anmeldung</h2>
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
                    <#if social.providers??>
                      <#list social.providers as p>
                          <li class="${properties.kcFormSocialAccountListLinkClass!}"><a href="${p.loginUrl}" id="zocial-${p.alias}" class="${p.providerId}">
                              <#-- show icons for IdPs -->
                              <div class="icon icon-gr"></div>
                              <span>${p.displayName}</span></a>
                          </li>
                      </#list>
                    </#if>
                </ul>
            </div>
        </#if>

        </div>
      </div>
    </#if>

</@layout.registrationLayout>
