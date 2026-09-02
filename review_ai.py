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

Después de la palabra APPROVED o REJECTED explica brevemente el motivo.

Código:

```python
{codigo}