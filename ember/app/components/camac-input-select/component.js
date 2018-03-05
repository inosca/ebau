import Component from '@ember/component'
import { serialize, deserialize } from './serializer'
import CamacInputComponentMixin from 'citizen-portal/mixins/camac-input-component'

export default Component.extend(CamacInputComponentMixin, {
  _serialize: serialize,
  _deserialize: deserialize
})
