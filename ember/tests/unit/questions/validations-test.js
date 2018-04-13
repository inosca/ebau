import { module, test } from 'qunit'
import { setupTest } from 'ember-qunit'
import validations from 'citizen-portal/questions/validations'

const {
  validateRequired,
  validateText,
  validateNumber,
  validateRadio,
  validateCheckbox,
  validateSelect,
  validateMultiselect
} = validations

module('Unit | Validations | questions', function(hooks) {
  setupTest(hooks)

  test('it validates required fields correctly', function(assert) {
    assert.expect(3)

    assert.equal(validateRequired({}, 'test'), true)
    assert.equal(
      validateRequired({}, ''),
      'Diese Frage darf nicht leer gelassen werden'
    )
    assert.equal(
      validateRequired({}, null),
      'Diese Frage darf nicht leer gelassen werden'
    )
  })

  test('it validates text fields correctly', function(assert) {
    assert.expect(4)

    assert.equal(validateText({}, ''), true)
    assert.equal(validateText({}, 'test'), true)
    assert.equal(
      validateText({ minlength: 3 }, '12'),
      'Der Wert muss mehr als 2 Zeichen lang sein'
    )
    assert.equal(
      validateText({ maxlength: 3 }, '1234'),
      'Der Wert muss weniger als 4 Zeichen lang sein'
    )
  })

  test('it validates number fields correctly', function(assert) {
    assert.expect(5)

    assert.equal(validateNumber({}, ''), true)
    assert.equal(validateNumber({}, '1'), true)
    assert.equal(validateNumber({}, 'test'), 'Der Wert muss eine Zahl sein')
    assert.equal(
      validateNumber({ min: 3 }, '2'),
      'Der Wert muss grösser als 2 sein'
    )
    assert.equal(
      validateNumber({ max: 3 }, '4'),
      'Der Wert muss kleiner als 4 sein'
    )
  })

  test('it validates radio fields correctly', function(assert) {
    assert.expect(2)

    const options = ['option 1', 'option 2', 'option 3']

    assert.equal(validateRadio({ options }, 'option 1'), true)
    assert.equal(
      validateRadio({ options }, 'test'),
      'Der Wert muss in den vorgegebenen Optionen vorhanden sein'
    )
  })

  test('it validates checkbox fields correctly', function(assert) {
    assert.expect(4)

    const options = ['option 1', 'option 2', 'option 3']

    assert.equal(validateCheckbox({ options }, ['option 1']), true)
    assert.equal(validateCheckbox({ options }, ['option 1', 'option 2']), true)
    assert.equal(
      validateCheckbox({ options }, ['test']),
      'Die Werte müssen in den vorgegebenen Optionen vorhanden sein'
    )
    assert.equal(
      validateCheckbox({ options }, ['test 1', 'test 2']),
      'Die Werte müssen in den vorgegebenen Optionen vorhanden sein'
    )
  })

  test('it validates select fields correctly', function(assert) {
    assert.expect(2)

    const options = ['option 1', 'option 2', 'option 3']

    assert.equal(validateSelect({ options }, 'option 1'), true)
    assert.equal(
      validateSelect({ options }, 'test'),
      'Der Wert muss in den vorgegebenen Optionen vorhanden sein'
    )
  })

  test('it validates multiselect fields correctly', function(assert) {
    assert.expect(5)

    const options = ['option 1', 'option 2', 'option 3']

    assert.equal(validateMultiselect({ options }, ['option 1']), true)
    assert.equal(
      validateMultiselect({ options }, ['option 1', 'option 2']),
      true
    )
    assert.equal(
      validateMultiselect({ options }, ['test']),
      'Die Werte müssen in den vorgegebenen Optionen vorhanden sein'
    )
    assert.equal(
      validateMultiselect({ options }, ['test 1', 'test 2']),
      'Die Werte müssen in den vorgegebenen Optionen vorhanden sein'
    )
    assert.equal(
      validateMultiselect({ options, 'allow-custom': true }, ['test 1']),
      true
    )
  })
})
