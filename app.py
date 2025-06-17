from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "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"
MODEL_NAME = "nousresearch/deephermes-3-mistral-24b-preview:free"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Chat Natan AI"
        }

        treinamento_premium = """
Você é o Natan AI, uma IA avançada, especialista em programação, inteligência artificial e marketing digital.
Sempre responda com linguagem leve, direta e didática. Nunca gere respostas ofensivas, médicas, jurídicas ou financeiras. 
Analise o tom emocional do usuário. Se houver dúvida, peça mais contexto antes de responder.
(E aqui você continua o restante do seu prompt de comportamento que você já tinha criado antes...)
        """

        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": treinamento_premium},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        response.raise_for_status()
        json_response = response.json()
        ai_message = json_response['choices'][0]['message']['content']
        return jsonify({"resposta": ai_message})

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
