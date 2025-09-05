<#import "template.ftl" as layout>
    <@layout.registrationLayout displayMessage=!messagesPerField.existsError('username') displayInfo=(realm.password &&
        realm.registrationAllowed && !registrationDisabled??); section>
        <div class="login-helpertext">
            <p>${msg("loginProviderHint")}</p>
        </div>
        <#if section="form">
            <form id="kc-form-login" class="${properties.kcFormClass!}"
                onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                <fieldset>
                    <#if realm.password && social.providers??>
                        <div id="kc-social-providers">
                            <div id="kc-social-providers-buttons">
                                <#list social.providers as p>
                                    <button
                                        type="button"
                                        class="secondary"
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
                                </#list>
                            </div>
                        </div>
                    </#if>
                </fieldset>
            </form>
        </#if>
    </@layout.registrationLayout>
