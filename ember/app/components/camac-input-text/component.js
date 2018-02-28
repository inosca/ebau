import Component from '@ember/component'
import { computed } from '@ember/object'
import { serialize, deserialize } from './serializer'

export default Component.extend({
  tagName: 'input',
  classNames: ['uk-input'],
  attributeBindings: [
    'type',
    'rawValue:value',
    'config.maxlength:maxlength',
    'config.minlength:minlength'
  ],
  type: 'text',

  rawValue: computed('model.value', function() {
    let value = this.get('model.value')

    return (value && deserialize(value)) || ''
  }),

  change(e) {
    e.preventDefault()

    this.getWithDefault('attrs.on-change', () => {})(serialize(e.target.value))
  }
})
