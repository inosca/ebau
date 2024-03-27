# Keycloak configuration

## 1. Create new client "token-exchange"

![Create client](./images/create-client.png)

## 2. Grant service account role "manage-users" to "token-exchange" client

![Grant role](./images/grant-role.png)

## 3. Create client scope mapper "Audience" for "token-exchange" client

This is only needed because Keycloak doesn't support passing a specific audience
for the requested token exchange: https://github.com/keycloak/keycloak/issues/17668

![Create scope step 1](./images/client-scope-1.png)
![Create scope step 2](./images/client-scope-2.png)
![Create scope step 3](./images/client-scope-3.png)

## 4. Create new positive client policy "token-exchange"

![Create policy step 1](./images/create-policy-1.png)
![Create policy step 2](./images/create-policy-2.png)

## 5. Grant permissions for token exchange on "portal" client and assign policy "token-exchange"

![Grant token exchange permission step 1](./images/grant-token-exchange-1.png)
![Grant token exchange permission step 2](./images/grant-token-exchange-2.png)

## 6. Grant permissions for impersonate on user permission tab and assign policy "token-exchange"

![Grant impersonate permission step 1](./images/grant-impersonate-1.png)
![Grant impersonate permission step 2](./images/grant-impersonate-2.png)
