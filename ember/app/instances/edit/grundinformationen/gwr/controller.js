import Controller from '@ember/controller'
import { reads } from '@ember/object/computed'
import { task } from 'ember-concurrency'
import { v4 } from 'ember-uuid'

export default Controller.extend({
  value: reads('model.model.value'),

  editBuilding: task(function*(building) {
    yield this.set('editedBuilding', building)
  }),

  addBuilding: task(function*() {
    let building = {
      id: v4()
    }

    yield this.set('editedBuilding', building)
  }),

  deleteBuilding: task(function*(building) {
    let value = this.getWithDefault('model.model.value', []).filter(
      ({ id }) => id !== building.id
    )

    this.set('model.model.value', value)

    yield this.get('model.model').save()

    this.set('editedBuilding', null)
  }),

  saveBuilding: task(function*(building) {
    let value = [
      ...this.getWithDefault('model.model.value', []).filter(
        ({ id }) => id !== building.id
      ),
      building
    ]

    this.set('model.model.value', value)

    yield this.get('model.model').save()

    this.set('editedBuilding', null)
  })
})
