// ================================================
// COTIZACIÓN V2 - JAVASCRIPT FUNCIONAL
// Sin errores, listo para copiar y pegar
// ================================================

let categoryCounter = 0;
let itemCounter = 0;

// ================================================
// INICIALIZACIÓN AL CARGAR PÁGINA
// ================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Cotización JS cargado correctamente');
    
    // Establecer fechas por defecto si están vacías
    const fechaEmision = document.getElementById('fecha_emision');
    const fechaValidez = document.getElementById('fecha_validez');
    
    if (fechaEmision && !fechaEmision.value) {
        const today = new Date();
        fechaEmision.value = today.toISOString().split('T')[0];
    }
    
    if (fechaValidez && !fechaValidez.value) {
        const nextMonth = new Date();
        nextMonth.setMonth(nextMonth.getMonth() + 1);
        fechaValidez.value = nextMonth.toISOString().split('T')[0];
    }
    
    // Verificar si hay datos para precarga (modo edición)
    const itemsDataElement = document.getElementById('items-data-json');
    if (itemsDataElement && itemsDataElement.textContent.trim()) {
        try {
            const itemsData = JSON.parse(itemsDataElement.textContent);
            console.log('📦 Precargando items:', itemsData);
            precargarItems(itemsData);
        } catch (e) {
            console.error('❌ Error al parsear items:', e);
            addCategory(); // Crear categoría vacía si hay error
        }
    } else {
        console.log('➕ Modo creación - agregando categoría inicial');
        addCategory(); // Modo creación: agregar categoría vacía
    }
    
    // Sincronizar datos al enviar formulario
    const form = document.getElementById('cotizacion-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const itemsData = recolectarItems();
            document.getElementById('items_data').value = JSON.stringify(itemsData);
            console.log('📤 Enviando items:', itemsData);
        });
    }
});

// ================================================
// AGREGAR NUEVA CATEGORÍA
// ================================================

function addCategory() {
    categoryCounter++;
    const container = document.getElementById('categorias-container');
    
    if (!container) {
        console.error('❌ Container de categorías no encontrado');
        return;
    }
    
    const categoryWrapper = document.createElement('div');
    categoryWrapper.className = 'category-wrapper';
    categoryWrapper.setAttribute('data-category-id', categoryCounter);
    categoryWrapper.setAttribute('data-next-item', '1');
    
    categoryWrapper.innerHTML = `
        <div class="category-header">
            <input type="text" 
                   class="category-name-input" 
                   value="CATEGORÍA ${categoryCounter}" 
                   placeholder="Nombre de categoría">
            <button type="button" 
                    class="btn-delete-category" 
                    onclick="deleteCategory(${categoryCounter})">
                ✕ Eliminar categoría
            </button>
        </div>
        <table class="items-table">
            <thead>
                <tr>
                    <th style="width:50px">ITEM</th>
                    <th>DESCRIPCIÓN</th>
                    <th style="width:80px">CANTIDAD</th>
                    <th style="width:120px">VALOR UNITARIO</th>
                    <th style="width:120px">VALOR TOTAL</th>
                    <th style="width:80px">ACCIONES</th>
                </tr>
            </thead>
            <tbody class="items-body">
            </tbody>
            <tfoot>
                <tr class="subtotal-row-cat">
                    <td colspan="4" style="text-align:right;">SUBTOTAL CATEGORÍA ${categoryCounter}</td>
                    <td class="subtotal-display">$0</td>
                    <td></td>
                </tr>
            </tfoot>
        </table>
        <button type="button" 
                class="btn-add-item" 
                onclick="addItemRow(${categoryCounter})">
            + Agregar Ítem
        </button>
    `;
    
    container.appendChild(categoryWrapper);
    addItemRow(categoryCounter); // Agregar una fila inicial
    console.log(`✅ Categoría ${categoryCounter} creada`);
}

// ================================================
// ELIMINAR CATEGORÍA
// ================================================

function deleteCategory(categoryId) {
    if (!confirm('¿Deseas eliminar esta categoría y todos sus ítems?')) {
        return;
    }
    
    const category = document.querySelector(`[data-category-id="${categoryId}"]`);
    if (category) {
        category.remove();
        actualizarTotales();
        console.log(`🗑️ Categoría ${categoryId} eliminada`);
    }
}

// ================================================
// AGREGAR FILA DE ITEM
// ================================================

