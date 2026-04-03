from pathlib import Path
import json
import urllib.request
from django.conf import settings
import requests
import os
import concurrent.futures
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book,Paper,Event, Profile,TranslationCache, DictionaryCache
from django.contrib.auth.decorators import login_required
from .forms import BookForm, PaperForm , ProfileForm , EventForm
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Página incial"""
    return render(request, 'appliance/index.html')

@login_required
def book_list(request):
    """Retorna os cadernos que o usuário tem"""
    my_books = Book.objects.filter(owner=request.user)
    
    context = {'books': my_books}

    return render(request,'appliance/my_books.html', context)

@login_required
def book_detail(request, book_id):
        """"Retorna um livro específico"""
        book = Book.objects.get(id=book_id)

        if book.owner != request.user:
            raise Http404
        
        paper_book = Paper.objects.filter(book= book)

        context = {'book':book,'pages': paper_book}
        return render(request,'appliance/book_detail.html',context)


@login_required
def new_book(request):
    """Adiciona um novo caderno."""

    if request.method != "POST":
        form = BookForm()
    else:
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
           
            new_book.owner = request.user
            
            new_book.save()
            
            return redirect("appliance:books")
 
    context = {"form": form}
    return render(request, "appliance/new_book.html", context)

@login_required
def new_paper(request,book_id):
    """Permite adicionar páginas utilizaveís"""

    book = Book.objects.get(id=book_id)

    if book.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = PaperForm()

    else:
        form = PaperForm(data=request.POST)

        if form.is_valid():
            new_paper = form.save(commit=False)

            new_paper.book= book

            new_paper.save()

            return redirect("appliance:book_detail", book_id=book.id)

    context = {"book": book, "form": form}
    return render(request,"appliance/new_paper.html",context)


@login_required
def edit_paper(request, paper_id):  
    """Permite editar as páginas criadas"""

    paper = Paper.objects.get(id=paper_id)

    if paper.book.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = PaperForm(instance=paper)

    else:
        form = PaperForm(instance=paper, data=request.POST)
        
        if form.is_valid():  
            form.save()

            return redirect("appliance:book_detail", book_id=paper.book.id)

    context = {"paper": paper, "form": form}  
    return render(request, "appliance/edit_paper.html", context)


@login_required
def del_paper(request, paper_id):
    """Apaga uma anotação após confirmação."""
    paper = Paper.objects.get(id=paper_id)

    if paper.book.owner != request.user:
        raise Http404

    if request.method != "POST":
        context = {"paper": paper}
        return render(request, "appliance/del_paper.html", context)

    else:

        book_id = paper.book.id

        paper.delete()

        return redirect("appliance:book_detail", book_id=book_id)


@login_required
def del_book(request, book_id):
    """Apaga o caderno após confirmação."""
    book = Book.objects.get(id=book_id)

    if book.owner != request.user:
        raise Http404

    if request.method != "POST":
        context = {"book": book}
        return render(request, "appliance/del_book.html", context)

    else:
        
        book.delete()

        return redirect("appliance:books")


