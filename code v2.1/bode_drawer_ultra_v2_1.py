from tkinter import *
from tkinter.filedialog import askdirectory
from numpy import array
from control.matlab import tf, pole, zero, bode
from matplotlib.pyplot import savefig, show
import latex_div as ld


def saveFile():
    file_dir = askdirectory()
    if file_dir is None:
        return

    inP_up, inP_down = first_text.get(), second_text.get()

    inP_up, inP_down = list(map(float, inP_up.split())), list(
        map(float, inP_down.split()))

    inP_up_str, inP_down_str = ld.to_math_equ(
        math_coff=inP_up), ld.to_math_equ(math_coff=inP_down)

    out_lat = ld.div_str_latex(a=inP_up_str, b=inP_down_str).replace(
        'x', 's').replace('1.0*', '')

    num, den = array(inP_up), array(inP_down)
    G = tf(num, den)
    pole(G)
    zero(G)

    mag, phase, omega = bode(G)
    savefig('\\'.join([file_dir, 'bode.png']))
    show()

    with open('\\'.join([file_dir, 'formlar.txt']), mode='w') as f:
        f.write(str(G))

    ld.latex_div(lat=out_lat, path='\\'.join([file_dir, 'latex.png']))

    window.destroy()


def main() -> None:
    global window
    window = Tk()

    window.title('bode drawer (design by KYLiN)')
    # label
    first_label = Label(window,
                        text='輸入分子多項式係數 : ',
                        font=('Arial', 12)).grid(row=1, column=0)

    global first_text
    first_text = Entry(window)
    first_text.grid(row=1, column=1)

    # label
    second_label = Label(window,
                         text='輸入分母多項式係數 : ',
                         font=('Arial', 12)).grid(row=2, column=0)

    global second_text
    second_text = Entry(window)
    second_text.grid(row=2, column=1)

    # button
    save_button = Button(text='save and run', command=saveFile).grid(
        row=3, column=0, columnspan=2)

    window.mainloop()


if __name__ == '__main__':
    main()
