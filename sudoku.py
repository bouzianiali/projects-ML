import tkinter as tk
from tkinter import Button, Frame, Label, messagebox  
import random

def n_valide(sudoku, y, x, n):
    # On vérifie si le nombre est valide sur sa ligne
    for x0 in range(9):
        if x0 != x and sudoku[y][x0] == n:
            return False
    # On vérifie si le nombre est valide sur sa colonne
    for y0 in range(9):
        if y0 != y and sudoku[y0][x] == n:
            return False
    # On vérifie si le nombre est valide dans sa sous-grille
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if (y0 + i != y or x0 + j != x) and sudoku[y0 + i][x0 + j] == n:
                return False
    return True

def solve(sudoku):
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                for n in range(1, 10):
                    if n_valide(sudoku, y, x, n):
                        sudoku[y][x] = n
                        if solve(sudoku):
                            return True
                        sudoku[y][x] = 0
                return False
    return True

def est_valide(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                val = sudoku[i][j]
                sudoku[i][j] = 0
                if not n_valide(sudoku, i, j, val):
                    sudoku[i][j] = val
                    return False
                sudoku[i][j] = val
    return True

def afficher_sudoku():
    for i in range(9):
        for j in range(9):
            valeur = sudoku[i][j]
            couleur = 'black'  # Couleur par défaut
            if not n_valide(sudoku, i, j, valeur):
                couleur = 'red'  # Si le nombre n'est pas valide, changer la couleur en rouge
            cell_entries[i][j].delete(0, tk.END)  # Effacer les anciennes valeurs
            cell_entries[i][j].insert(0, str(valeur))  # Insérer la nouvelle valeur
            cell_entries[i][j].config(fg=couleur, justify="center")  # Changer la couleur du texte et centrer le texte

def confirmer():
    global sudoku
    # Vérifier si la grille est vide
    if all(all(cell_entries[i][j].get() == '' for j in range(9)) for i in range(9)):
        messagebox.showerror("Validation", "La grille est vide !")
        return
    for i in range(9):
        for j in range(9):
            val = cell_entries[i][j].get()
            if val.isdigit() and 1 <= int(val) <= 9:
                sudoku[i][j] = int(val)
            else:
                sudoku[i][j] = 0
    afficher_sudoku()  # Appeler afficher_sudoku() après la confirmation

    if est_valide(sudoku):
        messagebox.showinfo("Validation", "Sudoku valide !")
    else:
        messagebox.showerror("Validation", "Sudoku non valide !")

def charger_exemple():
    global sudoku
    sudoku = [[random.randint(1, 9) for _ in range(9)] for _ in range(9)]
    afficher_sudoku()  # Afficher le Sudoku après avoir généré un nouvel exemple

# Créer la fenêtre principale
root = tk.Tk()
root.title("Validation Sudoku")

# Frame pour les cellules du Sudoku
sudoku_frame = Frame(root)
sudoku_frame.pack()

# Entrées pour les cellules du Sudoku
cell_entries = [[None]*9 for _ in range(9)]
for i in range(9):
    for j in range(9):
        if (i // 3 + j // 3) % 2 == 0:
            bg_color = 'white'
        else:
            bg_color = 'lightgrey'
        cell_entries[i][j] = tk.Entry(sudoku_frame, width=3, bg=bg_color, font=('Helvetica', 16), bd=2, relief="solid")
        cell_entries[i][j].grid(row=i, column=j)

        # Ajouter des colonnes vides supplémentaires
        if j % 3 == 2 and j != 8:
            Label(sudoku_frame, width=1).grid(row=i, column=j+1)

    # Ajouter des lignes vides supplémentaires
    if i % 3 == 2 and i != 8:
        for j in range(9):
            Label(sudoku_frame, height=1).grid(row=i+1, column=j)

# Bouton Confirmer
confirm_button = Button(root, text='Confirmer', command=confirmer, font=('Helvetica', 14))
confirm_button.pack(pady=5)

# Bouton Charger exemple
charger_button = Button(root, text='Charger Exemple', command=charger_exemple, font=('Helvetica', 14))
charger_button.pack(pady=5)

# Sudoku initial
sudoku = [[0]*9 for _ in range(9)]

# Afficher la fenêtre principale
root.mainloop()
