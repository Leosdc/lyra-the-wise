# 🎨 EXEMPLO VISUAL - Interface v3.0

## 📺 **Como Ficará a Interface Durante o Jogo**

---

### **1️⃣ Mestre Usa !narrativa**

```
[Mestre RPG] 18:30
!narrativa Os heróis entram na Taverna do Javali Dourado. 
O ambiente está cheio, mas um silêncio estranho paira no ar.
```

---

### **2️⃣ Lyra Responde (Apenas Narrativa)**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📖 Narrativa de Lyra              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

A porta da Taverna do Javali Dourado range ao se 
abrir, revelando um interior repleto de corpos e 
sombras dançantes à luz de velas tremulantes. O ar 
é denso — fumaça de cachimbos, cheiro azedo de 
cerveja velha e algo mais... ferro. Sangue.

Dezenas de olhos viram-se para vocês. Humanos, 
meio-orcs, até um tiefling no canto. Mas ninguém 
fala. O único som é o crepitar da lareira e o 
ranger de uma tábua sob os pés de vocês.

No fundo, atrás do balcão, o taverneiro — um 
homão careca com cicatrizes no rosto — limpa um 
copo lentamente, sem tirar os olhos de vocês. 
Seus dedos tremem levemente.

Algo está muito, muito errado aqui.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use os botões abaixo para controlar a sessão
```

**[Botões Interativos do Mestre]**
```
┌─────────────────────┐ ┌─────────────────────┐
│  🎲 Solicitar       │ │  ⚔️ Iniciar        │
│     Rolagens        │ │     Combate         │
└─────────────────────┘ └─────────────────────┘

┌─────────────────────┐ ┌─────────────────────┐
│  📊 Status Geral    │ │  📖 Ver Ações      │
│                     │ │     Pendentes       │
└─────────────────────┘ └─────────────────────┘
```

**[Mensagem Automática para Jogadores]**
```
📖 A história continua...

💡 Próximos passos:
• Use !acao <descrição> para descrever o que seu personagem faz
• Aguarde o mestre solicitar rolagens (se necessário)
• O mestre controlará o ritmo da aventura
```

---

### **3️⃣ Jogadores Usam !acao**

```
[Thorin Escudo-de-Ferro] 18:32
!acao Me aproximo do balcão mantendo a mão no cabo da 
espada, observando atentamente o taverneiro
```

**[Resposta Visual]**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎭 Thorin Escudo-de-Ferro age!    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Me aproximo do balcão mantendo a mão no cabo da 
espada, observando atentamente o taverneiro

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Aguardando aprovação do mestre | Use !acoespendentes
```

```
[Elara Chama-Lunar] 18:32
!acao Fico próxima à porta, de costas para a parede, 
escaneando o ambiente em busca de ameaças
```

```
[Kael Sombrio] 18:33
!acao Sento-me em uma mesa próxima e finjo beber, 
tentando ouvir conversas
```

---

### **4️⃣ Mestre Clica "Ver Ações Pendentes"**

**[Resposta Privada para o Mestre]**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📋 Ações Declaradas pelos Jogadores┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

• Thorin Escudo-de-Ferro: Me aproximo do balcão 
  mantendo a mão no cabo da espada, observando 
  atentamente o taverneiro

• Elara Chama-Lunar: Fico próxima à porta, de 
  costas para a parede, escaneando o ambiente em 
  busca de ameaças

• Kael Sombrio: Sento-me em uma mesa próxima e 
  finjo beber, tentando ouvir conversas

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Use !narrativa para narrar as consequências
```

---

### **5️⃣ Mestre Decide: Solicitar Rolagens**

**[Clica "🎲 Solicitar Rolagens"]**

**[Modal Aparece]**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Solicitar Rolagem de Dados        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Tipo de Rolagem:
┌─────────────────────────────────┐
│ 1d20+SAB                        │ (ex: 1d20+3, 2d6)
└─────────────────────────────────┘

        [Enviar]  [Cancelar]
```

**[Após Enviar - Seleção de Jogadores]**
```
👥 Mestre, selecione os jogadores:

┌─────────────────────────────────┐
│ Selecione os jogadores...       │▼│
│ ☑ Thorin Escudo-de-Ferro        │
│ ☑ Elara Chama-Lunar             │
│ ☐ Kael Sombrio                  │
└─────────────────────────────────┘

      [✅ Confirmar]  [❌ Cancelar]
```

