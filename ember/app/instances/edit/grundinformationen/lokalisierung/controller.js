import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import { task } from 'ember-concurrency'
import { computed } from '@ember/object'

export default Controller.extend({
  questionStore: service(),
  ajax: service(),
  notification: service(),

  parcels: computed('model.instance.id', function() {
    return this.questionStore.peek('parzellen', this.model.instance.id)
  }),

  points: computed('model.instance.id', function() {
    return this.questionStore.peek('punkte', this.model.instance.id)
  }),

  attachment: computed('model.instance.id', function() {
    return this.questionStore.peek('dokument-parzellen', this.model.instance.id)
  }),

  _saveImage: task(function*(image) {
    let attachment = this.attachment
    let filename = `${attachment.get('name')}.${image.type.split('/').pop()}`
    let formData = new FormData()

    formData.append('instance', attachment.get('instanceId'))
    formData.append('question', attachment.get('name'))
    formData.append('path', image, filename)

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
  }),

  _saveParcels: task(function*(parcels) {
    this.set(
      'parcels.model.value',
      parcels.map(({ number, ...p }) => {
        return { ...p, number: parseInt(number), coordinates: undefined }
      })
    )

    yield this.get('questionStore.saveQuestion').perform(this.parcels)
  }),

  _savePoints: task(function*(points) {
    this.set('points.model.value', points)

    yield this.get('questionStore.saveQuestion').perform(this.points)
  }),

  _saveLocation: task(function*(parcels) {
    let location = yield this.store.query('location', {
      name: parcels.get('firstObject.municipality')
    })
    let instance = this.get('model.instance')

    instance.set('location', location.get('firstObject'))

    yield instance.save()
  }),

  saveLocation: task(function*(parcels, points, image) {
    if (this.get('model.instance.identifier')) {
      return
    }

    try {
      yield this._saveLocation.perform(parcels)
      yield this._saveImage.perform(image)

      yield this._saveParcels.perform(parcels)
      yield this._savePoints.perform(points)

      this.notification.success('Ihre Auswahl wurde erfolgreich gespeichert', {
        status: 'success'
      })
    } catch (e) {
      this.notification.danger(
        'Hoppla, etwas ist schief gelaufen. Bitte versuchen Sie es erneut.'
      )
    }
  })
})
