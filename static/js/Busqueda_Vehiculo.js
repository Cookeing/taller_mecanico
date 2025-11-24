/**
 * Vehiculo Search Module
 * Búsqueda combinada por cliente y patente
 */
class VehiculoSearch {
  constructor(options = {}) {
    this.clientInput = document.getElementById(options.clientInputId || "search-client-input");
    this.vehiculoInput = document.getElementById(options.vehiculoInputId || "search-vehiculo-input");
    this.resultsBody = document.getElementById(options.resultsBodyId || "results-body");

    this.apiVehiculosPorCliente = options.apiVehiculosPorCliente;
    this.apiVehiculosPorPatente = options.apiVehiculosPorPatente;
    this.debounceDelay = options.debounceDelay || 300;
    this.detailUrlPattern = options.detailUrlPattern || "/vehiculos/{id}/";
    this.editUrlPattern = options.editUrlPattern || "/vehiculos/{id}/editar/";
    this.listUrl = options.listUrl;
    this.originalData = null;

    if (!this.apiVehiculosPorCliente || !this.apiVehiculosPorPatente) {
      console.error("VehiculoSearch: faltan URLs de API");
      return;
    }

    this.init();
  }

  init() {
    if (!this.clientInput || !this.vehiculoInput) {
      console.error("VehiculoSearch: No se encontraron los inputs");
      return;
    }

    this.guardarDatosOriginales();

    const debouncedSearch = this.debounce(() => {
      this.realizarBusquedaCombinada();
    }, this.debounceDelay);

    this.clientInput.addEventListener("input", debouncedSearch);
    this.vehiculoInput.addEventListener("input", debouncedSearch);
  }

  guardarDatosOriginales() {
    const originalRows = document.querySelectorAll("#results-body tr");
    if (originalRows.length > 0 && !originalRows[0].innerHTML.includes("No hay")) {
      this.originalData = Array.from(originalRows).map((row) => {
        const cells = row.querySelectorAll("td");
        const verLink = row.querySelector('a[href*="/vehiculos/"]');
        const id = verLink ? verLink.getAttribute("href").match(/\/vehiculos\/(\d+)\//)?.[1] : null;

        return {
          id: id,
          patente: cells[0].textContent.trim(),
          marca: cells[1].textContent.trim(),
          modelo: cells[2].textContent.trim(),
          cliente: cells[3].textContent.trim(),
          cliente_rut: cells[4].textContent.trim(),
        };
      });
    }
  }

  debounce(fn, delay) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  escape(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  render(items) {
    if (!items || items.length === 0) {
      this.resultsBody.innerHTML = '<tr><td colspan="6">No se encontraron vehículos.</td></tr>';
      return;
    }

    const rows = items.map((v) => {
      const detailUrl = this.detailUrlPattern.replace("{id}", v.id);
      const editUrl = this.editUrlPattern.replace("{id}", v.id);

      return `<tr>
        <td>${this.escape(v.patente)}</td>
        <td>${this.escape(v.marca || "-")}</td>
        <td>${this.escape(v.modelo || "-")}</td>
        <td>${this.escape(v.cliente || "")}</td>
        <td>${this.escape(v.cliente_rut || "")}</td>
        <td>
          <a href="${detailUrl}" class="btn btn-sm btn-outline-primary">Ver</a>
          <a href="${editUrl}" class="btn btn-sm btn-outline-secondary">Editar</a>
        </td>
      </tr>`;
    }).join("");

    this.resultsBody.innerHTML = rows;
  }

  async realizarBusquedaCombinada() {
    const clienteQuery = this.clientInput.value.trim();
    const patenteQuery = this.vehiculoInput.value.trim();

    if (!clienteQuery && !patenteQuery) {
      if (this.originalData) {
        this.render(this.originalData);
      } else {
        window.location.href = this.listUrl;
      }
      return;
    }

    try {
      let resultados = [];

      if (clienteQuery) {
        const url = `${this.apiVehiculosPorCliente}?q=${encodeURIComponent(clienteQuery)}`;
        const respCliente = await fetch(url);
        if (!respCliente.ok)
          throw new Error(`Error en búsqueda por cliente: ${respCliente.status}`);
        const dataCliente = await respCliente.json();
        resultados = dataCliente;
      }

      if (patenteQuery) {
        if (resultados.length > 0) {
          resultados = resultados.filter((v) =>
            v.patente.toLowerCase().includes(patenteQuery.toLowerCase())
          );
        } else {
          const url = `${this.apiVehiculosPorPatente}?q=${encodeURIComponent(patenteQuery)}`;
          const respPatente = await fetch(url);
          if (!respPatente.ok)
            throw new Error(`Error en búsqueda por patente: ${respPatente.status}`);
          const dataPatente = await respPatente.json();
          resultados = dataPatente;
        }
      }

      this.render(resultados);
    } catch (err) {
      console.error("Error en búsqueda combinada:", err);
      this.resultsBody.innerHTML =
        '<tr><td colspan="6">Error al buscar. Intente de nuevo.</td></tr>';
    }
  }
}

// Exportar
if (typeof module !== "undefined" && module.exports) {
  module.exports = VehiculoSearch;
}
