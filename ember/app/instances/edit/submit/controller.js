import Controller, { inject as controller } from '@ember/controller'
import { inject as service } from '@ember/service'
import { computed } from '@ember/object'
import { task } from 'ember-concurrency'
import { all } from 'rsvp'
import UIkit from 'uikit'

export default Controller.extend({
  ajax: service(),
  questionStore: service(),

  editController: controller('instances.edit'),

  canSubmit: computed(
    'editController.modules.lastSuccessful.value.[]',
    'questionStore._store.@each.{value,hidden,isNew}',
    function() {
      let task = this.get('_canSubmit')
      task.perform()
      return task
    }
  ),
  _canSubmit: task(function*() {
    let states = yield all(
      this.getWithDefault(
        'editController.modules.lastSuccessful.value',
        []
      ).map(async mod => await mod.get('state'))
    )

    return (
      states.length && states.filter(Boolean).every(state => state === 'valid')
    )
  }),

  submit: task(function*() {
    try {
      yield this.get('ajax').request(
        `/api/v1/instances/${this.get('model.instance.id')}/submit`,
        { method: 'POST' }
      )

      UIkit.notification('Das Dossier wurde erfolgreich eingereicht', {
        status: 'success'
      })

      yield this.transitionToRoute('instances')
    } catch (e) {
      UIkit.notification(
        'Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals.',
        { status: 'danger' }
      )
    }
  })
})
