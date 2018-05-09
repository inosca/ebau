import Controller, { inject as controller } from '@ember/controller'
import { inject as service } from '@ember/service'
import computedTask from 'citizen-portal/lib/computed-task'
import { task } from 'ember-concurrency'
import { all } from 'rsvp'
import UIkit from 'uikit'

export default Controller.extend({
  ajax: service(),
  questionStore: service(),

  editController: controller('instances.edit'),

  canSubmit: computedTask(
    '_canSubmit',
    'editController.modules.lastSuccessful.value.[]',
    'questionStore._store.@each.{value,hidden,isNew}'
  ),
  _canSubmit: task(function*() {
    let modules = this.get('editController.modules.lastSuccessful.value')

    if (!modules) {
      return false
    }

    let questions = (yield all(
      (yield this.get('questionStore.findSet').perform(
        modules.reduce((flat, m) => [...flat, ...m.get('allQuestions')], []),
        this.get('model.instance.id')
      )).map(async q => ((await q.get('hidden')) ? null : q))
    )).filter(Boolean)

    return questions.every(q => q.validate() === true)
  }),

  submit: task(function*() {
    try {
      yield this.ajax.request(
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
