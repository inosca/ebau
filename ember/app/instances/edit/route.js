import Route from '@ember/routing/route'
import { inject as service } from '@ember/service'

export default Route.extend({
  ajax: service(),

  async model({ instance_id: id }) {
    let response = await this.get('ajax').request(`/api/v1/instances/${id}`, {
      data: {
        include: 'form,instance_state'
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