---

### **6️⃣ Jogadores Recebem Solicitação**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎲 Rolagem Solicitada!            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Tipo: 1d20+SAB
Jogadores: @Thorin Escudo-de-Ferro, @Elara Chama-Lunar

Clique nos botões abaixo para rolar ou use !acao

┌─────────────────┐ ┌─────────────────┐
│  🎲 Rolar Dados │ │  🚫 Não Fazer  │
└─────────────────┘ └─────────────────┘
```

---

### **7️⃣ Resultados das Rolagens**

```
🎲 Thorin Escudo-de-Ferro rolou:
🎲 Rolando 1d20+SAB → [15] + 2
🧮 Resultado: [15] → 17
```

```
🎲 Elara Chama-Lunar rolou:
🎲 Rolando 1d20+SAB → [8] + 4
🧮 Resultado: [8] → 12
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 Todas as Rolagens Concluídas!  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Resultados:
• Thorin Escudo-de-Ferro: 17
• Elara Chama-Lunar: 12

✨ A história continua...
```

---

### **8️⃣ Lyra Narra Consequências**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📖 A História Continua...         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

O taverneiro estremece sob o olhar penetrante de 
Thorin. Seus dedos largam o copo, que rola pelo 
balcão e cai no chão com um estrondo. O silêncio 
se aprofunda.

"E-eles estão embaixo," ele sussurra, voz rouca. 
"No porão. Por favor... não me matem. Eu só... 
eu só deixei eles entrarem."

Elara capta movimento nas sombras — três figuras 
encapuzadas levantam-se lentamente de mesas 
separadas. Suas mãos deslizam para dentro dos 
mantos. Metal reluz à luz das velas.

Enquanto isso, Kael ouve fragmentos de uma 
conversa na mesa ao lado:
"...antes da meia-noite... o ritual... a menina..."

O ar fica mais frio. Vocês sentem isso — magia 
escura pulsando sob seus pés.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estilo: EXTENSO
```

**[Botões do Mestre Aparecem Novamente]**
```
┌─────────────────────┐ ┌─────────────────────┐
│  🎲 Solicitar       │ │  ⚔️ Iniciar        │
│     Rolagens        │ │     Combate         │
└─────────────────────┘ └─────────────────────┘
```

---

### **9️⃣ Mestre Inicia Combate**

**[Clica "⚔️ Iniciar Combate"]**

```
✅ Combate iniciado!

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚔️ Combate Iniciado!              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Jogadores adicionados: 3

Próximos passos:
1. Use !addinimigo <nome> <HP> <CA> para cada inimigo
2. Use !statuscombate para ver status
3. Use !rolariniciativa para começar
4. Use !atacar <alvo> <dano> para atacar
5. Use !curar <alvo> <HP> para curar
6. Use !proximoturno para passar turno
7. Use !encerrarcombate para encerrar
```

**[Mestre Adiciona Inimigos]**
```
[Mestre RPG] 18:38
!addinimigo "Cultista 1" 15 13
!addinimigo "Cultista 2" 15 13
!addinimigo "Cultista 3" 15 13
```

---

### **🔟 Fim do Combate - Recompensas**

```
[Mestre RPG] 18:55
!encerrarcombate
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🏁 Combate Encerrado              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✅ HP dos jogadores atualizado nas fichas.

💡 A aventura continua...
```

```
[Mestre RPG] 18:56
!darxpgrupo 300
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 XP Distribuído para o Grupo    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

✨ Todos receberam +300 XP!

Jogadores: Thorin Escudo-de-Ferro, Elara 
Chama-Lunar, Kael Sombrio

🎉 LEVEL UP:
• Thorin Escudo-de-Ferro → Nível 4!
```

---

## 🎯 **Principais Diferenças Visuais**

### ❌ **ANTES (v2.x):**
- Lyra dizia: "Vocês veem um orc. [ROLL: 1d20, todos]"
- Botões apareciam automaticamente
- Inimigos eram adicionados pela IA

### ✅ **AGORA (v3.0):**
- Lyra diz: "Vocês veem um orc feroz..."
- Mestre recebe botões de controle
- Mestre escolhe quem rola e quando
- Inimigos são adicionados manualmente
- Orientação clara para jogadores

---

**🎨 Interface mais limpa, controle total do mestre, narrativa de qualidade!**
