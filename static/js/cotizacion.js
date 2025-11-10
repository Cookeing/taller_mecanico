// cotizacion.js - VERSIÓN COMPLETA Y FUNCIONAL
let categoryCounter = 0;
let itemCounter = 0;

// Initialize - SOLO FRONTEND
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript de cotización cargado');
    
    // Set default dates si no están establecidas
    const fechaEmision = document.getElementById('ui-fecha-emision');
    const fechaValidez = document.getElementById('ui-fecha-validez');
    
    if (fechaEmision && !fechaEmision.value) {
        const today = new Date().toISOString().split('T')[0];
        fechaEmision.value = today;
    }
    
    if (fechaValidez && !fechaValidez.value) {
        const nextMonth = new Date();
        nextMonth.setMonth(nextMonth.getMonth() + 1);
        const validez = nextMonth.toISOString().split('T')[0];
        fechaValidez.value = validez;
    }
});

function clearClientFields() {
    document.getElementById('ui-client-name').value = '';
    document.getElementById('ui-client-rut').value = '';
    document.getElementById('ui-client-phone').value = '';
    document.getElementById('ui-client-address').value = '';
    document.getElementById('ui-client-email').value = '';
    document.getElementById('ui-client-contact').value = '';
}

function formatCurrency(value) {
    return '$' + Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function loadLogo(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const logoUpload = document.getElementById('logo-upload');
            logoUpload.innerHTML = `<img src="${e.target.result}" alt="Logo">`;
        }
        reader.readAsDataURL(file);
    }
}

// ========== SISTEMA DE CATEGORÍAS Y FILAS ==========

function addCategory() {
    console.log('Ejecutando addCategory...');
    categoryCounter++;
    const container = document.getElementById('categories-container');
    
    if (!container) {
        console.error('No se encontró el contenedor de categorías');
        return;
    }
    
    const categoryWrapper = document.createElement('div');
    categoryWrapper.className = 'category-wrapper';
    categoryWrapper.setAttribute('data-category-id', categoryCounter);
    // contador local de items para esta categoría (se usará para numeración visible)
    categoryWrapper.setAttribute('data-next-item', '1');
    
    categoryWrapper.innerHTML = `
        <div class="category-header-section">
            <input type="text" class="category-name-input" placeholder="Nombre de la categoría ${categoryCounter}" value="CATEGORÍA ${categoryCounter}">
            <button type="button" class="delete-category-btn">🗑️ Eliminar Categoría</button>
        </div>
        
        <table>
            <tr>
                <td class="column-header">ITEM</td>
                <td class="column-header">DESCRIPCIÓN</td>
                <td class="column-header">UNIDAD</td>
                <td class="column-header">CANTIDAD</td>
                <td class="column-header">PRECIO UNITARIO</td>
                <td class="column-header">TOTAL</td>
                <td class="column-header">ACCIONES</td>
            </tr>
            <tbody class="category-body">
                <!-- Rows will be added here -->
            </tbody>
            <tr class="subtotal-row">
                <td colspan="5">SUBTOTAL</td>
                <td class="category-subtotal">$0</td>
                <td></td>
            </tr>
        </table>
        
        <div class="action-buttons">
            <button type="button" class="add-row-btn" data-category-id="${categoryCounter}">+ Agregar Fila</button>
        </div>
    `;
    
    container.appendChild(categoryWrapper);
    console.log('Categoría agregada al DOM');
    
    // Agregar event listeners
    const deleteBtn = categoryWrapper.querySelector('.delete-category-btn');
    const addRowBtn = categoryWrapper.querySelector('.add-row-btn');
    
    deleteBtn.addEventListener('click', function() {
        console.log('Eliminando categoría...');
        deleteCategory(categoryWrapper);
    });
    
    addRowBtn.addEventListener('click', function() {
        console.log('Agregando fila a categoría...');
        const categoryId = parseInt(this.getAttribute('data-category-id'));
        addRowToCategory(categoryId);
    });
    
    // Add 1 initial row
    addRowToCategory(categoryCounter);
    
    // Retornar el elemento creado
    return categoryWrapper;
}

