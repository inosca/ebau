import Controller from '@ember/controller'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task } from 'ember-concurrency'
import UIkit from 'uikit'

export default Controller.extend({
  questionStore: service(),

  selected: computed(
    'model.instance.location',
    'questionStore._store.@each.value',
    async function() {
      let instance = this.get('model.instance')

      let parcelQuestion = await this.get('questionStore.find').perform(
        'parzelle',
        instance.id
      )
      let location = await instance.get('location')

      if (!location || !parcelQuestion.get('value')) {
        return null
      }

      return {
        municipality: location.get('name'),
        number: parcelQuestion.get('value')
      }
    }
  ),

  saveLocation: task(function*({ municipality, number } /*, image*/) {
    if (this.get('model.instance.identifier')) {
      return
    }

    try {
      let location = yield this.store.query('location', { name: municipality })
      let instance = this.get('model.instance')

      instance.set('location', location.get('firstObject'))

      // TODO: Upload image of parcel as document

      yield instance.save()

      let parcelQuestion = yield this.get('questionStore.find').perform(
        'parzelle',
        instance.id
      )

      parcelQuestion.set('model.value', parseInt(number))

      yield parcelQuestion.get('model').save()

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
