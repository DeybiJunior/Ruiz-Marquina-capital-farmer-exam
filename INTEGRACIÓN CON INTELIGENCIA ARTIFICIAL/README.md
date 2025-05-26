# Sistema de Cotización Legal con IA (Gemini)

Un sistema inteligente para analizar casos legales y generar cotizaciones automáticas utilizando la API de Google Gemini AI.

## 🚀 Características

- **Análisis inteligente de casos**: Evalúa automáticamente la complejidad de casos legales
- **Cotización dinámica**: Calcula precios basados en complejidad y tipo de servicio
- **Propuestas profesionales**: Genera propuestas personalizadas para clientes
- **Múltiples áreas legales**: Soporte para 8 especialidades jurídicas
- **Estimación de tiempo**: Calcula tiempos de resolución realistas
- **Servicios adicionales**: Identifica servicios complementarios necesarios

## 🛠️ Instalación

### Requisitos
- Python 3.7+
- Cuenta de Google AI Studio
- API Key de Gemini

### Instalación de dependencias

```bash
pip install google-generativeai
```

### Configuración de API Key

#### Opción 1: Variable de entorno (Recomendado)
```bash
export GEMINI_API_KEY='tu_api_key_aqui'
```

#### Opción 2: Directamente en el código
**Sitio de obtención de API**: https://aistudio.google.com/apikey

```python
api_key = "tu_api_key_aqui"
resultado = analizar_con_ia(descripcion, tipo_servicio, api_key)
```

## 📖 Uso Básico

### Niveles de Complejidad

**🟢 Baja**
- Casos rutinarios
- Documentación estándar
- Procedimientos conocidos
- Sin ajuste de precio (0%)

**🟡 Media**
- Elementos únicos en el caso
- Investigación moderada requerida
- Algunas complicaciones menores
- Ajuste de precio: 25%

**🔴 Alta**
- Casos muy complejos
- Múltiples partes involucradas
- Precedentes especiales
- Investigación exhaustiva
- Ajuste de precio: 50%

## 🔧 Configuración del Modelo

### Parámetros de Gemini

```python
generation_config = {
    'temperature': 0.3,        # Creatividad controlada
    'max_output_tokens': 800,  # Límite de tokens optimizado
    'top_p': 0.8              # Control de diversidad
}
```

## 📋 Estructura de Respuesta

```python
{
    'exito': True,
    'complejidad': 'Media',           # Baja/Media/Alta
    'ajuste_precio': 25,              # 0, 25 o 50
    'servicios_adicionales': ['Revisión de contratos', 'Due diligence'],
    'propuesta_texto': 'Propuesta profesional generada...',
    'tiempo_estimado': '4-6 semanas',
    'precio_base': 350.00,
    'precio_final': 437.50,           # Base + ajuste
    'observaciones': 'Análisis detallado del caso'
}
```

## 📝 Ejemplos de Casos

### Caso 1: Derecho Laboral
```python
caso_laboral = """
Empleado despedido injustificadamente después de 5 años.
Requiere cálculo de indemnizaciones y posible demanda laboral.
Hay evidencia de discriminación por edad.
"""

resultado = analizar_con_ia(caso_laboral, "Derecho Laboral")
# Resultado esperado: Complejidad Media, Ajuste 25%, ~$312.50
```

### Caso 2: Derecho Familiar
```python
caso_familiar = """
Proceso de divorcio contencioso con menores de edad.
Disputas sobre custodia y división de bienes.
Incluye empresa familiar valorada en $500,000.
"""

resultado = analizar_con_ia(caso_familiar, "Derecho Familiar")
# Resultado esperado: Complejidad Alta, Ajuste 50%, ~$300.00
```

### Caso 3: Derecho Corporativo
```python
caso_corporativo = """
Fusión de dos empresas tecnológicas.
Due diligence completo, revisión regulatoria.
Estructuración fiscal y contratos complejos.
"""

resultado = analizar_con_ia(caso_corporativo, "Derecho Corporativo")
# Resultado esperado: Complejidad Alta, Ajuste 50%, ~$600.00
```

## ⚠️ Manejo de Errores

El sistema maneja automáticamente:

- **API Key inválida**: Error 401
- **Límite de solicitudes**: Error 429
- **Cuota excedida**: Quota exceeded
- **Errores de red**: Timeout y conexión
- **Respuestas malformadas**: Parser robusto

```python
# Ejemplo de manejo de errores
resultado = analizar_con_ia(descripcion, tipo_servicio)

if not resultado['exito']:
    print(f"Error: {resultado['error']}")
    # El sistema proporciona valores por defecto
    print(f"Propuesta de respaldo: {resultado['propuesta_texto']}")
```
## 👨‍💻 Autor

**DeybiJunior**
- GitHub: [@DeybiJunior](https://github.com/DeybiJunior)
- Email: deybijuniorr@gmail.com

---

⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella en GitHub!