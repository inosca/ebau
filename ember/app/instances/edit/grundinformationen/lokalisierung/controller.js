import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import UIkit from 'uikit'
import computedTask from 'citizen-portal/lib/computed-task'

export default Controller.extend({
  questionStore: service(),
  ajax: service(),

  parcel: computedTask('_parcel', 'model.instance.id'),
  _parcel: task(function*() {
    return yield this.get('questionStore.find').perform(
      'parzelle',
      this.get('model.instance.id')
    )
  }),

  attachment: computedTask('_attachment', 'model.instance.id'),
  _attachment: task(function*() {
    return yield this.get('questionStore.find').perform(
      'dokument-parzelle',
      this.get('model.instance.id')
    )
  }),

  selected: computedTask(
    '_selected',
    'model.instance.location',
    'questionStore._store.@each.value'
  ),
  _selected: task(function*() {
    let location = yield this.get('model.instance.location')
    let parcel = yield this.get('parcel.last')

    if (!location || !parcel.get('value')) {
      return null
    }

    return {
      municipality: location.get('name'),
      number: parcel.get('value')
    }
  }),

  saveLocation: task(function*({ municipality, number }, file) {
    if (this.get('model.instance.identifier')) {
      return
    }

    try {
      let location = yield this.store.query('location', { name: municipality })
      let instance = this.get('model.instance')

      instance.set('location', location.get('firstObject'))

      let attachment = yield this.get('attachment.last')

      let filename = `${attachment.get('name')}.${file.type.split('/').pop()}`

      let formData = new FormData()
      formData.append('instance', attachment.get('model.instance.id'))
      formData.append('path', file, filename)

      let response = yield this.ajax.request('/api/v1/attachments', {
        method: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        headers: {
          Accept: 'application/vnd.api+json'
        }
      })

      this.store.pushPayload(response)

      attachment.set(
        'model',
        this.store.peekRecord('attachment', response.data.id)
      )

      yield instance.save()

      let parcel = yield this.get('parcel.last')
      parcel.set('model.value', parseInt(number))
      yield parcel.get('model').save()

      UIkit.notification('Die Parzelle wurde erfolgreich ausgewält', {
        status: 'success'
      })
    } catch (e) {
      UIkit.notification(
        'Hoppla, etwas ist schief gelaufen. Bitte versuchen Sie es erneut.',
        { status: 'danger' }
      )
    }
  })
})