def formatar_url_dicio(palavra):
    """Formata a palavra selecionada para pesquisa"""
    palavra = palavra.lower().strip().replace(" ", "-")
    return ''.join(c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn')


def buscar_em_uma_fonte(palavra, fonte):
    """Envia uma requisição para o site"""
    idioma, url_base, tag, classe = fonte
    url = f"{url_base}{palavra}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    try:
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            alvo = soup.find(tag, class_=classe)

            if alvo:
                if "wiktionary" in url:
                    item = alvo.find("p")
                    descricao = item.get_text(strip=True) if item else ""
                else:
                    descricao = alvo.get_text(separator=" ", strip=True)

                if descricao and len(descricao) > 5:
                    if descricao.endswith(":"): 
                        descricao = descricao[:-1]
                    return f"[{idioma}] {descricao}"
    except:
        pass
    return None


@login_required
def word_translate(request):
    """Acha a definição da palavra nos dicionários de Inglês e Português"""
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        palavra = data.get("traduzir", "").strip().lower()

        if not palavra:
            return JsonResponse({"erro": "Palavra não fornecida"}, status=400)

        cache_existente = DictionaryCache.objects.filter(word=palavra).first()
        if cache_existente:
            return JsonResponse({"palavra": cache_existente.definition})

        fontes = [ ("Inglês", "https://dictionary.cambridge.org/dictionary/english/", "div",  "def ddef_d db", ), ("Português", "https://www.dicio.com.br/", "p", "significado"), ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futuros = [ executor.submit(buscar_em_uma_fonte, palavra, fonte) for fonte in fontes ]

            for futuro in concurrent.futures.as_completed(futuros):
                resultado = futuro.result()
                if resultado:
                    DictionaryCache.objects.create(word=palavra, definition=resultado)
                    return JsonResponse({"palavra": resultado})

        return JsonResponse({"erro": "Não encontrado em Inglês/Português"}, status=404)

    except Exception as e:
        print(f"Erro: {e}")
        return JsonResponse({"erro": "Erro interno"}, status=500)


@login_required
def profile(request):
    """Página de Dashboard"""
    perfil, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form1 = ProfileForm(request.POST, request.FILES, instance=perfil)
        if form1.is_valid():
            form1.save()
            return redirect("appliance:profile")
    else:
        form1 = ProfileForm(instance=perfil)

    context = {"form1": form1, "perfil": perfil}
    return render(request, "appliance/profile.html", context)


@login_required
def calendar_get(request):
    """Busca eventos na tabela event"""
    
    if request.method == "GET":
        eventos = Event.objects.filter(user=request.user)
        lista_eventos = []
        for event in eventos:
            lista_eventos.append(
                {   "id": event.id, 
                    "title": event.title,
                    "start": event.start_date.strftime("%Y-%m-%d"),
                    "end": (event.end_date.strftime("%Y-%m-%d") if event.end_date else None),
                }
            )

        return JsonResponse(lista_eventos, safe=False)


@login_required
def calendar_post(request):
    """Insere os dados no calendário"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            start_date = data.get("start_date")
            end_date = data.get("end_date")

            if title and start_date:
                Event.objects.create(
                    user=request.user,
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                )
                return JsonResponse({"status": "sucesso"})
            else:
                return JsonResponse(
                    {"erro": "Título e data inicial são obrigatórios"}, status=400
                )

        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)

    return JsonResponse({"erro": "Método não permitido"}, status=405)


@login_required
def calendar_delete(request, event_id):
    """Deleta um evento específico do calendário"""
    if request.method == "DELETE":
        try:
            evento = get_object_or_404(Event, id=event_id, user=request.user)
            evento.delete()
            return JsonResponse({"status": "sucesso"})
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)

    return JsonResponse({"erro": "Método não permitido"}, status=405)


def google_translate(texto, idioma_destino):
    """Se comunica diretamente com API do Google"""
    CHAVE_API = settings.GOOGLE_API_KEY

    url = f"https://translation.googleapis.com/language/translate/v2?key={CHAVE_API}"

    pacote_de_dados = {"q": texto,"target": idioma_destino,"format": "text"}

    try:
        resposta = requests.post(url, data=pacote_de_dados)

        if resposta.status_code == 200:
            resultado_json = resposta.json()
            return resultado_json["data"]["translations"][0]["translatedText"]
        else:
            print(f"Erro do Google: {resposta.text}")
            return None
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None


@login_required
def translate_to_language(request):
    """Tradução bidirecional com API"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            frase = data.get("traduzir", "").strip()
            idioma_destino = data.get("idioma", "en")

            if not frase:
                return JsonResponse({"erro": "Nenhum texto fornecido"}, status=400)

            cache_existente = TranslationCache.objects.filter(original_text=frase, target_language=idioma_destino).first()

            if cache_existente:
                return JsonResponse({"palavra": cache_existente.translated_text})

            traducao = google_translate(frase, idioma_destino)

            if not traducao:
                return JsonResponse(
                    {"erro": "Falha na API Oficial do Google"}, status=500
                )

            if traducao.lower() == frase.lower():
                idioma_destino = "pt"
                traducao = google_translate(frase, idioma_destino)

            if traducao and traducao != frase:
                TranslationCache.objects.create(original_text=frase, target_language=idioma_destino,translated_text=traducao,)

            return JsonResponse({"palavra": traducao})

        except Exception as e:
            print(f"Erro no tradutor: {e}")
            return JsonResponse({"erro": "Erro interno no servidor"}, status=500)

    return JsonResponse({"erro": "Método não permitido"}, status=405)


@login_required
def translate_sentence(request):
    """Tradução bidirecional com API para outras línguas"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            frase = data.get("traduzir", "").strip()

            if not frase:
                return JsonResponse({"erro": "Nenhum texto fornecido"}, status=400)

            cache_en = TranslationCache.objects.filter(original_text=frase, target_language="en").first()
            if cache_en and cache_en.translated_text.lower() != frase.lower():
                return JsonResponse({"palavra": cache_en.translated_text})

            traducao = google_translate(frase, "en")
            idioma_final = "en"

            if traducao and traducao.lower() == frase.lower():
                cache_pt = TranslationCache.objects.filter(original_text=frase, target_language="pt").first()
                if cache_pt:
                    return JsonResponse({"palavra": cache_pt.translated_text})

                traducao = google_translate(frase, "pt")
                idioma_final = "pt"

            if traducao and traducao != frase:
                TranslationCache.objects.create(original_text=frase,target_language=idioma_final,translated_text=traducao,)
                
            return JsonResponse({"palavra": traducao})

        except Exception as e:
            print(f"Erro no tradutor: {e}")
            return JsonResponse({"erro": "Erro na comunicação com o tradutor"}, status=500)

    return JsonResponse({"erro": "Método não permitido"}, status=405)
