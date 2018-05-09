import Controller from '@ember/controller'
import { task } from 'ember-concurrency'

export default Controller.extend({
  forms: task(function*() {
    return yield this.store.findAll('form')
  }).restartable(),

  save: task(function*() {
    let model = this.model

    yield model.save()

    yield this.transitionToRoute('instances.edit', model.id)
  }).drop()
})
