<#import "template.ftl" as layout>
<@layout.mainLayout active='totp' bodyClass='totp'; section>

    <h2>${msg("authenticatorTitle")}</h2>

    <#if totp.enabled>
        <table class="uk-table uk-table-divider">
            <thead>
            <#if totp.otpCredentials?size gt 1>
                <tr>
                    <th colspan="4">${msg("configureAuthenticators")}</th>
                </tr>
            <#else>
                <tr>
                    <th colspan="3">${msg("configureAuthenticators")}</th>
                </tr>
            </#if>
            </thead>
            <tbody>
            <#list totp.otpCredentials as credential>
                <tr>
                    <td class="provider">${msg("mobile")}</td>
                    <#if totp.otpCredentials?size gt 1>
                        <td class="provider">${credential.id}</td>
                    </#if>
                    <td class="provider">${credential.userLabel!}</td>
                    <td class="uk-text-right">
                        <form action="${url.totpUrl}" method="post" class="form-inline">
                            <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">
                            <input type="hidden" id="submitAction" name="submitAction" value="Delete">
                            <input type="hidden" id="credentialId" name="credentialId" value="${credential.id}">
                            <button id="remove-mobile" class="uk-button uk-button-link">Löschen</button>
                        </form>
                    </td>
                </tr>
            </#list>
            </tbody>
        </table>
    <#else>

    <ol class="uk-list uk-list-decimal">
        <li>
            <p>${msg("totpStep1")}</p>

            <ul class="uk-list uk-list-disc uk-list-collapse">
                <#list totp.supportedApplications as app>
                    <li>${msg(app)}</li>
                </#list>
            </ul>
        </li>

        <#if mode?? && mode = "manual">
            <li>
                <p>${msg("totpManualStep2")}</p>
                <p class="uk-text-bold"><span id="kc-totp-secret-key">${totp.totpSecretEncoded}</span></p>
                <p><a href="${totp.qrUrl}" id="mode-barcode">${msg("totpScanBarcode")}</a></p>
            </li>
            <li>
                <p>${msg("totpManualStep3")}</p>
                <ul>
                    <li id="kc-totp-type">${msg("totpType")}: ${msg("totp." + totp.policy.type)}</li>
                    <li id="kc-totp-algorithm">${msg("totpAlgorithm")}: ${totp.policy.getAlgorithmKey()}</li>
                    <li id="kc-totp-digits">${msg("totpDigits")}: ${totp.policy.digits}</li>
                    <#if totp.policy.type = "totp">
                        <li id="kc-totp-period">${msg("totpInterval")}: ${totp.policy.period}</li>
                    <#elseif totp.policy.type = "hotp">
                        <li id="kc-totp-counter">${msg("totpCounter")}: ${totp.policy.initialCounter}</li>
                    </#if>
                </ul>
            </li>
        <#else>
            <li>
                <p>${msg("totpStep2")}</p>
                <p><img src="data:image/png;base64, ${totp.totpSecretQrCode}" alt="Figure: Barcode"></p>
                <p><a href="${totp.manualUrl}" id="mode-manual">${msg("totpUnableToScan")}</a></p>
            </li>
        </#if>
        <li>
            <p>${msg("totpStep3")}</p>
            <p>${msg("totpStep3DeviceName")}</p>
        </li>
    </ol>

    <form action="${url.totpUrl}" class="form-horizontal" method="post">
        <input type="hidden" id="stateChecker" name="stateChecker" value="${stateChecker}">
        <div class="form-group">
            <div class="uk-margin">
                <label for="totp" class="uk-form-label">${msg("authenticatorCode")}</label> <span class="uk-text-danger">*</span>
                <input type="text" class="${properties.kcInputClass!}" id="totp" name="totp" autocomplete="off" autofocus>
                <input type="hidden" id="totpSecret" name="totpSecret" value="${totp.totpSecret}"/>
            </div>


        </div>

        <div class="form-group" ${messagesPerField.printIfExists('userLabel',properties.kcFormGroupErrorClass!)}">
            <div class="uk-margin">
                <label for="userLabel" class="uk-form-label">${msg("totpDeviceName")}</label> <#if totp.otpCredentials?size gte 1><span class="required">*</span></#if>
                <input type="text" class="${properties.kcInputClass!}" id="userLabel" name="userLabel" autocomplete="off">
            </div>
        </div>

        <div class="form-group">
            <div id="kc-form-buttons" class="col-md-offset-2 col-md-10 submit">
                <div class="">
                    <button type="submit"
                            class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonLargeClass!}"
                            id="saveTOTPBtn" name="submitAction" value="Save">${msg("doSave")}
                    </button>
                    <button type="submit"
                            class="${properties.kcButtonClass!} ${properties.kcButtonDefaultClass!} ${properties.kcButtonLargeClass!}"
                            id="cancelTOTPBtn" name="submitAction" value="Cancel">${msg("doCancel")}
                    </button>
                </div>
            </div>
        </div>
    </form>
    </#if>

</@layout.mainLayout>
