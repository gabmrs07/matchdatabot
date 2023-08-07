import datetime
import dropbox
import io
import json
import os
import time
from functools import wraps


### MÓDULO ORIGINAL EM EGGBERTO ###


class DropBox(object):
	"""Gerencia os arquivos do Dropbox com os arquivos duma pasta física."""

	def __init__(self, token):
		"""Gera as variáveis chave para acessar o DropBox.
		:param token: O token de acesso para a conta do dropbox.
		:param dbox_root_folder: O caminho do diretório raiz na nuvem.
		:param local_folder: O caminho local dos arquivos.
		"""
		self.token = token
		self.online = False
		self.connection_loop()

	def on(function):
		"""Decorator que verifica a conexão da internet antes de executar a função."""

		@wraps(function)
		def wrapper(self, *args, **kwargs):
			if self.online:
				return function(self, *args, **kwargs)
			else:
				if self.connection_loop():
					return function(self, *args, **kwargs)
				else:
					raise ConnectionError
		return wrapper

	def connection_loop(self, timeout=10):
		"""Loop de conexão com o dropbox.
		:param timeout: O tempo de espera para conexão, em segundos.
		"""
		while self.online != True:
			self.online = self.connect()
			time.sleep(1)
			if timeout != None:
				if timeout < 0.0:
					return False
				else:
					timeout -= 1
		else:
			return True

	def connect(self):
		"""Verifica a conexão com o dropbox."""

		try:
			self.db = dropbox.Dropbox(self.token)
			return True
		except:
			return False

	@on
	def exists(self, file, path='/'):
		"""Checa se há um arquivo no caminho declarado na nuvem.
		:param file: O nome do arquivo para checagem.
		:param path: O caminho de referência na nuvem.
		"""
		return file in self.get_files(path)

	@on
	def mkdir(self, path):
		"""Cria uma pasta na nuvem.
		:param path: O caminho para ser criado.
		"""
		self.db.files_create_folder(self.fp('/', path))

	@on
	def get_files(self, path, metadata=None):
		"""Gera todos os arquivos no caminho fornecido.
		:param path: O caminho na nuvem.
		:param metadata: Os metadatas dos arquivos na nuvem, para optimização.
		"""
		metadata = self.get_metadata(path) if metadata is None else metadata
		return [entry.name for entry in metadata.entries]

	@on
	def get_metadata(self, path):
		"""Gera a metadata de todos os arquivos no caminho fornecido.
		:param path: O caminho na nuvem.
		"""
		return self.db.files_list_folder('' if path == '/' else self.fp('/', path))

	def get_local_files(self, path):
		"""Verifica os arquivos do diretório físico.
		:param path: O caminho local.
		"""
		return os.listdir(path)

	@on
	def sync(self, cloud_path, local_path):
		"""Compara os arquivos do diretório físico com os arquivos do Dropbox.
		Se há arquivos somente no diretório físico, então ele faz upload para o Dropbox.
		Se há arquivos somente no Dropbox, então ele faz download para o diretório físico.
		Se há um ambos, então ele compara e vê se há diferenças nas datas de modificação do arquivo.
		Ao se detectar diferença nas datas de modificação do arquivo, ele faz download ou upload.
		:param cloud_path: O caminho dos arquivos na nuvem.
		:param local_path: O caminho físico para baixar.
		"""
		metadata = self.get_metadata(cloud_path)
		cloud_files = self.get_files(cloud_path, metadata)
		local_files = self.get_local_files(local_path)
		for file in local_files:
			if file not in cloud_files:
				self.upload(file, cloud_path, local_path)

		for file in cloud_files:
			if file not in local_files:
				self.download(file, cloud_path, local_path)
			else:
				self.file_checker(file, cloud_path, local_path, metadata, True)

	@on
	def download(self, filename, cloud_path):
		"""Baixa os arquivos de Dropbox.
		:param filename: O nome dos arquivo para baixar.
		"""
		metadata, request_object = self.db.files_download(self.fp(cloud_path, filename))
		return json.loads(request_object.content)

	@on
	def upload(self, filename, data, cloud_path, mode='add'):
		"""Sobe os arquivos ao Dropbox.
		:param filename: O nome dos arquivo para subir.
		:param data: Os dados para transformar em bytes.
		:param cloud_path: O local de upload na nuvem.
		:param mode: O modo de operação: add = Adição sem sobreescrever; overwrite = Adição com sobreescrever.
		"""
		mode = dropbox.files.WriteMode.add if mode == 'add' else dropbox.files.WriteMode.overwrite
		f = io.BytesIO(json.dumps(data).encode('utf-8')).read()
		self.db.files_upload(f, self.fp(cloud_path, filename), mode)

	def file_checker(self, filename, cloud_path, local_path, metadata=None, sync=False):
		"""Checa se há um arquivo com igual nome, tempo de modificação e tamanho.
		Em *time.localtime(mtime)[:6], o asterisco serve para desempacotar o tuple retornado
		de time.localtime(). Este pedaço escreve em client_modified o mesmo valor da data do
		arquivo armazenado fisicamente.
		:param filename: O nome do arquivo.
		:param cloud_path: O caminho na nuvem, para geração da metadata.
		:param local_path: O caminho físico do arquivo.
		:param metadata: Os metadatas dos arquivos na nuvem, para optimização.
		:param sync: Define o que será retornado pela função. Se True, indica a operação para self.sync; False, retorna mtime.
		"""
		metadata = self.get_metadata(cloud_path) if metadata is None else metadata
		if os.uname()[0] == "Linux":
			size = os.path.getsize(local_path)
			mtime = os.path.getmtime(local_path)
			mtime = datetime.datetime(*time.localtime(mtime)[:6])
			mtime = mtime + datetime.timedelta(hours=3)		# Desfaz o time zone (-3 GMT)
			for mdata in metadata.entries:
				if (filename == mdata.name) and isinstance(mdata, dropbox.files.FileMetadata):
					if (mdata.client_modified == mtime) and (mdata.size == size):
						return False
					else:
						if sync:
							if mtime > mdata.client_modified:
								return self.upload(filename, cloud_path, local_path, mode='overwrite')
							else:
								return self.download(filename, cloud_path, local_path)
						else:
							return mtime
			else:
				return mtime

	@on
	def remove(self, filename, cloud_path):
		"""Remove os arquivos do Dropbox.
		:param filaname: O nome do arquivo.
		:param cloud_path: O caminho do arquivo na nuvem.
		"""
		self.db.files_delete(self.fp(cloud_path, filename))

	def fp(self, path, filename):
		"""Retorna o caminho completo até o arquivo.
		:param path: O caminho do arquivo.
		:param filename: O nome do arquivo.
		"""
		path = os.path.join('/', path)
		return os.path.join(path, filename)
