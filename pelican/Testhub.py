from pelican.utils import slugify
from pelican.settings import DEFAULT_CONFIG
assert slugify("asdf fdsa", regex_subs=DEFAULT_CONFIG['SLUG_REGEX_SUBSTITUTIONS']) == "asdf-fdsa"
print(slugify("asdf fdsa", regex_subs=DEFAULT_CONFIG['SLUG_REGEX_SUBSTITUTIONS']))
print(slugify("asdf fdsa"))
