<#-- Copied from: https://github.com/keycloak/keycloak/blob/release/26.2/themes/src/main/resources/theme/base/login/login.ftl -->
<#import "template.ftl" as layout>
    <@layout.registrationLayout pageId="login" displayMessage=!messagesPerField.existsError('username') displayInfo=(realm.password &&
        realm.registrationAllowed && !registrationDisabled??); section>
        <#if section="header">
            ${msg("loginHeading")}
        </#if>
        <#if section="form">
            <div class="login-helpertext">
                <p>${msg("loginProviderHint")}</p>
            </div>
            <form id="kc-form-login" class="${properties.kcFormClass!}" onsubmit="login.disabled = true; return true;"
                action="${url.loginAction}" method="post">
                <fieldset>
                    <#if realm.password && social.providers??>
                        <div id="kc-social-providers">
                            <div id="kc-social-providers-buttons">
                                <#list social.providers as p>
                                    <button type="button" class="secondary"
                                        onclick="window.location='${p.loginUrl}'; return false;" id="social-${p.alias}">
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
        <#if section="context">
            <ul class='box-beige open' data-accordion data-allow-all-closed='true' data-multi-expand='false'>
                <li class="default infobox-wrapper is-active" data-accordion-item>
                    <h4 class="infobox-title">${msg("loginFaqHeading")}</h4>
                    <div class="accordion-content" data-tab-content>
                        <hr class="accordion">
                        ${kcSanitize(msg("loginFaqContent"))?no_esc}
                        <div class='arrow-link'>
                            <span class='link-arrow'></span>
                            <a class='text-link-2' href="${msg('loginFaqLinkTarget')}">${msg("loginFaqLinkText")}</a>
                        </div>
                    </div>
                </li>
            </ul>
        </#if>
    </@layout.registrationLayout>
