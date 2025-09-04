<#import "template.ftl" as layout>
    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username') displayInfo=(realm.password &&
        realm.registrationAllowed && !registrationDisabled??); section>
        <div class="login-helpertext">
            <p>hint</p>
            <p>${msg("loginProviderHint")}</p>
        </div>
        <#if section="header">
            <p>header</p>
            ${msg("loginAccountTitle")}
        <#elseif section="form">
            <form id="kc-form-login" class="${properties.kcFormClass!}"
                onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                <fieldset>
                    <#if realm.password && social.providers??>
                        <div id="kc-social-providers">
                            <div id="kc-social-providers-buttons">
                                <#list social.providers as p>
                                    <div>
                                        <button type="button"
                                            onclick="window.location='${p.loginUrl}'; return false;"
                                            id="zocial-${p.alias}">
                                            <span>
                                                <#if msg(p.alias)=p.alias>
                                                    ${msg(p.displayName)}
                                                    <#else>
                                                        ${msg(p.alias)}
                                                </#if>
                                            </span>
                                        </button>
                                    </div>
                                </#list>
                            </div>
                        </div>
                    </#if>
                </fieldset>
            </form>
        </#if>
    </@layout.registrationLayout>
