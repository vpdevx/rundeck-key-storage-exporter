import json, requests, jaydebeapi
from logging_config import logger


class StorageExporter:
    def __init__(self, dest_rundeck, dest_rundeck_token, db_path, username, password):
        print("Inicializando...")
        self.dest_rundeck = dest_rundeck
        self.dest_rundeck_token = dest_rundeck_token
        self.db_path = db_path
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            logger.info(
                "Conectando ao banco de dados utilizando a url: " + self.db_path
            )
            self.connection = jaydebeapi.connect(
                "org.h2.Driver", "jdbc:h2:" + self.db_path, ["", ""], "./h2-2.1.214.jar"
            )
            self.cursor = self.connection.cursor()
            logger.info("Conexão realizada com sucesso.")
        except Exception as e:
            logger.error("Erro ao conectar ao banco de dados:", e)

    def upload_key_storage(self, name, content_type, dir, payload):
        # Name: Nome do key storage
        # Content-Type: application/octet-stream
        # Dir: Diretório do key storage
        # Payload: Conteúdo do key storage

        if not self.dest_rundeck.endswith("/"):
            self.dest_rundeck += "/"

        # Upload key storrage para o novo rundeck através da API
        logger.info("Fazendo upload do key storage: " + name)
        try:
            headers = {
                "Accept": "application/json",
                "X-Rundeck-Auth-Token": self.dest_rundeck_token,
                "Content-Type": content_type,
            }

            final_url = self.dest_rundeck + "api/11/storage/" + dir + "/" + name
            response = requests.request(
                "POST", final_url, headers=headers, data=payload, verify=False
            )
            # return http response code
            if response.status_code == 201:
                logger.debug("Key storage " + name + " criado com sucesso.")
            elif response.status_code == 409:
                logger.error(
                    "Erro ao criar o key storage "
                    + name
                    + ", o objeto já existe. Response code: "
                    + str(response.status_code)
                )
            else:
                logger.error(
                    "Erro ao criar o key storage "
                    + name
                    + ". Response code: "
                    + str(response.status_code)
                )

        except Exception as e:
            logger.error("Erro ao fazer upload do key storage:", e)

    def get_key_storage(self):
        logger.info("Obtendo os valores do key storage do banco de dados.")

        try:
            self.cursor.execute(
                'SELECT NAME, JSON_DATA, DIR, CAST("DATA" AS BINARY VARYING) FROM PUBLIC.STORAGE;'
            )
            result = self.cursor.fetchall()

            if result and len(result) > 0:
                for key in result:
                    json_data = json.loads(key[1])

                    if "Rundeck-content-type" in json_data:
                        self.upload_key_storage(
                            key[0], json_data["Rundeck-content-type"], key[2], key[3]
                        )
                    else:
                        logger.warning(
                            "O campo Rundeck-content-type não foi encontrado no key storage: "
                            + key[0]
                        )
            else:
                logger.warning("Nenhum key storage encontrado.")

        except Exception as e:
            logger.error("Erro ao obter os valores do key storage:", e)

    def close_connection(self):
        logger.info("Fechando conexão com o banco de dados.")
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
