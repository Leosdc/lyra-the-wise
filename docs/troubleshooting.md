# 🔧 Guia de Solução de Problemas — Lyra v3.0

## 🔴 Erros Críticos

### **1. `AttributeError: 'str' object has no attribute 'append'`**

**Quando acontece:**
```
!addinventario Espada Longa
❌ Ocorreu um erro ao executar o comando.
```

**Causa:**  
Fichas antigas têm `inventario` como string `""` ao invés de lista `[]`.

**Solução Automática:**
```bash
# No Discord (requer permissão de admin)
!migrarinventario
```

**Solução Manual (se admin não funcionar):**
```python
# No arquivo data/fichas_personagens.json
# ANTES:
{
  "progressao": {
    "inventario": ""
  }
}

# DEPOIS:
{
  "progressao": {
    "inventario": []
  }
}
```

**Prevenção:**  
O novo código já corrige automaticamente, mas fichas antigas precisam ser migradas.

---

### **2. HP não salva após combate**

**Quando acontece:**
```
!fimcombate
✅ Combate finalizado!

[Jogador verifica ficha]
❌ HP ainda está no valor antigo
```

**Causa:**  
Versão antiga do `!fimcombate` não salvava HP nas fichas permanentes.

**Solução:**  
Use o comando atualizado de `fix_inventario_structure.py`:

```python
# O novo !fimcombate inclui:
# CRÍTICO: Salva HP antes de limpar
for entry in iniciativa:
    nome = entry.get("nome")
    hp_atual = entry.get("hp_atual")
    
    if nome in fichas:
        fichas[nome]["combate"]["HP Atual"] = hp_atual

salvar_dados(fichas)
```

**Teste:**
```
1. !iniciarcombate
2. !addjogador Guerreiro
3. !atacar Guerreiro 10
4. !fimcombate
5. !ficha Guerreiro  # ✅ HP deve estar atualizado
```

---

### **3. `Member "Lyra, the Wise" not found`**

**Quando acontece:**
```
!darxpgrupo 300
❌ Member "Lyra, the Wise" not found.
```

**Causa:**  
Comando tentando dar XP para o próprio bot.

**Solução:**  
Filtrar membros do bot:

```python
# No comando !darxpgrupo
members = [
    m for m in ctx.channel.members 
    if not m.bot  # ✅ Ignora bots
]
```

**Correção no código:**
```python
@bot.command(name="darxpgrupo")
async def dar_xp_grupo(ctx: commands.Context, quantidade: int):
    """[MESTRE] Dá XP para todos os jogadores."""
    from utils import carregar_dados, salvar_dados
    
    fichas = carregar_dados()
    
    # FILTRO CRÍTICO
    jogadores = [
        m.display_name for m in ctx.channel.members
        if not m.bot and m.display_name in fichas  # ✅ Ignora bots
    ]
    
    # ... resto do código
```

---

## ⚠️ Erros Comuns

### **4. Lyra ainda pede rolagens automaticamente**

**Sintoma:**
```
Lyra: Vocês veem um orc! [ROLL: 1d20+3, todos]
```

**Causa:**  
Prompts antigos em cache ou não atualizados.

**Solução:**
```bash
# 1. Verifique se core/sessao_prompts.py existe
ls core/sessao_prompts.py

# 2. Reinicie o bot completamente
python main.py

# 3. Teste com nova sessão
!iniciarsessao
!narrativa Teste
```

**Se persistir:**  
Verifique se `commands/sessoes_acao.py` importa corretamente:
```python
from core.sessao_prompts import get_narrative_system_prompt
```

---

### **5. Botões de controle do mestre não aparecem**

**Sintoma:**
```
!narrativa Os heróis encontram...
[Lyra narra]
❌ Nenhum botão aparece
```

**Causa:**  
View não registrada ou timeout.

**Solução:**
```python
# Verifique se views/sessao_master_control_views.py existe

# No comando !narrativa, deve ter:
view = MasterControlView(bot, sessoes_ativas, ...)
await ctx.send(embed=embed, view=view)
```

**Timeout de views:**  
Views expiram após 15 minutos. Use `timeout=None`:
```python
class MasterControlView(discord.ui.View):
    def __init__(self, ...):
        super().__init__(timeout=None)  # ✅ Nunca expira
```

---

### **6. `!inventario` mostra vazio, mas tenho itens**

**Sintoma:**
```
!inventario
🎒 Jogador não possui itens no inventário.

[Mas adicionei itens antes]
```

