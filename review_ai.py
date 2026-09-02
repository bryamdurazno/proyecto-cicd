import os
import sys
from openai import OpenAI


def get_api_key():
    """Obtiene la API key de OpenRouter desde las variables de entorno."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("No se encontró OPENROUTER_API_KEY.")
    return api_key


def build_client(api_key):
    """Crea el cliente OpenAI apuntando a OpenRouter."""
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )


def read_code(path="app.py"):
    """Lee el contenido del archivo de código a revisar."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"No se encontró el archivo {path}.")


def build_prompt(codigo):
    """Construye el prompt de revisión para la IA."""
    return f"""
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
```
"""


def review_with_ai(client, prompt, model="openrouter/free"):
    """Envía el prompt a la IA y devuelve el texto de la respuesta."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"ERROR al comunicarse con OpenRouter: {e}")


def interpret_result(resultado):
    """
    Interpreta el resultado de la IA y devuelve el código de salida
    apropiado (0 = aprobado, 1 = rechazado o respuesta inválida).
    """
    if resultado.startswith("REJECTED"):
        print("La IA rechazó el código. Se detiene el pipeline.")
        return 1

    if resultado.startswith("APPROVED"):
        print("La IA aprobó el código.")
        return 0

    print("La IA no devolvió una respuesta válida.")
    return 1


def main():
    try:
        api_key = get_api_key()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    client = build_client(api_key)

    try:
        codigo = read_code("app.py")
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    prompt = build_prompt(codigo)

    try:
        resultado = review_with_ai(client, prompt)
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    print("Resultado de la revisión de IA:")
    print(resultado)

    exit_code = interpret_result(resultado)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()