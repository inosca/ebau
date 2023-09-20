<#import "template.ftl" as layout>
<@layout.mainLayout active='password' bodyClass='password'; section>
    <h2>${msg("changePasswordHtmlTitle")}</h2>

    <form action="${url.passwordUrl}" class="form-horizontal" method="post">
        <#if password.passwordSet>
            <div class="uk-margin">
                <label for="password" class="uk-form-label">${msg("password")} <span class="uk-text-danger">*</span></label>
                <input type="password" class="${properties.kcInputClass!}" id="password" name="password" autofocus autocomplete="current-password">
            </div>
        </#if>

        <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">

        <div class="uk-margin">
            <label for="password-new" class="uk-form-label">${msg("passwordNew")} <span class="uk-text-danger">*</span></label>
            <input type="password" class="${properties.kcInputClass!}" id="password-new" name="password-new" autocomplete="new-password">
        </div>

        <div class="uk-margin">
            <label for="password-confirm" class="uk-form-label" class="two-lines">${msg("passwordConfirm")} <span class="uk-text-danger">*</span></label>
            <input type="password" class="${properties.kcInputClass!}" id="password-confirm" name="password-confirm" autocomplete="new-password">
        </div>

        <div class="uk-margin">
            <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}" name="submitAction" value="Save">${msg("doSave")}</button>
        </div>
    </form>
</@layout.mainLayout>
