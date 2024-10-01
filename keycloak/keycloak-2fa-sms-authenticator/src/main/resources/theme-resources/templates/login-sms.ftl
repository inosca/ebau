<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=true; section>
	<#if section = "show-username">
		<h1>${msg("smsAuthTitle", realm.displayName)}</h1>
	<#elseif section = "form">
		<form id="kc-sms-code-login-form" class="${properties.kcFormClass!}" action="${url.loginAction}" method="post">
			<div class="${properties.kcFormGroupClass!}">
				<div class="${properties.kcLabelWrapperClass!}">
					<label for="code" class="${properties.kcLabelClass!}">${msg("smsAuthLabel")}</label>
				</div>
				<div class="${properties.kcInputWrapperClass!}">
					<input type="text" id="code" name="code" class="${properties.kcInputClass!}" autofocus/>
					<span class="uk-text-small uk-text-muted">${msg("smsAuthInstruction")}</span>
				</div>
			</div>
			<div class="${properties.kcFormGroupClass!} uk-flex-right">
				<div id="kc-form-buttons" class="${properties.kcFormButtonsClass!}">
					<input class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" type="submit" value="${msg("doSubmit")}"/>
				</div>
			</div>
		</form>
	</#if>
</@layout.registrationLayout>
