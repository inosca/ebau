import Component from '@ember/component'
import { serialize, deserialize } from './serializer'
import CamacInputComponentMixin from 'citizen-portal/mixins/camac-input-component'

export default Component.extend(CamacInputComponentMixin, {
  tagName: 'input',

  classNames: ['uk-input'],

  attributeBindings: [
    'type',
    'value',
    'config.maxlength:maxlength',
    'config.minlength:minlength'
  ],

  type: 'text',

  change(e) {
    e.preventDefault()

    this._change(e.target.value)
  },

  _serialize: serialize,
  _deserialize: deserialize
})
