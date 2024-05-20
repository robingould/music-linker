from time import sleep 
import threading
from rich.console import Console

console = Console()
class Loading:
    def __init__(self, finish="[bold green]Finished processing!~ :D  ", sleep=.1):
        """
        Processing class

        Args: 
            end (str, optional): What to print when finished. Default is "Finished processing!"
            sleep (float, optional): Time to sleep between animation frames. Default is .1.
        """
        self.finish=finish
        self.sleep=sleep

        self.thread = threading.Thread(target=self.animate)
        self.frames = [
                       "[bold blue] [ \\ ] Processing         ",
                       "[bold blue] [ | ] Processin g         ",
                       "[bold blue] [ / ] Processi n g        ",
                       "[bold blue] [ - ] Process i n g       ",
                       "[bold blue] [ \\ ] Proces s i n g     ",
                       "[bold blue] [ | ] Proce s s i n g     ",
                       "[bold blue] [ / ] Proc e s s i n g    ",
                       "[bold blue] [ - ] Pro c e s s i n g   ",
                       "[bold blue] [ \\ ] Pr o c e s s i n g ",
                       "[bold blue] [ | ] P r o c e s s i n g ",
                       "[bold blue] [ / ]  P r o c e s s i ng ",
                       "[bold blue] [ - ]   P r o c e s s ing ",
                       "[bold blue] [ \\ ]    P r o c e s sing ",
                       "[bold blue] [ | ]     P r o c e ssing ",
                       "[bold blue] [ / ]      P r o c essing ",
                       "[bold blue] [ - ]       P r o cessing ",
                       "[bold blue] [ \\ ]        P r ocessing ",
                       "[bold blue] [ | ]         P rocessing ",
                       "[bold blue] [ / ]          Processing ",
                       "[bold blue] [ - ]          Processing "
                    ]
        self.total_frames = len(self.frames)
        self.running = True

    def start(self):
        print()
        self.thread.start()
        return self
    
    def animate(self):
        i = 0
        while self.running:
            console.print(self.frames[i], end='\r')
            sleep(.1)
            i += 1 
            i = i % self.total_frames

    def stop(self):
        self.running = False
        console.print(f"{self.finish}")

if __name__ == "__main__":
    loader = Loading().start()
    for i in range(20):
        sleep(0.25)
    loader.stop()


