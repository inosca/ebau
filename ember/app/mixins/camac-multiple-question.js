import Mixin from '@ember/object/mixin'
import { task } from 'ember-concurrency'
import { v4 } from 'ember-uuid'

export default Mixin.create({
  addRow: task(function*() {
    let question = yield this.get('question')

    let row = {
      uuid: v4(),
      ...question
        .get('field.config.columns')
        .reduce((obj, { name }) => ({ ...obj, [name]: undefined }), {})
    }

    this.setProperties({
      editedRow: row,
      showEdit: true
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
      showEdit: false
    })
  }).restartable(),

  editRow: task(function*(row) {
    yield this.setProperties({
      editedRow: row,
      showEdit: true
    })
  }).restartable(),

  deleteRow: task(function*(row) {
    let question = yield this.get('question')

    yield this.get('save').perform(
      question
        .getWithDefault('model.value', [])
        .filter(r => r.uuid !== row.uuid)
    )

    this.setProperties({
      editedRow: null,
      showEdit: false
    })
  })
})
