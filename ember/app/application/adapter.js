import DS from 'ember-data'
import { inject as service } from '@ember/service'
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin'

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, {
  session: service(),

  namespace: 'api/v1',

  authorize(xhr) {
    let { access_token } = this.get('session.data.authenticated')
    xhr.setRequestHeader('Authorization', `Bearer ${access_token}`)
  }
})
