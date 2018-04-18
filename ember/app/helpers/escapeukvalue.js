import { helper } from '@ember/component/helper'

export function escapeukvalue([string = '']) {
  return string.replace(/:/, '&colon;')
}

export default helper(escapeukvalue)
