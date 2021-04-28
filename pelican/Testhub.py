from pelican.utils import slugify
from pelican.settings import DEFAULT_CONFIG
assert slugify("asdf fdsa") == "asdf-fdsa"
print(slugify("asdf fdsa"))
