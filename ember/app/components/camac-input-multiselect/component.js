import Component from '@ember/component'
import { computed } from '@ember/object'

export default Component.extend({
  renderInPlace: false,

  searchable: computed('config.{allowCustom,searchable}', function() {
    return this.get('config.allowCustom') || this.get('config.searchable')
  }),

  actions: {
    handleKeydown(_, e) {
      if (e.keyCode !== 13 || !this.get('config.allowCustom')) {
        return
      }

      let custom = e.target.value

      if (custom.length > 0 && !this.get('config.options').includes(custom)) {
        this.getWithDefault('attrs.on-change', () => {})([
          ...this.get('model.value'),
          custom
        ])
      }
    }
  }
})
