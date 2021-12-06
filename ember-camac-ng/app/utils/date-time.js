export default function dateTime(date) {
  const dateDate = `${date.getDate()}.${date.getMonth()}.${date.getFullYear()}`;
  const dateTime = `${`0${date.getHours()}`.slice(
    -2
  )}:${`0${date.getMinutes()}`.slice(-2)}`;
  return `${dateDate}, ${dateTime}`;
}
