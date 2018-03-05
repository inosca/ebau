/**
 * This file describes the conditions on which certain questions will be
 * displayed.
 *
 * The name of the function is always the name of the question. It receives two
 * functions as arguments:
 *
 * 1. findQuestions: Function to find a question object (generated in the
 *                   camac-questions service) by name
 *
 * 2. findValue: Function to find the value of a question (limited to the same
 *               instance)
 */

export default {
  'vorgesehene-nutzung'(findQuestion, findValue) {
    return (
      findValue('art-des-vorhabens') ===
      findQuestion('art-des-vorhabens').config.options[0]
    )
  }
}
