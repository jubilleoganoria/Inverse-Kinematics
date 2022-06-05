 # SCARA RRP Forward Kinematics
import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme('purple')

# Excel read code

EXCEL_FILE = 'SCARA RRP Forward Kinematics.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

Main_layout = [
    [sg.Text('Fill out the following fields:')],
    [sg.Push(), sg.Text('SCARA RRP MEXE Calculator', font = ("Book Antiqua", 20)), sg.Push()],
    [sg.Text('Forward Kinematics Calculator', font = ("Book Antiqua", 12))],
    [sg.Text('Fill out the following fields: ', font = ("Book Antiqua", 10))],
    
    [sg.Text('a1= '),sg.InputText('0', key='a1', size=(20,10)), 
     sg.Text('T1= '),sg.InputText('0', key='T1', size=(20,10)),
     sg.Push(), sg.Button('Jacobian Matrix (J)', font = ("Book Antiqua", 12), size=(15,2), button_color=('white','#595B83')),
     sg.Button('Det(J)', font = ("Book Antiqua", 12), size=(15,2), button_color=('white','#595B83')), sg.Push()],
     
    [sg.Text('a2= '),sg.InputText('0', key='a2', size=(20,10)), sg.Text('T2= '),sg.InputText('0', key='T2', size=(20,10)),
     sg.Push(), sg.Button('Inverse of J', font = ("Book Antiqua", 12), size=(15,2), button_color=('white','#595B83')),
     sg.Button('Transpose of J', font = ("Book Antiqua", 12), size=(15,2), button_color=('white','#595B83')), sg.Push()],

    [sg.Text('a3= '),sg.InputText('0', key='a3', size=(20,10)), sg.Text('d3= '),sg.InputText('0', key='d3', size=(20,10))],


    [sg.Text('a4= '),sg.InputText('0', key='a4', size=(20,10)),
      sg.Text('a5= '),sg.InputText('0', key='a5', size=(20,10))],
     
    [sg.Button('Click this before Solving Forward Kinematics', font = ("Book Antiqua", 14), size=(41,0), )],

    [sg.Push(), sg.Button('Solve Inverse Kinematics', font = ("Courier New", 12), size=(15,3), button_color=('white','#595B83')),
    sg.Button('Path and Trajectory Planning' , font = ("Courier New", 12), size=(15,3), button_color=('white','#595B83')), sg.Push()],
      
     
     
    [sg.Button('Solve Forward Kinematics', font = ("Book Antiqua", 10), button_color=('white','#595B83'))],
    [sg.Frame('Postion Vector: ',
             
         [[sg.Text('X = '), sg.InputText(key='X', size=(10,1)),
         sg.Text('Y = '), sg.InputText(key='Y', size=(10,1)),
         sg.Text('Z = '), sg.InputText(key='Z', size=(10,1))]])],
    [sg.Frame('H0_3 Transformation Matrix = ',[[sg.Output(size=(60,12))]]),
     sg.Push(),sg.Image('rrp.png'), sg.Push()],
 
    [sg.Submit(),sg.Exit()]


    ]

#Window
window = sg.Window('SCARA RRP Manipulator MEXE Calculator',Main_layout, resizable=True)


#Inverse Kinematics window function
def Inverse_Kinematics_Window():
    sg.theme('purple')


    EXCEL_FILE = 'SCARA_Manipulator_RRP_IK.xlsx'
    IK_df = pd.read_excel(EXCEL_FILE)

    IK_layout =[
    [sg.Push(), sg.Text('Inverse Kinematics', font = ("Book Antiqua", 14 )),sg.Push()],
    [sg.Text('Fill out the following fields:', font = ("Book Antiqua", 14 ))],
    [sg.Text('a1 =', font= ("Book Antiqua", 10)),sg.InputText('0', key= 'a1', size =(8,10)),
     sg.Text('mm',font=("Book Antiqua", 10)),
     sg.Text('X =', font = ("Book Antiqua", 10)) , sg.InputText('0',key = 'X', size = (8,10)),
     sg.Text('mm', font = ("Book Antiqua", 10))],
    [sg.Text('a2=', font =("Book Antiqua", 10)),sg.InputText('0',key='a2',size =(8,10)),
     sg.Text('mm', font = ("Book Antiqua", 10)),
     sg.Text('Y=',font = ("Book Antiqua", 10)),sg.InputText('0',key ='Y',size =(8,10)),
     sg.Text('mm',font =("Book Antiqua", 10))],
    [sg.Text('a3=', font =("Book Antiqua", 10)),sg.InputText('0',key='a3',size =(8,10)),
     sg.Text('mm', font = ("Book Antiqua", 10)),
     sg.Text('Z=',font = ("Book Antiqua", 10)),sg.InputText('0',key ='Z',size =(8,10)),
     sg.Text('mm',font =("Book Antiqua", 10))],
    [sg.Text('a4=', font =("Book Antiqua", 10)),sg.InputText('0',key='a4',size =(8,10)),
     sg.Text('mm', font = ("Book Antiqua", 10))],
    [sg.Text('a5=', font =("Book Antiqua", 10)),sg.InputText('0',key='a5',size =(8,10)),
     sg.Text('mm', font = ("Book Antiqua", 10))],
    [sg.Button('Solve Inverse Kinematics', font = ("Book Antiqua", 10), button_color =('blue','yellow')), sg.Push()],    
    [sg.Frame('Position Vector:',[[
        sg.Text('Th1=',font = ("Book Antiqua", 10)),sg.InputText(key ='IK_Th1',size =(10,1)),
        sg.Text('degree',font =("Book Antiqua", 10)),
        sg.Text('Th2=',font = ("Book Antiqua", 10)),sg.InputText(key ='IK_Th2',size =(10,1)),
        sg.Text('degree',font =("Book Antiqua", 10)),
        sg.Text('d3=',font = ("Book Antiqua", 10)),sg.InputText(key ='IK_d3',size =(10,1)),
        sg.Text('mm',font =("Book Antiqua", 10))]])],
    [sg.Submit(font =("Book Antiqua", 10)),
        sg.Exit(font=("Book Antiqua", 10))]
     ]
               
    
    
