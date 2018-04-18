import { computed } from '@ember/object'

const computedTask = (taskName, ...keys) => {
  return computed(...keys, function() {
    let task = this.get(taskName)
    task.perform()
    return task
  })
}

export default computedTask
