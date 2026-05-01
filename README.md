# 📊 Colletor - Hardware Monitoring System

Um sistema modular e configurável para coleta, processamento e monitoramento de métricas de hardware em tempo real. Desenvolvido em Python com suporte a múltiplos coletores e processadores de dados.

## 🎯 Características

- **Coleta Modular**: Arquitetura extensível com coletores independentes
  - CPU
  - Disco
  - Bateria
  - Nós (Tailscale)
  
- **Processadores Configuráveis**: Defina como processar os dados coletados
  - Registro em logs
  - Envio de dados via rede
  
- **Configuração YAML**: Defina comportamentos complexos através de arquivos YAML
- **Cache em Disco**: Armazenamento inteligente de dados com cache JSON
- **Notificações**: Integração com Telegram para alertas
- **Suporte a Roteador**: Coleta de dados via API de roteador
- **Estrutura de Sistema**: Exploração dinâmica de estruturas `/sys/`

## 📦 Requisitos

- Python 3.8+
- Dependências principais:
  ```
  python-dotenv
  requests
  pyyaml
  ```

- Desenvolvimento:
  ```
  isort
  import-analyzer-py
  ```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/AndreOliveiraMendes/colletor.git
cd colletor
```

2. Instale as dependências:
```bash
pip install -r requeriments.txt
```

3. Configure as variáveis de ambiente (crie um arquivo `.env`):
```env
# Sistema
BASE_SYS=/sys/class/
HOSTNAME=seu_hostname
HOSTIP=seu_ip_local

# Servidor/Log
SERVER=seu_servidor
LOG_FOLDER=/var/log

# Telegram (opcional)
TELEGRAM_TOKEN=seu_token
TELEGRAM_CHAT_ID=seu_chat_id

# Roteador (opcional)
ROUTER_URL=url_do_roteador
ROUTER_USER=usuario
ROUTER_PASS=senha
```

## 💡 Uso

### Executar Collector

```bash
python -m app run base
```

Substitua `base` pelo nome de qualquer outro modo definido em `data/runs.yaml`.

### Executar Testes

```bash
python -m app test
```

### Modo de Ajuda

```bash
python -m app --help
```

## ⚙️ Configuração (runs.yaml)

O arquivo `data/runs.yaml` define os modos de execução. Exemplo de estrutura:

```yaml
runs:
  base:
    description: "Coleta básica de métricas"
    collectors:
      - cpu
      - disk
      - battery
    processors:
      - log
      - send
  
  advanced:
    description: "Coleta avançada com nós"
    collectors:
      - cpu
      - disk
      - battery
      - nodes
    processors:
      - log
      - send
  
  minimal:
    description: "Apenas registro em log"
    include:
      - base
```

## 📂 Estrutura do Projeto

```
colletor/
├── app/
│   ├── __main__.py           # Entrada principal
│   ├── config.py             # Configuração de coletores/processadores
│   ├── utils.py              # Utilitários para leitura de sistema
│   ├── collector/            # Módulos de coleta
│   │   ├── cpu.py
│   │   ├── disk.py
│   │   ├── battery.py
│   │   └── tailscale.py
│   ├── runner/               # Processadores e executores
│   │   ├── run.py
│   │   └── test.py
│   ├── channel/              # Canais de comunicação
│   ├── services/             # Serviços auxiliares
│   ├── mem/                  # Gestão de memória
│   └── data/                 # Cache e dados
├── data/
│   ├── runs.yaml             # Configuração de modos de execução
│   └── disk_cache.json       # Cache em disco
├── config.py                 # Configuração global
├── requeriments.txt          # Dependências de produção
├── requeriments-dev.txt      # Dependências de desenvolvimento
└── .gitignore
```

## 🔧 Desenvolvimento

### Instalar dependências de desenvolvimento

```bash
pip install -r requeriments-dev.txt
```

### Adicionar um novo Collector

1. Crie um arquivo em `app/collector/novo_collector.py`:

```python
def get_novo_collector():
    """Coleta dados do novo collector"""
    return [
        {
            "name": "novo_metric",
            "value": 100,
            "unit": "unit"
        }
    ]
```

2. Registre em `app/config.py`:

```python
from app.collector.novo_collector import get_novo_collector

COLLECTORS = {
    # ...
    "novo_collector": get_novo_collector,
}
```

3. Use em `data/runs.yaml`:

```yaml
runs:
  custom:
    collectors:
      - novo_collector
```

### Adicionar um novo Processor

Siga o mesmo padrão, mas registre em `PROCESSORS` no `app/config.py`.

## 📝 Notas Importantes

- O sistema utiliza variáveis de ambiente configuráveis
- O cache é armazenado em `app/data/disk_cache.json`
- Logs são salvos em `/var/log` por padrão (configurável)
- Suporte a symlinks em estruturas do sistema
- Detecção automática de loops em caminhos de filesystem

## 🛠️ Troubleshooting

**Erro: "Collector desconhecido"**
- Verifique o nome do collector em `data/runs.yaml`
- Confirme se foi registrado em `COLLECTORS` no `app/config.py`

**Erro: "Processor desconhecido"**
- Verifique o nome do processor em `data/runs.yaml`
- Confirme se foi registrado em `PROCESSORS` no `app/config.py`

**Permissões negadas ao ler `/sys`**
- Execute com permissões apropriadas ou configure `BASE_SYS` para um caminho acessível

## 📄 Licença

Este projeto é público. Sinta-se livre para usar, modificar e distribuir.

## 👤 Autor

**Andre Oliveira Mendes**  
[GitHub](https://github.com/AndreOliveiraMendes)

---

**Criado em:** Abril 2026  
**Última atualização:** Maio 2026
