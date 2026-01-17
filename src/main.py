import ollama
import json
import re

def generar_preguntas_json(tema, num_preguntas=3):
    # Pedimos JSON para que Python pueda "entender" el examen
    prompt = f"""
    Eres un experto en {tema}. Genera un examen de {num_preguntas} preguntas.
    RESPONDE EXCLUSIVAMENTE EN FORMATO JSON.
    
    Estructura del JSON:
    {{
      "examen": [
        {{
          "id": 1,
          "pregunta": "¿...?",
          "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
          "correcta": "A",
          "explicacion": "..."
        }}
      ]
    }}
    """
    
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        format="json" # Mistral/Ollama soportan modo JSON
    )
    
    return json.loads(response["message"]["content"])

def ejecutar_entrenamiento(datos_examen):
    score = 0
    preguntas = datos_examen["examen"]
    total = len(preguntas)

    print(f"\n--- INICIO DEL ENTRENAMIENTO ---")
    
    for p in preguntas:
        print(f"\nPregunta {p['id']}: {p['pregunta']}")
        for letra, texto in p['opciones'].items():
            print(f"  {letra}) {texto}")
        
        respuesta_usuario = input("\nTu respuesta (A, B, C, D): ").upper().strip()
        
        if respuesta_usuario == p['correcta']:
            print("✅ ¡Correcto!")
            score += 1
        else:
            print(f"❌ Incorrecto. La respuesta era {p['correcta']}.")
        
        # Aquí es donde ocurre el aprendizaje/retroalimentación
        print(f"Feedback: {p['explicacion']}")
        print("-" * 30)

    print(f"\nResultado final: {score}/{total}")

if __name__ == "__main__":
    tema_input = input("¿Sobre qué quieres entrenar hoy?: ")
    try:
        data = generar_preguntas_json(tema_input)
        ejecutar_entrenamiento(data)
    except Exception as e:
        print(f"Error al procesar el examen: {e}")