import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import UIkit from 'uikit'
import { computed } from '@ember/object'
import computedTask from 'citizen-portal/lib/computed-task'

export default Controller.extend({
  questionStore: service(),
  ajax: service(),

  parcel: computed('model.instance.id', function() {
    return this.questionStore.peek('parzelle', this.model.instance.id)
  }),

  attachment: computed('model.instance.id', function() {
    return this.questionStore.peek('dokument-parzelle', this.model.instance.id)
  }),

  selected: computedTask(
    '_selected',
    'model.instance.location',
    'questionStore._store.@each.value'
  ),
  _selected: task(function*() {
    let location = yield this.get('model.instance.location')
    let parcel = this.parcel

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

      let attachment = this.attachment

      let filename = `${attachment.get('name')}.${file.type.split('/').pop()}`

      let formData = new FormData()
      formData.append('instance', attachment.get('instanceId'))
      formData.append('question', attachment.get('name'))
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
        this.questionStore._getModelForAttachment(
          attachment.get('name'),
          attachment.get('instanceId')
        )
      )

      yield instance.save()

      let parcel = this.parcel
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
