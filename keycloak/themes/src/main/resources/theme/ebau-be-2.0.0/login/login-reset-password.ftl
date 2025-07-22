<#import "template.ftl" as layout>
    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username'); section>
        <#if section="header">
            ${msg("resetPasswordTitle")}
            <#elseif section="form">
                <form id="kc-reset-password-form" class="form-horizontal" action="${url.loginAction}" method="post">
                    <div class="form-group">
                        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                            <#-- <label for="username" class="pf-c-form__label pf-c-form__label-text">
                                ${msg("usernameOrEmail")}
                                </label> -->
                        </div>
                        <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                            <input type="text" id="username" name="username" class="pf-c-form-control" autofocus value="" aria-invalid="" placeholder="Benutzername oder E-Mail / Nom d'utilisateur ou courriel">
                        </div>
                    </div>
                    <div class=" form-group login-pf-settings">
                        <div id="kc-form-options" class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                            <div class="back-to-login">
                                <a href="${url.loginUrl}">
                                    <#-- « ${msg("backToLogin")} -->
                                        <span class="german-text">Zurück zur Anmeldung</span>/<span class="french-text">Retour au login</span>
                                </a>
                            </div>
                        </div>
                        <div id="kc-form-buttons" class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                            <input class="pf-c-button pf-m-primary pf-m-block btn-lg" type="submit" value="${msg('doSubmit')}">
                        </div>
                    </div>
                </form>
                <#elseif section="info">
                    <p>
                        ${msg("emailInstruction")}
                    </p>
        </#if>
    </@layout.registrationLayout>