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
      "https://www.bve.be.ch/bve/de/index/direktion/organisation/awa/formulare_bewilligungen/Grundwasser.assetref/dam/documents/BVE/AWA/de/WASSER/Grundwasser/Bauten%20im%20Grundwasser/BA_GA_Merkblatt_Bauten_Grundwasser.pdf"
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
