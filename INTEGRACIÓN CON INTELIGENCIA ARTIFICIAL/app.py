import google.generativeai as genai
import json
from typing import Dict, List
from enum import Enum

class ComplejidadNivel(Enum):
    BAJA = "Baja"
    MEDIA = "Media" 
    ALTA = "Alta"

class AjustePrecio(Enum):
    SIN_AJUSTE = 0
    AJUSTE_MEDIO = 25
    AJUSTE_ALTO = 50

class AnalizadorLegalIA:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel("gemini-2.0-flash")
        
        # Tarifas base por tipo de servicio
        self.tarifas_base = {
            "Consultoría General": 150.00,
            "Redacción de Contratos": 300.00,
            "Litigio Civil": 500.00,
            "Derecho Laboral": 250.00,
            "Derecho Penal": 600.00,
            "Derecho Familiar": 200.00,
            "Derecho Corporativo": 400.00,
            "Derecho Inmobiliario": 350.00,
        }
    
    def analizar_con_ia(self, descripcion: str, tipo_servicio: str) -> Dict:
        try:
            prompt = self._crear_prompt_analisis(descripcion, tipo_servicio)
            
            # Configuración optimizada para Gemini
            generation_config = genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=800,
                top_p=0.8
            )
            
            response = self.client.generate_content(prompt, generation_config=generation_config)
            resultado = self._procesar_respuesta_ia(response.text, tipo_servicio)
            
            return {
                'exito': True,
                'complejidad': resultado['complejidad'],
                'ajuste_precio': resultado['ajuste_precio'],
                'servicios_adicionales': resultado['servicios_adicionales'],
                'propuesta_texto': resultado['propuesta_texto'],
                'tiempo_estimado': resultado['tiempo_estimado'],
                'precio_base': self.tarifas_base.get(tipo_servicio, 200.00),
                'precio_final': self._calcular_precio_final(tipo_servicio, resultado['ajuste_precio']),
                'observaciones': resultado['observaciones']
            }
            
        except Exception as e:
            return self._manejar_error(str(e))
    
    def _crear_prompt_analisis(self, descripcion: str, tipo_servicio: str) -> str:
        return f"""
        Analiza este caso legal de manera profesional:

        DESCRIPCIÓN DEL CASO: {descripcion}
        TIPO DE SERVICIO: {tipo_servicio}

        Responde en el siguiente formato EXACTO:

        COMPLEJIDAD: [Baja/Media/Alta]
        AJUSTE_PRECIO: [0/25/50]
        TIEMPO_ESTIMADO: [X semanas/meses]
        SERVICIOS_ADICIONALES: [lista separada por comas, o "Ninguno"]
        OBSERVACIONES: [puntos clave del análisis]

        PROPUESTA_PROFESIONAL:
        [Genera exactamente 2-3 párrafos profesionales dirigidos al cliente que incluyan:
        - Servicios específicos incluidos
        - Metodología de trabajo clara
        - Tiempo estimado de resolución
        - Condiciones y compromisos básicos
        - Tono profesional y confiable]

        Criterios:
        - BAJA: Casos rutinarios, documentación estándar
        - MEDIA: Casos con elementos únicos, investigación moderada  
        - ALTA: Casos complejos, múltiples partes, precedentes especiales
        
        Ajustes de precio:
        - 0%: Caso completamente estándar
        - 25%: Complejidad media o factores adicionales
        - 50%: Alta complejidad, urgencia o riesgo elevado
        """
    
    def _procesar_respuesta_ia(self, respuesta: str, tipo_servicio: str) -> Dict:
        lineas = respuesta.split('\n')
        
        # Valores por defecto
        resultado = {
            'complejidad': 'Media',
            'ajuste_precio': 0,
            'servicios_adicionales': [],
            'tiempo_estimado': '2-4 semanas',
            'observaciones': 'Análisis estándar',
            'propuesta_texto': ''
        }
        
        capturando_propuesta = False
        
        for linea in lineas:
            linea_limpia = linea.strip()
            
            if linea_limpia.startswith("COMPLEJIDAD:"):
                valor = linea_limpia.split(":", 1)[1].strip()
                if valor in ["Baja", "Media", "Alta"]:
                    resultado['complejidad'] = valor
            
            elif linea_limpia.startswith("AJUSTE_PRECIO:"):
                valor = linea_limpia.split(":", 1)[1].strip()
                if valor in ["0", "25", "50"]:
                    resultado['ajuste_precio'] = int(valor)
            
            elif linea_limpia.startswith("TIEMPO_ESTIMADO:"):
                resultado['tiempo_estimado'] = linea_limpia.split(":", 1)[1].strip()
            
            elif linea_limpia.startswith("SERVICIOS_ADICIONALES:"):
                servicios_str = linea_limpia.split(":", 1)[1].strip()
                if servicios_str.lower() != "ninguno":
                    resultado['servicios_adicionales'] = [s.strip() for s in servicios_str.split(",")]
            
            elif linea_limpia.startswith("OBSERVACIONES:"):
                resultado['observaciones'] = linea_limpia.split(":", 1)[1].strip()
            
            elif linea_limpia.startswith("PROPUESTA_PROFESIONAL:"):
                capturando_propuesta = True
                continue
            
            elif capturando_propuesta and linea_limpia:
                resultado['propuesta_texto'] += linea_limpia + " "
        
        # Generar propuesta básica si no se capturó
        if not resultado['propuesta_texto'].strip():
            resultado['propuesta_texto'] = self._generar_propuesta_basica(tipo_servicio, resultado['tiempo_estimado'])
        
        return resultado
    
    def _generar_propuesta_basica(self, tipo_servicio: str, tiempo_estimado: str) -> str:
        return f"""Estimado cliente, tras revisar su consulta sobre {tipo_servicio.lower()}, hemos evaluado los aspectos técnicos y legales involucrados en su caso. Nuestro equipo especializado se encargará de brindarle el soporte jurídico necesario con la máxima calidad y profesionalismo.

El tiempo estimado para la resolución de su caso es de {tiempo_estimado}, durante el cual mantendremos comunicación constante para informarle sobre los avances. Incluimos asesoría completa, revisión documental y representación según sea necesario.

Nos comprometemos a manejar su caso con total confidencialidad y dedicación, aplicando nuestra experiencia para obtener los mejores resultados posibles en su situación particular."""
    
    def _calcular_precio_final(self, tipo_servicio: str, ajuste_precio: int) -> float:
        precio_base = self.tarifas_base.get(tipo_servicio, 200.00)
        factor_ajuste = 1 + (ajuste_precio / 100)
        return round(precio_base * factor_ajuste, 2)
    
    def _manejar_error(self, error_msg: str) -> Dict:
        # Manejo específico de errores comunes
        if "API_KEY_INVALID" in error_msg or "401" in error_msg:
            mensaje = "API key inválida o expirada"
        elif "RATE_LIMIT_EXCEEDED" in error_msg or "429" in error_msg:
            mensaje = "Límite de solicitudes excedido. Intente más tarde."
        elif "QUOTA_EXCEEDED" in error_msg:
            mensaje = "Cuota de API excedida"
        else:
            mensaje = f"Error en el análisis: {error_msg}"
        
        return {
            'exito': False,
            'error': mensaje,
            'complejidad': 'Media',
            'ajuste_precio': 0,
            'servicios_adicionales': [],
            'propuesta_texto': 'Error al generar propuesta automática. Contacte directamente para cotización personalizada.',
            'tiempo_estimado': '2-4 semanas',
            'precio_base': 200.00,
            'precio_final': 200.00,
            'observaciones': 'Error en análisis automático'
        }