**Causa:**  
Estrutura de inventário inconsistente.

**Solução:**
```python
# Execute no console Python
from utils import carregar_dados, salvar_dados
fichas = carregar_dados()

# Verifique estrutura
print(fichas["NomeJogador"]["progressao"]["inventario"])

# Se for string ou None:
fichas["NomeJogador"]["progressao"]["inventario"] = []
salvar_dados(fichas)
```

**Ou use migração:**
```
!migrarinventario
```

---

## 🐞 Erros de Sistema

### **7. `KeyError: 'progressao'`**

**Causa:**  
Ficha antiga sem seção `progressao`.

**Solução Automática:**
```python
# O código já corrige automaticamente em garantir_estrutura_inventario()
if "progressao" not in ficha:
    ficha["progressao"] = {}
```

**Solução Manual:**
```json
// Em data/fichas_personagens.json
{
  "NomeJogador": {
    "basico": { ... },
    "atributos": { ... },
    "progressao": {        // ✅ Adicione esta seção
      "xp_atual": 0,
      "xp_proximo_nivel": 300,
      "inventario": []
    }
  }
}
```

---

### **8. `TypeError: 'NoneType' object is not subscriptable`**

**Quando acontece:**
```
!xp
❌ Ocorreu um erro ao executar o comando.
```

**Causa:**  
XP não inicializado.

**Solução:**
```python
# garantir_estrutura_xp() corrige isso
if "progressao" not in ficha:
    ficha["progressao"] = {}

if "xp_atual" not in ficha["progressao"]:
    ficha["progressao"]["xp_atual"] = 0
```

**Teste:**
```
!migrarinventario  # Corrige todas as fichas
!xp                # Deve funcionar
```

---

## 🔍 Debugging Avançado

### **Logs Detalhados**

**Adicione ao `main.py`:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('lyra_debug.log'),
        logging.StreamHandler()
    ]
)
```

**Verifique erros:**
```bash
tail -f lyra_debug.log
```

---

### **Validar Estrutura de Fichas**

**Script de validação:**
```python
# validate_fichas.py
from utils import carregar_dados

fichas = carregar_dados()

for nome, ficha in fichas.items():
    print(f"\n✅ Validando: {nome}")
    
    # Verifica seções obrigatórias
    secoes = ["basico", "atributos", "combate", "progressao"]
    for secao in secoes:
        if secao not in ficha:
            print(f"  ❌ Faltando: {secao}")
        else:
            print(f"  ✅ {secao}")
    
    # Verifica inventário
    if "progressao" in ficha:
        inv = ficha["progressao"].get("inventario")
        if isinstance(inv, list):
            print(f"  ✅ Inventário: {len(inv)} itens")
        else:
            print(f"  ❌ Inventário inválido: {type(inv)}")
```

**Execute:**
```bash
python validate_fichas.py
```

---

## 📊 Checklist de Problemas

Antes de reportar um bug, verifique:

- [ ] Bot está atualizado (`git pull`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] `.env` configurado corretamente
- [ ] `!migrarinventario` executado
- [ ] Bot reiniciado após mudanças
- [ ] Permissões do bot no Discord
- [ ] Logs verificados (`lyra_debug.log`)

---

## 🆘 Suporte

### **Reportar Bug**

**Informações necessárias:**
```
1. Comando usado: !addinventario Espada
2. Erro exato: AttributeError: 'str' object...
3. Versão: v3.0.0
4. Sistema operacional: Ubuntu 22.04
5. Python: 3.11.2
6. Logs: [anexar lyra_debug.log]
```

**Onde reportar:**
- [GitHub Issues](https://github.com/Leosdc/lyra-the-wise/issues)
- Discord do projeto

---

## ✅ Solução Rápida — Tudo Quebrado?

**Reset completo (último recurso):**
```bash
# 1. Backup
cp data/fichas_personagens.json backup_$(date +%Y%m%d).json

# 2. Reset do bot
git reset --hard origin/main
git pull

# 3. Reinstala dependências
pip install --upgrade -r requirements.txt

# 4. Migra fichas
python migrate_to_v3.py

# 5. No Discord
!migrarinventario

# 6. Reinicia bot
python main.py
```

---

<div align="center">

**Ainda com problemas?**  
Abra uma [Issue no GitHub](https://github.com/Leosdc/lyra-the-wise/issues) com detalhes!

</div>
