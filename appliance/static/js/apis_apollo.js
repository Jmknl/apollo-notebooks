function getTextoSelecionado() {
    return window.getSelection().toString().trim();
}

function realizarBuscaDicionario(rota_api, nome_dicionario) {
    var palavraSelecionada = getTextoSelecionado();
    if (!palavraSelecionada) {
        alert('Selecione uma palavra primeiro!');
        return;
    }
    const csrftoken = getCookie('csrftoken');
    fetch(rota_api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ traduzir: palavraSelecionada })
    })
        .then(response => response.json())
        .then(data => {
            if (data.palavra) {
                mostrarHolograma(`${palavraSelecionada} (${nome_dicionario})`, data.palavra);
            } else if (data.erro) {
                mostrarHolograma(palavraSelecionada, null, nome_dicionario);
            }
        })
        .catch(error => console.error('Erro na conexão:', error));
}

function traduzirFraseCmd() {
    var textoSelecionado = getTextoSelecionado();
    if (!textoSelecionado) {
        alert('Selecione a frase que deseja traduzir!');
        return;
    }
    mostrarHologramaFrase("Processando...", "...");
    const csrftoken = getCookie('csrftoken');
    fetch('/api/traduzir_frase/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ traduzir: textoSelecionado })
    })
        .then(response => response.json())
        .then(data => {
            if (data.palavra) {
                mostrarHologramaFrase("Tradução:", data.palavra);
            } else if (data.erro) {
                mostrarHologramaFrase("Erro", data.erro);
            }
        })
        .catch(error => {
            console.error('Erro na conexão:', error);
            mostrarHologramaFrase("Falha", "O servidor não respondeu.");
        });
}

function realizarTraducaoIdioma(codigo_idioma, nome_idioma) {
    var textoSelecionado = getTextoSelecionado();
    if (!textoSelecionado) {
        alert('Selecione a frase que deseja traduzir!');
        return;
    }
    const csrftoken = getCookie('csrftoken');
    fetch('/api/traduzir_idioma/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify({ traduzir: textoSelecionado, idioma: codigo_idioma })
    })
        .then(response => response.json())
        .then(data => {
            if (data.palavra) mostrarHologramaFrase(`Tradução (${nome_idioma}):`, data.palavra);
            else if (data.erro) mostrarHologramaFrase("Erro", data.erro);
        }).catch(error => console.error('Erro na conexão:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function mostrarHolograma(palavra, definicao, idiomaErro = "") {
    const janelaAntiga = document.getElementById('holograma-tradutor');
    if (janelaAntiga) janelaAntiga.remove();

    const janela = document.createElement('div');
    janela.id = 'holograma-tradutor';
    janela.style.position = 'fixed';
    janela.style.top = '15%';
    janela.style.left = '50%';
    janela.style.transform = 'translateX(-50%)';
    janela.style.backgroundColor = 'rgba(63, 7, 85, 0.95)';
    janela.style.color = '#ffffff';
    janela.style.padding = '12px 30px 12px 15px';
    janela.style.borderRadius = '8px';
    janela.style.boxShadow = '0 8px 20px rgba(0,0,0,0.2)';
    janela.style.zIndex = '999999';
    janela.style.maxWidth = '280px';
    janela.style.textAlign = 'left';
    janela.style.fontFamily = 'sans-serif';

    const botaoX = `<span onclick="this.parentElement.remove()" style="position: absolute; top: 8px; right: 10px; cursor: pointer; font-size: 16px; color: #bbbbbb; transition: 0.2s; font-family: monospace;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#bbbbbb'">&times;</span>`;

    if (definicao) {
        let textoLimitado = definicao;
        if (definicao.length > 100) {
            textoLimitado = definicao.substring(0, 100) + "...";
        }
        janela.innerHTML = botaoX +
            `<h3 style="margin: 0 0 5px 0; color: #e0b0ff; font-size: 15px;">${palavra}</h3>
            <p style="margin: 0; font-size: 13px; line-height: 1.4;">${textoLimitado}</p>`;
    } else {
        let txtErro = idiomaErro ? ` no dicionário de ${idiomaErro}.` : ` no dicionário.`;
        janela.innerHTML = botaoX +
            `<p style="margin: 0; font-size: 13px;">A palavra <strong>"${palavra}"</strong> não foi encontrada${txtErro}</p>`;
    }

    document.body.appendChild(janela);
    setTimeout(() => { if (document.body.contains(janela)) janela.remove(); }, 10000);
}

function mostrarHologramaFrase(titulo, traducao) {
    const janelaAntiga = document.getElementById('holograma-tradutor');
    if (janelaAntiga) janelaAntiga.remove();

    const janela = document.createElement('div');
    janela.id = 'holograma-tradutor';
    janela.style.position = 'fixed';
    janela.style.top = '15%';
    janela.style.left = '50%';
    janela.style.transform = 'translateX(-50%)';
    janela.style.backgroundColor = 'rgba(10, 45, 80, 0.95)';
    janela.style.color = '#ffffff';
    janela.style.padding = '15px 35px 15px 20px';
    janela.style.borderRadius = '8px';
    janela.style.boxShadow = '0 8px 25px rgba(0,0,0,0.25)';
    janela.style.zIndex = '999999';
    janela.style.maxWidth = '450px';
    janela.style.textAlign = 'left';
    janela.style.fontFamily = 'sans-serif';

    const botaoX = `<span onclick="this.parentElement.remove()" style="position: absolute; top: 8px; right: 10px; cursor: pointer; font-size: 16px; color: #bbbbbb; transition: 0.2s; font-family: monospace;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#bbbbbb'">&times;</span>`;

    if (traducao) {
        janela.innerHTML = botaoX +
            `<h3 style="margin: 0 0 8px 0; color: #66ccff; font-size: 15px;">${titulo}</h3>
            <p style="margin: 0; font-size: 14px; line-height: 1.5;">${traducao}</p>`;
    } else {
        janela.innerHTML = botaoX + `<p style="margin: 0; font-size: 14px;">Erro ao processar a frase.</p>`;
    }

    document.body.appendChild(janela);
    setTimeout(() => { if (document.body.contains(janela)) janela.remove(); }, 15000);
}