# Función principal requerida
def analizar_con_ia(descripcion: str, tipo_servicio: str, api_key: str = None) -> Dict:
    """
    Función principal para análisis con IA usando Gemini
    
    Args:
        descripcion: Descripción del caso legal
        tipo_servicio: Tipo de servicio legal  
        api_key: Clave de API de Gemini
    
    Returns:
        Dict con análisis completo del caso
    """
    if not api_key:
        import os
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            return {
                'exito': False,
                'error': 'API key de Gemini no configurada',
                'complejidad': 'Media',
                'ajuste_precio': 0,
                'servicios_adicionales': [],
                'propuesta_texto': 'Configure la API key de Gemini para usar el análisis automático.',
                'tiempo_estimado': '2-4 semanas',
                'precio_base': 200.00,
                'precio_final': 200.00
            }
    
    analizador = AnalizadorLegalIA(api_key)
    return analizador.analizar_con_ia(descripcion, tipo_servicio)

# PRUEBA FUNCIONAL
if __name__ == "__main__":
    # Caso de prueba para demostrar funcionalidad
    caso_prueba = {
        "descripcion": """
        Necesito revisar un contrato de compraventa de una propiedad comercial. 
        El inmueble tiene algunos problemas de títulos de propiedad que deben resolverse, 
        y hay cláusulas específicas sobre uso comercial que requieren análisis detallado. 
        Además, una de las partes está en proceso de reestructuración empresarial.
        """,
        "tipo_servicio": "Derecho Inmobiliario"
    }
    
    # Prueba con API key real
    api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    resultado = analizar_con_ia(
        caso_prueba['descripcion'], 
        caso_prueba['tipo_servicio'], 
        api_key
    )
    
    print("=== RESULTADO DEL ANÁLISIS CON IA ===")
    if resultado['exito']:
        print(f"✓ Complejidad detectada: {resultado['complejidad']}")
        print(f"✓ Ajuste de precio recomendado: {resultado['ajuste_precio']}%")
        print(f"✓ Precio base: ${resultado['precio_base']}")
        print(f"✓ Precio final: ${resultado['precio_final']}")
        print(f"✓ Tiempo estimado: {resultado['tiempo_estimado']}")
        print(f"✓ Servicios adicionales: {', '.join(resultado['servicios_adicionales']) if resultado['servicios_adicionales'] else 'Ninguno'}")
        print(f"✓ Observaciones: {resultado['observaciones']}")
        print(f"\n=== PROPUESTA PROFESIONAL GENERADA ===")
        print(resultado['propuesta_texto'])
    else:
        print(f"❌ Error: {resultado['error']}")
        print(f"📄 Propuesta de respaldo: {resultado['propuesta_texto']}")