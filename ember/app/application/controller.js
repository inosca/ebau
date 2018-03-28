import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import config from 'ember-get-config'

const { environment } = config

export default Controller.extend({
  session: service(),

  environment,

  actions: {
    logout() {
      this.get('session').invalidate()
    }
  }
})
