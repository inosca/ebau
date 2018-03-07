import EmberObject from '@ember/object'
import KeycloakRedirectRouteMixin from 'citizen-portal/mixins/keycloak-redirect-route'
import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import config from 'ember-get-config'

const { host, realm, clientId } = config['ember-simple-auth-keycloak']

module('Unit | Mixin | keycloak-redirect-route', function(hooks) {
  setupTest(hooks)

  test('it can handle an unauthenticated request', function(assert) {
    assert.expect(3)

    let Route = EmberObject.extend(KeycloakRedirectRouteMixin)

    let subject = Route.create({
      redirectUri: 'test',
      session: EmberObject.create({ data: { authenticated: {} } }),
      _redirectToUrl(url) {
        assert.ok(
          new RegExp(
            `${host}/auth/realms/${realm}/protocol/openid-connect/auth`
          ).test(url)
        )

        assert.ok(new RegExp(`client_id=${clientId}`).test(url))
        assert.ok(new RegExp('redirect_uri=test').test(url))
      }
    })

    subject.afterModel(null, { queryParams: {} })
  })

  test('it can handle a request with an authentication code', function(assert) {
    assert.expect(1)

    let Route = EmberObject.extend(KeycloakRedirectRouteMixin)

    let subject = Route.create({
      redirectUri: 'test',
      session: EmberObject.create({
        data: {
          authenticated: {}
        },
        async authenticate(_, { code }) {
          assert.equal(code, 'sometestcode')
        }
      })
    })

    subject.afterModel(null, { queryParams: { code: 'sometestcode' } })
  })

  test('it can handle a failing authentication', function(assert) {
    assert.expect(2)

    let Route = EmberObject.extend(KeycloakRedirectRouteMixin)

    let subject = Route.create({
      redirectUri: 'test',
      session: EmberObject.create({
        data: {
          authenticated: {},
          state: 'state2'
        },
        async authenticate() {
          return true
        }
      }),
      _redirectToUrl(url) {
        assert.equal(url, 'test')
      }
    })

    // fails because the state is not correct (CSRF)
    subject.afterModel(null, {
      queryParams: { code: 'sometestcode', state: 'state1' }
    })

    subject.session.authenticate = async () => {
      throw new Error()
    }

    // fails because of the error in authenticate
    subject.afterModel(null, {
      queryParams: { code: 'sometestcode', state: 'state2' }
    })
  })
})
