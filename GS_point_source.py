#%% imports
from __future__ import print_function
from math import degrees
from fenics import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, gcf, title
import datetime
from numpy import add
import sympy
from termcolor import colored
import point_source_data as psd
#%% Functions
def Form_f_text(A1, A2):
    #A1 = -4*pi*p', A2 = -FF'
    #expression is inverced because f deined as -f0 (what you see in GS equation)
    #deriviation are calculated using sympy library
    x = sympy.symbols('x[0]') # r coordinate
    f_text = sympy.printing.ccode(A1 * pow(x, 2) + A2)
    print(colored("\nRight equation side: ", 'magenta') + f_text)

    return f_text

def Save_figure(addition, f_expr):
    # Plot solution and mesh. Save plot
    #nothing passed to function, because variables are global
    if plot_mesh == 1:
        plot(mesh)

    mesh_title = "%sx%s mesh" % (str(mesh_r), str(mesh_z))
    curr_time = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    time_title = str(curr_time)  #get current time to make figure name unique
    path_my_file = '/home/george/Projects2/Projects/Figures/Point_source/%s' % time_title


    if addition == '_notitle':
        plt.savefig("%s%s.png" %(path_my_file, addition), dpi = dpi) #no title figure for reports
    elif addition == '_title':
        plt.title('Point source: %s\n%s' % (mesh_title, f_expr._cppcode)) # titled figure for my self
        plt.savefig("%s%s.png" %(path_my_file, addition), dpi = dpi) #no title figure for reports
    else:
        plt.title(addition) # titled figure for my self
        plt.savefig("%s%s.png" %(path_my_file, addition), dpi = dpi) #no title figure for reports

def Analyt_sol(c):
    x = sympy.symbols('x[0]') # r coordinate
    z = sympy.symbols('x[1]') # r coordinate

    psi_p = A1 * pow(x, 4) + A2 * pow(z, 2) #private splotion
    psi_gen = \
        c[0] + \
        c[1] * pow(x, 2) + \
        c[2] * (pow(x, 4) - 4*pow(x, 2)*pow(z, 2)) + \
        c[3] * (- pow(z, 2)) # general solution
        #pow(x, 2)*sympy.log(x) 
    psi_text = sympy.printing.ccode(psi_p + psi_gen)
    print(colored("\nAnalytical solution: ", 'magenta') + psi_text + "\n")

    return psi_text

def CreatePointSource(r, I, disp):
    x = sympy.symbols('x[0]') # r coordinate
    z = sympy.symbols('x[1]') # r coordinate

    pre_exp = -4*pi * I * x # in sympy write stuff that works
    inner_exp = - (pow(x - r[0], 2) + pow(z - r[1], 2)) / pow(disp, 2) # in sympy write stuff that works
    pre_exp_text = sympy.printing.ccode(pre_exp) # transfer it to text
    inner_exp_text = sympy.printing.ccode(inner_exp) # transfer it to text
    
    point_source_text = "%s*exp(%s)" % (pre_exp_text, inner_exp_text) # assemble function of the point source
    print(colored("Point source: ", 'magenta') + point_source_text)
    return point_source_text 
def ArrayOfPointSources(pnt_src_data):
    #create an array of all point source text expressions 
    
    pnt_src_text = []
    for i in range(len(pnt_src_data.r)):
        pnt_src_text.append(CreatePointSource(pnt_src_data.r[i], pnt_src_data.i_disp[i][0], pnt_src_data.i_disp[i][1]))
        
    return pnt_src_text
#%% paremeters definition
mesh_r, mesh_z = 100, 100 # mesh for r-z space
area = [0, 1, -1, 1] # format is: [r1, r2, z1, z2]
rect_low = Point(area[0], area[2]) #define rectangle size: lower point
rect_high = Point(area[1], area[3]) #define rectangle size: upper point

plot_mesh = 0 #choose whether to plot mesh or not
show_plot = 0 # show plot by the end of the program or not
dpi = 200 # quality of a figure 

A1, A2 = 0.14, -0.01
f_text = Form_f_text(A1, A2) # form right hand side that corresponds to analytical solution

pnt_src_data = psd.PointSource()
point_source_text = ArrayOfPointSources(pnt_src_data)
#%% Create mesh and define function space
mesh = RectangleMesh(rect_low, rect_high, mesh_r, mesh_z) # points define domain size rect_low x rect_high
V = FunctionSpace(mesh, 'P', 1) # standard triangular mesh
u_D = Expression('0', degree = 0) # Define boundary condition

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary) #гран условие как в задаче дирихле
#%% Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f_expr = Expression(f_text, degree = 2)
point_source = Expression(point_source_text, degree = 2) #Expression is expected to modify array of text into array of expressions
w = interpolate(Expression('x[0]*x[0]', degree = 2), V) # interpolation is needed so that 'a' could evaluate deriviations and such

a = dot(grad(u)/w, grad(w*v))*dx
L = (f_expr + sum(point_source))*v*dx
#%% Compute solution
u = Function(V)
solve(a == L, u, bc)
plot(u) # its fenics' plot not python's
#%% Save output
Save_figure('_notitle', f_expr)
Save_figure('_title', f_expr)
vtkfile = File('poisson/solution.pvd') # Save solution to file in VTK format
vtkfile << u
#%% 'plt.show()' holds plot while the programm is still running
if show_plot == 1:
    plt.show()