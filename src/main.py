import ollama

def generar_examen(tema, nivel="universidad", num_preguntas= 5):
    prompt = f"""
Actúa como un profesor experto y examinador.

Tema: {tema}
Nivel educativo: {nivel}

Instrucciones:
- Genera {num_preguntas} preguntas de opción múltiple.
- Cada pregunta debe tener 4 opciones (A, B, C, D).
- Marca la respuesta correcta.
- Incluye una breve explicación por pregunta.
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    tema = input("👉 Tema del examen: ")
    examen = generar_examen(tema)

    print("\n📘 EXAMEN GENERADO\n")
    print(examen)
