import { LitElement, html } from "lit";

class RoedertalPanel extends LitElement {

  render() {
    return html`
      <h1>📰 Rödertal-Anzeiger</h1>

      <p>Version alpha2</p>
    `;
  }

}

customElements.define(
  "roedertal-panel",
  RoedertalPanel,
);