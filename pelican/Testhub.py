from pelican.utils import slugify
assert slugify("asdf fdsa") == "asdf-fdsa"
print(slugify("asdf fdsa"))
