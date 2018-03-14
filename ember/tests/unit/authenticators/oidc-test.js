import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Unit | Authenticator | OIDC', function(hooks) {
  setupTest(hooks)
  setupMirage(hooks)

  test('it can authenticate', async function(assert) {
    assert.expect(4)

    let subject = this.owner.lookup('authenticator:oidc')

    subject.set('redirectUri', 'test')
    subject._scheduleRefresh = dt => {
      assert.ok(dt)
    }

    let data = await subject.authenticate({ code: 'test' })

    assert.ok(data.access_token, 'Returns an access token')
    assert.ok(data.refresh_token, 'Returns a refresh token')
    assert.ok(data.data.exp, 'Parses the access token correctly')
  })

  test('it can restore a session', async function(assert) {
    assert.expect(4)

    let subject = this.owner.lookup('authenticator:oidc')

    subject.set('redirectUri', 'test')
    subject._scheduleRefresh = dt => {
      assert.ok(dt)
    }

    let data = await subject.restore({
      access_token: 'a.b.c',
      refresh_token: 'x.y.z'
    })

    assert.ok(data.access_token, 'Returns an access token')
    assert.ok(data.refresh_token, 'Returns a refresh token')
    assert.ok(data.data.exp, 'Parses the access token correctly')
  })

  test('it can invalidate a session', async function(assert) {
    assert.expect(1)

    let subject = this.owner.lookup('authenticator:oidc')

    subject.set('redirectUri', 'test')

    assert.ok(
      await subject.invalidate({
        refresh_token: 'x.y.z'
      })
    )
  })

  test('it can refresh a session', async function(assert) {
    assert.expect(4)

    let subject = this.owner.lookup('authenticator:oidc')

    subject.set('redirectUri', 'test')
    subject._scheduleRefresh = dt => {
      assert.ok(dt)
    }

    let data = await subject._refresh({
      access_token: 'a.b.c',
      refresh_token: 'x.y.z'
    })

    assert.ok(data.access_token, 'Returns an access token')
    assert.ok(data.refresh_token, 'Returns a refresh token')
    assert.ok(data.data.exp, 'Parses the access token correctly')
  })

  test('it can schedule a refresh', async function(assert) {
    assert.expect(1)

    let subject = this.owner.lookup('authenticator:oidc')

    subject._refresh = token => {
      assert.equal(token, 'testtoken')
    }

    subject._scheduleRefresh(new Date() + 30, 'testtoken')
  })

  test('it can convert a unix timestamp to a date', async function(assert) {
    assert.expect(1)

    let subject = this.owner.lookup('authenticator:oidc')

    let timestamp = new Date().getTime() / 1000

    assert.equal(
      subject._timestampToDate(timestamp).toString(),
      new Date(timestamp * 1000).toString(),
      'Datetime is the correct representation of the timestamp'
    )
  })
})
