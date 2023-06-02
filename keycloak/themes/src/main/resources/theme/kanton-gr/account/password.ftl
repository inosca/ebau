<#import "template.ftl" as layout>
<@layout.mainLayout active='password' bodyClass='password'; section>

    <div class="row">
        <h2>${msg("changePasswordHtmlTitle")}</h2>
        <div class="col-md-2 subtitle">
            <span class="subtitle">${msg("allFieldsRequired")}</span>
        </div>
    </div>

    <form action="${url.passwordUrl}" class="form-horizontal" method="post">
        <input type="text" id="username" name="username" value="${(account.username!'')}" autocomplete="username" readonly="readonly" style="display:none;">

        <#if password.passwordSet>
            <div class="uk-margin">
                <label for="password" class="uk-form-label">${msg("password")}</label>
                <input type="password" class="${properties.kcInputClass!}" id="password" name="password" autofocus autocomplete="current-password">
            </div>
        </#if>

        <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">

        <div class="uk-margin">
            <label for="password-new" class="uk-form-label">${msg("passwordNew")}</label>
            <input type="password" class="${properties.kcInputClass!}" id="password-new" name="password-new" autocomplete="new-password">
        </div>

        <div class="uk-margin">
            <label for="password-confirm" class="uk-form-label" class="two-lines">${msg("passwordConfirm")}</label>
            <input type="password" class="${properties.kcInputClass!}" id="password-confirm" name="password-confirm" autocomplete="new-password">
        </div>

        <div class="form-group">
            <div id="kc-form-buttons" class="col-md-offset-2 col-md-10 submit">
                <div class="">
                    <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}" name="submitAction" value="Save">${msg("doSave")}</button>
                </div>
            </div>
        </div>
    </form>

</@layout.mainLayout>
