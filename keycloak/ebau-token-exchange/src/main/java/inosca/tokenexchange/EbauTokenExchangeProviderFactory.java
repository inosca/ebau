/*
 * This is almost a 1:1 copy of Keycloak's DefaultTokenExchangeProviderFactory, see
 * https://github.com/keycloak/keycloak/blob/25.0.6/services/src/main/java/org/keycloak/protocol/oidc/DefaultTokenExchangeProviderFactory.java
 * changes are marked with "CHANGED"
 */

/*
 *  Copyright 2021 Red Hat, Inc. and/or its affiliates
 *  and other contributors as indicated by the @author tags.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 */
package inosca.tokenexchange; // CHANGED: renamed package

import org.keycloak.Config;
import org.keycloak.models.KeycloakSession;
import org.keycloak.models.KeycloakSessionFactory;
// CHANGED: added missing imports
import org.keycloak.protocol.oidc.TokenExchangeProvider;
import org.keycloak.protocol.oidc.TokenExchangeProviderFactory;

/**
 * Default token exchange provider factory
 *
 * @author <a href="mailto:dmitryt@backbase.com">Dmitry Telegin</a>
 */
public class EbauTokenExchangeProviderFactory implements TokenExchangeProviderFactory {

    @Override
    public TokenExchangeProvider create(KeycloakSession session) {
        return new EbauTokenExchangeProvider();
    }

    @Override
    public void init(Config.Scope config) {
    }

    @Override
    public void postInit(KeycloakSessionFactory factory) {
    }

    @Override
    public void close() {
    }

    @Override
    public String getId() {
        return "ebau"; // CHANGED: renamed ID
    }

    // CHANGED: added missing order method
    @Override
    public int order() {
        return 200;
    }

}
