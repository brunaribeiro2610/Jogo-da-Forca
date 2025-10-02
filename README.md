# Forca Django

Jogo da Forca simples feito com Django.

## Descrição
Projeto de exemplo de um jogo da forca (hangman) com backend em Django e frontend simples em HTML/CSS/JS. Possui rotas para estado do jogo, envio de tentativas e reinício (`/state/`, `/guess/`, `/reset/`).

## Pré-requisitos
- Windows (instruções em PowerShell)
- Python 3.10+ instalado
- (Opcional, recomendado) Git instalado

## Estrutura importante
O arquivo `manage.py` está dentro da subpasta `forca_django` (ou seja, `C:\Users\Bruna\Downloads\forca_django\forca_django\manage.py`).

## Preparando o ambiente (PowerShell)
Recomendo criar e ativar um ambiente virtual e instalar dependências:

```powershell
cd C:\Users\Bruna\Downloads\forca_django
# criar venv (uma única vez)
python -m venv venv
# ativar o venv
.\venv\Scripts\Activate.ps1
# instalar dependências (Django)
pip install django
# opcional: congelar dependências
pip freeze > requirements.txt
```

Se já houver um `requirements.txt`, instale com:

```powershell
pip install -r requirements.txt
```

## Migrar o banco e rodar o servidor
Como o `manage.py` está na subpasta interna, você pode rodar os comandos a partir da raiz do projeto apontando para o manage.py, ou entrar na pasta que contém o `manage.py`.

Opção 1 — executar a partir da raiz (sem mudar de pasta):

```powershell
# usando o python do venv
.\venv\Scripts\python.exe .\forca_django\manage.py migrate
.\venv\Scripts\python.exe .\forca_django\manage.py runserver
```

Opção 2 — mudar para a pasta que contém manage.py e rodar:

```powershell
Set-Location 'C:\Users\Bruna\Downloads\forca_django\forca_django'
# se o venv está na pasta pai, use o python do venv
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py runserver
```

Acesse no navegador: http://127.0.0.1:8000/ e jogue.

## Reiniciar o jogo (frontend)
Há um botão "Jogar novamente" que envia POST para `/reset/`. Se o botão não reiniciar, atualize a página e verifique o Console do navegador (F12) para mensagens de erro. O frontend já inclui lógica para limpar o teclado e pedir o estado atualizado ao backend.

## Subir para o GitHub
Se já criou o repositório no GitHub (ex.: `forca_django` na conta `brunaribeiro2610`), execute estes comandos na pasta do projeto:

```powershell
cd C:\Users\Bruna\Downloads\forca_django
# inicializar (se ainda não inicializou)
git init
git add .
git commit -m "Initial commit"
git branch -M main
# adicionar remote (HTTPS)
git remote add origin https://github.com/brunaribeiro2610/forca_django.git
git push -u origin main
```

Se preferir SSH (recomendado), gere uma chave e adicione ao GitHub:

```powershell
ssh-keygen -t ed25519 -C "seu-email@example.com"
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
# copie o conteúdo e cole em GitHub > Settings > SSH and GPG keys
# então use o remote SSH
git remote add origin git@github.com:brunaribeiro2610/forca_django.git
git push -u origin main
```

Observação: se o Git não estiver instalado no Windows, baixe em https://git-scm.com/download/win e reabra o PowerShell.

## Arquivos importantes
- `forca_django/` (aplicação Django)
- `forca_django/forca_django/` (config do projeto, onde está `manage.py`)
- `forca_django/game/` (app do jogo)
- `forca_django/forca_django/static/style.css` (estilos modificados)
- `.gitignore` (adicionado)

## Licença
MIT — fique à vontade para adaptar.

---
Se quiser, eu posso:
- executar os comandos Git para você se o Git estiver instalado por aqui;
- criar um `requirements.txt` automático (`pip freeze`) enquanto o venv estiver ativo;
- melhorar o README com instruções de deploy ou screenshots.

Me diga o que prefere que eu faça em seguida.