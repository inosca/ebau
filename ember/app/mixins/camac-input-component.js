import Mixin from '@ember/object/mixin'
import { computed } from '@ember/object'

export default Mixin.create({
  _serialize: value => value,
  _deserialize: value => value,

  value: computed('model.value', function() {
    let value = this.get('model.value')

    return (value && this._deserialize(value)) || ''
  }),

  _change(value) {
    this.getWithDefault('attrs.on-change', () => {})(this._serialize(value))
  }
})
