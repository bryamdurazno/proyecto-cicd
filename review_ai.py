import os
import sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

with open("app.py", "r", encoding="utf-8") as f:
    codigo = f.read()

prompt = f"""
Eres un revisor de código dentro de un pipeline CI/CD.

Revisa el siguiente código Python.

Debes detectar:
- errores de sintaxis o programación;
- errores evidentes que impidan ejecutar la aplicación;
- problemas graves de seguridad;
- código incompleto o claramente incorrecto.

Si el código puede continuar al despliegue, responde exactamente:
APPROVED

Si encuentras un problema que debería impedir el despliegue, responde exactamente:
REJECTED

Después de APPROVED o REJECTED explica brevemente el motivo.

Código:

```python
{codigo}

"""

response = client.responses.create(
model="gpt-5-mini",
input=prompt
)

resultado = response.output_text.strip()

print("Resultado de la revisión de IA:")
print(resultado)

if resultado.startswith("REJECTED"):
    print("La IA rechazó el código. Se detiene el pipeline.")
sys.exit(1)

if resultado.startswith("APPROVED"):
    print("La IA aprobó el código.")
sys.exit(0)

print("La IA no devolvió una respuesta válida.")
sys.exit(1)