function addRowToCategory(categoryId) {
    console.log('Ejecutando addRowToCategory para categoría:', categoryId);
    // itemCounter sirve solo como ID único; la numeración visible se recalcula por categoría
    itemCounter++;
    const categoryWrapper = document.querySelector(`[data-category-id="${categoryId}"]`);
    
    if (!categoryWrapper) {
        console.error('No se encontró la categoría:', categoryId);
        return;
    }
    
    const tbody = categoryWrapper.querySelector('.category-body');
    
    const row = document.createElement('tr');
    row.setAttribute('data-row-id', itemCounter);
    
    row.innerHTML = `
        <td class="item-number">0</td>
        <td class="description-cell"><input type="text" placeholder="Descripción del servicio"></td>
        <td class="unit-cell">
            <select>
                <option value="un">Unidad</option>
                <option value="hr">Hora</option>
                <option value="servicio">Servicio</option>
            </select>
        </td>
        <td class="quantity-cell"><input type="number" class="quantity" value="1" min="0" step="0.01"></td>
        <td class="unit-price-cell"><input type="number" class="unit-price" value="0" min="0" step="1"></td>
        <td class="total-cell"><input type="text" class="row-total" value="$0" readonly></td>
        <td class="actions-cell">
            <button type="button" class="delete-row-btn">✕</button>
        </td>
    `;
    
    tbody.appendChild(row);
    console.log('Fila agregada al DOM');

    // Recalcular numeración visible para esta categoría
    renumberCategoryRows(categoryWrapper);
    
    // Event listeners
    const deleteBtn = row.querySelector('.delete-row-btn');
    deleteBtn.addEventListener('click', function() {
        console.log('Eliminando fila...');
        deleteRow(this);
    });
    
    const cantidadInput = row.querySelector('.quantity');
    const precioInput = row.querySelector('.unit-price');
    
    cantidadInput.addEventListener('input', function() {
        calculateRow(this);
    });
    precioInput.addEventListener('input', function() {
        calculateRow(this);
    });
}

function deleteRow(button) {
    const row = button.closest('tr');
    const tbody = row.closest('tbody');
    
    if (tbody.querySelectorAll('tr').length <= 1) {
        alert('Debe mantener al menos una fila por categoría');
        return;
    }
    
    row.remove();
    // Re-numerar filas de la categoría después de eliminar
    const categoryWrapper = tbody.closest('.category-wrapper');
    if (categoryWrapper) renumberCategoryRows(categoryWrapper);
    calculateGrandTotal();
}

function deleteCategory(categoryRef) {
    const categories = document.querySelectorAll('.category-wrapper');
    
    if (categories.length <= 1) {
        alert('Debe mantener al menos una categoría');
        return;
    }
    
    if (!confirm('¿Está seguro que desea eliminar esta categoría?')) return;

    // categoryRef puede ser el elemento wrapper o un ID
    let categoryWrapper = null;
    if (typeof categoryRef === 'object' && categoryRef.classList && categoryRef.classList.contains('category-wrapper')) {
        categoryWrapper = categoryRef;
    } else {
        categoryWrapper = document.querySelector(`[data-category-id="${categoryRef}"]`);
    }

    if (categoryWrapper) {
        categoryWrapper.remove();
        // Recalcular numeración de categorías y totales
        renumberCategories();
        calculateGrandTotal();
    }
}

// Recalcula la numeración visible de filas dentro de una categoría (1..n)
function renumberCategoryRows(categoryWrapper) {
    const rows = categoryWrapper.querySelectorAll('.category-body tr');
    rows.forEach((row, idx) => {
        const itemCell = row.querySelector('.item-number');
        if (itemCell) itemCell.textContent = (idx + 1).toString();
    });
}

