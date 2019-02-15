var test = require("tape");
const reduceData = data => {
  return data.reduce((prev, curr) => {
    [...new Set([...Object.keys(prev), ...Object.keys(curr)])].forEach(key => {
      if (!curr[key]) {
        curr[key] = prev[key];
      } else if (typeof curr[key] === "string" && prev[key]) {
        prev[key] = prev[key].includes(curr[key])
          ? prev[key]
          : `${prev[key]}, ${curr[key]}`;
      } else if (!prev[key]) {
        prev[key] = curr[key];
      } else if (Array.isArray(curr[key])) {
        prev[key].includes(curr[key])
          ? [`${prev[key]}`]
          : [`${prev[key]}, ${curr[key]}`];
      } else {
        prev[key] = Boolean(prev[key] || curr[key]);
      }
    });
    return prev;
  });
};

test("hello test", function(t) {
  t.deepEqual(
    reduceData([
      { a: true, b: "foo", c: false, d: true, e: "test" },
      { a: false, b: "bar", c: false, d: true, e: "user" }
    ]),
    { a: true, b: "foo, bar", c: false, d: true, e: "test, user" }
  );
  t.deepEqual(reduceData([{}, {}]), {});
  t.deepEqual(
    reduceData([
      { a: false, b: true, c: "Bauzone", d: "Schulhausstrasse 23" },
      { a: true, b: true, c: "Mischzone", d: "Grabenstrasse 17", e: "Au" }
    ]),
    {
      a: true,
      b: true,
      c: "Bauzone, Mischzone",
      d: "Schulhausstrasse 23, Grabenstrasse 17",
      e: "Au"
    }
  );
  t.deepEqual(
    reduceData([
      { a: false, b: true, c: "false", d: "Schulhausstrasse 23" },
      { a: true, b: true, c: "false", d: "Schulhausstrasse 23" }
    ]),
    {
      a: true,
      b: true,
      c: "false",
      d: "Schulhausstrasse 23"
    }
  );
  t.deepEqual(
    reduceData([
      { a: false, b: true, c: "false", d: "Schulhausstrasse 23" },
      { a: true, b: true, c: "false", d: "Schulhausstrasse 23" },
      { a: false, b: true, c: "false", d: "Schulhausstrasse 23", e: "Test" }
    ]),
    {
      a: true,
      b: true,
      c: "false",
      d: "Schulhausstrasse 23",
      e: "Test"
    }
  );
  t.deepEqual(
    reduceData([
      { a: false, b: true, c: ["Bauzone", "Nutzungszone"] },
      { a: false, b: true, c: ["Bauzone"] }
    ]),
    { a: false, b: true, c: ["Bauzone", "Nutzungszone"] }
  );
  t.end();
});
