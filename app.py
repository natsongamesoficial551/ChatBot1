from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Configuração da Together API
TOGETHER_API_URL = 'https://api.together.xyz/v1/chat/completions'
TOGETHER_API_KEY = '2cf51a2b235f73a6fac6335f527a29e8e893646c5b381a0c791c1c99ec2b31d1'
TOGETHER_MODEL = 'meta-llama/Llama-3-70b-instruct-turbo-free'

HISTORICO_MAX = 10
historico_conversa = []

# -------- Treinamento Premium --------
treinamento_premium = """
Você é o Natan AI, um assistente de inteligência artificial extremamente avançado.

Idioma:
- Responda sempre 100% em português brasileiro. Nunca use inglês, mesmo que a pergunta venha em outro idioma.

Áreas de conhecimento:
- História, Geografia, Matemática, Português, Física, Química, Biologia, Programação, SEO, Marketing Digital, Psicologia, Finanças, Cultura Brasileira, Canal Natson Games, entre outras.

Estilo de resposta:
- Sempre didático, claro, objetivo.
- Linguagem simples e acessível.
- Respostas curtas quando possível.
- Respostas longas: use tópicos e espaços entre parágrafos.
- Nunca use termos técnicos sem explicar.
- Mantenha um tom humano, educado e amigável.
- Evite começar respostas com "Bem-vindo" de forma repetitiva.
- Caso o usuário peça por respostas curtas, em 1 linha ou simples: Responda de forma extremamente curta e direta.

Limitações:
- Não oferece diagnósticos médicos ou jurídicos.
- Pode falar de saúde apenas de forma educativa, sempre indicando procurar um profissional humano.

Mini Dicionário de Cultura Brasileira:
- Miojo: Macarrão instantâneo de preparo rápido.
- Feijoada: Prato típico com feijão preto e carnes.
- Coxinha: Salgado frito recheado de frango.
- Brigadeiro: Doce de chocolate com granulado.
- Churrasco: Carne assada na brasa.
- Guaraná: Refrigerante típico brasileiro.
- Açaí: Fruta amazônica servida gelada.
- Pão de Queijo: Pão mineiro feito com queijo.
- Pastel: Massa frita com recheio.
- Farofa: Farinha de mandioca com temperos.
- Carnaval: Festa popular com samba e desfiles.
- Futebol: Esporte mais amado do Brasil.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global historico_conversa

    mensagem_usuario = request.json.get('mensagem', '').strip()

    if not mensagem_usuario:
        return jsonify({'error': 'Mensagem vazia. Por favor, envie uma pergunta.'}), 400

    # Atualizar histórico
    historico_conversa.append({"role": "user", "content": mensagem_usuario})
    if len(historico_conversa) > HISTORICO_MAX:
        historico_conversa = historico_conversa[-HISTORICO_MAX:]

    # Montar mensagens no formato OpenAI Chat API
    messages = [{"role": "system", "content": treinamento_premium}]
    for msg in historico_conversa:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    payload = {
        "model": TOGETHER_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resposta_api = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
        resposta_api.raise_for_status()
        dados_resposta = resposta_api.json()
        resposta_texto = dados_resposta['choices'][0]['message']['content'].strip()

        historico_conversa.append({"role": "assistant", "content": resposta_texto})

        return jsonify({'response': resposta_texto})

    except Exception as e:
        return jsonify({'error': f'Erro: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
