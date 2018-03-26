import Component from '@ember/component'
import UIkit from 'uikit'
import { scheduleOnce } from '@ember/runloop'
import { computed } from '@ember/object'
import Changeset from 'ember-changeset'

export default Component.extend({
  modal: null,

  container: document.body,

  _value: computed('value', function() {
    return new Changeset(this.get('value') || {})
  }),

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

  actions: {
    change(name, value) {
      this.set(`_value.${name}`, value)
    },

    save() {
      this.get('_value').execute()

      this.getWithDefault('attrs.on-save', () => {})(this.get('value'))
    }
  }
})
