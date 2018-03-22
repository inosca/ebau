import Component from '@ember/component'
import UIkit from 'uikit'
import { scheduleOnce } from '@ember/runloop'

export default Component.extend({
  modal: null,

  didInsertElement() {
    let id = `#${this.get('elementId')}`

    this.set('modal', UIkit.modal(id))

    UIkit.util.on(id, 'shown', () => this.set('visible', true))
    UIkit.util.on(id, 'hidden', () => this.set('visible', false))
  },

  didReceiveAttrs() {
    scheduleOnce('afterRender', () => {
      if (this.get('visible')) {
        this.get('modal').show()
      } else {
        this.get('modal').hide()
      }
    })
  }
})
