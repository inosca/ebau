import { getWithDefault } from '@ember/object'
import { isBlank } from '@ember/utils'

export const valueInOptions = (obj, value) => {
  let options = getWithDefault(obj, 'configuration.options', [])

  return (
    options.includes(value) ||
    'Die Antwort muss in den vorgegebenen Optionen vorhanden sein'
  )
}

export const notBlank = (_, value) => {
  return !isBlank(value) || 'Diese Frage darf nicht leer gelassen werden'
}

export default {
  'art-der-nutzung': function() {
    return valueInOptions(...arguments) && notBlank(...arguments)
  },
  'vorgesehene-nutzung': function() {
    return notBlank(...arguments)
  }
}
