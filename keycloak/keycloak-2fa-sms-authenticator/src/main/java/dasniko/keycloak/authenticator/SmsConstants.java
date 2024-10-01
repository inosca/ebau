package dasniko.keycloak.authenticator;

import lombok.experimental.UtilityClass;

@UtilityClass
public class SmsConstants {
	public String CODE = "code";
	public String CODE_LENGTH = "length";
	public String CODE_TTL = "ttl";
	public String SENDER_NR = "senderNr";
	public String SIMULATION_MODE = "simulation";
	public String USERNAME = "username";
	public String PASSWORD = "password";
	public String FAILED_ATTEMPTS = "failedAttempts";
	public String LOCKED_UNTIL = "lockedUntil";
	public String MAX_FAILED_ATTEMPTS = "maxFailedAttempts";
	public String LOCK_DURATION = "lockDuration";
}
