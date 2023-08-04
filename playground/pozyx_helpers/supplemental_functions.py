from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def nice_print(string_to_print):
    """
    Prints a string with a border of '*' characters.
    """
    str_len = len(string_to_print)
    print("*" * (str_len + 4))
    print(f"* {string_to_print} *")
    print("*" * (str_len + 4))

def create_two_figs_in_tab(layout):

    figure_plot0 = Figure()
    canvas_plot0 = FigureCanvas(figure_plot0)
    layout.addWidget(canvas_plot0)

    figure_plot1= Figure()
    canvas_plot1 = FigureCanvas(figure_plot1)
    layout.addWidget(canvas_plot1)

    return figure_plot0, figure_plot1
