import flet
class MyApp(flet.App):

    def __init__(self):

        self.progress_bars = []

        for i in range(4):
            self.progress_bars.append(flet.CircularProgressBar(value=0))

        super().__init__()

    def build(self):

        return flet.Column(
            [
                flet.AppBar(
                    title="My App",
                ),
                flet.Row(
                    [
                        self.progress_bars[0],
                        self.progress_bars[1],
                        self.progress_bars[2],
                        self.progress_bars[3],
                    ],
                ),
            ],
        )

    def update_progress_bars(self, input_values):

        for i in range(4):
            self.progress_bars[i].value = input_values[i]

