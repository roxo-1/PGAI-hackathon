# from django.shortcuts import render

# def index(request):
#     return render(request, "index.html")
import os
from dotenv import load_dotenv
import openai
from django.shortcuts import render
from django.http import HttpResponse

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("API_KEY")

# Função para processar o prompt e retornar a resposta
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
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
    return response['choices'][0]['message']['content']

# View para renderizar a página e exibir a resposta
def index(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('user_prompt', '')
        if user_prompt:
            answer = get_openai_response(user_prompt)
        else:
            answer = "Por favor, forneça um prompt."
        return render(request, "index.html", {'answer': answer, 'prompt': user_prompt})
    
    return render(request, "index.html", {'answer': '', 'prompt': ''})
