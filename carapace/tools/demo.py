import carapace





class Printer(carapace.Tool):

    Identifier = 'Mikes Tool'
    Description = 'This tool does almost nothing'

    DEFAULT_OPTIONS = dict(
        foo='a',
        bar=True,
    )
    @classmethod
    def run(cls, foo, bar):
        print('Printer', foo, bar)


class Printer2(carapace.Tool):

    Identifier = 'Mikes Other Tool'
    Description = 'This tool does almost nothing'
    Graphic = None

    DEFAULT_OPTIONS = dict(
        foo='a',
        bar=True,
    )
    @classmethod
    def run(cls, foo, bar):
        print('printer2', foo, bar)