from os import name
from imports import *
import time

DPI = 200
TEXT_FILE_U_MAX = "Text_data/func_max"
M0 = 1.25e-6

def Form_f_text(A1, A2):
    #A1 = 4*mo*p', A2 = FF'
    #deriviation are calculated using sympy library
    x = sympy.symbols('x[0]') # r coordinate
    f_text = sympy.printing.ccode(A1 * pow(x, 2) + A2)
    print(colored("Right-hand equation side (f): \n", 'magenta') + f_text)

    return f_text

def Twod_plot(psi, x0, y1, y2, path): 
    # y1, y2 - min and max points in an interval of interest, 
    # x0 - point along which 2d graph is plotted
    # psi.set_allow_extrapolation(True)
    tol, point_num = 0.001, 100 + 1  # avoid hitting points outside the domain
    y = numpy.linspace(y1 + tol, y2 - tol, point_num)
    
    points = [(x0, y_) for y_ in y]  # create 2D points
    psi_line = numpy.array([psi(point) for point in points])
    matplt.plot(y, psi_line, 'k', linewidth=2)  # magnify w
    matplt.grid(True)
    matplt.xlabel('$r$')
    matplt.ylabel('$psi$')
    matplt.legend(["Point: %s, interval: [%s, %s]" % (x0, y1, y2), 'Load'], loc='best')
    
    time_title = Time_name()
    matplt.savefig('Figures/%s/%s_%s.png' % (path, time_title, x0), dpi = DPI)
    matplt.close() # close created plot
    
    print(colored("2d plot saved!", 'green'))
    return numpy.amax(psi_line)
    
def Time_name():
    ttime = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
    time_title = str(ttime)  #get current time to make figure name unique
    return time_title

def Save_figure(f_expr, mesh_r, mesh_z, addition, PATH):
    # move to funcs, add missing args, fix save path 
    # Plot solution and mesh. Save plot
    #nothing passed to function, because variables are global
    mesh_title = "%sx%s mesh" % (str(mesh_r), str(mesh_z))
    
    time_title = Time_name()

    path_my_file = 'Figures/%s/%s' % (PATH, time_title) # file path+unique time name

    if addition == '_notitle':
        matplt.savefig("%s%s.png" % (path_my_file, addition), dpi = DPI) #no title figure for reports
    elif addition == '_title':
        matplt.title('Analyt Soloviev: %s\n%s' % (mesh_title, f_expr._cppcode)) # titled figure for my self
        matplt.savefig("%s%s.png" % (path_my_file, addition), dpi = DPI) #no title figure for reports
    else:
        matplt.title(addition) # titled figure for my self
        matplt.savefig("%s%s.png" % (path_my_file, addition), dpi = DPI) #no title figure for reports
    print(colored("Plot saved!", 'green'))
    
def Write2file_umax_vs_def_mesh(mesh_r, mesh_z, u_max):
    file = open("%s.txt" % TEXT_FILE_U_MAX, "a") # append write to file mode
    
    text = "%s,%s,%s\n" % (mesh_r, mesh_z, u_max)
    file.write(text)
    file.close()

def Write2file_umax_vs_square_size(mesh_r, mesh_z, u_max):
    file = open("%s_vs_square_mesh.txt" % TEXT_FILE_U_MAX, "a") # append write to file mode
    
    text = "%s,%s,%s\n" % (mesh_r, mesh_z, u_max)
    file.write(text)
    file.close()
    
    
def Column(matrix, col):
    return [row[col] for row in matrix]
    
def Plot_umax_vs_def_mesh(name): # u max as a function of mesh parameters on the same solution area
    with open("%s.txt" % TEXT_FILE_U_MAX, "r") as file:
        data = [[float(num) for num in line.split(',')] for line in file]
        
    mesh = Column(data, 0) 
    u_max = Column(data, 2)
    
    matplt.scatter(mesh, u_max, linewidth=2)  # magnify w
    matplt.legend(["u_max vs default mesh size"], loc='best')
    matplt.grid(True)
    matplt.xlabel('mesh square size')
    matplt.ylabel('$u_{max}$')
    
    matplt.savefig("Figures/umax_vs_mesh_%s.png" % name, dpi = DPI)
    
    matplt.close() # close created plot

