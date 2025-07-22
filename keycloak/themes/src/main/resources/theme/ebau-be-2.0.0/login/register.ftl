<#import "template.ftl" as layout>
    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username'); section>
        <#if section="header">
            ${msg("registerTitle")}
            <#elseif section="form">
                <form id="kc-register-form" class="form-horizontal" action="${url.registrationAction}" method="post">
                    <div class="form-group">
                        <div class="col-xs-12">
                            <#-- <label for="firstName" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("firstName")}
                                </label> -->
                                <input type="text" id="firstName" class="pf-c-form-control" name="firstName" value="${(register.formData.firstName!'')}" aria-invalid=""
                                    placeholder="Vorname / Prénom">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-xs-12">
                            <#-- <label for="lastName" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("lastName")}
                                </label> -->
                                <input type="text" id="lastName" class="pf-c-form-control" name="lastName" value="${(register.formData.lastName!'')}" aria-invalid="" placeholder="Nachname / Nom de famille">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-xs-12">
                            <#-- <label for="email" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("email")}
                                </label> -->
                                <input type="text" id="email" class="pf-c-form-control" name="email" value="${(register.formData.email!'')}" autocomplete="email" aria-invalid="" placeholder="E-Mail / Courriel">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-xs-12">
                            <#-- <label for="username" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("username")}
                                </label> -->
                                <input type="text" id="username" class="pf-c-form-control" name="username" value="${(register.formData.username!'')}" autocomplete="username" aria-invalid="" placeholder="Benutzername / Nom d'utilisateur">
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-xs-12 passwordField">
                            <#-- <label for="password" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("password")}
                                </label> -->
                                <input type="password" id="password" class="pf-c-form-control" name="password" autocomplete="new-password" aria-invalid="" placeholder="Passwort / Mot de passe">
                                <div id="passwordIcon"></div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-xs-12, passwordField">
                            <#-- <label for="password-confirm" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("passwordConfirm")}
                                </label> -->
                                <input type="password" id="password-confirm" class="pf-c-form-control" name="password-confirm" aria-invalid="" placeholder="Passwort bestätigen / Confirmer le mot de passe">
                                <div id="passwordConfirmIcon"></div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div id="kc-form-options" class="col-xs-12">
                            <#-- <span><a href="${url.loginUrl}">« ${msg("backToLogin")}
                                </a></span> -->
                                <a href="${url.loginUrl}">
                                    <#-- « ${msg("backToLogin")} -->
                                        <span class="german-text">Zurück zur Anmeldung</span>/<span class="french-text">Retour au login</span>
                                </a>
                        </div>
                        <div id="kc-form-buttons" class="col-xs-12">
                            <input class="pf-c-button pf-m-primary pf-m-block btn-lg" type="submit" value="${msg('doRegister')}">
                        </div>
                    </div>
                </form>
                <#elseif section="info">
                    <p>
                        ${msg("registerInstructions")}
                    </p>
        </#if>
    </@layout.registrationLayout>