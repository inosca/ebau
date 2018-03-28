import CamacInputComponent from 'citizen-portal/components/camac-input/component'
import { task } from 'ember-concurrency'
import { v4 } from 'ember-uuid'

export default CamacInputComponent.extend({
  showModal: false,

  modalContainer: document.body,

  addRow: task(function*() {
    let question = yield this.get('question')

    let row = {
      uuid: v4(),
      ...question
        .get('field.config.columns')
        .reduce((obj, { name }) => ({ ...obj, [name]: '' }), {})
    }

    this.setProperties({
      editedRow: row,
      showModal: true
    })
  }).drop(),

  saveRow: task(function*(row) {
    let question = yield this.get('question')

    yield this.get('save').perform([
      ...question
        .getWithDefault('model.value', [])
        .filter(r => r.uuid !== row.uuid),
      row
    ])

    this.setProperties({
      editedRow: null,
      showModal: false
    })
  }).restartable(),

  editRow: task(function*(row) {
    yield this.setProperties({
      editedRow: row,
      showModal: true
    })
  }).restartable(),

  deleteRow: task(function*(row) {
    let question = yield this.get('question')

    yield this.get('save').perform(
      question
        .getWithDefault('model.value', [])
        .filter(r => r.uuid !== row.uuid)
    )
  })
})
