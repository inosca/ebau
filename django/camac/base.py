class Base:
    def __init__(self, characters: str):
        self.base = len(characters)
        self.characters = characters
        self.lookup = {char: characters.index(char) for char in characters}

    def encode(self, value: int) -> str:
        if value == 0:
            return self.characters[0]

        encoded = []
        append = encoded.append
        base = self.base
        while value:
            value, remainder = divmod(value, base)
            append(self.characters[remainder])

        return "".join(reversed(encoded))

    def decode(self, encoded: str) -> int:
        decoded = 0
        power = 0
        lookup = self.lookup
        base = self.base
        for char in reversed(encoded):
            decoded += lookup[char] * (base**power)
            power += 1

        return decoded


_base36 = "0123456789abcdefghijklmnopqrstuvwxyz"
base36 = Base(_base36)
base10 = Base(_base36[:10])
