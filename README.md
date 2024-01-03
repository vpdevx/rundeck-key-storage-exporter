
# Rundeck key storage exporter 

Script para exportar o key storage de um banco h2 do rundeck.



## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar definir as seguintes variáveis de ambiente

`DB_PATH`
: Caminho para o arquivo do banco de dados (ex. /home/user/grailsdb) sem a extensão **.mv.db**

`DB_PASSWORD`: Senha do banco de dados (Default: "")

`DB_USER`: Usuário para o bando de dados (Default: "")

`RUNDECK_TOKEN`: Token da API do Rundeck.

`RUNDECK_URL`: URL do Rundeck no qual deseja inserir o antigo key storage. (Default: http://127.0.0.1:4440)




## Instalação

- Certifique-se de ter acesso ao arquivo ou host do banco.
- **Certifique-se de que as variáveis de ambientes estejam definidas corretamente**.

```bash
    git clone https://github.com/viniciuscarvalhopires/rundeck-key-storage-exporter.git
    cd rundeck-key-storage-exporter
    pip install -r requirements.txt
    python3 main.py
```

<h3>OBS: Testes realizados da versão 4.1.0 até a 4.17.0</h3>
