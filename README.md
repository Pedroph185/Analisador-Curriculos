# 📄 Analisador de Currículos com Python + IA
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
Um sistema inteligente para extrair e analisar informações de currículos em PDF usando Python.

---

## 🚀 Funcionalidades

- ✅ Extrai texto de arquivos PDF (com suporte a formatação complexa)
- ✅ Identifica e-mails, telefones, LinkedIn e GitHub
- ✅ Reconhece habilidades técnicas (Python, SQL, Linux, etc.)
- ✅ Classifica seções do currículo (formação, experiência, cursos)
- ✅ Gera resumo estruturado em JSON

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **PyPDF2** - Leitura de PDFs
- **pdfplumber** - Extração precisa de texto
- **Expressões Regulares (regex)** - Extração de informações

---

## 📦 Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/Pedroph185/Analisador-Curriculos.git

# Entre na pasta
cd Analisador-Curriculos

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python main.py