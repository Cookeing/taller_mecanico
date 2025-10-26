/**
 * Cliente Search Module
 * Módulo reutilizable para búsqueda en vivo de clientes
 * Usa SearchUtils para funcionalidades compartidas
 * 
 */

class ClienteSearch {
  constructor(options = {}) {
    // Elementos del DOM
    this.input = document.getElementById(options.inputId || "search-input");
    this.resultsBody = document.getElementById(
      options.resultsBodyId || "results-body"
    );
    this.feedback = document.getElementById(
      options.feedbackId || "search-feedback"
    );
    this.querySpan = document.getElementById(
      options.querySpanId || "search-query"
    );

    // Configuración
    this.apiUrl = options.apiUrl;
    this.debounceDelay = options.debounceDelay || 300;
    this.editUrlPattern = options.editUrlPattern || "/clientes/{id}/editar/";
    this.deleteUrlPattern =
      options.deleteUrlPattern || "/clientes/{id}/borrar/";
    this.colspan = options.colspan || 4;

    // Usar utilidades compartidas si están disponibles
    this.utils =
      typeof SearchUtils !== "undefined"
        ? SearchUtils
        : this.createFallbackUtils();

    if (!this.apiUrl) {
      console.error("ClienteSearch: apiUrl es requerido");
      return;
    }

    this.init();
  }

  /**
   * Crea utilidades fallback si SearchUtils no está disponible
   */
  createFallbackUtils() {
    return {
      escapeHtml: (str) => {
        if (!str) return "";
        return String(str).replace(/[&<>'"]/g, (m) => {
          return {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "'": "&#39;",
            '"': "&quot;",
          }[m];
        });
      },
      debounce: (fn, delay) => {
        let timer;
        return function (...args) {
          clearTimeout(timer);
          timer = setTimeout(() => fn.apply(this, args), delay);
        };
      },
      fetchJson: async (url, params = {}) => {
        const queryString = new URLSearchParams(params).toString();
        const fullUrl = queryString ? `${url}?${queryString}` : url;
        const response = await fetch(fullUrl);
        if (!response.ok)
          throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
      },
    };
  }

  init() {
    if (!this.input) {
      console.error("ClienteSearch: No se encontró el input de búsqueda");
      return;
    }

    // Vincular evento con debounce
    this.input.addEventListener(
      "input",
      this.utils.debounce((e) => {
        this.doSearch(e.target.value);
      }, this.debounceDelay)
    );
  }

  /**
   * Renderiza las filas de la tabla con los resultados
   */
  renderRows(items) {
    if (!items || items.length === 0) {
      this.resultsBody.innerHTML = `<tr><td colspan="${this.colspan}">No se encontraron clientes.</td></tr>`;
      return;
    }

    let html = "";
    for (const c of items) {
      const editUrl = this.editUrlPattern.replace("{id}", c.id);
      const deleteUrl = this.deleteUrlPattern.replace("{id}", c.id);

      html += `<tr>
        <td>${this.utils.escapeHtml(c.nombre)}</td>
        <td>${this.utils.escapeHtml(c.rut)}</td>
        <td>${this.utils.escapeHtml(c.telefono || "")}</td>
        <td>
          <a href="${editUrl}" class="btn btn-sm btn-outline-secondary">Editar</a>
          <a href="${deleteUrl}" class="btn btn-sm btn-outline-danger">Borrar</a>
        </td>
      </tr>`;
    }
    this.resultsBody.innerHTML = html;
  }

  /**
   * Realiza la búsqueda mediante fetch
   */
  async doSearch(query) {
    const q = query.trim();

    // Si el campo está vacío, recargar la página para mostrar todos los clientes
    if (!q || q.length === 0) {
      window.history.replaceState({}, "", window.location.pathname);
      location.href = window.location.pathname;
      return;
    }

    try {
      const data = await this.utils.fetchJson(this.apiUrl, { q });

      // Renderizar resultados
      this.renderRows(data);

      // Mostrar/ocultar feedback
      if (this.feedback && this.querySpan) {
        this.feedback.style.display = data.length ? "block" : "none";
        this.querySpan.textContent = q;
      }
    } catch (err) {
      console.error("Error en búsqueda:", err);
      this.resultsBody.innerHTML = `<tr><td colspan="${this.colspan}">Error al buscar. Intente de nuevo.</td></tr>`;
      if (this.feedback) {
        this.feedback.style.display = "none";
      }
    }
  }

  /**
   * Método público para destruir la instancia espesifica
   */
  destroy() {
    if (this.input) {
      this.input.removeEventListener("input", this.doSearch);
    }
  }
}

// Exportar para uso global o como módulo
if (typeof module !== "undefined" && module.exports) {
  module.exports = ClienteSearch;
}
