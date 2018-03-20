import Transform from 'ember-data/transform'

export default Transform.extend({
  deserialize(serialized) {
    return (serialized && serialized.value) || null
  },

  serialize(deserialized) {
    return (deserialized && { value: deserialized }) || null
  }
})
