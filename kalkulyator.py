import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chiroyli Kalkulyator")
        self.root.geometry("350x500")
        self.root.configure(bg="#2C2F33")
        self.root.resizable(False, False)

        # Kirish maydoni
        self.entry = tk.Entry(root, width=20, font=('Arial', 18, 'bold'), 
                            justify='right', bg="#23272A", fg="white", 
                            bd=0, insertbackground="white")
        self.entry.grid(row=0, column=0, columnspan=4, padx=20, pady=20, ipady=10)

        # Tugmalar dizayni
        self.create_buttons()

    def button_click(self, number):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current + str(number))

    def clear(self):
        self.entry.delete(0, tk.END)

    def calculate(self):
        try:
            result = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(round(result, 8)))
        except:
            messagebox.showerror("Xato", "Iltimos, to'g'ri ifoda kiriting!")
            self.clear()

    def create_buttons(self):
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#7289DA',
            'fg': 'white',
            'activebackground': '#99AAB5',
            'activeforeground': 'white',
            'bd': 0,
            'relief': 'flat',
            'width': 5,
            'height': 2
        }

        buttons = [
            ('C', self.clear, 1, 0), ('(', lambda: self.button_click('('), 1, 1), (')', lambda: self.button_click(')'), 1, 2), ('/', lambda: self.button_click('/'), 1, 3),
            ('7', lambda: self.button_click('7'), 2, 0), ('8', lambda: self.button_click('8'), 2, 1), ('9', lambda: self.button_click('9'), 2, 2), ('*', lambda: self.button_click('*'), 2, 3),
            ('4', lambda: self.button_click('4'), 3, 0), ('5', lambda: self.button_click('5'), 3, 1), ('6', lambda: self.button_click('6'), 3, 2), ('-', lambda: self.button_click('-'), 3, 3),
            ('1', lambda: self.button_click('1'), 4, 0), ('2', lambda: self.button_click('2'), 4, 1), ('3', lambda: self.button_click('3'), 4, 2), ('+', lambda: self.button_click('+'), 4, 3),
            ('0', lambda: self.button_click('0'), 5, 0), ('.', lambda: self.button_click('.'), 5, 1), ('=', self.calculate, 5, 2)
        ]

        for (text, command, row, col) in buttons:
            btn = tk.Button(self.root, text=text, command=command, **button_style)
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#99AAB5"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#7289DA"))

        # Grid sozlash
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()