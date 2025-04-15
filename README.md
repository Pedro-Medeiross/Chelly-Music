# 🎵 Discord Music Bot - Multi-Instance & Scalable

Um bot de música completo para Discord, desenvolvido em Python com a biblioteca **Disnake**. Suporta reprodução de músicas do YouTube e Spotify, possui múltiplos comandos úteis e foi estruturado para rodar com múltiplas instâncias via **Kubernetes**, garantindo performance e estabilidade mesmo em servidores movimentados.

---

## 🚀 Tecnologias Utilizadas

- **Python**
- **Disnake** (fork do Discord.py)
- **FFmpeg** (para reprodução de áudio)
- **Spotify API** e **YouTube Search API**
- **Genius API** (para letras)
- **Kubernetes** (5 containers rodando simultaneamente)

---

## 🎧 Principais Comandos

| Comando                        | Função |
|-------------------------------|--------|
| `play`, `p`, `playmusic`      | Toca uma música (YouTube/Spotify) |
| `skip`, `s`, `next`           | Pula para a próxima faixa |
| `pause` / `resume`            | Pausa ou retoma a reprodução |
| `queue`, `q`                  | Mostra a fila atual |
| `clearqueue`, `cq`            | Limpa a fila |
| `recentplayed`, `history`     | Exibe histórico das faixas tocadas |
| `playrecent`, `replayhistory`| Reproduz novamente músicas do histórico |
| `search`, `find`              | Pesquisa músicas e permite seleção |
| `lyrics`, `letra`             | Mostra letra da música atual via Genius |
| `volume`, `vol`               | Ajusta o volume |
| `join`, `j` / `leave`, `dc`   | Entra ou sai do canal de voz |
| `clean`                       | Limpa mensagens do bot no canal |
| `currentplaying`, `np`        | Mostra a música atual |

E muitos outros!

---

## 🧠 Aprendizados

Esse projeto foi essencial para aprofundar meu conhecimento em:

- Manipulação de áudio e streaming com FFMPEG
- Integração com APIs públicas e autenticação
- Orquestração de múltiplos containers com Kubernetes
- Estruturação de comandos em bots com Disnake
- Tratamento de exceções e melhoria de performance em tempo real
