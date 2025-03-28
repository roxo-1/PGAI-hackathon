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
        return response.choices[0].message.content
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
            temperature=0,
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
# Função para processar o prompt e retornar a resposta usado no flashcard
def get_openai_response_Exercicios(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''
                Você é um assistente especializado em auxiliar estudantes de engenharia. Seu objetivo é fornecer perguntas de multipla escolha para estudos.

                Requisitos para suas respostas:
                1. Não escreva nada além da pergunta, suas alternativas e suas respostas.
                2. Clareza e precisão: Use uma linguagem objetiva, evitando ambiguidades.
                3. Tom acessível: Seja formal, mas mantenha um tom didático e amigável para facilitar o aprendizado.
                4. Os exercicos são de multipla escolha de 'A', 'B', 'C' e 'D'.
                5. Separe com # cada vez que você fizer uma alternativa.
                6. Sempre separe com a pergunta das alternativas com o símbolo $.
                7. Coloque depois de cada alternativa separado por '|' se ela esta correta ou incorreta.
                '''},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


def exercicios(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response_Exercicios(user_prompt)
            
            # Separa a string usando '$' como delimitador
            if '$' in answer:
                # Separa a pergunta das alternativas e resposta
                question, alternative_answer = answer.split('$', 1)  # Divide apenas no primeiro $
                question = question.strip()
                alternative_answer = alternative_answer.strip()
                
                # Vai ter que separar alternativas
                if '|' in alternative_answer:
                    alternatives = alternative_answer.split('|')
                    
                    # Inicializa listas para alternativas e respostas
                    alternatives_list = []
                    answers_list = []
                    
                    # Processa cada alternativa
                    for alt in alternatives:
                        if '#' in alt:
                            alternative, answer = alt.split('#', 1)  # Divide apenas no primeiro #
                            alternative = alternative.strip()
                            answer = answer.strip()
                            alternatives_list.append(alternative)
                            answers_list.append(answer)
                        else:
                            # Caso não encontre o separador '#'
                            alternatives_list.append(alt)
                            answers_list.append("Resposta não encontrada")
                    
                    # Ajusta para garantir que tenhamos 4 alternativas
                    while len(alternatives_list) < 4:
                        alternatives_list.append("")
                        answers_list.append("")
                    
                    return render(request, "exercicios.html", {
                        'question': question,
                        'altA': alternatives_list[0],
                        'AnwA': answers_list[0],
                        'altB': alternatives_list[1],
                        'AnwB': answers_list[1],
                        'altC': alternatives_list[2],
                        'AnwC': answers_list[2],
                        'altD': alternatives_list[3],
                        'AnwD': answers_list[3]
                    })
                else:
                    # Caso não encontre o separador '|'
                    return render(request, "exercicios.html", {
                        'question': question,
                        'altA': "Alternativa não encontrada",
                        'AnwA': "Resposta não encontrada",
                        'altB': "",
                        'AnwB': "",
                        'altC': "",
                        'AnwC': "",
                        'altD': "",
                        'AnwD': ""
                    })
            else:
                # Caso não encontre o separador '$'
                question = answer
                alternative_answer = "Resposta não encontrada"
                return render(request, "exercicios.html", {
                    'question': question,
                    'altA': "Alternativa não encontrada",
                    'AnwA': "Resposta não encontrada",
                    'altB': "",
                    'AnwB': "",
                    'altC': "",
                    'AnwC': "",
                    'altD': "",
                    'AnwD': ""
                })
        else:
            answer = "Por favor, forneça um prompt."
            return render(request, "exercicios.html", {'answer': answer, 'prompt': user_prompt})
    
    return render(request, "exercicios.html", {'answer': '', 'prompt': ''})
