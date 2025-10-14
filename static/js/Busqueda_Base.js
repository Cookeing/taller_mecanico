const SearchUtils = {
  /**
   * Escapa HTML para prevenir XSS
   */
  escapeHtml(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  },

  /**
   * Debounce - retrasa ejecución de función
   */
  debounce(fn, delay) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  },

  /**
   * Fetch JSON con parámetros
   */
  async fetchJson(url, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    const response = await fetch(fullUrl);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  },

  /**
   * Búsqueda case-insensitive
   */
  containsIgnoreCase(haystack, needle) {
    if (!haystack || !needle) return false;
    return haystack.toLowerCase().includes(needle.toLowerCase());
  },
};

// Exportar
if (typeof module !== "undefined" && module.exports) {
  module.exports = SearchUtils;
}
