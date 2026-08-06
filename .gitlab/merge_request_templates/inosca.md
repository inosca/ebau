- [Project issue link]() or gitlab reference...
- [Timed link]()

## Description of changes

<!-- Describe your changes so people outside of your project team understand your changes. -->

<!-- In case of setup changes: Clearly document the change and what steps need to be taken. -->
/label ~"Breaking Setup"

<!-- In case of a bugfix: Clearly document the Bug and the fix so its also understandable for someone not involved in the technical implementation and review. Clearly state if migrations or manual actions are needed!-->
/label ~Bugfix

## Screenshots in case of UI changes


## Testing 
**[What to test?](https://git.adfinis.com/camac-ng/camac-ng/-/blob/main/CONTRIBUTING.md)**
- [ ] I tested the change locally in the UI and with the test suite
- [ ] If this MR includes database migrations, they have been tested against existing data

### Canton testing & communication
<!-- Either use the "All cantons" row OR individual canton rows — not both. Remove whichever rows don't apply, including their /label line. -->

**All cantons**
/label ~"eBau AG" ~"eBau BE" ~"eBau GR" ~"eBau SG" ~"eBau SO" ~"eBau SZ" ~"eBau UR"
- [ ] tested
- [ ] tech lead informed

~"eBau AG"
/label  ~"eBau AG"
- [ ] tested
- [ ] tech lead informed

~"eBau BE"
/label ~"eBau BE"
- [ ] tested
- [ ] tech lead informed

~"eBau GR"
/label ~"eBau GR"
- [ ] tested
- [ ] tech lead informed

~"eBau SG"
/label ~"eBau SG"
- [ ] tested
- [ ] tech lead informed

~"eBau SO"
/label ~"eBau SO"
- [ ] tested
- [ ] tech lead informed

~"eBau SZ"
/label ~"eBau SZ"
- [ ] tested
- [ ] tech lead informed

~"eBau UR"
/label ~"eBau UR"
- [ ] tested
- [ ] tech lead informed

## Ready
Steps to complete before assigning reviews:
- [ ] Template is filled out, the `/label` lines are removed if not applicable, and unaffected canton rows (including their `/label` lines) are removed from Canton testing & communication.
- [ ] Pipeline is green
- [ ] Commits are meaningful and split up if needed
- [ ] MR description contains all necessary information for affected cantons
