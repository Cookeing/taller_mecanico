// cotizacion.js - CORREGIDO PARA PRECARGA

let categoryCounter = 0;
let itemCounter = 0;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Intentar cargar items precargados si existen
    loadPreloadedItems();
    
    // Si no hay items precargados, agregar una categoría vacía
    if (categoryCounter === 0) {
        addCategory();
    }
    
    // Calcular totales iniciales
    calculateGrandTotal();
});

// FUNCIÓN PARA CARGAR ITEMS PRECARGADOS
function loadPreloadedItems() {
    const itemsDataElement = document.getElementById('items-data-json');
    if (!itemsDataElement) {
        return;
    }
    
    try {
        const itemsData = JSON.parse(itemsDataElement.textContent);
        
        if (!itemsData || itemsData.length === 0) {
            return;
        }
        
        // Agrupar items por categoría
        const itemsByCategory = {};
        itemsData.forEach(item => {
            const cat = item.categoria || 'Servicios';
            if (!itemsByCategory[cat]) {
                itemsByCategory[cat] = [];
            }
            itemsByCategory[cat].push(item);
        });
        
        // Crear categorías y agregar items
        Object.keys(itemsByCategory).forEach(categoryName => {
            const categoryId = addCategory();
            const categoryWrapper = document.querySelector(`[data-category-id="${categoryId}"]`);
            
            if (categoryWrapper) {
                // Setear nombre de categoría
                const categoryInput = categoryWrapper.querySelector('.category-name-input');
                if (categoryInput) {
                    categoryInput.value = categoryName;
                }
                
                // Limpiar fila inicial vacía
                const tbody = categoryWrapper.querySelector('.category-body');
                tbody.innerHTML = '';
                
                // Agregar items
                itemsByCategory[categoryName].forEach(item => {
                    addRowToCategory(categoryId, item);
                });
            }
        });
        
        // Calcular totales
        calculateGrandTotal();
        
    } catch (error) {
        console.error('Error al cargar items precargados:', error);
    }
}

// FUNCIÓN PARA AGREGAR CATEGORÍA
function addCategory() {
    categoryCounter++;
    const container = document.getElementById('categorias-container');
    
    if (!container) {
        return null;
    }
    
    const categoryWrapper = document.createElement('div');
    categoryWrapper.className = 'category-wrapper';
    categoryWrapper.setAttribute('data-category-id', categoryCounter);
    
    categoryWrapper.innerHTML = `
        <div class="category-header">
            <input type="text" class="category-name-input" placeholder="Nombre de la categoría" value="CATEGORÍA ${categoryCounter}">
            <button type="button" class="btn-delete-category" onclick="deleteCategory(this)">Eliminar Categoría</button>
        </div>
        <table class="items-table">
            <thead>
                <tr>
                    <th style="width: 40px;">IT</th>
                    <th>DESCRIPCIÓN</th>
                    <th style="width: 80px;">CANTIDAD</th>
                    <th style="width: 120px;">PRECIO UNIT.</th>
                    <th style="width: 120px;">TOTAL</th>
                    <th style="width: 80px;">ACCIONES</th>
                </tr>
            </thead>
            <tbody class="category-body"></tbody>
            <tfoot>
                <tr class="subtotal-row-cat">
                    <td colspan="4" style="text-align: right; font-weight: bold;">SUBTOTAL CATEGORÍA ${categoryCounter}</td>
                    <td class="category-subtotal" style="text-align: right; font-weight: bold;">$0</td>
                    <td></td>
                </tr>
            </tfoot>
        </table>
        <button type="button" class="btn-add-item" onclick="addRowToCategory(${categoryCounter})">+ Agregar Ítem</button>
    `;
    
    container.appendChild(categoryWrapper);
    
    // Agregar una fila inicial si no se están cargando datos precargados
    const itemsDataElement = document.getElementById('items-data-json');
    if (!itemsDataElement) {
        addRowToCategory(categoryCounter);
    }
    
    return categoryCounter;
}

