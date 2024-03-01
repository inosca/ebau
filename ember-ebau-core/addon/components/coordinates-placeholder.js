import Component from "@glimmer/component";

export default class CoordinatesPlaceholderComponent extends Component {
  get x() {
    return this.args.field.document.findAnswer("parzellen")?.[0]?.[
      "lagekoordinaten-ost"
    ];
  }

  get y() {
    return this.args.field.document.findAnswer("parzellen")?.[0]?.[
      "lagekoordinaten-nord"
    ];
  }

  get text() {
    const raw = this.args.field.question.raw.staticContent;
    const matches = raw.matchAll(/{replace-coords:([^}]*)}/g);

    const text = matches.reduce((text, match) => {
      const value =
        this.x && this.y
          ? match[1].replace(/x/g, this.x).replace(/y/g, this.y)
          : "";

      return text.replace(match[0], value);
    }, raw);

    return text;
  }
}
