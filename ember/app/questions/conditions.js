/**
 * This file describes the conditions on which certain questions will be
 * displayed.
 *
 * The name of the function is always the name of the question. It receives a
 * `find` function as argument, which helps you to find other questions and
 * their values for the same instance.
 */

const otherValueIs = async (find, otherName, expectedValue) => {
  let otherQuestion = await find(otherName)

  return (await otherQuestion.get('value')) === expectedValue
}

export default {
  'vorgesehene-nutzung': f => otherValueIs(f, 'art-des-vorhabens', 'Baute(n)')
}