// FUNCIÓN PARA AGREGAR FILA A CATEGORÍA
function addRowToCategory(categoryId, itemData = null) {
    itemCounter++;
    const categoryWrapper = document.querySelector(`[data-category-id="${categoryId}"]`);
    
    if (!categoryWrapper) {
        return;
    }
    
    const tbody = categoryWrapper.querySelector('.category-body');
    const row = document.createElement('tr');
    row.setAttribute('data-row-id', itemCounter);
    
    // Calcular número de ítem dentro de la categoría
    const itemNumber = tbody.querySelectorAll('tr').length + 1;
    
    // Valores por defecto o precargados
    const descripcion = itemData ? itemData.descripcion : '';
    const cantidad = itemData ? itemData.cantidad : 1;
    const precioUnitario = itemData ? itemData.precio_unitario : 0;
    const total = cantidad * precioUnitario;
    
    row.innerHTML = `
        <td class="item-number">${itemNumber}</td>
        <td><input type="text" class="item-descripcion" value="${descripcion}" placeholder="Descripción del ítem"></td>
        <td><input type="number" class="quantity" value="${cantidad}" min="0" step="0.01" oninput="calculateRow(this)"></td>
        <td><input type="number" class="unit-price" value="${precioUnitario}" min="0" step="1" oninput="calculateRow(this)"></td>
        <td class="item-total-cell">${formatCurrency(total)}</td>
        <td><button type="button" class="btn-delete-item" onclick="deleteRow(this)">🗑</button></td>
    `;
    
    tbody.appendChild(row);
    
    // Calcular subtotal de categoría
    calculateCategorySubtotal(categoryWrapper);
}

// FUNCIÓN PARA ELIMINAR FILA
function deleteRow(button) {
    const row = button.closest('tr');
    const tbody = row.closest('tbody');
    
    if (tbody.querySelectorAll('tr').length === 1) {
        showInfoModal('Debe mantener al menos una fila por categoría');
        return;
    }
    showConfirmModal('¿Está seguro que desea eliminar esta fila?', function() {
        row.remove();
        const categoryWrapper = tbody.closest('.category-wrapper');
        renumberCategoryRows(categoryWrapper);
        calculateCategorySubtotal(categoryWrapper);
        calculateGrandTotal();
    });
}

// FUNCIÓN PARA ELIMINAR CATEGORÍA
function deleteCategory(button) {
    const categories = document.querySelectorAll('.category-wrapper');
    
    if (categories.length === 1) {
        showInfoModal('Debe mantener al menos una categoría');
        return;
    }
    showConfirmModal('¿Está seguro que desea eliminar esta categoría?', function() {
        const categoryWrapper = button.closest('.category-wrapper');
        categoryWrapper.remove();
        calculateGrandTotal();
    });
}

// Modal helpers (usa el modal presente en la plantilla)
function showConfirmModal(message, onConfirm) {
    const modal = document.getElementById('confirm-modal');
    if (!modal) {
        // Si el modal no existe, ejecutar acción para mantener compatibilidad
        onConfirm();
        return;
    }
    const msgEl = document.getElementById('confirm-modal-message');
    const btnConfirm = document.getElementById('confirm-modal-confirm');
    const btnCancel = document.getElementById('confirm-modal-cancel');

    msgEl.textContent = message;
    modal.style.display = 'flex';

    function cleanup() {
        modal.style.display = 'none';
        btnConfirm.removeEventListener('click', confirmHandler);
        btnCancel.removeEventListener('click', cancelHandler);
    }

    function confirmHandler() {
        cleanup();
        onConfirm();
    }
    function cancelHandler() { cleanup(); }

    btnConfirm.addEventListener('click', confirmHandler);
    btnCancel.addEventListener('click', cancelHandler);
}