function addItemRow(categoryId) {
    const category = document.querySelector(`[data-category-id="${categoryId}"]`);
    if (!category) {
        console.error(`❌ Categoría ${categoryId} no encontrada`);
        return;
    }
    
    itemCounter++;
    const itemNumber = parseInt(category.getAttribute('data-next-item'));
    category.setAttribute('data-next-item', itemNumber + 1);
    
    const tbody = category.querySelector('.items-body');
    const row = document.createElement('tr');
    row.className = 'item-row';
    row.setAttribute('data-item-id', itemCounter);
    
    row.innerHTML = `
        <td class="item-number">${itemNumber}</td>
        <td>
            <input type="text" 
                   class="item-descripcion" 
                   placeholder="Descripción del ítem">
        </td>
        <td>
            <input type="number" 
                   class="item-cantidad" 
                   value="1" 
                   min="0" 
                   step="0.01" 
                   oninput="calcularFilaTotal(this)">
        </td>
        <td>
            <input type="number" 
                   class="item-precio" 
                   value="0" 
                   min="0" 
                   step="1" 
                   oninput="calcularFilaTotal(this)">
        </td>
        <td class="item-total-cell">$0</td>
        <td style="text-align:center;">
            <button type="button" 
                    class="btn-delete-item" 
                    onclick="deleteItemRow(${itemCounter})">
                🗑️
            </button>
        </td>
    `;
    
    tbody.appendChild(row);
}

// ================================================
// ELIMINAR FILA DE ITEM
// ================================================

function deleteItemRow(itemId) {
    const row = document.querySelector(`[data-item-id="${itemId}"]`);
    if (!row) return;
    
    const category = row.closest('.category-wrapper');
    row.remove();
    
    if (category) {
        renumerarItems(category);
        actualizarSubtotalCategoria(category.getAttribute('data-category-id'));
    }
    
    actualizarTotales();
}

// ================================================
// RENUMERAR ITEMS DE UNA CATEGORÍA
// ================================================

function renumerarItems(category) {
    const rows = category.querySelectorAll('.item-row');
    rows.forEach((row, index) => {
        const numberCell = row.querySelector('.item-number');
        if (numberCell) {
            numberCell.textContent = index + 1;
        }
    });
    category.setAttribute('data-next-item', rows.length + 1);
}

// ================================================
// CALCULAR TOTAL DE UNA FILA
// ================================================

function calcularFilaTotal(input) {
    const row = input.closest('tr');
    const cantidad = parseFloat(row.querySelector('.item-cantidad').value) || 0;
    const precio = parseFloat(row.querySelector('.item-precio').value) || 0;
    const total = cantidad * precio;
    
    row.querySelector('.item-total-cell').textContent = formatearMoneda(total);
    
    const category = row.closest('.category-wrapper');
    if (category) {
        actualizarSubtotalCategoria(category.getAttribute('data-category-id'));
    }
    
    actualizarTotales();
}

// ================================================
// ACTUALIZAR SUBTOTAL DE CATEGORÍA
// ================================================

function actualizarSubtotalCategoria(categoryId) {
    const category = document.querySelector(`[data-category-id="${categoryId}"]`);
    if (!category) return;
    
    const rows = category.querySelectorAll('.item-row');
    let subtotal = 0;
    
    rows.forEach(row => {
        const cantidad = parseFloat(row.querySelector('.item-cantidad').value) || 0;
        const precio = parseFloat(row.querySelector('.item-precio').value) || 0;
        subtotal += cantidad * precio;
    });
    
    const subtotalDisplay = category.querySelector('.subtotal-display');
    if (subtotalDisplay) {
        subtotalDisplay.textContent = formatearMoneda(subtotal);
    }
}

// ================================================
// ACTUALIZAR TOTALES GENERALES
// ================================================

function actualizarTotales() {
    let subtotalGeneral = 0;
    
    document.querySelectorAll('.category-wrapper').forEach(category => {
        category.querySelectorAll('.item-row').forEach(row => {
            const cantidad = parseFloat(row.querySelector('.item-cantidad').value) || 0;
            const precio = parseFloat(row.querySelector('.item-precio').value) || 0;
            subtotalGeneral += cantidad * precio;
        });
    });
    
    const iva = subtotalGeneral * 0.19;
    const total = subtotalGeneral + iva;
    
    const subtotalEl = document.getElementById('display-subtotal');
    const ivaEl = document.getElementById('display-iva');
    const totalEl = document.getElementById('display-total');
    
    if (subtotalEl) subtotalEl.textContent = formatearMoneda(subtotalGeneral);
    if (ivaEl) ivaEl.textContent = formatearMoneda(iva);
    if (totalEl) totalEl.textContent = formatearMoneda(total);
}

// ================================================
// FORMATEAR MONEDA (FORMATO CHILENO)
// ================================================

function formatearMoneda(valor) {
    return '$' + Math.round(valor).toLocaleString('es-CL');
}

// ================================================
// PRECARGAR ITEMS (MODO EDICIÓN)
// ================================================

