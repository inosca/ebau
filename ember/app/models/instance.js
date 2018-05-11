import Model from 'ember-data/model'
import attr from 'ember-data/attr'
import { belongsTo, hasMany } from 'ember-data/relationships'

export default Model.extend({
  identifier: attr('string'),
  creationDate: attr('date'),
  location: belongsTo('location'),
  form: belongsTo('form'),
  fields: hasMany('form-field'),
  attachments: hasMany('attachment'),
  instanceState: belongsTo('instance-state'),
  previousInstanceState: belongsTo('instance-state')
})
