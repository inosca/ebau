<#macro content pageId="">
    <footer class="footer-container">
        <div class="inner">
            <div class="footer-nav">
                <#list ["Department","Contact","Privacy","Impressum"] as site>
                    <#if msg("nav"+site) !="nav" + site && msg("nav"+site)?has_content>
                        <a href="${msg('nav'+site+'Link')}" class="service-menue">${msg("nav"+site)}</a>
                    </#if>
                </#list>
            </div>
            <span class="copyright">© ${msg("copyright")}</span>
        </div>
    </footer>
</#macro>
