from datetime import date

from click import ParamType


class EntryRef(ParamType):
    name = 'entryref'

    def convert(self, value, param, ctx):
        try:
            d = date.fromisoformat(value)
        except ValueError:
            pass
        else:
            return d

        i = int(value, 10)
        if i < 1:
            self.fail(f'{value!r} is not a valid entry number', param, ctx)
        return i


ENTRY_REF = EntryRef()
