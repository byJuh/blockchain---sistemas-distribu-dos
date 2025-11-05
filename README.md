
---

## 📄 **Resumo Técnico da POC (para anexar no trabalho)**

---

### **Título:** POC – Blockchain como Sistema Distribuído  

### **Objetivo:**  
Comprovar a viabilidade de um sistema distribuído baseado em blockchain, onde diferentes nós trocam informações (blocos) via rede e mantêm consistência entre si.

---

### **Descrição da Arquitetura**
A POC foi implementada em **Python**, utilizando **HTTP** e **WebSocket** para comunicação entre os componentes:

- **Servidor Central:** responsável por receber novos blocos via HTTP e redistribuí-los em tempo real a todos os clientes conectados.
- **Nós (clientes):** simulam os participantes da blockchain, gerando e validando blocos de forma independente, mantendo uma cópia local da cadeia.

---

### **Componentes principais:**
| Componente | Função |
|-------------|--------|
| `server.py` | Mantém conexões WebSocket e retransmite blocos recebidos. |
| `cliente.py` | Cria, valida e armazena blocos localmente, enviando novos blocos à rede. |
| `blockchain_local` | Lista que representa a cadeia de blocos em cada nó. |

---

### **Funcionamento**
1. Ao iniciar, o nó cria um **bloco gênese**.
2. Quando o usuário digita uma mensagem, é gerado um novo bloco contendo:
   - Índice,
   - Timestamp,
   - Hash do bloco anterior,
   - Dados da transação,
   - Hash atual.
3. O nó envia o bloco ao servidor via **HTTP POST (/publish)**.
4. O servidor retransmite o bloco via **WebSocket** para todos os nós conectados.
5. Cada nó valida e adiciona o bloco à sua blockchain local, calculando **latência** e exibindo logs no terminal.

---

### **Métricas observadas**
| Métrica | Descrição |
|----------|------------|
| **Latência de rede** | Diferença entre envio e recebimento (em ms). |
| **Entrega** | Todos os nós recebem os blocos enviados (broadcast). |
| **Consistência** | Cadeias idênticas entre nós (mesmos hashes finais). |

---

### **Resultados esperados**
- Todos os nós mantêm o mesmo estado final.
- Latência média baixa (milissegundos em rede local).
- Blocos inválidos são rejeitados.
- Rede distribuída demonstra coerência e integridade.

---

### **Conclusão**
A POC atinge o objetivo de comprovar o **comportamento distribuído e a integridade da comunicação** em uma rede blockchain simples.  
Ela demonstra:
- **Troca de mensagens assíncrona (HTTP + WebSocket);**
- **Validação e encadeamento de blocos;**
- **Coerência entre múltiplos nós.**

Com pequenas expansões, esse modelo pode evoluir para uma blockchain funcional com mecanismos de consenso e persistência de dados.

---

### **Palavras-chave:**  
Blockchain · Sistemas Distribuídos · Comunicação HTTP · WebSocket · Latência · Consistência  

---

Se quiser, posso agora gerar pra você **os arquivos reais (README.md + resumo em .docx)** prontos pra enviar ou subir no repositório — quer que eu gere esses arquivos e te disponibilize pra download?
