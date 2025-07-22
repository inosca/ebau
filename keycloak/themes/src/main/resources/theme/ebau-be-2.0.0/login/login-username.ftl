<#import "template.ftl" as layout>
    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username') hideOtherWays=true displayInfo=(realm.password && realm.registrationAllowed && !registrationDisabled??); section>
        <#if section="header">
            ${msg("loginAccountTitle")}
            <#elseif section="form">
                <#if realm.password && realm.loginWithEmailAllowed>
                    <form class="sign-in-form" id="kc-form-login" onsubmit="login.disabled = true; return true;"
                        action="${url.loginAction}" method="post">
                        <div class="usernameField">
                            <#if usernameEditDisabled??>
                                <input type="text" name="username" id="username" tabindex="1" disabled placeholder="Benutzername / Nom d'utilisateur"
                                    value="${(login.username!'')}" /><br />
                                <#else>
                                    <input type="text" name="username" id="username" tabindex="1" autofocus placeholder="Benutzername / Nom d'utilisateur"
                                        autocomplete="off"
                                        value="${(login.username!'')}" /><br />
                            </#if>
                        </div>
                        <button tabindex="4" name="login" id="kc-login" class="sign-in-button" type="submit" value="${msg('doLogIn')}">
                            <span>Anmelden</span>
                            <div class="sign-in-icon"></div>
                        </button>
                        <div class="additionalOptions">
                            <#if realm.rememberMe && !usernameEditDisabled??>
                                <div class="rememberMe">
                                    <label>
                                        <#if login.rememberMe??>
                                            <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"
                                                checked>
                                            ${msg("rememberMe")}
                                            <#else>
                                                <input tabindex="3" id="rememberMe" name="rememberMe"
                                                    type="checkbox">
                                                ${msg("rememberMe")}
                                        </#if>
                                    </label>
                                </div>
                            </#if>
                            <div class="optionLinks">
                                <#if realm.resetPasswordAllowed>
                                    <div class="passwordReset">
                                        <a tabindex="5"
                                            href="${url.loginResetCredentialsUrl}">
                                            <#-- ${msg("doForgotPassword")} -->
                                                <span class="german-text">Passwort vergessen</span>/<span class="french-text">S'inscrire à nouveau</span>
                                        </a>
                                    </div>
                                </#if>
                                <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
                                    <div id="kc-registration">
                                        <a tabindex="6" href="${url.registrationUrl}">
                                            <span class="german-text">Neu registrieren</span>/<span class="french-text">Mot de passe oubilé</span>
                                        </a>
                                    </div>
                                </#if>
                            </div>
                        </div>
                    </form>
                </#if>
                <#elseif section="info">
                    <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
                        <div id="kc-registration">
                            <span>
                                ${msg("noAccount")}
                                <a tabindex="6" href="${url.registrationUrl}">
                                    ${msg("doRegister")}
                                </a></span>
                        </div>
                    </#if>
                    <#elseif section="socialProviders">
                        <#if auth.authenticationSelections?filter(a -> a.authenticationExecution.authenticator == 'webauthn-authenticator-passwordless')?first??>
                            <#assign passwordless=auth.authenticationSelections?filter(a -> a.authenticationExecution.authenticator == 'webauthn-authenticator-passwordless')?first>
                        </#if>
                        <#if social?? && social.providers??>
                            <#assign socialProviders=social.providers?filter(p -> p.alias != 'linkyard-support')>
                                <#assign hasAnySocial=(socialProviders?? && socialProviders?size> 0) || passwordless??>
                                    <#else>
                                        <#assign hasAnySocial=false>
                        </#if>
                        <#if hasAnySocial>
                            <#if passwordless??>
                                <#-- Stupid, but we need the form across all buttons or the layout gets weird -->
                                    <form id="kc-select-credential-form" action="${url.loginAction}" method="post">
                            </#if>
                            <div class="one-click-login">
                                <#-- IdPs -->
                                    <#list socialProviders as p>
                                        <div class="button-wrapper">
                                            <button type="button" onclick="window.location='${p.loginUrl}'; return false;" id="zocial-${p.alias}">
                                                <span>
                                                    ${p.displayName}
                                                </span></button>
                                        </div>
                                    </#list>
                                    <#-- passwordless login -->
                                        <#if passwordless??>
                                            <input type="hidden" name="authenticationExecution" value="${passwordless.authExecId}" />
                                            <button type="submit">
                                                ${msg("webauthn-passwordless-display-name")}
                                            </button>
                                        </#if>
                            </div>
                            <#if passwordless??>
                                </form>
                            </#if>
                            <#elseif passwordless??>
                                <#-- Only passwordless -->
                                    <div class="one-click-login-title">Login with</div>
                                    <form id="kc-select-credential-form" action="${url.loginAction}" method="post">
                                        <div class="one-click-login">
                                            <input type="hidden" name="authenticationExecution" value="${passwordless.authExecId}" />
                                            <button type="submit">
                                                ${msg("webauthn-passwordless-display-name")}
                                            </button>
                                        </div>
                                    </form>
                        </#if>
                        <#if realm.password && realm.loginWithEmailAllowed && (passwordless?? || hasAnySocial)>
                            <p class="separator">OR</p>
                        </#if>
        </#if>
    </@layout.registrationLayout>