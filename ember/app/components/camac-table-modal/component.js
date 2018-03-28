import Component from '@ember/component'
import UIkit from 'uikit'
import { scheduleOnce } from '@ember/runloop'
import { computed, getWithDefault } from '@ember/object'
import { task } from 'ember-concurrency'
import Changeset from 'ember-changeset'
import { resolve } from 'rsvp'
import _validations, {
  required,
  inOptions,
  multipleInOptions
} from 'citizen-portal/questions/validations'

export default Component.extend({
  modal: null,

  container: document.body,

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
      let { type, required: isRequired } = this.get('columns').find(
        f => f.name === key
      )

      let builtInValidations = [
        isRequired ? required : () => true,
        ['select', 'radio'].includes(type) ? inOptions : () => true,
        ['multiselect', 'checkbox'].includes(type)
          ? multipleInOptions
          : () => true
      ]

      let validationFn = getWithDefault(
        this.get('_validations'),
        `${this.get('name')}-${key}`,
        () => true
      )

      let isValid = [...builtInValidations, validationFn].map(fn =>
        fn(this.get('field'), newValue)
      )

      return (
        isValid.every(v => v === true) ||
        isValid.filter(v => typeof v === 'string')
      )
    } catch (e) {
      return true
    }
  },

  _show() {
    this.set('visible', true)
  },

  _hide() {
    this.get('_value').rollback()

    this.set('visible', false)
  },

  didInsertElement() {
    let id = `#modal-${this.get('elementId')}`

    this.set('modal', UIkit.modal(id, { container: false }))

    UIkit.util.on(id, 'show', () => this._show())
    UIkit.util.on(id, 'hide', () => this._hide())
  },

  didReceiveAttrs() {
    scheduleOnce('afterRender', () => {
      if (this.get('visible')) {
        this.get('modal').show()
      } else {
        this.get('modal').hide()
      }
    })
  },

  willDestroyElement() {
    this.get('modal').hide()
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
