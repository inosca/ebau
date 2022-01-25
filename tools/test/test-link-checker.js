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
    ["www.google.com", "http://foo.bar"]
  );
  t.end();
});

t.test("extraction test", (t) => {
  const links = extract();
  t.equal(links.length, 118);
  t.end();
});

t.test("checks links", async (t) => {
  t.equal(
    await checkLink(
      "https://www.bvd.be.ch/content/dam/bvd/dokumente/de/awa/wasser/gew%C3%A4sserschutz/grundwasserschutz/merkblatt-bauten-im-grundwasser-und-grundwasserabsenkungen-de.pdf"
    ),
    true
  );
  t.equal(
    await checkLink(
      "https://www.bve.be.ch/bve/de/index/direktion/organisation/awa/formulare_bewilligungen/Grundwasser.assetref/dam/documents/BVE/nope.pdf"
    ),
    false
  );
  t.end();
});
