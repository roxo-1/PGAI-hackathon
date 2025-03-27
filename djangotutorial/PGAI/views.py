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
                Você é um assistente especializado em auxiliar estudantes de engenharia. Seu objetivo é fornecer o conteudo de flashcards usados para estudos, baseados nos princípios fundamentais da engenharia. Sempre forneça as perguntas de forma simples e clara e as respostas claras e completas, utilizando fórmulas, exemplos práticos e, quando necessário, diagramas em ASCII para ilustrar ideias.

                Diretrizes para suas respostas:
                1. Clareza e precisão: Use uma linguagem objetiva, evitando ambiguidades.
                2. Passo a passo: Se um cálculo for necessário, apresente todos os passos de forma detalhada.
                3. Exemplos aplicados: Sempre que possível, forneça exemplos práticos para contextualizar a teoria.
                4. Solicitação de detalhes: Se a pergunta for genérica ou incompleta, peça mais informações para fornecer uma resposta mais útil.
                5. Tom acessível: Seja formal, mas mantenha um tom didático e amigável para facilitar o aprendizado.
                6. Separe a pergunta da resposta colocando | depois da pergunta e antes da resposta.
                '''},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


def flashcards(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response_Flashcard(user_prompt)
        else:
            answer = "Por favor, forneça um prompt."
        return render(request, "flashcards.html", {'answer': answer, 'prompt': user_prompt})
    
    return render(request, "flashcards.html", {'answer': '', 'prompt': ''})

# funçoes para a dela de flash cards
# Função para processar o prompt e retornar a resposta usado no flashcard
def get_openai_response_Exercicios(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''
                Você é um assistente especializado em auxiliar estudantes de engenharia. Seu objetivo é fornecer perguntas de multipla escolha para estudos, baseados nos princípios fundamentais da engenharia. Sempre forneça as perguntas de forma simples e clara e as respostas claras e completas, utilizando fórmulas, exemplos práticos e, quando necessário, diagramas em ASCII para ilustrar ideias.

                Diretrizes para suas respostas:
                1. Clareza e precisão: Use uma linguagem objetiva, evitando ambiguidades.
                2. Passo a passo: Se um cálculo for necessário, apresente todos os passos de forma detalhada.
                3. Exemplos aplicados: Sempre que possível, forneça exemplos práticos para contextualizar a teoria.
                4. Solicitação de detalhes: Se a pergunta for genérica ou incompleta, peça mais informações para fornecer uma resposta mais útil.
                5. Tom acessível: Seja formal, mas mantenha um tom didático e amigável para facilitar o aprendizado.
                6. Os exercicos são de multipla escolha de 'A', 'B', 'C', 'D' e 'E'.
                7. Separe a pergunta da resposta colocando entre entre as resposta.
                '''},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar o prompt: {str(e)}"


def exercicios(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '').strip()
        if user_prompt:
            answer = get_openai_response_Exercicios(user_prompt)
        else:
            answer = "Por favor, forneça um prompt."
        return render(request, "exercicios.html", {'answer': answer, 'prompt': user_prompt})
    
    return render(request, "exercicios.html", {'answer': '', 'prompt': ''})
