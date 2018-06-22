import { module, test } from 'qunit'
import { visit, currentURL, click, fillIn } from '@ember/test-helpers'
import { setupApplicationTest } from 'ember-qunit'
import { authenticateSession } from 'ember-simple-auth/test-support'
import setupMirage from 'ember-cli-mirage/test-support/setup-mirage'

module('Acceptance | instance list', function(hooks) {
  setupApplicationTest(hooks)
  setupMirage(hooks)

  hooks.beforeEach(async function() {
    await authenticateSession()
  })

  test('has correct empty state', async function(assert) {
    assert.expect(4)

    await visit('/dossiers')

    assert.dom('svg').exists()
    assert.dom('h4').hasText('Sie haben noch keine Dossiers!')
    assert.dom('.uk-button-primary').exists()

    await click('.uk-button-primary')

    assert.equal(currentURL(), '/dossiers/new')
  })

  test('has correct default state', async function(assert) {
    assert.expect(2)

    this.server.createList('instance', 5)

    await visit('/dossiers')

    // Should have 5 data rows and one to add a new row
    assert.dom('table > tbody > tr').exists({ count: 6 })

    await click('table > tbody > tr:last-of-type')

    assert.equal(currentURL(), '/dossiers/new')
  })

  test('can sort and search for identifier', async function(assert) {
    assert.expect(3)

    this.server.createList('instance', 5)

    await visit('/dossiers')

    assert.equal(currentURL(), '/dossiers')

    await click('a.uk-search-icon.uk-toggle')
    await fillIn('input.uk-search-input', '123')

    assert.ok(/(\?|&)identifier=123/.test(currentURL()))

    await click('table > thead > tr > th:last-of-type > span.pointer')

    assert.ok(/(\?|&)sort=creation_date/.test(currentURL()))
  })
})
