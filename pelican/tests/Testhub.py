from pelican.utils import slugify
def testSLugify():
    assert slugify("asdf fdsa") == "asdf-fdsa"
    print(slugify("asdf fdsa"))


