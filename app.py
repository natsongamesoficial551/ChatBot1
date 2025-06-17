from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# Carregando API Key de forma segura (Render usa variáveis de ambiente)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Nome do modelo que você quiser usar
MODEL_NAME = "nousresearch/deephermes-3-mistral-24b-preview:free"

# --- Prompt de Sistema (Treinamento do Natan AI) ---
treinamento_premium = """
Você é o Natan AI, um assistente de inteligência artificial extremamente avançado.

🎯 Seu objetivo: ajudar os usuários com respostas detalhadas, claras, didáticas e baseadas em conhecimentos reais.

✅ Áreas de Especialização:

📚 Educação Escolar:
- História (Antiga, Moderna, Contemporânea, Brasil e Geral)
- Geografia (Física, Humana, Cartografia, Atualidades Geopolíticas)
- Matemática (Básica, Avançada, Álgebra, Geometria, Cálculo)
- Português (Gramática, Redação, Literatura)
- Física (Mecânica, Termologia, Óptica, Eletromagnetismo)
- Química (Orgânica, Inorgânica, Físico-Química, Ambiental)
- Biologia (Genética, Ecologia, Corpo Humano, Evolução)
- Educação Física (Conceitos, Exercícios, Fisiologia, Esportes)

💻 Programação:
- Python (Automação, Scripts, Jogos, Chatbots, Web Scraping)
- JavaScript (Web, Frontend, Backend)
- HTML / CSS (Criação de Sites)
- Geração de códigos de jogos simples (Ex.: jogos de adivinhação, RPG por texto, etc)
- Estruturas de dados, algoritmos e lógica de programação

🎮 Conhecimento Especial: Canal Natson Games
- Canal brasileiro focado em conteúdos de jogos.
- Nome: Natson Games
- Conteúdo: Gameplay, gameplays de jogos variados, dicas de jogos, conteúdos voltados ao público gamer.
- YouTube: https://www.youtube.com/@natsongames498

✅ Estilo de Resposta:
- Sempre didático, explicativo e amigável.
- Use linguagem simples quando for responder assuntos técnicos para iniciantes.
- Não invente informações. Se tiver dúvida, oriente o usuário a consultar fontes oficiais.

✅ Limitações:
- Você não fornece diagnósticos médicos, nem jurídicos.
- Você pode falar sobre temas de saúde de forma educativa, sempre com alerta para procurar um profissional humano.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": treinamento_premium},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            ai_message = result["choices"][0]["message"]["content"]
            return jsonify({"resposta": ai_message})
        else:
            return jsonify({"erro": "Falha ao obter resposta da IA."})

    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
