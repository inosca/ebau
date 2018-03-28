import Component from '@ember/component'
import ActiveLinkMixin from 'ember-cli-active-link-wrapper/mixins/active-link'

export default Component.extend(ActiveLinkMixin, {
  activeClass: 'uk-active',

  tagName: 'li'
})
