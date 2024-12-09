<#import "template-be.ftl" as layout>
<@layout.registrationLayout; section>
  <#if section = "title">
    ${msg("loginProfileTitle")}
  <#elseif section = "form">
    <form id="kc-update-profile-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">
        <fieldset>
            <legend>${msg("loginProfileTitle")}</legend>

            <#if user.editUsernameAllowed>
                <div class="hidden row ${messagesPerField.printIfExists('username',properties.kcFormGroupErrorClass!)}" aria-hidden="true">
                    <label for="username" class="${properties.kcLabelClass!}">
                      ${msg("username")}
                      <span class="hidden" aria-hidden="true">Pflichtfeld</span>
                    </label>
                    <input type="text" id="username" name="username" value="${(user.username!'')}" class="text large ${properties.kcInputClass!}"/>
                </div>
            </#if>
            <div class="row ${messagesPerField.printIfExists('email',properties.kcFormGroupErrorClass!)}">
                <label for="email" class="${properties.kcLabelClass!}">
                  ${msg("email")}
                  <span class="hidden" aria-hidden="true">Pflichtfeld</span>
                </label>
                <div class="${properties.kcInputWrapperClass!}">
                    <input type="text" id="email" name="email" value="${(user.email!'')}" class="text large" />
                </div>
            </div>
            <div class="row ${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('firstName',properties.kcFormGroupErrorClass!)}">
                <label for="firstName" class="${properties.kcLabelClass!}">
                  ${msg("firstName")}
                  <span class="hidden" aria-hidden="true">Pflichtfeld</span>
                </label>
                <input type="text" id="firstName" name="firstName" value="${(user.firstName!'')}" class="text large ${properties.kcInputClass!}" />
            </div>
            <div class="row ${properties.kcFormGroupClass!} ${messagesPerField.printIfExists('lastName',properties.kcFormGroupErrorClass!)}">
                <label for="lastName" class="${properties.kcLabelClass!}">
                  ${msg("lastName")}
                  <span class="hidden" aria-hidden="true">Pflichtfeld</span>
                </label>
                <div class="${properties.kcInputWrapperClass!}">
                    <input type="text" id="lastName" name="lastName" value="${(user.lastName!'')}" class="text large ${properties.kcInputClass!}" />
                </div>
            </div>
        </fieldset>
        <div class="${properties.kcFormGroupClass!}">
            <div id="kc-form-options" class="row ${properties.kcFormOptionsClass!}">
                <div class="${properties.kcFormOptionsWrapperClass!}">
                </div>
            </div>

            <div id="kc-form-buttons" class="row ${properties.kcFormButtonsClass!}">
                <input class="submit primary ${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}" type="submit" value="${msg("doSubmit")}" />
            </div>
        </div>
  </form>
  </#if>
</@layout.registrationLayout>