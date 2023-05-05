<#import "template-be.ftl" as layout>
<@layout.registrationLayout displayInfo=social.displayInfo; section>
<#if section = "title">
    ${msg("loginTitle",(realm.displayName!''))}
<#elseif section = "form">
    <form id="kc-form-login" class="${properties.kcFormClass!}" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
        <fieldset>
            <legend>${msg("login")}</legend>
            <#if realm.password && social.providers??>
                <div id="kc-social-providers">
                    <div id="kc-social-providers-buttons">
                        <#list social.providers as p>
                        <div>
                            <a href="${p.loginUrl}" class="zocial ${p.providerId}">
                                <#if msg(p.alias) = p.alias>
                                    ${msg(p.displayName)}
                                <#else>
                                    ${msg(p.alias)}
                                </#if>
                            </a>
                        </div>
                        </#list>
                    </div>
                </div>
            </#if>
        </fieldset>
        <div class="row kc-basic-password-login" style="display: none;">
            <input class="submit primary" name="submit" value="${msg("doLogIn")}" type="submit">
        </div>
    </form>
</#if>
</@layout.registrationLayout>
