package dasniko.keycloak.authenticator.gateway;

import java.io.IOException;
import java.util.Map;

/**
 * @author Niko Köbler, https://www.n-k.de, @dasniko
 */
public interface SmsService {

	void send(String phoneNumber, String message) throws IOException;

}
