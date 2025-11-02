# 🔄 GUIA DE MIGRAÇÃO v2.x → v3.0

## ⚠️ **ATENÇÃO: Mudanças Importantes**

Se você já usa Lyra v2.x, leia este guia **antes** de atualizar!

---

## 📊 **O Que Mudou?**

### ❌ **REMOVIDO (v2.x):**
- ❌ Detecção automática de combate pela IA
- ❌ Auto-adição de inimigos
- ❌ Solicitação automática de rolagens
- ❌ Lyra tomando decisões sozinha

### ✅ **ADICIONADO (v3.0):**
- ✅ Sistema de inventário completo
- ✅ Sistema de XP com progressão visual
- ✅ Controle total do mestre (botões interativos)
- ✅ Comando `!narrativa` para narrativas controladas
- ✅ Integração total de dados das fichas

---

## 🔧 **Atualização de Fichas Existentes**

### **1. Adicionar Seção de Progressão**

Se suas fichas não têm XP, adicione manualmente:

```python
# Execute este código Python:
from config import fichas_personagens
from core.ficha_helpers import salvar_fichas_agora

for chave, ficha in fichas_personagens.items():
    secoes = ficha.get("secoes", {})
    
    # Adiciona progressão se não existir
    if "progressao" not in secoes:
        secoes["progressao"] = {
            "XP Atual": 0,
            "XP Total": 0
        }
        print(f"✅ Progressão adicionada: {ficha.get('nome', chave)}")

salvar_fichas_agora()
print("🎉 Todas as fichas atualizadas!")
```

### **2. Atualizar Inventário**

Transforme inventários antigos em novo formato:

```python
from config import fichas_personagens
from core.ficha_helpers import salvar_fichas_agora

for chave, ficha in fichas_personagens.items():
    secoes = ficha.get("secoes", {})
    equipamento = secoes.get("equipamento", {})
    
    # Inventário antigo (lista de strings)
    itens_antigos = equipamento.get("Itens", [])
    
    # Converte para novo formato
    inventario_novo = []
    for item in itens_antigos:
        if isinstance(item, str):
            inventario_novo.append({
                "nome": item,
                "quantidade": 1,
                "tipo": "geral"
            })
    
    # Atualiza
    equipamento["Inventário"] = inventario_novo
    equipamento["Equipado"] = {
        "Arma": equipamento.get("Armas", ["—"])[0] if equipamento.get("Armas") else "—",
        "Armadura": equipamento.get("Armadura", "—")
    }
    
    print(f"✅ Inventário atualizado: {ficha.get('nome', chave)}")

salvar_fichas_agora()
print("🎉 Inventários convertidos!")
```

---

## 🎮 **Mudanças no Fluxo de Jogo**

### **ANTES (v2.x):**
```
1. Mestre: !cenanarrada Entram na taverna
2. Lyra: [Narra] "Vocês veem um orc! [ROLL: 1d20, todos]"
3. [Botões de rolagem aparecem automaticamente]
4. Jogadores rolam
5. Lyra continua a história
```

### **AGORA (v3.0):**
```
1. Mestre: !narrativa Entram na taverna e veem um orc
2. Lyra: [Narra] "Vocês entram na taverna. Um orc bêbado vira-se..."
3. [Mestre recebe botões de controle]
4. Jogadores: !acao Aproximo do orc
5. Mestre: [Clica "Solicitar Rolagens"]
6. Mestre: [Escolhe "Intimidação 1d20+CAR" e seleciona jogadores]
7. Jogadores rolam
8. Mestre: !narrativa <consequências>
```

---

## 📝 **Comandos Renomeados/Modificados**

| v2.x | v3.0 | Mudança |
|------|------|---------|
| `!cenanarrada` | `!narrativa` | Renomeado para clareza |
| `!acao` | `!acao` | Mantido, mas agora registra ação pendente |
| Botões automáticos | Botões do mestre | Só aparecem para o mestre após `!narrativa` |

---

## ⚔️ **Sistema de Combate**

### **ANTES (v2.x):**
- IA detectava combate automaticamente
- Inimigos eram adicionados pela IA (muitas vezes com valores errados)

### **AGORA (v3.0):**
- Mestre clica botão **⚔️ Iniciar Combate**
- Mestre adiciona inimigos manualmente: `!addinimigo Goblin 10 15`
- Valores corretos e controlados

---

## 🆕 **Novos Comandos que Você Precisa Aprender**

### **Para Mestres:**
```
!narrativa <descrição> — Substitui !cenanarrada
!acoespendentes — Ver ações dos jogadores
!limparacoes — Limpar ações após narrativa
!darxp <@jogador> <qtd> — Dar XP individual
!darxpgrupo <qtd> — Dar XP para todos
```

### **Para Jogadores:**
```
!inventario — Ver inventário
!addinventario <item> — Adicionar item
!equiparitem <item> — Equipar item
!usaritem <item> — Consumir item
!xp — Ver XP e progressão
```

---

## 🎯 **Checklist de Migração**

### **Antes de Atualizar:**
- [ ] Faça backup: `!backup`
- [ ] Anote nível atual de cada personagem
- [ ] Anote itens importantes no inventário

### **Após Atualizar:**
- [ ] Execute script de atualização de fichas (acima)
- [ ] Teste `!xp` em cada ficha
- [ ] Teste `!inventario` em cada ficha
- [ ] Configure XP inicial se necessário
- [ ] Popule inventários com `!addinventario`

### **Primeira Sessão v3.0:**
- [ ] Explique aos jogadores o novo comando `!acao`
- [ ] Mostre aos jogadores `!inventario` e `!xp`
- [ ] Como mestre, pratique `!narrativa` + botões
- [ ] Experimente dar XP: `!darxpgrupo 100`

---

## 💡 **Dicas de Adaptação**

### **Para Mestres:**
1. **Use `!narrativa`** sempre que quiser que Lyra descreva algo
2. **Não espere rolagens automáticas** — você controla quando rolar
3. **Use os botões** para escolher quem participa de cada cena
4. **Dê XP regularmente** — mantenha engajamento dos jogadores

### **Para Jogadores:**
1. **Use `!acao`** sempre que quiser fazer algo
2. **Não espere a IA pedir rolagens** — o mestre decidirá
3. **Cheque `!inventario`** e `!xp` regularmente
4. **Equipem itens** com `!equiparitem` para usar em combate

---

## ❓ **FAQ de Migração**

**P: Minhas sessões antigas funcionarão?**  
R: Sim, mas use `!narrativa` ao invés de esperar ações automáticas.

**P: Perdi meu XP/inventário?**  
R: Execute os scripts de migração acima para restaurar.

**P: A IA ficou "mais burra"?**  
R: Não! Ela narra MELHOR porque não precisa gerenciar mecânicas.

**P: Posso voltar para v2.x?**  
R: Sim, mas precisará de backup. Recomendamos testar v3.0 primeiro.

**P: Como sei se atualizou?**  
R: Digite `!rpghelp` — se mostrar "v3.0" no título, está atualizado.

---

## 🆘 **Suporte**

Problemas na migração?

- Use `!ajudasessao` para guia completo
- Entre no Discord: [Taverna](https://discord.gg/SdWnWJ6w)
- Abra uma issue: [GitHub](https://github.com/Leosdc/lyra-the-wise/issues)

---

**🎉 Boa sorte com a v3.0! O controle está em suas mãos agora! 🎲**
