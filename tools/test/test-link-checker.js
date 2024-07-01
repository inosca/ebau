import t from "tap";
import {
  getLinksFromMarkdown,
  extract,
  checkLink,
} from "../lib/link-checker.js";

t.test("parse markdown links", (t) => {
  t.same(
    getLinksFromMarkdown(`
#Foo
bar
asdasd [link](www.google.com) dafjlkdasf
asdjsklf

## heading

### subheading

[another link](http://foo.bar)`),
    ["www.google.com", "http://foo.bar"],
  );
  t.end();
});

t.test("extraction test", (t) => {
  const links = extract();
  t.equal(links.length, 126);
  t.end();
});

t.test("checks links", async (t) => {
  t.equal(await checkLink("https://www.google.com/"), true);
  t.equal(await checkLink("https://www.google.com/404"), false);
  t.end();
});
