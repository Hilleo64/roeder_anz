class RoedertalPanel extends HTMLElement {

    connectedCallback() {

        this.innerHTML = `
            <ha-card>
                <div style="padding:24px">
                    <h1>📰 Rödertal-Anzeiger</h1>

                    <p>Version 0.5.0-alpha2</p>

                    <p>Frontend erfolgreich geladen.</p>

                </div>
            </ha-card>
        `;

    }

}

customElements.define(
    "roedertal-panel",
    RoedertalPanel
);