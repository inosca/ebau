import Component from '@ember/component'
import { computed } from '@ember/object'
import Changeset from 'ember-changeset'

const CamacGwrBuildingComponent = Component.extend({
  building: computed('_building', function() {
    return new Changeset(this.get('building'))
  }),

  actions: {
    save() {
      let building = this.get('building')

      building.validate(() => {
        if (building.get('isValid')) {
          building.execute()

          this.getWithDefault('attrs.on-save', () => {})(this.get('_building'))
        }
      })
    }
  }
})

CamacGwrBuildingComponent.reopenClass({
  positionalParams: ['_building']
})

export default CamacGwrBuildingComponent
