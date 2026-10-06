# espanso-webui

Interface web **local** para gerenciar os snippets do [espanso](https://espanso.org) —
uma alternativa gráfica para quem vem do Beeftext (ou só não quer editar YAML na mão).
*A local web UI to manage your espanso snippets, with Beeftext import.*

- **Sem serviço em segundo plano:** você roda o comando, ele abre no navegador; Ctrl+C (ou 15 min sem uso) e tudo encerra.
- **Zero dependências além de Python 3.8+ e PyYAML.** Sem internet, sem CDN, sem telemetria.
- Criar/editar/duplicar/excluir snippets, busca, variáveis globais (valores secretos ocultos), botões para inserir cursor, Tab, data, clipboard.
- **Importa o JSON do Beeftext** (`#{cursor}`, `#{key:tab}`, `#{combo:...}`, `#{date}`, `#{clipboard}`…) com relatório do que não tem equivalente.
- **Backup automático** antes de cada gravação (`~/.local/share/espanso-webui/backups`, últimos 30 por arquivo), com restauração pela interface.
- Detecta se o arquivo mudou no disco antes de salvar; só grava YAML que foi conferido por releitura.
- Funciona igual em X11 e Wayland — ele só edita os arquivos; quem digita é o espanso.

## Uso

```bash
git clone https://github.com/renato-figueiredo/espanso-webui
cd espanso-webui && ./install.sh     # cria o comando em ~/.local/bin
espanso-webui                        # abre http://127.0.0.1:8765/?t=<token>
```

Opções: `--match-dir PASTA` (padrão: `espanso path config`/match), `--port`, `--idle MIN` (0 = nunca), `--no-browser`.

## Importar do Beeftext

No Beeftext: *File → Export*. Na interface: **Importar Beeftext** → escolha o `.json` → confira o resumo → **Adicionar** → **Salvar arquivo**.

| Beeftext | espanso |
|---|---|
| `#{cursor}` | `$\|$` |
| `#{key:tab}` / `#{key:enter}` | `\t` / `\n` com `force_mode: keys` |
| `#{combo:-x}` | variável `type: match` |
| `#{date}` / `#{time}` / `#{dateTime:fmt}` | variável `type: date` |
| `#{clipboard}` | variável `type: clipboard` |
| `#{input:...}` | só o cursor (formulários exigem o recurso *modulo* do espanso) |

Não migrado: combos desabilitados viram ativos (o espanso não tem esse campo), modo de casamento/maiúsculas, sons e atalhos do Beeftext.

## Segurança e privacidade

- Escuta **só em 127.0.0.1**, exige um token aleatório por sessão (impresso no terminal) e valida o cabeçalho `Host`, o que bloqueia CSRF e DNS-rebinding por outras páginas abertas no navegador.
- Só edita arquivos `.yml` dentro da pasta `match` do espanso.
- Seus snippets **nunca** vão para este repositório. Se guardar senhas em variáveis, lembre que ficam em texto puro no YAML — não versione esse arquivo em repositório público.

## Limitações

- Reescrever um arquivo pela interface **descarta comentários YAML** escritos à mão (use o campo *Descrição*, que vira `label`). Para arquivos cheios de comentários, crie um arquivo novo (**+ Arquivo**) em vez de editar o existente.
- Matches avançados (regex, formulários, imagens) são preservados, mas editados só como JSON/somente leitura.

## Desenvolvimento

```bash
python3 -m unittest discover -s tests -v
```

Licença: MIT.
