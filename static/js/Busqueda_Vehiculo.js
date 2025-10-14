//vehiculos 

class ClienteSearch {
  constructor(config) {
    // Elementos DOM
    this.input = document.getElementById(config.inputId);
    this.resultsBody = document.getElementById(config.resultsBodyId);
    this.feedback = document.getElementById(config.feedbackId);
    this.querySpan = document.getElementById(config.querySpanId);

    // Configuración
    this.apiUrl = config.apiUrl;
    this.editUrl = config.editUrlPattern;
    this.deleteUrl = config.deleteUrlPattern;

    if (!this.apiUrl) return;
    this.init();
  }

  init() {
    if (!this.input) return;

    this.input.addEventListener(
      "input",
      this.debounce((e) => {
        this.buscar(e.target.value);
      }, 300)
    );
  }

  async buscar(query) {
    const q = query.trim();

    // Si está vacío, recargar página
    if (!q) {
      window.history.replaceState({}, "", window.location.pathname);
      return (location.href = window.location.pathname);
    }

    try {
      const url = `${this.apiUrl}?q=${encodeURIComponent(q)}`;
      const res = await fetch(url);
      const data = await res.json();

      this.render(data);

      // Mostrar feedback
      if (this.feedback && this.querySpan) {
        this.feedback.style.display = data.length ? "block" : "none";
        this.querySpan.textContent = q;
      }
    } catch (err) {
      this.resultsBody.innerHTML =
        '<tr><td colspan="4">Error al buscar.</td></tr>';
      if (this.feedback) this.feedback.style.display = "none";
    }
  }

  render(items) {
    if (!items || items.length === 0) {
      this.resultsBody.innerHTML =
        '<tr><td colspan="4">No se encontraron clientes.</td></tr>';
      return;
    }

    const rows = items
      .map(
        (c) => `
      <tr>
        <td>${this.escape(c.nombre)}</td>
        <td>${this.escape(c.rut)}</td>
        <td>${this.escape(c.telefono || "")}</td>
        <td>
          <a href="${this.editUrl.replace(
            "{id}",
            c.id
          )}" class="btn btn-sm btn-outline-secondary">Editar</a>
          <a href="${this.deleteUrl.replace(
            "{id}",
            c.id
          )}" class="btn btn-sm btn-outline-danger">Borrar</a>
        </td>
      </tr>
    `
      )
      .join("");

    this.resultsBody.innerHTML = rows;
  }

  escape(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  debounce(fn, delay) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }
}

// Exportar
if (typeof module !== "undefined" && module.exports) {
  module.exports = ClienteSearch;
}
