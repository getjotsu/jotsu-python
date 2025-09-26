from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env', usecwd=True))
load_dotenv(find_dotenv('.env.local', usecwd=True), override=True)

from .main import cli
from . import corpora
from . import documents
from . import whoami
from . import workflows

__all__ = (cli, corpora, documents, whoami, workflows)