// Recalcula la etiqueta/placeholder visible de las categorías según su orden en el DOM
function renumberCategories() {
    const wrappers = document.querySelectorAll('.category-wrapper');
    wrappers.forEach((wrapper, idx) => {
        const input = wrapper.querySelector('.category-name-input');
        const defaultLabel = `CATEGORÍA ${idx + 1}`;
        // Solo reemplazar si el usuario no cambió el nombre (mantiene si no comienza con 'CATEGORÍA')
        if (input) {
            const val = input.value || '';
            if (val.trim() === '' || /^CATEGORÍA\s*\d+/i.test(val)) {
                input.value = defaultLabel;
            }
            input.setAttribute('placeholder', `Nombre de la categoría ${idx + 1}`);
        }
        // Actualizar el data-category-id del botón add-row NO se toca; IDs internos permanecen únicos
    });
}

// ========== CÁLCULOS ==========

function calculateRow(element) {
    const row = element.closest('tr');
    const quantity = parseFloat(row.querySelector('.quantity').value) || 0;
    const unitPrice = parseFloat(row.querySelector('.unit-price').value) || 0;
    const total = quantity * unitPrice;
    
    row.querySelector('.row-total').value = formatCurrency(total);
    
    calculateCategorySubtotal(element);
}

function calculateCategorySubtotal(element) {
    const categoryWrapper = element.closest('.category-wrapper');
    const rows = categoryWrapper.querySelectorAll('.category-body tr');
    let categoryTotal = 0;

    rows.forEach(row => {
        const totalInput = row.querySelector('.row-total');
        if (totalInput) {
            const value = totalInput.value.replace(/[^\d]/g, '');
            categoryTotal += parseFloat(value) || 0;
        }
    });

    const subtotalCell = categoryWrapper.querySelector('.category-subtotal');
    if (subtotalCell) {
        subtotalCell.textContent = formatCurrency(categoryTotal);
    }

    calculateGrandTotal();
}

function calculateGrandTotal() {
    let grandSubtotal = 0;
    
    document.querySelectorAll('.category-subtotal').forEach(cell => {
        const value = cell.textContent.replace(/[^\d]/g, '');
        grandSubtotal += parseFloat(value) || 0;
    });

    const iva = Math.round(grandSubtotal * 0.19);
    const total = grandSubtotal + iva;

    document.getElementById('subtotal').textContent = formatCurrency(grandSubtotal);
    document.getElementById('iva').textContent = formatCurrency(iva);
    document.getElementById('total').textContent = formatCurrency(total);
}

function updateItemsData() {
    const items = [];
    
    document.querySelectorAll('.category-wrapper').forEach(wrapper => {
        const categoria = wrapper.querySelector('.category-name-input').value;
        
        wrapper.querySelectorAll('.category-body tr').forEach(row => {
            const descInput = row.querySelector('.description-cell input');
            const unitSelect = row.querySelector('.unit-cell select');
            const qtyInput = row.querySelector('.quantity');
            const priceInput = row.querySelector('.unit-price');
            
            if (descInput && qtyInput && priceInput) {
                items.push({
                    categoria: categoria,
                    descripcion: descInput.value || 'Servicio',
                    cantidad: parseFloat(qtyInput.value) || 0,
                    precio_unitario: parseFloat(priceInput.value) || 0,
                    unidad: unitSelect ? unitSelect.value : 'un'
                });
            }
        });
    });
    
    // Actualizar el campo hidden del formulario Django
    if (document.getElementById('items-data')) {
        document.getElementById('items-data').value = JSON.stringify(items);
        console.log('Items data actualizado:', items);
    }
}

// ========== ACCIONES ==========

function printQuote() {
    window.print();
}

function exportToCSV() {
    alert('Funcionalidad de exportación a CSV - Solo frontend');
}

// Prevenir cualquier comportamiento no deseado
document.addEventListener('click', function(e) {
    // Prevenir cualquier acción en botones que no sean submit
    if (e.target.type === 'button') {
        e.preventDefault();
        e.stopPropagation();
    }
});