import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin'
import Mixin from '@ember/object/mixin'
import { computed } from '@ember/object'
import { inject as service } from '@ember/service'
import Configuration from 'ember-simple-auth/configuration'
import config from '../config/environment'
import v4 from 'uuid/v4'
import { assert } from '@ember/debug'

const { authEndpoint, clientId } = config['ember-simple-auth-oidc']

export default Mixin.create(UnauthenticatedRouteMixin, {
  session: service(),
  router: service(),

  redirectUri: computed(function() {
    let { protocol, host } = location
    let path = this.router.urlFor(Configuration.authenticationRoute)

    return `${protocol}//${host}${path}`
  }),

  _redirectToUrl(url) {
    location.replace(url)
  },

  /**
   * Handle unauthenticated requests
   *
   * This handles two cases:
   *
   * 1. The URL contains an authentication code and a state. In this case the
   *    client will try to authenticate with the given parameters.
   *
   * 2. The URL does not contain an authentication. In this case the client
   *    will be redirected to the configured keycloak login mask, which will
   *    then redirect to this route after a successful login.
   *
   * @param {*} model The model of the route
   * @param {Ember.Transition} transition The current transition
   * @param {Object} transition.queryParams The query params of the transition
   * @param {String} transition.queryParams.code The authentication code given by keycloak
   * @param {String} transition.queryParams.state The state given by keycloak
   */
  async afterModel(
    _,
    {
      queryParams: { code, state }
    }
  ) {
    if (code) {
      return await this._handleCallbackRequest(code, state)
    }

    return this._handleRedirectRequest()
  },

  /**
   * Authenticate with the authentication code given by keycloak in the redirect.
   *
   * This will check if the passed state equals the state in the application to
   * prevent from CSRF attacks.
   *
   * If the authentication fails, it will redirect to this route again but
   * remove application state and query params. This is very unlikely to happen.
   *
   * If the authentication succeeds the default behaviour of ember-simple-auth
   * will apply and redirect to the entry point of the authenticated part of
   * the application.
   *
   * @param {String} code The authentication code passed by keycloak
   * @param {String} state The state (uuid4) passed by keycloak
   */
  async _handleCallbackRequest(code, state) {
    if (state !== this.get('session.data.state')) {
      assert('State did not match')
    }

    this.session.set('data.state', undefined)

    try {
      await this.session.authenticate('authenticator:oidc', {
        code
      })
    } catch (e) {
      assert('Authentication failed')
    }
  },

  /**
   * Redirect the client to the configured keycloak to login.
   *
   * This will also generate a uuid4 state which the application stores to the
   * local storage. When authenticating, the state passed by keycloak needs to
   * match this state, otherwise the authentication will fail to prevent from
   * CSRF attacks.
   */
  _handleRedirectRequest() {
    let state = v4()

    this.session.set('data.state', state)

    let attemptedTransition = this.get('session.attemptedTransition')

    if (attemptedTransition) {
      let {
        intent: { url }
      } = attemptedTransition

      this.session.set('data.next', url)
    }

    this._redirectToUrl(
      `${authEndpoint}?` +
        `client_id=${clientId}&` +
        `redirect_uri=${this.redirectUri}&` +
        `response_type=code&` +
        `state=${state}`
    )
  }
})
