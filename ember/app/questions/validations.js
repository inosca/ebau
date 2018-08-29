/**
 * This file defines how questions will be validated.
 *
 * The name of the question is always the function name. It receives the
 * question object and the value as arguments. It has to return true in case
 * the value is valid or a string containing an error message in case it is an
 * invalid value.
 */

import { isBlank } from "@ember/utils";

const validateRequired = (_, value) => {
  return !isBlank(value) || "Diese Frage darf nicht leer gelassen werden";
};

const validateText = ({ minlength, maxlength }, value) => {
  if (isBlank(value)) {
    return true;
  }

  minlength = parseFloat(minlength);
  maxlength = parseFloat(maxlength);

  if (!isNaN(minlength) && value && value.length < minlength) {
    return `Der Wert muss mehr als ${minlength - 1} Zeichen lang sein`;
  }

  if (!isNaN(maxlength) && value && value.length > maxlength) {
    return `Der Wert muss weniger als ${maxlength + 1} Zeichen lang sein`;
  }

  return true;
};

const validateNumber = ({ min, max }, value) => {
  if (isBlank(value)) {
    return true;
  }

  value = parseFloat(value);
  max = parseFloat(max);
  min = parseFloat(min);

  if (isNaN(value)) {
    return "Der Wert muss eine Zahl sein";
  }

  if (!isNaN(min) && value < min) {
    return `Der Wert muss grösser als ${min - 1} sein`;
  }

  if (!isNaN(max) && value > max) {
    return `Der Wert muss kleiner als ${max + 1} sein`;
  }

  return true;
};

const validateCheckbox = ({ options }, value) => {
  if (isBlank(value)) {
    return true;
  }

  if (!value.every(v => options.includes(v))) {
    return "Die Werte müssen in den vorgegebenen Optionen vorhanden sein";
  }

  return true;
};

const validateRadio = ({ options }, value) => {
  if (isBlank(value)) {
    return true;
  }

  if (!options.includes(value)) {
    return "Der Wert muss in den vorgegebenen Optionen vorhanden sein";
  }

  return true;
};

const checkActiveConditionContainsAny = (value, conditionValues) => {
  return value.some(v => conditionValues.includes(v));
};

const checkActiveConditionContainsNotAny = (value, conditionValues) => {
  return value.every(v => !conditionValues.includes(v));
};

const checkActiveConditionGreaterThan = (value, conditionValue) => {
  return value.every(v => v > conditionValue);
};

const checkActiveConditionGreaterThanEquals = (value, conditionValue) => {
  return value.every(v => v >= conditionValue);
};

const checkActiveConditionLowerThan = (value, conditionValue) => {
  return value.every(v => v < conditionValue);
};

const checkActiveConditionLowerThanEquals = (value, conditionValue) => {
  return value.every(v => v <= conditionValue);
};

export default {
  validateRequired,
  validateText,
  validateNumber,
  validateCheckbox,
  validateRadio,

  checkActiveConditionContainsAny,
  checkActiveConditionContainsNotAny,
  checkActiveConditionGreaterThan,
  checkActiveConditionGreaterThanEquals,
  checkActiveConditionLowerThan,
  checkActiveConditionLowerThanEquals
};
