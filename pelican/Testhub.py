from pelican.utils import slugify

if slugify("asdf fsda") == "asdf-fsda":
    print("true")
else:
    print("false")
print(slugify("asdf fsda"))
