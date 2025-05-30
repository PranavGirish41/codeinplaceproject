import tkinter as tk
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")

        self.size = 7
        self.cell = 40

        self.canvas = tk.Canvas(root, width=self.size*self.cell, height=self.size*self.cell, bg='skyblue')
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        self.side = tk.Canvas(root, width=self.cell*self.size//2, height=self.cell*self.size//2, bg='white')
        self.side.grid(row=1, column=1, sticky='n')

        self.msg = tk.Label(root, text="", font=("Arial", 12))
        self.msg.grid(row=2, column=0, columnspan=2)

        self.reset_btn = tk.Button(root, text="Restart", command=self.restart)
        self.reset_btn.grid(row=3, column=0, columnspan=2)

        self.turn = 1

        self.ships1 = []
        self.ships2 = []

        self.hits1 = set()
        self.hits2 = set()
        self.misses1 = set()
        self.misses2 = set()

        self.ship_sizes = [3,2,2]

        self.place_all()

        self.canvas.bind('<Button-1>', self.click)
        self.draw()

    def place(self):
        all_ships = []
        taken = set()
        for sz in self.ship_sizes:
            while True:
                dir = random.choice(['h','v'])
                if dir == 'h':
                    x = random.randint(0, self.size - sz)
                    y = random.randint(0, self.size - 1)
                    locs = [(x+i,y) for i in range(sz)]
                else:
                    x = random.randint(0, self.size - 1)
                    y = random.randint(0, self.size - sz)
                    locs = [(x,y+i) for i in range(sz)]

                if any(l in taken for l in locs):
                    continue
                for l in locs:
                    taken.add(l)
                all_ships.append(locs)
                break
        return all_ships

    def place_all(self):
        self.ships1 = self.place()
        self.ships2 = self.place()

    def draw(self):
        self.canvas.delete("all")
        self.side.delete("all")
        
        hits = self.hits2 if self.turn == 1 else self.hits1
        misses = self.misses2 if self.turn == 1 else self.misses1
        for i in range(self.size):
            for j in range(self.size):
                x1 = i*self.cell
                y1 = j*self.cell
                x2 = x1+self.cell
                y2 = y1+self.cell
                self.canvas.create_rectangle(x1,y1,x2,y2,fill='lightblue')
        for (x,y) in hits:
            self.canvas.create_oval(x*self.cell+5, y*self.cell+5, x*self.cell+self.cell-5, y*self.cell+self.cell-5, fill='red')
        for (x,y) in misses:
            self.canvas.create_line(x*self.cell+5, y*self.cell+5, x*self.cell+self.cell-5, y*self.cell+self.cell-5, fill='black')
            self.canvas.create_line(x*self.cell+5, y*self.cell+self.cell-5, x*self.cell+self.cell-5, y*self.cell+5, fill='black')

        # own board
        scale = self.cell//2
        ships = self.ships1 if self.turn == 1 else self.ships2
        own_hits = self.hits1 if self.turn == 1 else self.hits2
        own_misses = self.misses1 if self.turn == 1 else self.misses2

        for i in range(self.size):
            for j in range(self.size):
                self.side.create_rectangle(i*scale, j*scale, i*scale+scale, j*scale+scale, fill='white')

        for s in ships:
            for (x,y) in s:
                self.side.create_rectangle(x*scale+1, y*scale+1, x*scale+scale-1, y*scale+scale-1, fill='gray')

        for (x,y) in own_hits:
            self.side.create_oval(x*scale+3, y*scale+3, x*scale+scale-3, y*scale+scale-3, fill='red')
        for (x,y) in own_misses:
            self.side.create_line(x*scale+3, y*scale+3, x*scale+scale-3, y*scale+scale-3, fill='black')
            self.side.create_line(x*scale+3, y*scale+scale-3, x*scale+scale-3, y*scale+3, fill='black')

        self.msg.config(text=f"Player {self.turn}'s move")

    def click(self, e):
        cx, cy = e.x // self.cell, e.y // self.cell
        if self.turn == 1:
            if (cx, cy) in self.hits2 or (cx, cy) in self.misses2:
                return
            if any((cx,cy) in s for s in self.ships2):
                self.hits2.add((cx,cy))
                if self.check_sink(cx, cy, self.ships2, self.hits2):
                    self.msg.config(text="Player 1 sunk something!")
                if self.winner(self.ships2, self.hits2):
                    self.msg.config(text="Player 1 wins!")
                    self.canvas.unbind('<Button-1>')
                    return
            else:
                self.misses2.add((cx,cy))
                self.turn = 2
        else:
            if (cx, cy) in self.hits1 or (cx, cy) in self.misses1:
                return
            if any((cx,cy) in s for s in self.ships1):
                self.hits1.add((cx,cy))
                if self.check_sink(cx, cy, self.ships1, self.hits1):
                    self.msg.config(text="Player 2 sunk a ship!")
                if self.winner(self.ships1, self.hits1):
                    self.msg.config(text="Player 2 wins!")
                    self.canvas.unbind('<Button-1>')
                    return
            else:
                self.misses1.add((cx,cy))
                self.turn = 1
        self.draw()

    def check_sink(self, x, y, ships, hits):
        for s in ships:
            if (x,y) in s and all(c in hits for c in s):
                return True
        return False

    def winner(self, ships, hits):
        return all(cell in hits for s in ships for cell in s)

    def restart(self):
        self.turn = 1
        self.hits1.clear()
        self.hits2.clear()
        self.misses1.clear()
        self.misses2.clear()
        self.place_all()
        self.canvas.bind('<Button-1>', self.click)
        self.draw()

if __name__ == '__main__':
    root = tk.Tk()
    Game(root)
    root.mainloop()
