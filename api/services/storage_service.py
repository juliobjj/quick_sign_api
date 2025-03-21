import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads/"

class StorageService:
  @staticmethod
  def salvar_arquivo(arquivo):
      """
      Salva um arquivo na pasta local definida.

      :param arquivo: Arquivo enviado pelo usuário (objeto FileStorage)
      :param nome_arquivo: Nome do arquivo a ser salvo
      :return: Caminho completo do arquivo salvo
      """

      # Garante que o diretório de destino existe
      os.makedirs(UPLOAD_FOLDER, exist_ok=True)

      # Assegura um nome seguro para o arquivo
      nome_arquivo_seguro = secure_filename(arquivo.filename.lower())
      caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo_seguro)

      # Salva o arquivo no diretório
      arquivo.save(caminho_arquivo)

      return caminho_arquivo
