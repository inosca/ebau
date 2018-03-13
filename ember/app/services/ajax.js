import AjaxService from 'ember-ajax/services/ajax'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { reads } from '@ember/object/computed'

export default AjaxService.extend({
  session: service(),

  token: reads('session.data.authenticated.access_token'),

  headers: computed('token', function() {
    let token = this.get('token')

    return token ? { Authorization: `Bearer ${token}` } : {}
  }),

  isUnauthorizedError() {
    this.get('session').invalidate()
  }
})