function precargarItems(itemsData) {
    if (!itemsData || itemsData.length === 0) {
        console.log('ℹ️ Sin items para precargar');
        addCategory();
        return;
    }
    
    const container = document.getElementById('categorias-container');
    container.innerHTML = '';
    categoryCounter = 0;
    itemCounter = 0;
    
    // Agrupar items por categoría
    const categorias = {};
    itemsData.forEach(item => {
        const catNombre = item.categoria || 'Sin categoría';
        if (!categorias[catNombre]) {
            categorias[catNombre] = [];
        }
        categorias[catNombre].push(item);
    });
    
    console.log('📦 Categorías agrupadas:', Object.keys(categorias));
    
    // Crear cada categoría
    Object.keys(categorias).forEach(nombreCategoria => {
        const items = categorias[nombreCategoria];
        
        categoryCounter++;
        const categoryWrapper = document.createElement('div');
        categoryWrapper.className = 'category-wrapper';
        categoryWrapper.setAttribute('data-category-id', categoryCounter);
        categoryWrapper.setAttribute('data-next-item', String(items.length + 1));
        
        categoryWrapper.innerHTML = `
            <div class="category-header">
                <input type="text" 
                       class="category-name-input" 
                       value="${nombreCategoria}">
                <button type="button" 
                        class="btn-delete-category" 
                        onclick="deleteCategory(${categoryCounter})">
                    ✕ Eliminar categoría
                </button>
            </div>
            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width:50px">ITEM</th>
                        <th>DESCRIPCIÓN</th>
                        <th style="width:80px">CANTIDAD</th>
                        <th style="width:120px">VALOR UNITARIO</th>
                        <th style="width:120px">VALOR TOTAL</th>
                        <th style="width:80px">ACCIONES</th>
                    </tr>
                </thead>
                <tbody class="items-body">
                </tbody>
                <tfoot>
                    <tr class="subtotal-row-cat">
                        <td colspan="4" style="text-align:right;">SUBTOTAL CATEGORÍA</td>
                        <td class="subtotal-display">$0</td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
            <button type="button" 
                    class="btn-add-item" 
                    onclick="addItemRow(${categoryCounter})">
                + Agregar Ítem
            </button>
        `;
        
        container.appendChild(categoryWrapper);
        
        // Agregar cada item a la categoría
        const tbody = categoryWrapper.querySelector('.items-body');
        items.forEach((item, index) => {
            itemCounter++;
            const row = document.createElement('tr');
            row.className = 'item-row';
            row.setAttribute('data-item-id', itemCounter);
            
            const cantidad = parseFloat(item.cantidad) || 0;
            const precio = parseFloat(item.precio_unitario) || 0;
            const total = cantidad * precio;
            
            row.innerHTML = `
                <td class="item-number">${index + 1}</td>
                <td>
                    <input type="text" 
                           class="item-descripcion" 
                           value="${(item.descripcion || '').replace(/"/g, '&quot;')}">
                </td>
                <td>
                    <input type="number" 
                           class="item-cantidad" 
                           value="${cantidad}" 
                           min="0" 
                           step="0.01" 
                           oninput="calcularFilaTotal(this)">
                </td>
                <td>
                    <input type="number" 
                           class="item-precio" 
                           value="${precio}" 
                           min="0" 
                           step="1" 
                           oninput="calcularFilaTotal(this)">
                </td>
                <td class="item-total-cell">${formatearMoneda(total)}</td>
                <td style="text-align:center;">
                    <button type="button" 
                            class="btn-delete-item" 
                            onclick="deleteItemRow(${itemCounter})">
                        🗑️
                    </button>
                </td>
            `;
            
            tbody.appendChild(row);
        });
        
        actualizarSubtotalCategoria(categoryCounter);
        console.log(`✅ Categoría "${nombreCategoria}" cargada con ${items.length} ítems`);
    });
    
    actualizarTotales();
    console.log('✅ Precarga completada exitosamente');
}

// ================================================
// RECOLECTAR ITEMS PARA ENVÍO AL BACKEND
// ================================================

function recolectarItems() {
    const items = [];
    
    document.querySelectorAll('.category-wrapper').forEach(category => {
        const categoryName = category.querySelector('.category-name-input').value || 'Sin categoría';
        
        category.querySelectorAll('.item-row').forEach(row => {
            const descripcion = row.querySelector('.item-descripcion').value || '';
            const cantidad = parseFloat(row.querySelector('.item-cantidad').value) || 0;
            const precio_unitario = parseFloat(row.querySelector('.item-precio').value) || 0;
            
            // Solo agregar si tiene algún dato
            if (descripcion.trim() || cantidad > 0 || precio_unitario > 0) {
                items.push({
                    categoria: categoryName,
                    descripcion: descripcion,
                    cantidad: cantidad,
                    precio_unitario: precio_unitario
                });
            }
        });
    });
    
    return items;
}
