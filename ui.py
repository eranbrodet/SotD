import webbrowser
from functools import partial
from random import choice
from tkinter import Tk, Label, StringVar, Button, DISABLED, NORMAL


class SotdUI:
    def __init__(self, sender_options, data):
        self._root = Tk()
        self._data = data
        self._sender_options = sender_options
        self._choice = None

        self._right_answers = 0
        self._wrong_answers = 0
        self._balance_format = 'Right: {} Wrong: {}'

        self._init_window()
        self._init_ui_elements()
        self._choose_next()

        self._root.mainloop()

    def _init_window(self):
        w = self._root.winfo_screenwidth()
        h = self._root.winfo_screenheight()
        size = w//2, h//2
        # Center position on screen
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self._root.geometry("%dx%d+%d+%d" % (size + (x, y)))
        self._root.minsize(*size)

        # self._parent.iconbitmap('icon.ico')
        self._root.title("Song of the Day game")

    def _init_ui_elements(self):
        self._next = Button(self._root, text='Next', width=20, command=self._choose_next, state=DISABLED)
        self._next.grid(row=0, column=0)

        self._balance = StringVar()
        self._balance.set(self._balance_format.format(self._right_answers, self._wrong_answers))
        Label(self._root, textvariable=self._balance).grid(row=0, column=1)

        self._result = StringVar()
        Label(self._root, textvariable=self._result).grid(row=0, column=2)

        self._name = StringVar()
        self._name_label = Label(self._root, textvariable=self._name, fg="blue", cursor="hand2")
        self._name_label.grid(row=1, column=2)
        self._name_label.bind("<Button-1>", self._open_link)

        self._sender_buttons = []
        for i, sender in enumerate(self._sender_options, 1):
            b = Button(self._root, text=sender, width=10, command=partial(self._check, sender))
            b.grid(row=i, column=1)
            self._sender_buttons.append(b)

    def _open_link(self, event):
        if self._choice:
            webbrowser.open_new(self._choice[0])

    def _check(self, sender):
        success = sender == self._choice[2]
        if success:
            self._right_answers += 1
        else:
            self._wrong_answers += 1
        self._result.set('Yep' if success else f'Nop: {self._choice[2]}')
        for b in self._sender_buttons:
            b.configure(state=DISABLED)
        self._next.configure(state=NORMAL)
        self._balance.set(self._balance_format.format(self._right_answers, self._wrong_answers))

    def _choose_next(self):
        self._choice = choice(self._data)
        self._name.set(self._choice[1])
        self._result.set('')
        for b in self._sender_buttons:
            b.configure(state=NORMAL)
