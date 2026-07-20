import re
import json
import os
import PyPDF2
import pdfplumber

# ============================================
# 1. FUNÇÕES DE EXTRAÇÃO DE TEXTO
# ============================================

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF usando pdfplumber (fallback para PyPDF2)."""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = ''
            for pagina in pdf.pages:
                texto += pagina.extract_text() + '\n'
            return texto
    except Exception as e:
        print(f"⚠️ pdfplumber falhou: {e}")
        try:
            with open(caminho_pdf, 'rb') as arquivo:
                leitor = PyPDF2.PdfReader(arquivo)
                texto = ''
                for pagina in leitor.pages:
                    texto += pagina.extract_text() + '\n'
                return texto
        except Exception as e2:
            print(f"❌ Erro ao ler PDF: {e2}")
            return ""


# ============================================
# 2. FUNÇÕES DE EXTRAÇÃO DE INFORMAÇÕES
# ============================================

def extrair_emails(texto):
    """Extrai endereços de e-mail do texto."""
    padrao = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(padrao, texto, re.IGNORECASE)))


def extrair_telefones(texto):
    """Extrai números de telefone do texto."""
    padrao = r'\(?\d{2}\)?\s?\d{4,5}[-\s]?\d{4}'
    return list(set(re.findall(padrao, texto)))


def extrair_linkedin(texto):
    """Extrai URL do LinkedIn do texto."""
    padrao = r'(?:linkedin\.com/in/|linkedin\.com/pub/)[a-zA-Z0-9-]+'
    resultado = re.search(padrao, texto, re.IGNORECASE)
    return resultado.group() if resultado else None


def extrair_github(texto):
    """Extrai URL do GitHub do texto."""
    padrao = r'(?:github\.com/)[a-zA-Z0-9-]+'
    resultado = re.search(padrao, texto, re.IGNORECASE)
    return resultado.group() if resultado else None


def extrair_habilidades(texto):
    """Extrai habilidades técnicas do texto."""
    habilidades_padrao = [
        'python', 'java', 'c++', 'javascript', 'html', 'css', 'sql',
        'linux', 'windows', 'git', 'github', 'docker', 'kubernetes',
        'aws', 'azure', 'gcp', 'redes', 'tcp/ip', 'vpn', 'active directory',
        'firewall', 'segurança', 'cibersegurança', 'cloud', 'devops'
    ]
    texto_lower = texto.lower()
    encontradas = [h for h in habilidades_padrao if h in texto_lower]
    return encontradas


def extrair_secoes(texto):
    """Identifica seções do currículo (formação, experiência, cursos)."""
    secoes = {'formacao': [], 'experiencias': [], 'cursos': []}
    paragrafos = texto.split('\n')
    
    padrao_formacao = r'(formação|educação|graduação|faculdade|universidade)'
    padrao_experiencia = r'(experiência|experiencia|profissional|trabalho|cargo)'
    padrao_curso = r'(curso|complementar|certificação|certificacao)'
    
    for p in paragrafos:
        p = p.strip()
        if not p:
            continue
        if re.search(padrao_formacao, p, re.IGNORECASE):
            secoes['formacao'].append(p)
        elif re.search(padrao_experiencia, p, re.IGNORECASE):
            secoes['experiencias'].append(p)
        elif re.search(padrao_curso, p, re.IGNORECASE):
            secoes['cursos'].append(p)
    
    return secoes


# ============================================
# 3. FUNÇÃO PRINCIPAL
# ============================================

def analisar_curriculo(caminho_pdf):
    """Analisa um currículo em PDF e retorna um dicionário com os dados extraídos."""
    print(f"🔍 Analisando: {caminho_pdf}")
    
    texto = extrair_texto_pdf(caminho_pdf)
    if not texto:
        return {"erro": "Não foi possível extrair texto do PDF"}
    
    return {
        'informacoes_basicas': {
            'emails': extrair_emails(texto),
            'telefones': extrair_telefones(texto),
            'linkedin': extrair_linkedin(texto),
            'github': extrair_github(texto),
            'habilidades': extrair_habilidades(texto)
        },
        'secoes': extrair_secoes(texto),
        'texto_completo': texto[:500] + "..." if len(texto) > 500 else texto
    }


# ============================================
# 4. INTERFACE DO USUÁRIO
# ============================================

def exibir_resumo(resultado):
    """Exibe um resumo formatado da análise."""
    print("\n" + "="*60)
    print("📄 RESUMO DA ANÁLISE DO CURRÍCULO")
    print("="*60)
    
    info = resultado.get('informacoes_basicas', {})
    secoes = resultado.get('secoes', {})
    
    print("\n📬 INFORMAÇÕES DE CONTATO:")
    if info.get('emails'):
        print(f"  📧 E-mails: {', '.join(info['emails'])}")
    if info.get('telefones'):
        print(f"  📱 Telefones: {', '.join(info['telefones'])}")
    if info.get('linkedin'):
        print(f"  💼 LinkedIn: {info['linkedin']}")
    if info.get('github'):
        print(f"  🐙 GitHub: {info['github']}")
    
    print("\n🛠️ HABILIDADES TÉCNICAS:")
    if info.get('habilidades'):
        print(f"  {', '.join(info['habilidades'])}")
    else:
        print("  Nenhuma habilidade identificada")
    
    print("\n📂 SEÇÕES IDENTIFICADAS:")
    for secao, conteudo in secoes.items():
        if conteudo:
            print(f"  {secao}: {len(conteudo)} itens encontrados")
    
    print("\n" + "="*60)


def main():
    """Função principal do programa."""
    print("🚀 ANALISADOR DE CURRÍCULOS COM IA")
    print("-" * 40)
    
    pasta = "curriculos_exemplo"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"📁 Pasta '{pasta}' criada. Coloque seus currículos lá!")
        return
    
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]
    if not arquivos:
        print("❌ Nenhum arquivo PDF encontrado em 'curriculos_exemplo'")
        return
    
    print("\n📄 Currículos disponíveis:")
    for i, f in enumerate(arquivos, 1):
        print(f"  {i}. {f}")
    
    try:
        escolha = int(input("\n📌 Escolha o número do arquivo: "))
        if 1 <= escolha <= len(arquivos):
            caminho = os.path.join(pasta, arquivos[escolha-1])
        else:
            print("❌ Escolha inválida!")
            return
    except ValueError:
        print("❌ Digite um número válido!")
        return
    
    resultado = analisar_curriculo(caminho)
    if 'erro' in resultado:
        print(f"❌ {resultado['erro']}")
        return
    
    exibir_resumo(resultado)
    
    # Salvar resultado em JSON
    os.makedirs("outputs", exist_ok=True)
    nome_saida = os.path.join("outputs", f'analise_{arquivos[escolha-1].replace(".pdf", ".json")}')
    with open(nome_saida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
    print(f"\n💾 Resultado salvo em: {nome_saida}")


if __name__ == "__main__":
    main()