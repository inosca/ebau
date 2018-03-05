/**
 * This file defines how questions will be validated.
 *
 * The name of the question is always the function name. It receives the
 * question object and the value as arguments. It has to return true in case
 * the value is valid or a string containing an error message in case it is an
 * invalid value.
 */

import { isBlank } from '@ember/utils'

const inOptions = ({ config: { options } }, value) => {
  return (
    options.includes(value) ||
    'Die Antwort muss in den vorgegebenen Optionen vorhanden sein'
  )
}

const notBlank = (_, value) => {
  return !isBlank(value) || 'Diese Frage darf nicht leer gelassen werden'
}

export default {
  'art-des-vorhabens'(q, v) {
    return inOptions(q, v) && notBlank(q, v)
  },
  'vorgesehene-nutzung'(q, v) {
    return notBlank(q, v)
  }
}
