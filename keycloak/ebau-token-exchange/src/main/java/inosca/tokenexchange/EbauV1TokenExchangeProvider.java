/*
 * Monkey-patch of Keycloak's V1TokenExchangeProvider, see
 * https://github.com/keycloak/keycloak/blob/26.5.3/services/src/main/java/org/keycloak/protocol/oidc/tokenexchange/V1TokenExchangeProvider.java
 * Changes are marked with "CHANGED".
 *
 * We use the v1 token exchange instead of Keycloak's new standard token exchange (v2, introduced in v26)
 * because v2 does not support direct naked impersonation, which ebau requires.
 * See https://www.keycloak.org/securing-apps/token-exchange#_standard-token-exchange-comparison
 *
 * === IMPORTANT ===
 * Before doing any maintenance, check if the new token-exchange now supports this or if
 * v1 token-exchange support was removed.
 */

package inosca.tokenexchange;

import java.util.List;

import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import org.keycloak.OAuth2Constants;
import org.keycloak.models.ClientModel;
import org.keycloak.models.ClientSessionContext;
import org.keycloak.models.UserModel;
import org.keycloak.models.UserSessionModel;
import org.keycloak.protocol.oidc.OIDCAdvancedConfigWrapper;
import org.keycloak.protocol.oidc.TokenManager;
import org.keycloak.protocol.oidc.tokenexchange.V1TokenExchangeProvider;
import org.keycloak.representations.AccessToken;
import org.keycloak.representations.AccessTokenResponse;
import org.keycloak.services.managers.AuthenticationManager;
import org.keycloak.services.managers.AuthenticationSessionManager;
import org.keycloak.sessions.AuthenticationSessionModel;
import org.keycloak.sessions.RootAuthenticationSessionModel;
import org.keycloak.util.TokenUtil;

import org.jboss.logging.Logger;

import static org.keycloak.models.ImpersonationSessionNote.IMPERSONATOR_CLIENT;

public class EbauV1TokenExchangeProvider extends V1TokenExchangeProvider {

    private static final Logger logger = Logger.getLogger(EbauV1TokenExchangeProvider.class);

    @Override
    protected Response exchangeClientToOIDCClient(UserModel targetUser, UserSessionModel targetUserSession, String requestedTokenType,
                                                  List<ClientModel> targetAudienceClients, String scope, AccessToken subjectToken) {
        ClientModel targetClient = getTargetClient(targetAudienceClients);
        RootAuthenticationSessionModel rootAuthSession = new AuthenticationSessionManager(session).createAuthenticationSession(realm, false);
        AuthenticationSessionModel authSession = createSessionModel(targetUserSession, rootAuthSession, targetUser, targetClient, scope);

        AuthenticationManager.setClientScopesInSession(session, authSession);
        ClientSessionContext clientSessionCtx = TokenManager.attachAuthenticationSession(this.session, targetUserSession, authSession);

        if (!AuthenticationManager.isClientSessionValid(realm, client, targetUserSession, targetUserSession.getAuthenticatedClientSessionByClient(client.getId()))) {
            AuthenticationSessionModel clientAuthSession = createSessionModel(targetUserSession, rootAuthSession, targetUser, client, scope);
            TokenManager.attachAuthenticationSession(this.session, targetUserSession, clientAuthSession);
        }

        updateUserSessionFromClientAuth(targetUserSession);

        TokenManager.AccessTokenResponseBuilder responseBuilder = tokenManager.responseBuilder(realm, targetClient, event, this.session, targetUserSession, clientSessionCtx)
                .generateAccessToken();
        responseBuilder.getAccessToken().issuedFor(targetClient.getClientId()); // CHANGED: use targetClient instead of client

        if (targetClient != null && !targetClient.equals(client)) {
            responseBuilder.getAccessToken().addAudience(targetClient.getClientId());
        }

        if (formParams.containsKey(OAuth2Constants.REQUESTED_SUBJECT)) {
            targetUserSession.setNote(IMPERSONATOR_CLIENT.toString(), client.getId());
        }

        if (targetUserSession.getPersistenceState() == UserSessionModel.SessionPersistenceState.TRANSIENT) {
            responseBuilder.getAccessToken().setSessionId(null);
        }

        String issuedTokenType;
        if (requestedTokenType.equals(OAuth2Constants.REFRESH_TOKEN_TYPE)
                && OIDCAdvancedConfigWrapper.fromClientModel(client).isUseRefreshToken()
                && targetUserSession.getPersistenceState() != UserSessionModel.SessionPersistenceState.TRANSIENT) {
            responseBuilder.generateRefreshToken();
            responseBuilder.getRefreshToken().issuedFor(targetClient.getClientId()); // CHANGED: use targetClient instead of client
            issuedTokenType = OAuth2Constants.REFRESH_TOKEN_TYPE;
        } else {
            issuedTokenType = OAuth2Constants.ACCESS_TOKEN_TYPE;
        }

        String scopeParam = clientSessionCtx.getClientSession().getNote(OAuth2Constants.SCOPE);
        if (TokenUtil.isOIDCRequest(scopeParam)) {
            responseBuilder.generateIDToken().generateAccessTokenHash();
        }

        AccessTokenResponse res = responseBuilder.build();
        res.setOtherClaims(OAuth2Constants.ISSUED_TOKEN_TYPE, issuedTokenType);

        event.detail(org.keycloak.events.Details.AUDIENCE, targetClient.getClientId())
                .user(targetUser);

        event.success();

        return cors.add(Response.ok(res, MediaType.APPLICATION_JSON_TYPE));
    }
}
