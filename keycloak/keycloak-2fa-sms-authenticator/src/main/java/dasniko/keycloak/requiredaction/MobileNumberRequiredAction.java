package dasniko.keycloak.requiredaction;

import java.util.logging.Logger;
import jakarta.ws.rs.core.MultivaluedMap;
import jakarta.ws.rs.core.Response;
import org.keycloak.authentication.InitiatedActionSupport;
import org.keycloak.authentication.RequiredActionContext;
import org.keycloak.authentication.RequiredActionProvider;
import org.keycloak.forms.login.LoginFormsProvider;
import org.keycloak.models.RealmModel;
import org.keycloak.models.UserModel;
import org.keycloak.models.utils.FormMessage;
import org.keycloak.services.validation.Validation;

import dasniko.keycloak.authenticator.SmsAuthenticator;

import java.util.function.Consumer;
import java.io.IOException;
import java.util.Map;

/**
 * @author Niko Köbler, https://www.n-k.de, @dasniko
 */
public class MobileNumberRequiredAction implements RequiredActionProvider {
	private static final Logger log = Logger.getLogger(MobileNumberRequiredAction.class.getName());

	public static final String PROVIDER_ID = "mobile-number-ra";

	private static final String MOBILE_NUMBER_FIELD = "mobile_number";

	@Override
	public InitiatedActionSupport initiatedActionSupport() {
		return InitiatedActionSupport.SUPPORTED;
	}

	@Override
	public void evaluateTriggers(RequiredActionContext context) {
		String verifiedMobileNr = context.getUser().getFirstAttribute("verifiedMobileNr");
		if (context.getUser().getFirstAttribute(MOBILE_NUMBER_FIELD) == null || verifiedMobileNr == null
				|| !verifiedMobileNr.equals("true")) {
			context.getUser().addRequiredAction(PROVIDER_ID);
			context.getAuthenticationSession().addRequiredAction(PROVIDER_ID);
		}
	}

	@Override
	public void requiredActionChallenge(RequiredActionContext context) {
		// show initial form
		context.challenge(createForm(context, null));
	}

	@Override
	public void processAction(RequiredActionContext context) {
		// submitted form

		UserModel user = context.getUser();

		MultivaluedMap<String, String> formData = context.getHttpRequest().getDecodedFormParameters();
		String mobileNumber = formData.getFirst(MOBILE_NUMBER_FIELD);
		String code = formData.getFirst("code");

		if (Validation.isBlank(mobileNumber) || mobileNumber.length() < 5) {
			context.challenge(createForm(context, form -> form.addError(new FormMessage(
					MOBILE_NUMBER_FIELD,
					"setupInvalidMobileNr"))));
			return;
		}

		if (user.getFirstAttribute("code") == null || Validation.isBlank(code)) {
			RealmModel realm = context.getRealm();
			Map<String, String> config = realm.getAuthenticatorConfigByAlias("SMS auth").getConfig();

			String generatedCode;
			try {
				generatedCode = SmsAuthenticator.codeChallenge(
						config,
						context.getSession(),
						context.getSession().getContext().resolveLocale(user),
						mobileNumber);
				user.setSingleAttribute(MOBILE_NUMBER_FIELD, mobileNumber);
				user.setSingleAttribute("code", generatedCode);
				context.challenge(createForm(context, form -> {
					form.addSuccess(new FormMessage("code", "smsAuthCodeSent"));
					form.setAttribute("codeSent", true);
					form.setAttribute(MOBILE_NUMBER_FIELD, mobileNumber == null ? "" : mobileNumber);
				}));
			} catch (IOException e) {
				log.log(java.util.logging.Level.WARNING, "error sending code", e);
				context.challenge(createForm(context, form -> {
					form.addError(new FormMessage("code",
							"setupAuthCodeNotSent"));
					form.setAttribute(MOBILE_NUMBER_FIELD, mobileNumber == null ? "" : mobileNumber);
				}));
			}
			return;
		}

		if (!code.equals(user.getFirstAttribute("code"))) {
			context.challenge(createForm(context, form -> {
				form.addError(new FormMessage("code", "smsAuthCodeInvalid"));
				form.setAttribute("codeSent", true);
				form.setAttribute(MOBILE_NUMBER_FIELD, mobileNumber == null ? "" : mobileNumber);
			}));
			return;
		}

		user.setSingleAttribute("verifiedMobileNr", "true");
		user.removeAttribute("code");
		user.removeRequiredAction(PROVIDER_ID);
		context.getAuthenticationSession().removeRequiredAction(PROVIDER_ID);

		context.success();
	}

	@Override
	public void close() {
	}

	private Response createForm(RequiredActionContext context, Consumer<LoginFormsProvider> formConsumer) {
		LoginFormsProvider form = context.form();
		form.setAttribute("username", context.getUser().getUsername());

		String mobileNumber = context.getUser().getFirstAttribute(MOBILE_NUMBER_FIELD);
		form.setAttribute(MOBILE_NUMBER_FIELD, mobileNumber == null ? "" : mobileNumber);

		if (formConsumer != null) {
			formConsumer.accept(form);
		}

		return form.createForm("update-mobile-number.ftl");
	}

}
