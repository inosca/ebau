<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=social.displayInfo isLogin=true displayWide=(realm.password && social.providers??); section>
    <#if section = "form">
    <div id="kc-form" <#if realm.password && social.providers??>class="${properties.kcContentWrapperClass!}"</#if>>
      <div id="kc-form-wrapper" <#if realm.password && social.providers??>class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}"</#if>>
        <#if realm.password>
            <div id="kc-social-providers" class="${properties.kcFormSocialAccountContentClass!} ${properties.kcFormSocialAccountClass!}">
                <ul class="${properties.kcFormSocialAccountListClass!}">
                    <#if realm.password>
                        <div id="kc-welcome-login" class="kc-form-card is-login-form uk-form-horizontal uk-width-xlarge uk-margin-small-right">
                            <h1>${msg("loginWelcomeHeader")}</h1>
                            ${msg("loginWelcomeText")?no_esc}

                            <h2>Anleitungen</h2>
                            <p>
                                Für Gesuchsteller, Planer und interessierte Dritte:
                                <br /><a href="${url.resourcesPath}/pdf/Registrierung_Bürgerportal_eBau_v1.0-1.pdf">"Anleitung Registrierung auf Bürgerportal eBau"</a>
                                <br /><a href="${url.resourcesPath}/pdf/Anleitungen_für_Baugesuche_im_Grundwasserschutz_und_Erdwärmenutzung.pdf">"Anleitungen für Baugesuche im Grundwasserschutz und Erdwärmenutzung"</a>
                            </p>
                            <p>
                                Für Behörden:
                                <br /><a href="${url.resourcesPath}/pdf/Anleitung_Behördenportal_eBau_v3.0-1.pdf">"Anleitung Behördenportal"</a>
                                <br /><a href="${url.resourcesPath}/pdf/Anleitung_GWR-Modul_v1.0.pdf">"Anleitung zum GWR-Modul"</a>
                                <br /><a href="${url.resourcesPath}/pdf/Registrierung_Behördenportal_eBau_v3.0.pdf">"Anleitung Registrierung auf Behördenportal eBau"</a>
                                <br /><a href="${url.resourcesPath}/pdf/Anleitung_eBau_Vorlagenerstellung_220706-1.pdf">"Anleitung zur Erstellung von Dokumentenvorlagen"</a>
                            </p>
                        </div>
                        <form id="kc-form-login" class="kc-form-card is-login-form uk-form-horizontal uk-width-xlarge" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                            <h1>Anmeldung</h1>
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
                            ${msg("loginLoginHelpText")?no_esc}
                        </form>
                    </#if>
                </ul>
            </div>
        </#if>

        </div>
      </div>
    </#if>

</@layout.registrationLayout>