#Window code

    Inverse_Kinematics_Window = sg.Window('Inverse Kinematics', IK_layout)

    while True:
        event, values = Inverse_Kinematics_Window.read()
        if event == sg.WIN_CLOSED or event == 'Exit' :
            break
        elif event == 'Solve Inverse Kinematics':
            # Link Lengths
            a1 = float(values['a1']) 
            a2 = float(values['a2']) 
            a3 = float(values['a3']) 
            a4 = float(values['a4']) 
            a5 = float(values['a5'])
            
            # Position Vectors 
            X = float(values['X']) 
            Y = float(values['Y']) 
            Z = float(values['Z']) 

            try:
                phi2 = np.arctan(Y/X)
            except:
                phi2 = -1
                sg.popup('Warning! Present values cause error.')
                sg.popup('Restart the GUI then assign proper values!')
                break
                
            #Th2
            phi2 = np.arctan(Y/X)
            r1 = math.sqrt((abs(X**2))+(abs(Y**2)))
            phi1 = np.arccos(((a4*a4)-(r1*r1)-(a2*a2))/(-2*r1*a2))
            phi3 = np.arccos((r1**2-a2**2-a4**2)/(-2*a2*a4))  
            Th2 = 180 - phi3*(180/np.pi)

            #Th1
            Th1 = (phi2-phi1)*180/np.pi

            #d3
            d3 = (a1+a3-a5-Z)

           # print("Th1 = ", np.around (Th1,3))

           # print("Th2 = ", np.around (Th2,3))

           # print("d3 = ", np.around (d3,3))
           
            Th1 = Inverse_Kinematics_Window['IK_Th1'].Update(np.around(Th1, 3))
           
            Th2 = Inverse_Kinematics_Window['IK_Th2'].Update(np.around(Th2, 3))
           
            d3 = Inverse_Kinematics_Window['IK_d3'].Update(np.around(d3, 3))
           
    
        elif event == 'Submit':
             IK_df = IK_df.append(values, ignore_index=True)
             IK_df.to_excel(EXCEL_FILE, index=False)
             sg.popup('Data Saved!')
                
    Inverse_Kinematics_Window.close()

# Variable codes for disabling buttons
disable_J= window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IV = window['Inverse of J']
disable_TJ = window['Transpose of J']
disable_PT = window['Path and Trajectory Planning']


