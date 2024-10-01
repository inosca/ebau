package dasniko.keycloak.authenticator;

import java.util.Map;
import java.io.IOException;
import java.util.Locale;
import java.util.logging.Logger;

import org.keycloak.authentication.AuthenticationFlowContext;
import org.keycloak.authentication.AuthenticationFlowError;
import org.keycloak.authentication.Authenticator;
import org.keycloak.common.util.SecretGenerator;
import org.keycloak.models.AuthenticationExecutionModel;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.RealmModel;
import org.keycloak.models.UserModel;
import org.keycloak.sessions.AuthenticationSessionModel;
import org.keycloak.theme.Theme;

import dasniko.keycloak.authenticator.gateway.SmsServiceFactory;
import jakarta.ws.rs.core.Response;

/**
 * @author Niko Köbler, https://www.n-k.de, @dasniko
 */
public class SmsAuthenticator implements Authenticator {
	private static final Logger log = Logger.getLogger(SmsAuthenticator.class.getName());

	private static final String MOBILE_NUMBER_FIELD = "mobile_number";
	private static final String TPL_CODE = "login-sms.ftl";

	@Override
	public void authenticate(AuthenticationFlowContext context) {
		Map<String, String> config = context.getRealm().getAuthenticatorConfigByAlias("SMS auth").getConfig();
		KeycloakSession session = context.getSession();
		UserModel user = context.getUser();

		String mobileNumber = user.getFirstAttribute(MOBILE_NUMBER_FIELD);

		try {
			Locale locale = session.getContext().resolveLocale(user);
			String code = codeChallenge(config, session, locale, mobileNumber);
			AuthenticationSessionModel authSession = context.getAuthenticationSession();
			authSession.setAuthNote(SmsConstants.CODE, code);
			int ttl = Integer.parseInt(config.get(SmsConstants.CODE_TTL));
			authSession.setAuthNote(SmsConstants.CODE_TTL,
					Long.toString(System.currentTimeMillis() + (ttl * 1000L)));
			context.challenge(context.form().setAttribute("realm", context.getRealm()).createForm(TPL_CODE));
		} catch (Exception e) {
			log.log(java.util.logging.Level.SEVERE, "error sending code", e);
			context.failureChallenge(AuthenticationFlowError.INTERNAL_ERROR,
					context.form().setError("smsAuthSmsNotSent", e.getMessage())
							.createErrorPage(Response.Status.INTERNAL_SERVER_ERROR));
		}

	}

	public static String codeChallenge(Map<String, String> config, KeycloakSession session, Locale locale,
			String mobileNumber) throws IOException {

		if (locale == null) {
			locale = new Locale("de");
		}
		int len = Integer.parseInt(config.get(SmsConstants.CODE_LENGTH));
		String code = SecretGenerator.getInstance().randomString(len, SecretGenerator.DIGITS);

		Theme theme = session.theme().getTheme(Theme.Type.LOGIN);

		String smsAuthText = theme.getMessages(locale).getProperty("smsAuthText");
		int ttl = Integer.parseInt(config.get(SmsConstants.CODE_TTL));
		String smsText = String.format(smsAuthText, code, Math.floorDiv(ttl, 60));

		SmsServiceFactory.get(config, session).send(mobileNumber, smsText);
		return code;
	}

	@Override
	public void action(AuthenticationFlowContext context) {
		String enteredCode = context.getHttpRequest().getDecodedFormParameters().getFirst(SmsConstants.CODE);

		AuthenticationSessionModel authSession = context.getAuthenticationSession();
		String code = authSession.getAuthNote(SmsConstants.CODE);
		String ttl = authSession.getAuthNote(SmsConstants.CODE_TTL);
		String failedAttemptsString = authSession.getAuthNote(SmsConstants.FAILED_ATTEMPTS);
		Integer failedAttempts = failedAttemptsString == null ? 0 : Integer.parseInt(failedAttemptsString);

		if (code == null || ttl == null) {
			context.failureChallenge(AuthenticationFlowError.INTERNAL_ERROR,
					context.form().createErrorPage(Response.Status.INTERNAL_SERVER_ERROR));
			return;
		}

		// check if user is locked
		String lockedUntil = authSession.getAuthNote(SmsConstants.LOCKED_UNTIL);
		if (lockedUntil != null && Long.parseLong(lockedUntil) > System.currentTimeMillis()) {
			context.failureChallenge(AuthenticationFlowError.USER_TEMPORARILY_DISABLED,
					context.form().setAttribute("realm", context.getRealm())
							.setError("smsAuthCodeInvalid").createForm(TPL_CODE));
			return;
		} else if (lockedUntil != null) {
			authSession.removeAuthNote(SmsConstants.LOCKED_UNTIL);
			failedAttempts = 0;
		}

		Map<String, String> config = context.getRealm().getAuthenticatorConfigByAlias("SMS auth").getConfig();
		if (failedAttempts >= Integer.parseInt(config.get(SmsConstants.MAX_FAILED_ATTEMPTS))) {
			context.failureChallenge(AuthenticationFlowError.USER_TEMPORARILY_DISABLED,
					context.form().setAttribute("realm", context.getRealm())
							.setError("smsAuthCodeInvalid").createForm(TPL_CODE));
			authSession.setAuthNote(SmsConstants.LOCKED_UNTIL, Long.toString(
					System.currentTimeMillis() + Integer.parseInt(config.get(SmsConstants.LOCK_DURATION)) * 1000));
			log.log(java.util.logging.Level.SEVERE, "user locked after too many failed attempts to enter SMS code");
			return;
		}

		boolean isValid = enteredCode.equals(code);
		if (isValid) {
			if (Long.parseLong(ttl) < System.currentTimeMillis()) {
				// expired
				context.failureChallenge(AuthenticationFlowError.EXPIRED_CODE,
						context.form().setError("smsAuthCodeExpired").createErrorPage(Response.Status.BAD_REQUEST));
			} else {
				// valid
				context.success();
			}
		} else {
			// invalid
			AuthenticationExecutionModel execution = context.getExecution();
			if (execution.isRequired()) {
				authSession.setAuthNote(SmsConstants.FAILED_ATTEMPTS, Integer.toString(failedAttempts + 1));
				context.failureChallenge(AuthenticationFlowError.INVALID_CREDENTIALS,
						context.form().setAttribute("realm", context.getRealm())
								.setError("smsAuthCodeInvalid").createForm(TPL_CODE));
			} else if (execution.isConditional() || execution.isAlternative()) {
				context.attempted();
			}
		}
	}

	@Override
	public boolean requiresUser() {
		return true;
	}

	@Override
	public boolean configuredFor(KeycloakSession session, RealmModel realm, UserModel user) {
		String verifiedMobileNr = user.getFirstAttribute("verifiedMobileNr");
		return user.getFirstAttribute(MOBILE_NUMBER_FIELD) != null && verifiedMobileNr != null
				&& verifiedMobileNr.equals("true");
	}

	@Override
	public void setRequiredActions(KeycloakSession session, RealmModel realm, UserModel user) {
		user.addRequiredAction("mobile-number-ra");
	}

	@Override
	public void close() {
	}

}
