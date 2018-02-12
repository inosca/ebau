import { Promise } from 'rsvp'

export function initialize() {
  window.Promise = Promise
  window.NativePromise = Promise
}

export default {
  initialize
}
