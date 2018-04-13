import Mixin from '@ember/object/mixin'
import { computed } from '@ember/object'
import { capitalize } from '@ember/string'
import Changeset from 'ember-changeset'
import { task } from 'ember-concurrency'
import { resolve } from 'rsvp'
import _validations from 'citizen-portal/questions/validations'

export default Mixin.create({
  _validations,

  _value: computed('value', 'columns.[]', function() {
    return new Changeset(
      this.get('value') || {},
      (...args) => this._validate(...args),
      this.get('columns').reduce((map, f) => {
        return { ...map, [f.name]: () => this._validate }
      }, {})
    )
  }),

  _validate({ key, newValue }) {
    try {
      let { type, required: isRequired, config } = this.get('columns').find(
        f => f.name === key
      )

      let validations = [
        isRequired
          ? this.getWithDefault('_validations.validateRequired', () => true)
          : () => true,
        this.getWithDefault(
          `_validations.validate${capitalize(type)}`,
          () => true
        ),
        this.getWithDefault(
          `_validations.${this.get('parentName')}/${key}`,
          () => true
        )
      ]

      let isValid = validations.map(fn => fn(config, newValue))

      return (
        isValid.every(v => v === true) ||
        isValid.filter(v => typeof v === 'string')
      )
    } catch (e) {
      return true
    }
  },

  save: task(function*() {
    let changeset = this.get('_value')

    yield changeset.validate()

    if (changeset.get('isValid')) {
      changeset.execute()

      yield resolve(
        this.getWithDefault('attrs.on-save', () => {})(this.get('value'))
      )
    }
  }),

  actions: {
    change(name, value) {
      this.set(`_value.${name}`, value)
    }
  }
})
