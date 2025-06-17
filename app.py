from flask import Flask, request, jsonify, render_template, session
import os
import requests

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura_qualquer'  # Necessário para usar sessões no Flask

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "nousresearch/deephermes-3-mistral-24b-preview:free"

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

✅ +10 Áreas Extras:
- Marketing Digital
- SEO
- Empreendedorismo
- Finanças Pessoais
- Psicologia Comportamental
- Inteligência Emocional
- Desenvolvimento de Carreira
- Suporte Técnico Geral
- Dicas de Produtividade
- Criação de Conteúdo Online

✅ Partes 17 a 20:
- Aprendizado de Idiomas
- Ferramentas Digitais
- Criador de Conteúdo Criativo
- Aprendizado Contínuo e Fontes Confiáveis

✅ Estilo de resposta:
- Frases curtas e simples.
- Separe em tópicos.
- Espaços entre parágrafos.
- Sempre linguagem leve, acessível, e fácil de entender (ideal para TDAH).

✅ Limitações:
- Não fornece diagnósticos médicos, nem jurídicos.
- Para temas de saúde, sempre oriente o usuário a procurar um profissional humano.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')

        # Criar histórico se não existir
        if 'history' not in session:
            session['history'] = []

        # Adicionar nova entrada do usuário
        session['history'].append({"role": "user", "content": user_input})

        # Limitar o histórico das últimas 10 trocas
        history_limitado = session['history'][-10:]

        # Montar o payload
        messages = [{"role": "system", "content": treinamento_premium}] + history_limitado

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL_NAME,
            "messages": messages
        }

        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            ai_message = result["choices"][0]["message"]["content"]

            # Salvar a resposta da IA no histórico
            session['history'].append({"role": "assistant", "content": ai_message})

            # Limitar novamente o histórico
            session['history'] = session['history'][-10:]

            return jsonify({"resposta": ai_message})
        else:
            return jsonify({"erro": "Falha ao obter resposta da IA."})

    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