def Plot_umax_vs_square_size(): # u max as a function of solution square size
    with open("%s_vs_square_mesh.txt" % TEXT_FILE_U_MAX, "r") as file:
        data = [[float(num) for num in line.split(',')] for line in file]
        
    mesh = Column(data, 0) 
    u_max = Column(data, 2)
    
    matplt.scatter(mesh, u_max, linewidth=2)
    matplt.legend(["u_max vs solution square size"], loc='best')
    matplt.grid(True)
    matplt.xlabel('mesh square size')
    matplt.ylabel('$u_{max}$')
    
    matplt.savefig("Figures/umax_vs_square_size_%s.png" % name, dpi = DPI)
    
    matplt.close() # close created plot
    
def What_time_is_it(t0, message):
    print(colored("\tTime elapsed = %f (%s)" % (time.time() - t0, message), 'blue'))
    
def Analyt_sol(c, A1, A2):
    x = sympy.symbols('x[0]') # r coordinate
    z = sympy.symbols('x[1]') # r coordinate
    #sympy.log
    psi_p = A1 * pow(x, 4) + A2 * pow(z, 2) #private solution
    psi_gen = \
        c[0] + \
        c[1] * pow(x, 2) + \
        c[2] * (pow(x, 4) - 4*pow(x, 2)*pow(z, 2)) + \
        c[3] * (-pow(z, 2)) # general solution the rest of the 4th term is defined in MyLog(c) func
        #c[3] * (pow(x, 2)*sympy.log(x)- pow(z, 2)) # general solution
        #pow(x, 2)*sympy.log(x) 
    
    my_log = MyLog(c)
    
    psi_text = sympy.printing.ccode(psi_p + psi_gen)
    psi_p_text = sympy.printing.ccode(psi_p)
    
    # final_sol = psi_text 
    final_sol = psi_text + ' + ' + my_log
    print(colored("Private solution: \n", 'magenta') + psi_p_text)
    print(colored("Analytical solution: \n", 'magenta') + final_sol)
    # print(colored("Analytical solution: \n", 'magenta') + psi_text)

    return final_sol

def MyLog(c):
    x = sympy.symbols('x[0]') # r coordinate
    pre_log = c[3] * pow(x, 2)
    
    pre_log_text = sympy.printing.ccode(pre_log)
    log_text = "%s*std::log(%s)" % (pre_log_text, 'x[0]') # assemble function of the point source
    print(colored("Problem term in analyt solution: \n", 'magenta') + log_text)
    #c[3] * (pow(x, 2)*log(x)) # general solution
    
    return log_text

def ErrorEstimate(u, u_D, mesh):
    # Compute error in L2 norm
    error_L2 = errornorm(u_D, u, 'L2')

    # Compute maximum error at vertices
    vertex_values_u_D = u_D.compute_vertex_values(mesh)
    vertex_values_u = u.compute_vertex_values(mesh)
    error_max = numpy.max(numpy.abs(vertex_values_u_D - vertex_values_u))

    # Print errors
    print(colored('error_L2  = ', 'red'), error_L2)
    print(colored('error_max = ', 'red'), error_max)
    
    return error_L2, error_max

def CreatePointSource(r, I, disp):
    x = sympy.symbols('x[0]') # r coordinate
    z = sympy.symbols('x[1]') # r coordinate

    pre_exp = M0/pi/disp/disp * I * x # in sympy write stuff that works
    inner_exp = - (pow(x - r[0], 2) + pow(z - r[1], 2)) / pow(disp, 2) # in sympy write stuff that works
    pre_exp_text = sympy.printing.ccode(pre_exp) # transfer it to text
    inner_exp_text = sympy.printing.ccode(inner_exp) # transfer it to text
    
    point_source_text = "%s*exp(%s)" % (pre_exp_text, inner_exp_text) # assemble function of the point source
    print(colored("Point source: \n", 'magenta') + point_source_text)
    return point_source_text 

def ArrayOfPointSources(pnt_src_data):
    #create an array of all point source text expressions 
    
    pnt_src_text = []
    for i in range(len(pnt_src_data.r)):
        pnt_src_text.append(CreatePointSource(pnt_src_data.r[i], pnt_src_data.i_disp[i][0], pnt_src_data.i_disp[i][1]))
        
    return pnt_src_text

def My_sum(array):
    summa = array[0]
    for i in range(1, len(array)):
        summa = summa + array[i]
        
    return summa