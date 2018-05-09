import BaseAuthenticator from 'ember-simple-auth/authenticators/base'
import { computed } from '@ember/object'
import { later } from '@ember/runloop'
import { inject as service } from '@ember/service'
import Configuration from 'ember-simple-auth/configuration'
import config from '../config/environment'
import { assert } from '@ember/debug'

const { tokenEndpoint, logoutEndpoint, clientId } = config[
  'ember-simple-auth-oidc'
]

const REFRESH_OFFSET = 1000 * 30 // refresh the token 30 seconds before it expires

export default BaseAuthenticator.extend({
  ajax: service(),
  router: service(),

  redirectUri: computed(function() {
    let { protocol, host } = location
    let path = this.get('router').urlFor(Configuration.authenticationRoute)

    return `${protocol}//${host}${path}`
  }),

  /**
   * Authenticate the client with the given authentication code. The
   * authentication call will return an access and refresh token which will
   * then authenticate the client against the API.
   *
   * @param {Object} options The authentication options
   * @param {String} options.code The authentication code
   * @returns {Object} The parsed response data
   */
  async authenticate({ code }) {
    let data = await this.get('ajax').request(tokenEndpoint, {
      method: 'POST',
      responseType: 'application/json',
      contentType: 'application/x-www-form-urlencoded',
      data: {
        code,
        client_id: clientId,
        grant_type: 'authorization_code',
        redirect_uri: this.get('redirectUri')
      }
    })

    return this._handleAuthResponse(data)
  },

  /**
   * Invalidate the current session with the refresh token
   *
   * @param {Object} data The authenticated data
   * @param {String} data.refresh_token The refresh token
   * @return {Promise} The logout request
   */
  async invalidate({ refresh_token }) {
    return await this.get('ajax').request(logoutEndpoint, {
      method: 'POST',
      responseType: 'application/json',
      contentType: 'application/x-www-form-urlencoded',
      data: {
        refresh_token,
        client_id: clientId
      }
    })
  },

  /**
   * Restore the session after a page refresh. This will check if an access
   * token exists and tries to refresh said token. If the refresh token is
   * already expired, the auth backend will throw an error which will cause a
   * new login.
   *
   * @param {Object} sessionData The current session data
   * @param {String} sessionData.access_token The raw access token
   * @param {String} sessionData.refresh_token The raw refresh token
   * @returns {Object} The parsed response data
   */
  async restore({ access_token, refresh_token }) {
    if (!access_token) {
      assert('Token is missing')
    }

    return await this._refresh(refresh_token)
  },

  /**
   * Refresh the access token
   *
   * @param {String} refresh_token The refresh token
   * @returns {Object} The parsed response data
   */
  async _refresh(refresh_token) {
    let data = await this.get('ajax').request(tokenEndpoint, {
      method: 'POST',
      responseType: 'application/json',
      contentType: 'application/x-www-form-urlencoded',
      data: {
        refresh_token,
        client_id: clientId,
        grant_type: 'refresh_token',
        redirect_uri: this.get('redirectUri')
      }
    })

    return this._handleAuthResponse(data)
  },

  /**
   * Schedule a refresh of the access token.
   *
   * This refresh needs to happen before the access token actually expires.
   * This offset is defined in REFRESH_OFFSET.
   *
   * @param {*} datetime The datetime at which the access token expires
   * @param {*} token The refresh token
   */
  _scheduleRefresh(datetime, token) {
    later(
      this,
      async token => {
        this.trigger('sessionDataUpdated', await this._refresh(token))
      },
      token,
      datetime - REFRESH_OFFSET - new Date()
    )
  },

  /**
   * Convert a unix timestamp to a date object
   *
   * @param {Number} exp The unix timestamp
   * @returns {Date} The date which results out of the timestamp
   */
  _timestampToDate(ts) {
    return new Date(ts * 1000)
  },

  /**
   * Parse the body of a bearer token
   *
   * @param {String} token The raw bearer token
   * @returns {Object} The parsed token data
   */
  _parseToken(token) {
    let [, body] = token.split('.')

    return JSON.parse(decodeURIComponent(escape(atob(body))))
  },

  /**
   * Handle an auth response. This method parses the token and schedules a
   * token refresh before the received token expires.
   *
   * @param {Object} response The raw response data
   * @param {String} response.access_token The raw access token
   * @param {String} response.refresh_token The raw refresh token
   * @returns {Object} The authentication data
   */
  _handleAuthResponse({ access_token, refresh_token }) {
    let data = this._parseToken(access_token)

    this._scheduleRefresh(this._timestampToDate(data.exp), refresh_token)

    return { access_token, refresh_token, data }
  }
})
