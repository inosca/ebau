export const serialize = value => ({ value })
export const deserialize = ({ value }) => value

export default {
  serialize,
  deserialize
}
