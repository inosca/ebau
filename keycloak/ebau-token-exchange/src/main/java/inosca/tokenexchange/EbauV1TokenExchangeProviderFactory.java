/*
 * Monkey-patch of Keycloak's V1TokenExchangeProviderFactory, see
 * https://github.com/keycloak/keycloak/blob/26.5.3/services/src/main/java/org/keycloak/protocol/oidc/tokenexchange/V1TokenExchangeProviderFactory.java
 * Changes are marked with "CHANGED".
 */

package inosca.tokenexchange;

import org.keycloak.models.KeycloakSession;
import org.keycloak.protocol.oidc.TokenExchangeProvider;
import org.keycloak.protocol.oidc.tokenexchange.V1TokenExchangeProviderFactory;

public class EbauV1TokenExchangeProviderFactory extends V1TokenExchangeProviderFactory { // CHANGED: renamed class

    @Override
    public TokenExchangeProvider create(KeycloakSession session) {
        return new EbauV1TokenExchangeProvider(); // CHANGED: return patched provider
    }

    @Override
    public String getId() {
        return "ebau"; // CHANGED: renamed ID
    }

    @Override
    public int order() {
        return 200; // CHANGED: higher priority than the default factory (order 0)
    }
}
