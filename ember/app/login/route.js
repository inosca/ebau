import Route from '@ember/routing/route'
import KeycloakRedirectRouteMixin from 'citizen-portal/mixins/keycloak-redirect-route'

export default Route.extend(KeycloakRedirectRouteMixin, {})
