from flask import Flask, request, jsonify, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura_qualquer'  # Necessário para sessões no Flask

# Nome do modelo local (exemplo usando Ollama com Llama 2 7B)
MODEL_NAME = "llama2"

# Treinamento personalizado (seu treinamento completo)
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
- Geração de códigos de jogos simples
- Estruturas de dados, algoritmos e lógica de programação

🎮 Conhecimento Especial: Canal Natson Games
- Canal brasileiro focado em conteúdos de jogos.
- Nome: Natson Games
- Conteúdo: Gameplay, dicas de jogos e conteúdo gamer.
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
- Pode falar sobre temas de saúde de forma educativa, com alerta para procurar um profissional humano.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')

        # Criar histórico de memória curta
        if 'history' not in session:
            session['history'] = []

        # Adicionar mensagem do usuário ao histórico
        session['history'].append({"role": "user", "content": user_input})

        # Limitar para as últimas 10 mensagens
        history_limitado = session['history'][-10:]

        # Montar mensagens para o Llama 2
        messages = [{"role": "system", "content": treinamento_premium}] + history_limitado

        # Chamada para o Ollama local (ajuste a URL se estiver rodando diferente)
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            }
        )

        result = response.json()

        # Captura a resposta do Llama 2
        if "message" in result:
            ai_message = result['message']['content']

            # Salva a resposta no histórico
            session['history'].append({"role": "assistant", "content": ai_message})
            session['history'] = session['history'][-10:]

            return jsonify({"resposta": ai_message})
        else:
            return jsonify({"erro": "Falha ao obter resposta da IA local."})

    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
