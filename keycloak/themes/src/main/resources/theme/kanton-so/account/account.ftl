<#import "template.ftl" as layout>

<@layout.mainLayout active='account' bodyClass='user'; section>
    <h2>${msg("editAccountHtmlTitle")}</h2>

    <form action="${url.accountUrl}" class="form-horizontal" method="post">

        <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">

        <#if !realm.registrationEmailAsUsername>
            <div class="uk-margin">
                <label for="username" class="uk-form-label">${msg("username")}</label> <#if realm.editUsernameAllowed><span class="uk-text-danger">*</span></#if>
                <input type="text" class="${properties.kcInputClass!}" id="username" name="username" <#if !realm.editUsernameAllowed>disabled="disabled"</#if> autofocus value="${(account.username!'')}"/>
            </div>
        </#if>

        <div class="uk-margin">
            <label for="email" class="uk-form-label">${msg("email")}</label> <span class="uk-text-danger">*</span>
            <input type="text" class="${properties.kcInputClass!}" id="email" name="email" autofocus value="${(account.email!'')}"/>
        </div>

        <div class="uk-margin">
            <label for="firstName" class="uk-form-label">${msg("firstName")}</label> <span class="uk-text-danger">*</span>
            <input type="text" class="${properties.kcInputClass!}" id="firstName" name="firstName" value="${(account.firstName!'')}"/>
        </div>

        <div class="uk-margin">
            <label for="lastName" class="uk-form-label">${msg("lastName")}</label> <span class="uk-text-danger">*</span>
            <input type="text" class="${properties.kcInputClass!}" id="lastName" name="lastName" value="${(account.lastName!'')}"/>
        </div>

        <div class="uk-margin">
            <#if url.referrerURI??><a href="${url.referrerURI}">${kcSanitize(msg("backToApplication")?no_esc)}</a></#if>
            <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}" name="submitAction" value="Save">${msg("doSave")}</button>
            <button type="submit" class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonLargeClass!}" name="submitAction" value="Cancel">${msg("doCancel")}</button>
        </div>
    </form>
</@layout.mainLayout>
