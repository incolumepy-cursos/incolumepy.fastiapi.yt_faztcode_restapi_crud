try:
    import tomllib
except (ImportError, ModuleNotFoundError):
    import tomli as tomllib

from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)

pyproject = Path(__file__).parents[3] / 'pyproject.toml'
# assert pyproject.is_file(), f'{pyproject}'
logging.debug(f'{pyproject=}')

version_file = Path(__file__).parent / 'version.txt'
logging.debug(f'{version_file=}')

with pyproject.open('rb') as f:
    version_file.write_text(tomllib.load(f)['tool']['poetry']['version'])
__version__ = version_file.read_text()
logging.info(f'{__version__=}')
