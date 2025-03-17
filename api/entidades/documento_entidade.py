class DocumentoEntidade():
  def __init__(self, nome_arquivo, data_envio, pdf_data, usuario_id):
    self.__nome_arquivo = nome_arquivo
    self.__data_envio = data_envio
    self.__pdf_data = pdf_data
    self.__usuario_id = usuario_id

  @property
  def nome_arquivo(self):
    return self.__nome_arquivo
  
  @nome_arquivo.setter
  def nome_arquivo(self, nome_arquivo):
    self.__nome_arquivo = nome_arquivo

  @property
  def data_envio(self):
    return self.__data_envio
  
  @data_envio.setter
  def data_envio(self, data_envio):
    self.__data_envio = data_envio

  @property
  def pdf_data(self):
    return self.__pdf_data
  
  @pdf_data.setter
  def pdf_data(self, pdf_data):
    self.__pdf_data = pdf_data
  
  @property
  def pdf_data(self):
    return self.__pdf_data
  
  @pdf_data.setter
  def pdf_data(self, pdf_data):
    self.__pdf_data = pdf_data

  @property
  def usuario_id(self):
    return self.__usuario_id
  
  @usuario_id.setter
  def usuario_id(self, usuario_id):
    self.__usuario_id = usuario_id