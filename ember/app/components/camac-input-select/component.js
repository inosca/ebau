import Component from '@ember/component'

export default Component.extend({
  tagName: 'select',
  classNames: ['uk-select'],
  change(e) {
    e.preventDefault()

    this.getWithDefault('attrs.on-change', () => {})(e.target.value || null)
  }
})