function showInfoModal(message, onClose) {
    const modal = document.getElementById('confirm-modal');
    const errorAlert = document.getElementById('error-alert');
    if (!modal) {
        // Si no hay modal, mostrar en el banner de errores como fallback (sin native alert)
        if (errorAlert) {
            const list = document.getElementById('error-list');
            list.innerHTML = '<li>' + message + '</li>';
            errorAlert.classList.add('show');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        if (typeof onClose === 'function') onClose();
        return;
    }

    const msgEl = document.getElementById('confirm-modal-message');
    const btnConfirm = document.getElementById('confirm-modal-confirm');
    const btnCancel = document.getElementById('confirm-modal-cancel');

    msgEl.textContent = message;
    // Ocultar cancel para info
    btnCancel.style.display = 'none';
    btnConfirm.textContent = 'Aceptar';
    modal.style.display = 'flex';

    function cleanup() {
        modal.style.display = 'none';
        btnCancel.style.display = '';
        btnConfirm.textContent = 'Confirmar';
        btnConfirm.removeEventListener('click', confirmHandler);
    }

    function confirmHandler() { cleanup(); if (typeof onClose === 'function') onClose(); }
    btnConfirm.addEventListener('click', confirmHandler);
}

// RENUMERAR FILAS DE CATEGORÍA
function renumberCategoryRows(categoryWrapper) {
    const rows = categoryWrapper.querySelectorAll('.category-body tr');
    rows.forEach((row, idx) => {
        const itemCell = row.querySelector('.item-number');
        if (itemCell) {
            itemCell.textContent = (idx + 1).toString();
        }
    });
}

// CALCULAR FILA
function calculateRow(element) {
    const row = element.closest('tr');
    const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
    const unitPrice = parseFloat(row.querySelector('.unit-price').value) || 0;
    const total = quantity * unitPrice;
    
    row.querySelector('.item-total-cell').textContent = formatCurrency(total);
    
    const categoryWrapper = element.closest('.category-wrapper');
    calculateCategorySubtotal(categoryWrapper);
}

// CALCULAR SUBTOTAL DE CATEGORÍA
function calculateCategorySubtotal(categoryWrapper) {
    const rows = categoryWrapper.querySelectorAll('.category-body tr');
    let categoryTotal = 0;
    
    rows.forEach(row => {
        const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
        const unitPrice = parseFloat(row.querySelector('.unit-price').value) || 0;
        categoryTotal += (quantity * unitPrice);
    });
    
    const subtotalCell = categoryWrapper.querySelector('.category-subtotal');
    if (subtotalCell) {
        subtotalCell.textContent = formatCurrency(categoryTotal);
    }
    
    calculateGrandTotal();
}

// CALCULAR TOTAL GENERAL
function calculateGrandTotal() {
    let grandSubtotal = 0;
    
    document.querySelectorAll('.category-subtotal').forEach(cell => {
        const value = cell.textContent.replace(/[$.]/g, '').replace(',', '');
        grandSubtotal += parseFloat(value) || 0;
    });
    
    const iva = Math.round(grandSubtotal * 0.19);
    const total = grandSubtotal + iva;
    
    document.getElementById('display-subtotal').textContent = formatCurrency(grandSubtotal);
    document.getElementById('display-iva').textContent = formatCurrency(iva);
    document.getElementById('display-total').textContent = formatCurrency(total);
}

// FORMATEAR MONEDA
function formatCurrency(value) {
    return '$' + Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

// PREPARAR DATOS PARA ENVIAR
document.getElementById('cotizacion-form').addEventListener('submit', function(e) {
    const items = [];
    
    document.querySelectorAll('.category-wrapper').forEach(wrapper => {
        const categoria = wrapper.querySelector('.category-name-input').value || 'Servicios';
        
        wrapper.querySelectorAll('.category-body tr').forEach(row => {
            const descInput = row.querySelector('.item-descripcion');
            const qtyInput = row.querySelector('.quantity');
            const priceInput = row.querySelector('.unit-price');
            
            if (descInput && qtyInput && priceInput) {
                items.push({
                    categoria: categoria,
                    descripcion: descInput.value || 'Servicio',
                    cantidad: parseFloat(qtyInput.value) || 0,
                    precio_unitario: parseFloat(priceInput.value) || 0
                });
            }
        });
    });
    
    document.getElementById('items_data').value = JSON.stringify(items);
});

// Reconstruir la UI de categorías/filas a partir del hidden `items_data`
function rebuildItemsFromHidden() {
    const itemsJson = document.getElementById('items_data').value || '[]';
    let items = [];
    try { items = JSON.parse(itemsJson); } catch (e) { items = []; }

    const container = document.getElementById('categorias-container');
    if (!container) return;

    // Limpiar contenedor
    container.innerHTML = '';
    categoryCounter = 0;
    itemCounter = 0;

    if (!items || items.length === 0) {
        addCategory();
        return;
    }

    // Agrupar por categoría
    const itemsByCategory = {};
    items.forEach(item => {
        const cat = item.categoria || 'Servicios';
        if (!itemsByCategory[cat]) itemsByCategory[cat] = [];
        itemsByCategory[cat].push(item);
    });

    Object.keys(itemsByCategory).forEach(catName => {
        const cid = addCategory();
        const wrapper = document.querySelector(`[data-category-id="${cid}"]`);
        if (!wrapper) return;
        const nameInput = wrapper.querySelector('.category-name-input');
        if (nameInput) nameInput.value = catName;
        const tbody = wrapper.querySelector('.category-body');
        tbody.innerHTML = '';
        itemsByCategory[catName].forEach(it => addRowToCategory(cid, it));
    });

    calculateGrandTotal();
}
