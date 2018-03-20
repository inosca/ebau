/**
 * This file defines how questions will be validated.
 *
 * The name of the question is always the function name. It receives the
 * question object and the value as arguments. It has to return true in case
 * the value is valid or a string containing an error message in case it is an
 * invalid value.
 */

import { isBlank } from '@ember/utils'

export const inOptions = ({ config: { allowOthers, options } }, value) => {
  return (
    allowOthers ||
    options.includes(value) ||
    'Die Antwort muss in den vorgegebenen Optionen vorhanden sein'
  )
}

export const multipleInOptions = (
  { config: { allowOthers, options } },
  value
) => {
  return (
    value.every(
      v => inOptions({ config: { allowOthers, options } }, v) === true
    ) || 'Die Antworten müssen in den vorgegebenen Optionen vorhanden sein'
  )
}

export const required = (_, value) => {
  return !isBlank(value) || 'Diese Frage darf nicht leer gelassen werden'
}

export default {}
