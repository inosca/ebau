import { helper } from '@ember/component/helper'

export function formatDate([date]) {
  if (!(date instanceof Date)) {
    return ''
  }

  let day = String(date.getDate()).padStart(2, 0)
  let month = String(date.getMonth()).padStart(2, 0)
  let year = date.getFullYear()

  let hour = String(date.getHours()).padStart(2, 0)
  let minute = String(date.getMinutes()).padStart(2, 0)

  return `${day}.${month}.${year} ${hour}:${minute}`
}

export default helper(formatDate)
