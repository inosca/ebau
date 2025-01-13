# Keycloak configuration

## 1. Create new client "token-exchange"

![Create client](./images/create-client.png)

## 2. Grant service account role "manage-users" to "token-exchange" client

![Grant role](./images/grant-role.png)

## 3. Create new positive client policy "token-exchange"

![Create policy step 1](./images/create-policy-1.png)
![Create policy step 2](./images/create-policy-2.png)

## 4. Grant permissions for token exchange on "portal" client and assign policy "token-exchange"

![Grant token exchange permission step 1](./images/grant-token-exchange-1.png)
![Grant token exchange permission step 2](./images/grant-token-exchange-2.png)

## 5. Grant permissions for impersonate on user permission tab and assign policy "token-exchange"

![Grant impersonate permission step 1](./images/grant-impersonate-1.png)
![Grant impersonate permission step 2](./images/grant-impersonate-2.png)

## 6. Create new user attribute "LoT"

![Create user attribute step 1](./images/lot-attribute-1.png)
![Create user attribute step 2](./images/lot-attribute-2.png)

## 7. Create new client scope "token-exchange"

![Create client scope step 1](./images/create-client-scope-1.png)
![Create client scope step 2](./images/create-client-scope-2.png)

## 8. Add new token mapper "LoT" to client scope "token-exchange"

![Add LoT mapper step 1](./images/lot-mapper-1.png)
![Add LoT mapper step 2](./images/lot-mapper-2.png)

## 9. Assign client scope "token-exchange" to client "portal"

![Assign client scope step 1](./images/assign-client-scope-1.png)
![Assign client scope step 2](./images/assign-client-scope-2.png)
