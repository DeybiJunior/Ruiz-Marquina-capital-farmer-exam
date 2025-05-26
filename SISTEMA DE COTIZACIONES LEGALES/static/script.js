document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cotizacionForm');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const resultado = document.getElementById('resultado');
    const btnGenerar = form.querySelector('.btn-generar');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const formData = new FormData(form);
        const data = {
            nombre: formData.get('nombre').trim(),
            email: formData.get('email').trim(),
            tipo_servicio: formData.get('tipo_servicio'),
            descripcion: formData.get('descripcion').trim()
        };

        // Validar campos requeridos
        if (!data.nombre || !data.email || !data.tipo_servicio) {
            mostrarError('Por favor, complete todos los campos obligatorios.');
            return;
        }

        // Validar formato de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            mostrarError('Por favor, ingrese un email válido.');
            return;
        }

        try {
            // Mostrar loading
            mostrarLoading(true);
            ocultarElementos();

            // Enviar petición
            const response = await fetch('/generar_cotizacion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                mostrarResultado(result);
                form.reset();
            } else {
                mostrarError(result.error || 'Error al generar la cotización');
            }

        } catch (err) {
            console.error('Error:', err);
            mostrarError('Error de conexión. Por favor, intente nuevamente.');
        } finally {
            mostrarLoading(false);
        }
    });

    function mostrarLoading(show) {
        loading.style.display = show ? 'block' : 'none';
        btnGenerar.disabled = show;
        
        if (show) {
            btnGenerar.textContent = 'Procesando...';
        } else {
            btnGenerar.textContent = '🧮 Generar Cotización';
        }
    }

    function mostrarError(mensaje) {
        error.textContent = mensaje;
        error.style.display = 'block';
        resultado.style.display = 'none';
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            error.style.display = 'none';
        }, 5000);
    }

    function mostrarResultado(data) {
        error.style.display = 'none';
        
        // Actualizar contenido del resultado
        document.getElementById('numeroCotizacion').innerHTML = 
            `<strong>Número de Cotización:</strong> ${data.numero_cotizacion}`;
        
        document.getElementById('precio').innerHTML = 
            `S/ ${data.precio.toLocaleString()}`;

        const fecha = new Date(data.fecha_creacion).toLocaleDateString('es-PE', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        document.getElementById('detalles').innerHTML = `
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                <p><strong>Cliente:</strong> ${data.nombre_cliente}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Servicio:</strong> ${data.tipo_servicio}</p>
                ${data.descripcion_caso ? `<p><strong>Descripción:</strong> ${data.descripcion_caso}</p>` : ''}
                <p><strong>Fecha:</strong> ${fecha}</p>
            </div>
            <div style="margin-top: 20px; padding: 15px; background: #e8f5e8; border-radius: 8px; text-align: center;">
                <p style="margin: 0; color: #155724; font-weight: 600;">
                    ✅ Cotización generada exitosamente
                </p>
                <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #155724;">
                    Guarde el número de cotización para futuras referencias
                </p>
            </div>
        `;
        
        resultado.style.display = 'block';
        
        // Scroll suave al resultado
        resultado.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    function ocultarElementos() {
        error.style.display = 'none';
        resultado.style.display = 'none';
    }

    // Actualizar precio dinámicamente cuando cambia el servicio
    const selectServicio = document.getElementById('tipo_servicio');
    selectServicio.addEventListener('change', function() {
        const precios = {
            'constitucion': 'S/ 1,500',
            'defensa_laboral': 'S/ 2,000',
            'consultoria_tributaria': 'S/ 800'
        };
        
        // Aquí se podría mostrar el precio seleccionado en tiempo real
        // Por ejemplo, actualizar un elemento de vista previa
    });

    // Validación en tiempo real del email
    const emailInput = document.getElementById('email');
    emailInput.addEventListener('blur', function() {
        const email = this.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (email && !emailRegex.test(email)) {
            this.style.borderColor = '#dc3545';
            this.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
        } else {
            this.style.borderColor = '#e0e6ed';
            this.style.boxShadow = 'none';
        }
    });

    // Mejorar la experiencia del usuario con el campo de descripción
    const descripcionTextarea = document.getElementById('descripcion');
    descripcionTextarea.addEventListener('input', function() {
        // Auto-resize del textarea
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 200) + 'px';
    });

    // Agregar efectos visuales a los campos del formulario
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });

    console.log('🚀 Sistema de Cotizaciones Legales - Frontend cargado');
});