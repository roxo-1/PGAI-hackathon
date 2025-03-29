import os
from dotenv import load_dotenv
from openai import OpenAI
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Funções de homepage e processamento de prompt
# Função para processar o prompt e retornar a resposta usado na 
import re

# Função para formatar a resposta antes de enviá-la ao template
def format_response(response):
    if not response:
        return "Nenhuma resposta gerada."

    # Adiciona quebras de linha para melhorar a legibilidade
    formatted = response.replace("\n", "<br>")

    # Negrito para palavras-chave importantes
    keywords = ["Definição:", "Exemplo:", "Fórmula:", "Importante:", "Observação:"]
    for word in keywords:
        formatted = formatted.replace(word, f"<strong>{word}</strong>")

    # Convertendo listas para HTML (se detectar "- " no início das linhas)
    formatted = re.sub(r"- (.+)", r"<li>\1</li>", formatted)  
    formatted = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", formatted)  # Garante que seja uma lista UL

    # Código e fórmulas (se houver trechos dentro de crases ``)
    formatted = re.sub(r"``(.*?)``", r"<pre><code>\1</code></pre>", formatted)  

    return formatted


# Função para obter resposta da OpenAI
def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''
                Você é um assistente especializado em auxiliar estudantes de engenharia. Seu objetivo é fornecer respostas técnicas, diretas e baseadas nos princípios fundamentais da engenharia. Sempre explique os conceitos de maneira clara, utilizando fórmulas, exemplos práticos e, quando necessário, diagramas em ASCII para ilustrar ideias.

                Diretrizes para suas respostas:
                1. Clareza e precisão: Use uma linguagem objetiva, evitando ambiguidades.
                2. Passo a passo: Se um cálculo for necessário, apresente todos os passos de forma detalhada.
                3. Exemplos aplicados: Sempre que possível, forneça exemplos práticos para contextualizar a teoria.
                4. Solicitação de detalhes: Se a pergunta for genérica ou incompleta, peça mais informações para fornecer uma resposta mais útil.
                5. Tom acessível: Seja formal, mas mantenha um tom didático e amigável para facilitar o aprendizado.
                '''},
                {"role": "user", "content": prompt}
            ]
        )
        return format_response(response.choices[0].message.content)  # Formata antes de retornar
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


# View para renderizar a página e exibir a resposta
def index(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response(user_prompt)
        else:
            answer = "Por favor, forneça um prompt."
        return render(request, "index.html", {'answer': answer, 'prompt': user_prompt})

    return render(request, "index.html", {'answer': '', 'prompt': ''})


# funçoes para a dela de flash cards
# Função para processar o prompt e retornar a resposta usado no flashcard
def get_openai_response_Flashcard(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''
                Você é um assistente especializado em auxiliar estudantes de engenharia. Seu objetivo é fornecer o conteúdo de flashcards usados para estudos, baseados nos princípios fundamentais da engenharia. Sempre forneça as perguntas curtas e claras e as respostas claras, completas e concisas, utilizando fórmulas, exemplos curtos e práticos e sempre que vocÊ achar q precisa de mais detalhes para fornecer uma resposta você deve responder com algo aleatorio do topico declarado.

                Diretrizes para suas respostas:
                1. Clareza e precisão: Use uma linguagem objetiva, evitando ambiguidades.
                2. Passo a passo: Se um cálculo for necessário, apresente todos os passos de forma detalhada.
                # 3. Exemplos aplicados: Sempre que possível, forneça exemplos práticos para contextualizar a teoria.
                3. Solicitação de detalhes: Se a pergunta for genérica ou incompleta, peça mais informações para fornecer uma resposta mais útil.
                4. Tom acessível: Seja formal, mas mantenha um tom didático e amigável para facilitar o aprendizado.
                5. Sempre crie uma pergunta e resposta toda a vez sobre o assunto.
                6. Separe a pergunta da resposta colocando | depois da pergunta e antes da resposta.
                6. Envie sempre a mesma resposta para o conteúdo informado.
                7. Sempre forneça exatamente esta formatação de resposta sem nenhuma variação, independentemente do número de chamadas.
                '''},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


def flashcards(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response_Flashcard(user_prompt)
            
            # Separa a string usando '|' como delimitador
            if '|' in answer:
                question, answer_part = answer.split('|', 1)  # Divide apenas no primeiro |
                question = question.strip()
                answer_part = answer_part.strip()
            else:
                # Caso não encontre o separador
                question = answer
                answer_part = "Resposta não encontrada"
            
            return render(request, "flashcards.html", {
                'question': question,
                'answer': answer_part,
                'prompt': user_prompt
            })
        else:
            return render(request, "flashcards.html", {
                'error': "Por favor, forneça um prompt.",
                'prompt': ''
            })
    
    return render(request, "flashcards.html", {
        'question': '',
        'answer': '',
        'prompt': ''
    })

# funçoes para a dela de flash cards
# Função para processar o prompt e retornar a resposta usada no flashcard
def get_openai_response_exercicios(topic):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''
                Você é um assistente especializado em criar questões de múltipla escolha para estudantes de engenharia.  
                Seu objetivo é gerar perguntas desafiadoras e didáticas baseadas no tema fornecido pelo usuário.  

                **Instruções:**  
                - Gere uma pergunta sobre o tema solicitado. 
                - Escolha a resposta correta aleatoriamente. 
                - A pergunta deve ser de múltipla escolha com 4 alternativas.  
                - O formato da resposta deve ser exatamente o seguinte:  

                Pergunta: [texto da pergunta gerada]  
                $  
                A) [alternativa 1] | correta/incorreta  
                #  
                B) [alternativa 2] | correta/incorreta  
                #  
                C) [alternativa 3] | correta/incorreta  
                #  
                D) [alternativa 4] | correta/incorreta  

                **Regras:**  
                - Escolha a resposta correta aleatoriamente.  
                - As alternativas devem ser plausíveis e desafiadoras.  
                - Responda apenas no formato acima, sem explicações adicionais.  
                '''},
                {"role": "user", "content": f"Crie uma pergunta sobre {topic}."}
            ],
            temperature=1,  # Aumenta a variação das perguntas geradas
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


# Função para processar a requisição no Django
def exercicios(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response_exercicios(user_prompt)
            
            # Inicializa os valores padrão
            question = "Pergunta não encontrada"
            alternatives_list = ["Alternativa não encontrada"] * 4
            answers_list = ["Resposta não encontrada"] * 4

            # Separa a string usando '$' como delimitador
            if '$' in answer:
                question, alternative_answer = answer.split('$', 1)  # Divide no primeiro $
                question = question.strip()

                # Separa alternativas e respostas usando '#'
                alternative_blocks = alternative_answer.split('#')
                
                if len(alternative_blocks) >= 4:
                    for i in range(4):
                        if '|' in alternative_blocks[i]:
                            alternative, correctness = alternative_blocks[i].split('|', 1)
                            alternatives_list[i] = alternative.strip()
                            answers_list[i] = correctness.strip()

            return render(request, "exercicios.html", {
                'question': question,
                'altA': alternatives_list[0], 'AnwA': answers_list[0],
                'altB': alternatives_list[1], 'AnwB': answers_list[1],
                'altC': alternatives_list[2], 'AnwC': answers_list[2],
                'altD': alternatives_list[3], 'AnwD': answers_list[3]
            })

    return render(request, "exercicios.html", {'answer': '', 'prompt': ''})