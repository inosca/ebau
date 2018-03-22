import { helper } from '@ember/component/helper'

export function countKeys([obj = {}]) {
  return Object.keys(obj).length
}

export default helper(countKeys)
