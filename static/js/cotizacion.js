let categoryCounter = 0;
        let itemCounter = 0;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            // Set default dates
            const today = new Date().toISOString().split('T')[0];
            const nextMonth = new Date();
            nextMonth.setMonth(nextMonth.getMonth() + 1);
            const validez = nextMonth.toISOString().split('T')[0];
            
            document.getElementById('date-from').value = today;
            document.getElementById('date-to').value = validez;
            
            // Set default consecutive number
            if (!localStorage.getItem('lastConsecutive')) {
                localStorage.setItem('lastConsecutive', '0001');
            }
            document.getElementById('consecutive-number').value = localStorage.getItem('lastConsecutive');
            
            // Add first category
            addCategory();
            
            // Load saved data if exists
            loadQuote();
        });

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
                    localStorage.setItem('companyLogo', e.target.result);
                }
                reader.readAsDataURL(file);
            }
        }

        function addCategory() {
            categoryCounter++;
            const container = document.getElementById('categories-container');
            
            const categoryWrapper = document.createElement('div');
            categoryWrapper.className = 'category-wrapper';
            categoryWrapper.setAttribute('data-category-id', categoryCounter);
            
            categoryWrapper.innerHTML = `
                <div class="category-header-section">
                    <input type="text" class="category-name-input" placeholder="Nombre de la categoría ${categoryCounter}" value="CATEGORÍA ${categoryCounter}">
                    <button class="delete-category-btn" onclick="deleteCategory(${categoryCounter})">🗑️ Eliminar Categoría</button>
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
                    <button class="add-row-btn" onclick="addRowToCategory(${categoryCounter})">+ Agregar Fila</button>
                </div>
            `;
            
            container.appendChild(categoryWrapper);
            
            // Add 5 initial rows
            for (let i = 0; i < 5; i++) {
                addRowToCategory(categoryCounter);
            }
            
            saveQuote();
        }

        function addRowToCategory(categoryId) {
            itemCounter++;
            const categoryWrapper = document.querySelector(`[data-category-id="${categoryId}"]`);
            const tbody = categoryWrapper.querySelector('.category-body');
            
            const row = document.createElement('tr');
            row.setAttribute('data-row-id', itemCounter);
            
            row.innerHTML = `
                <td class="item-number">${itemCounter}</td>
                <td class="description-cell"><input type="text" placeholder="Descripción detallada del producto o servicio"></td>
                <td class="unit-cell">
                    <select onchange="saveQuote()">
                        <option value="un">Unidad</option>
                        <option value="m2">m²</option>
                        <option value="m3">m³</option>
                        <option value="ml">Metro lineal</option>
                        <option value="kg">Kilogramo</option>
                        <option value="lt">Litro</option>
                        <option value="gl">Galón</option>
                        <option value="hr">Hora</option>
                        <option value="mes">Mes</option>
                        <option value="servicio">Servicio</option>
                    </select>
                </td>
                <td class="quantity-cell"><input type="number" class="quantity" value="0" min="0" step="0.01" onchange="calculateRow(this)"></td>
                <td class="unit-price-cell"><input type="number" class="unit-price" value="0" min="0" step="1" onchange="calculateRow(this)"></td>
                <td class="total-cell"><input type="text" class="row-total" value="$0" readonly></td>
                <td class="actions-cell">
                    <button class="delete-row-btn" onclick="deleteRow(this)">✕</button>
                </td>
            `;
            
            tbody.appendChild(row);
            saveQuote();
        }

        function deleteRow(button) {
            const row = button.closest('tr');
            const tbody = row.closest('tbody');
            
            if (tbody.querySelectorAll('tr').length <= 1) {
                alert('Debe mantener al menos una fila por categoría');
                return;
            }
            
            row.remove();
            calculateGrandTotal();
            saveQuote();
        }

        function deleteCategory(categoryId) {
            const categories = document.querySelectorAll('.category-wrapper');
            
            if (categories.length <= 1) {
                alert('Debe mantener al menos una categoría');
                return;
            }
            
            if (confirm('¿Está seguro que desea eliminar esta categoría?')) {
                const categoryWrapper = document.querySelector(`[data-category-id="${categoryId}"]`);
                categoryWrapper.remove();
                calculateGrandTotal();
                saveQuote();
            }
        }

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
                    const value = totalInput.value.replace(/[$.\s]/g, '');
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
                const value = cell.textContent.replace(/[$.\s]/g, '');
                grandSubtotal += parseFloat(value) || 0;
            });

            const iva = Math.round(grandSubtotal * 0.19);
            const total = grandSubtotal + iva;

            document.getElementById('subtotal').textContent = formatCurrency(grandSubtotal);
            document.getElementById('iva').textContent = formatCurrency(iva);
            document.getElementById('total').textContent = formatCurrency(total);

            saveQuote();
        }

        function printQuote() {
            window.print();
        }

        function saveQuote() {
            const quoteData = {
                consecutive: document.getElementById('consecutive-number').value,
                dateFrom: document.getElementById('date-from').value,
                dateTo: document.getElementById('date-to').value,
                logo: localStorage.getItem('companyLogo') || '',
                company: {},
                client: {},
                categories: [],
                payment: {},
                observations: document.querySelector('.observations-textarea').value
            };

            // Save company info
            const companyInputs = document.querySelectorAll('.company-name input, .company-details input');
            companyInputs.forEach((input, index) => {
                quoteData.company[`field${index}`] = input.value;
            });

            // Save client info
            const clientInputs = document.querySelectorAll('.client-section input');
            clientInputs.forEach((input, index) => {
                quoteData.client[`field${index}`] = input.value;
            });

            // Save payment conditions
            const paymentSelects = document.querySelectorAll('.payment-conditions select');
            quoteData.payment.formaPago = paymentSelects[0].value;
            quoteData.payment.plazoPago = paymentSelects[1].value;

            // Save categories
            document.querySelectorAll('.category-wrapper').forEach(wrapper => {
                const categoryData = {
                    name: wrapper.querySelector('.category-name-input').value,
                    items: []
                };

                wrapper.querySelectorAll('.category-body tr').forEach(row => {
                    const descInput = row.querySelector('.description-cell input');
                    const unitSelect = row.querySelector('.unit-cell select');
                    const qtyInput = row.querySelector('.quantity');
                    const priceInput = row.querySelector('.unit-price');

                    if (descInput && unitSelect && qtyInput && priceInput) {
                        categoryData.items.push({
                            description: descInput.value,
                            unit: unitSelect.value,
                            quantity: qtyInput.value,
                            unitPrice: priceInput.value
                        });
                    }
                });

                quoteData.categories.push(categoryData);
            });

            localStorage.setItem('quoteData', JSON.stringify(quoteData));
            localStorage.setItem('lastConsecutive', document.getElementById('consecutive-number').value);
        }

        function loadQuote() {
            const savedData = localStorage.getItem('quoteData');
            if (!savedData) return;

            const quoteData = JSON.parse(savedData);

            // Load header info
            if (quoteData.consecutive) document.getElementById('consecutive-number').value = quoteData.consecutive;
            if (quoteData.dateFrom) document.getElementById('date-from').value = quoteData.dateFrom;
            if (quoteData.dateTo) document.getElementById('date-to').value = quoteData.dateTo;

            // Load logo
            if (quoteData.logo) {
                const logoUpload = document.getElementById('logo-upload');
                logoUpload.innerHTML = `<img src="${quoteData.logo}" alt="Logo">`;
            }

            // Load company info
            const companyInputs = document.querySelectorAll('.company-name input, .company-details input');
            Object.keys(quoteData.company).forEach((key, index) => {
                if (companyInputs[index]) {
                    companyInputs[index].value = quoteData.company[key];
                }
            });

            // Load client info
            const clientInputs = document.querySelectorAll('.client-section input');
            Object.keys(quoteData.client).forEach((key, index) => {
                if (clientInputs[index]) {
                    clientInputs[index].value = quoteData.client[key];
                }
            });

            // Load payment conditions
            if (quoteData.payment) {
                const paymentSelects = document.querySelectorAll('.payment-conditions select');
                if (quoteData.payment.formaPago) paymentSelects[0].value = quoteData.payment.formaPago;
                if (quoteData.payment.plazoPago) paymentSelects[1].value = quoteData.payment.plazoPago;
            }

            // Clear existing category
            document.getElementById('categories-container').innerHTML = '';
            categoryCounter = 0;
            itemCounter = 0;

            // Load categories
            if (quoteData.categories && quoteData.categories.length > 0) {
                quoteData.categories.forEach(categoryData => {
                    categoryCounter++;
                    const container = document.getElementById('categories-container');
                    
                    const categoryWrapper = document.createElement('div');
                    categoryWrapper.className = 'category-wrapper';
                    categoryWrapper.setAttribute('data-category-id', categoryCounter);
                    
                    categoryWrapper.innerHTML = `
                        <div class="category-header-section">
                            <input type="text" class="category-name-input" value="${categoryData.name || 'CATEGORÍA ' + categoryCounter}">
                            <button class="delete-category-btn" onclick="deleteCategory(${categoryCounter})">🗑️ Eliminar Categoría</button>
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
                            </tbody>
                            <tr class="subtotal-row">
                                <td colspan="5">SUBTOTAL</td>
                                <td class="category-subtotal">$0</td>
                                <td></td>
                            </tr>
                        </table>
                        
                        <div class="action-buttons">
                            <button class="add-row-btn" onclick="addRowToCategory(${categoryCounter})">+ Agregar Fila</button>
                        </div>
                    `;
                    
                    container.appendChild(categoryWrapper);
                    
                    // Load items
                    categoryData.items.forEach(item => {
                        itemCounter++;
                        const tbody = categoryWrapper.querySelector('.category-body');
                        
                        const row = document.createElement('tr');
                        row.setAttribute('data-row-id', itemCounter);
                        
                        row.innerHTML = `
                            <td class="item-number">${itemCounter}</td>
                            <td class="description-cell"><input type="text" value="${item.description || ''}" placeholder="Descripción detallada del producto o servicio"></td>
                            <td class="unit-cell">
                                <select onchange="saveQuote()">
                                    <option value="un" ${item.unit === 'un' ? 'selected' : ''}>Unidad</option>
                                    <option value="m2" ${item.unit === 'm2' ? 'selected' : ''}>m²</option>
                                    <option value="m3" ${item.unit === 'm3' ? 'selected' : ''}>m³</option>
                                    <option value="ml" ${item.unit === 'ml' ? 'selected' : ''}>Metro lineal</option>
                                    <option value="kg" ${item.unit === 'kg' ? 'selected' : ''}>Kilogramo</option>
                                    <option value="lt" ${item.unit === 'lt' ? 'selected' : ''}>Litro</option>
                                    <option value="gl" ${item.unit === 'gl' ? 'selected' : ''}>Galón</option>
                                    <option value="hr" ${item.unit === 'hr' ? 'selected' : ''}>Hora</option>
                                    <option value="mes" ${item.unit === 'mes' ? 'selected' : ''}>Mes</option>
                                    <option value="servicio" ${item.unit === 'servicio' ? 'selected' : ''}>Servicio</option>
                                </select>
                            </td>
                            <td class="quantity-cell"><input type="number" class="quantity" value="${item.quantity || 0}" min="0" step="0.01" onchange="calculateRow(this)"></td>
                            <td class="unit-price-cell"><input type="number" class="unit-price" value="${item.unitPrice || 0}" min="0" step="1" onchange="calculateRow(this)"></td>
                            <td class="total-cell"><input type="text" class="row-total" value="$0" readonly></td>
                            <td class="actions-cell">
                                <button class="delete-row-btn" onclick="deleteRow(this)">✕</button>
                            </td>
                        `;
                        
                        tbody.appendChild(row);
                        
                        // Calculate row total
                        const qtyInput = row.querySelector('.quantity');
                        calculateRow(qtyInput);
                    });
                });
            } else {
                addCategory();
            }

            // Load observations
            if (quoteData.observations) {
                document.querySelector('.observations-textarea').value = quoteData.observations;
            }

            calculateGrandTotal();
        }

        // Auto-save every 10 seconds
        setInterval(saveQuote, 10000);

        // Save before leaving
        window.addEventListener('beforeunload', saveQuote);

        // Save on any input change
        document.addEventListener('input', function(e) {
            if (e.target.matches('input, textarea, select')) {
                saveQuote();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + P to print
            if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
                e.preventDefault();
                printQuote();
            }
            
            // Ctrl/Cmd + S to save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                saveQuote();
                showNotification('Cotización guardada correctamente');
            }
        });

        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: #28a745;
                color: white;
                padding: 15px 25px;
                border-radius: 5px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                z-index: 2000;
                font-size: 14px;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        }

        // Format RUT as user types (Chilean format)
        function formatRUT(input) {
            let value = input.value.replace(/[^0-9kK]/g, '');
            
            if (value.length > 1) {
                const dv = value.slice(-1);
                let rut = value.slice(0, -1);
                
                // Add dots
                rut = rut.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                
                input.value = rut + '-' + dv;
            } else {
                input.value = value;
            }
        }

        // Add RUT formatting to RUT inputs
        document.addEventListener('input', function(e) {
            if (e.target.matches('input[placeholder*="12.345.678-9"]')) {
                formatRUT(e.target);
            }
        });

        // Export to CSV function
        function exportToCSV() {
            let csv = 'COTIZACIÓN\n\n';
            csv += 'Número:,' + document.getElementById('consecutive-number').value + '\n';
            csv += 'Fecha Emisión:,' + document.getElementById('date-from').value + '\n';
            csv += 'Validez hasta:,' + document.getElementById('date-to').value + '\n\n';
            
            csv += 'DATOS EMPRESA\n';
            document.querySelectorAll('.company-name input, .company-details input').forEach(input => {
                if (input.value) csv += input.value + '\n';
            });
            
            csv += '\nDATOS CLIENTE\n';
            document.querySelectorAll('.client-section input').forEach(input => {
                if (input.value) csv += input.value + ',';
            });
            csv += '\n\n';
            
            document.querySelectorAll('.category-wrapper').forEach(wrapper => {
                csv += wrapper.querySelector('.category-name-input').value + '\n';
                csv += 'Item,Descripción,Unidad,Cantidad,Precio Unitario,Total\n';
                
                wrapper.querySelectorAll('.category-body tr').forEach(row => {
                    const desc = row.querySelector('.description-cell input').value;
                    const unit = row.querySelector('.unit-cell select').value;
                    const qty = row.querySelector('.quantity').value;
                    const price = row.querySelector('.unit-price').value;
                    const total = row.querySelector('.row-total').value;
                    
                    csv += `"${desc}",${unit},${qty},${price},"${total}"\n`;
                });
                csv += '\n';
            });
            
            csv += '\nSUBTOTAL,' + document.getElementById('subtotal').textContent + '\n';
            csv += 'IVA (19%),' + document.getElementById('iva').textContent + '\n';
            csv += 'TOTAL,' + document.getElementById('total').textContent + '\n';
            
            // Download CSV
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'cotizacion_' + document.getElementById('consecutive-number').value + '.csv';
            link.click();
            
            showNotification('CSV exportado correctamente');
        }

        // Add export button
        const exportButton = document.createElement('button');
        exportButton.className = 'print-button';
        exportButton.textContent = '📊 Exportar CSV';
        exportButton.style.bottom = '80px';
        exportButton.style.backgroundColor = '#28a745';
        exportButton.onclick = exportToCSV;
        document.body.appendChild(exportButton);

        // Add new quote button
        const newQuoteButton = document.createElement('button');
        newQuoteButton.className = 'print-button';
        newQuoteButton.textContent = '📄 Nueva Cotización';
        newQuoteButton.style.bottom = '130px';
        newQuoteButton.style.backgroundColor = '#17a2b8';
        newQuoteButton.onclick = function() {
            if (confirm('¿Está seguro que desea crear una nueva cotización? Los datos actuales se perderán.')) {
                localStorage.removeItem('quoteData');
                location.reload();
            }
        };
        document.body.appendChild(newQuoteButton);

        // Console info
        console.log('%c📋 Sistema de Cotizaciones Chile', 'color: #4472c4; font-size: 16px; font-weight: bold;');
        console.log('%cAtajos de teclado:', 'color: #28a745; font-weight: bold;');
        console.log('Ctrl/Cmd + P: Imprimir o guardar como PDF');
        console.log('Ctrl/Cmd + S: Guardar manualmente');
        console.log('%cCaracterísticas:', 'color: #28a745; font-weight: bold;');
        console.log('✓ Autoguardado cada 10 segundos');
        console.log('✓ Formato chileno (RUT, IVA 19%)');
        console.log('✓ Exportación a CSV');
        console.log('✓ Carga de logo empresarial');
        console.log('✓ Cálculo automático de totales');