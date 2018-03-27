import Component from '@ember/component'

export default Component.extend({
  tagName: 'form',

  submit(e) {
    e.preventDefault()
  }
})
