import Component from '@ember/component'
import UIkit from 'uikit'
import { scheduleOnce } from '@ember/runloop'
import CamacMultipleQuestionRowMixin from 'citizen-portal/mixins/camac-multiple-question-row'
import config from '../../config/environment'

export default Component.extend(CamacMultipleQuestionRowMixin, {
  modal: null,

  init() {
    this._super(...arguments)

    this.set(
      'container',
      document.querySelector(config.APP.rootElement || 'body')
    )
  },

  _show() {
    this.set('visible', true)
  },

  _hide() {
    this._value.rollback()

    this.set('visible', false)
  },

  didInsertElement() {
    let id = `#modal-${this.elementId}`

    this.set('modal', UIkit.modal(id, { container: false }))

    UIkit.util.on(id, 'show', () => this._show())
    UIkit.util.on(id, 'hide', () => this._hide())
  },

  didReceiveAttrs() {
    scheduleOnce('afterRender', () => {
      if (this.visible) {
        this.modal.show()
      } else {
        this.modal.hide()
      }
    })
  },

  willDestroyElement() {
    this.modal.hide()
  }
})