def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    elif event == 'Click this before Solving \n Forward Kinematics':
        
       disable_J.update(disabled=True)
       disable_DetJ.update(disabled=True)
       disable_IV.update(disabled=True)
       disable_TJ.update(disabled=True)
       disable_PT.update(disabled=True)
        
    elif event == 'Solve Forward Kinematics':
        # Foward Kinematic Codes 
        a1 = values['a1']
        a2 = values['a2']
        a3 = values['a3']
        a4 = values['a4']
        a5 = values['a5']

        T1 = values['T1']
        T2 = values['T2']
        d3 = values['d3']

        T1 = (float(T1)/180.0)*np.pi # Theta 1 in radians
        T2 = (float(T2)/180.0)*np.pi # Theta 2 in radians

        PT = [[float(T1),(0.0/180.0)*np.pi,float(a2),float(a1)],
            [float(T2),(180.0/180.0)*np.pi,float(a4),float(a3)],
            [(0.0/180.0)*np.pi,(0.0/180.0)*np.pi,0,float(a5)+float(d3)]]

        i = 0
        H0_1 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        # print("H0_1 =" )
        # print(np.matrix(H0_1))
        # print("H1_2 =" )
        # print(np.matrix(H1_2))
        # print("H2_3 =" )
        # print(np.matrix(H2_3))

        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        print("H0_3=")
        print(np.matrix(H0_3))

        X0_3 = H0_3[0,3]
        print("X = ")
        print (X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ")
        print (Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ")
        print (Z0_3)
        
        disable_J.update(disabled=False)
        disable_PT.update(disabled=False)

        
    elif event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
      
    elif event == 'Jacobian Matrix (J)':
            
            ### Jacobian Matrix
            
            try:
                H0_1 = np.matrix(H0_1) 
            except:
                H0_1 = -1 #NAN
                sg.popup('Warning!!')
                sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
                break

            ### 1. Linear / Prismatic Vectors
            Z_1 = [[0],[0],[1]] # The [0,0,1] vector
            iden = [[1,0,0],[0,1,0],[0,0,1]] 

            # Row 1 - 3, Column 1
            J1a = np.dot(iden,Z_1)
            # print(J1a)

            J1b_1 = H0_3[0:3,3:]
            J1b_1 = np.matrix(J1b_1)

            J1b_2 = [[0],[0],[0]]

            J1b = J1b_1 - J1b_2

            J1 = [[(J1a[1,0]*J1b[2,0])-(J1a[2,0]*J1b[1,0])],
                  [(J1a[2,0]*J1b[0,0])-(J1a[0,0]*J1b[2,0])],
                  [(J1a[0,0]*J1b[1,0])-(J1a[1,0]*J1b[0,0])]]
            # print("J1 = ")
            # print(np.matrix(J1))

            # Row 1 - 3, Column 2
            J2a = H0_3[0:3,0:3]
            J2a = np.dot(J2a,Z_1)
           # print(J1a)

            J2b_1 = H0_3[0:3,3:]
            J2b_1 = np.matrix(J1b_1)

            J2b_2 = H0_1[0:3,3:]
            J2b_2 = np.matrix(J2b_2)

            J2b = J2b_1 - J2b_2

            J2 = [[(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
                 [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
                 [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]]
           # print("J1 = ")
           # print(np.matrix(J1))

            

            # Row 1 - 3, Column 3

            J3 = H0_2[0:3,0:3]
            J3 = np.dot(J3,Z_1)
            # print("J3 = ")
            # print(J3)


            ### 2. Rotation / Orientation Vectors
            J4= np.dot(iden,Z_1)
            # print("J4 = ")
            # print(J4)

           
            J5 = H0_1[0:3,0:3]
            J5 = np.dot(J5,Z_1)
            # print("J5 = ")
            # print(J5)

            J6 = [[0],[0],[0]]
            J6 = np.matrix(J6)
            # print("J6 = ")
            # print(J6)

            ### 3. Concatenated Jaccobian Matrix
            JM1 = np.concatenate((J1,J2,J3),1)
            # print(JM1)

            JM2 = np.concatenate((J4,J5,J6),1)
            # print(JM2)

            J = np.concatenate((JM1,JM2),0)
            # print("J = ")
            print(J)

            sg.popup('J = ', J)
            DJ = np.linalg.det(JM1)
            if DJ == 0.0 or DJ == -0.0:
               
               disable_IV.update(disabled=True)
               sg.popup('Warning: Jacobian Matrix is Non-Invertible')
            if DJ !=0.0 or DJ != -0.0:
                disable_IV.update(disabled=False)

            
            disable_J.update(disabled=True)
            disable_DetJ.update(disabled=False)
            disable_TJ.update(disabled=False)

    elif event == 'Det(J)':
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break
              
        DJ = np.linalg.det(JM1)
        #print("D = ",DJ)
        sg.popup('DJ = ',DJ)

        if DJ == 0.0 or DJ == -0.0:
               
            disable_IV.update(disabled=True)
            sg.popup('Warning: Jacobian Matrix is Non-Invertible')                                                                      

    elif event == 'Inverse of J':
           
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break

        IV = np.linalg.inv(JM1)
        #print("IV = ")
        #print(IV)
        sg.popup('IV = ',IV)

    elif event == 'Transpose of J':
          
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break
           
        TJ = np.transpose(JM1)
            #print("TJ = ")
            #print(TJ)

        sg.popup('TJ = ',TJ)
        
    elif event == 'Solve Inverse Kinematics' :
           Inverse_Kinematics_Window()
        
        
        
window.close()
