import Component from '@ember/component'

export default Component.extend({
  tagName: 'input',

  classNames: ['uk-input'],

  attributeBindings: [
    'type',
    'model.value:value',
    'config.maxlength:maxlength',
    'config.minlength:minlength'
  ],

  type: 'text',

  change(e) {
    e.preventDefault()

    this.getWithDefault('attrs.on-change', () => {})(e.target.value)
  }
})
