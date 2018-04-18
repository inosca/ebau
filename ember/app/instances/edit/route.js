import Route from '@ember/routing/route'
import { inject as service } from '@ember/service'

export default Route.extend({
  ajax: service(),

  queryParams: {
    group: { refreshModel: true }
  },

  async model({ instance_id: id, group }) {
    let response = await this.get('ajax').request(`/api/v1/instances/${id}`, {
      data: {
        group,
        include: 'form,instance_state,location'
      },
      headers: {
        Accept: 'application/vnd.api+json'
      }
    })
    let { data: { meta } } = response

    this.store.pushPayload(response)

    return {
      instance: this.store.peekRecord('instance', id),
      meta
    }
  }
})
