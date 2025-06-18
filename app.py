from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
HISTORICO_MAX = 10  # Memória de curto prazo (últimas 10 mensagens)

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

    # Atualizar memória de curto prazo
    historico_conversa.append({"role": "user", "content": mensagem_usuario})
    if len(historico_conversa) > HISTORICO_MAX:
        historico_conversa = historico_conversa[-HISTORICO_MAX:]

    # Se o usuário pedir resposta curta
    prompt_resposta_curta = ""
    if "responda em 1 linha" in mensagem_usuario.lower() or "resposta fácil" in mensagem_usuario.lower() or "resposta simples" in mensagem_usuario.lower():
        prompt_resposta_curta = "\nIMPORTANTE: Responda essa pergunta com no máximo 1 linha, de forma extremamente simples e objetiva."

    # Remover mensagens com "Bem-vindo" da memória
    historico_filtrado = []
    for msg in historico_conversa:
        if "bem-vindo" not in msg["content"].lower():
            historico_filtrado.append(msg)
    historico_conversa = historico_filtrado[-HISTORICO_MAX:]

    # Monta o histórico para o prompt
    historico_texto = ""
    for msg in historico_conversa:
        historico_texto += f"{msg['role'].upper()}: {msg['content']}\n"

    prompt_final = f"{treinamento_premium}\n\nHISTÓRICO DE CONVERSA:\n{historico_texto}\n\nPergunta atual:\n{mensagem_usuario}\n{prompt_resposta_curta}"

    payload = {
        "model": "openchat:latest",
        "prompt": prompt_final,
        "stream": False
    }

    try:
        resposta_api = requests.post(OLLAMA_API_URL, json=payload)
        resposta_api.raise_for_status()
        dados_resposta = resposta_api.json()
        resposta_texto = dados_resposta.get('response', 'Desculpe, não consegui gerar uma resposta.')

        historico_conversa.append({"role": "assistant", "content": resposta_texto})

        return jsonify({'response': resposta_texto})

    except Exception as e:
        return jsonify({'error': f'Erro: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
