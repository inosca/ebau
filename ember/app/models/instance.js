import Model from 'ember-data/model'
import attr from 'ember-data/attr'
import { belongsTo } from 'ember-data/relationships'

export default Model.extend({
  name: attr('string'),
  creationDate: attr('date'),
  modificationDate: attr('date'),
  location: belongsTo('location'),
  form: belongsTo('form'),
  instanceState: belongsTo('instance-state'),
  previousInstanceState: belongsTo('instance-state')
})
