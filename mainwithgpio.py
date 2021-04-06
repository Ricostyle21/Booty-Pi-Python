#!/usr/bin/python3
import RPi.GPIO as GPIO
import PySimpleGUIWebAuth as sg
import threading

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.106'
PORT = 8069
username = 'test'  # if you leave either one blank no authentication will be required
password = 'test'

r1 = 3
r2 = 5
r3 = 7
r4 = 11
r5 = 13
r6 = 15
r7 = 19
r8 = 21

GPIO.setmode(GPIO.BOARD)
GPIO.setup(r1, GPIO.OUT)
GPIO.setup(r2, GPIO.OUT)
GPIO.setup(r3, GPIO.OUT)
GPIO.setup(r4, GPIO.OUT)
GPIO.setup(r5, GPIO.OUT)
GPIO.setup(r6, GPIO.OUT)
GPIO.setup(r7, GPIO.OUT)
GPIO.setup(r8, GPIO.OUT)

GPIO.output(r1, GPIO.HIGH)  # this is vital, otherwise all of the pc's get booted when the script first starts running
GPIO.output(r2, GPIO.HIGH)
GPIO.output(r3, GPIO.HIGH)
GPIO.output(r4, GPIO.HIGH)
GPIO.output(r5, GPIO.HIGH)
GPIO.output(r6, GPIO.HIGH)
GPIO.output(r7, GPIO.HIGH)
GPIO.output(r8, GPIO.HIGH)


def turnon(selector):
    GPIO.output(selector, GPIO.LOW)
    threading.Timer(0.2, GPIO.output, [selector, GPIO.HIGH]).start()


def forceshutdown(selector):
    GPIO.output(selector, GPIO.LOW)
    threading.Timer(5, GPIO.output, [selector, GPIO.HIGH]).start()


def confirmation_window(pc_name):
    conflayout = [[sg.T('Are you sure you want to FORCE SHUT-DOWN'),
                   sg.T(pc_name, text_color='red', pad=(0, 3)), sg.T('?', pad=(0, 3))],
                  [sg.OK(button_color=('white', 'red')), sg.Cancel(button_color=('white', 'green'))]]

    confevent, confvalues = sg.Window('Are you sure?', conflayout).read(close=True)
    return confevent


sg.theme('Default1')

layout = [[sg.Text('Welcome to Booty-Python!')],
          [sg.Text('Running on port ' + str(PORT) + '@' + IP)],
          [sg.Text('Select the PC\'s you want to turn on below:')],
          [sg.Checkbox(key='-PC01P-', text='', size=(0, 0)), sg.Text('Henk')],
          [sg.Checkbox(key='-PC02P-', text='', size=(0, 0)), sg.Text('NDI Pro 1')],
          [sg.Checkbox(key='-PC03P-', text='', size=(0, 0)), sg.Text('NDI Pro 2')],
          [sg.Checkbox(key='-PC04P-', text='', size=(0, 0)), sg.Text('NDI Rec')],
          [sg.Checkbox(key='-PC05P-', text='', size=(0, 0)), sg.Text('Regie')],
          [sg.Checkbox(key='-PC06P-', text='', size=(0, 0)), sg.Text('Storage')],
          [sg.Checkbox(key='-PC07P-', text='', size=(0, 0)), sg.Text('Videoserver')],
          [sg.Checkbox(key='-PC08P-', text='', size=(0, 0)), sg.Text('PC-08')],
          [sg.Button(button_text='Turn on PC')],
          [sg.T()],
          [sg.Text('Select a PC to force shut-down below:')],
          [sg.Text(' BE CAREFUL!', text_color='red')],
          [sg.Combo(['', 'Henk', 'NDI Pro 1', 'NDI Pro 2', 'NDI Rec', 'Regie', 'Storage', 'Videoserver', 'PC-08'],
                    default_value='', readonly=True, key='-PCDROP-'),
           sg.Button(button_text='Force Shut-down PC', button_color=('white', 'red'), key='-FORCESD-')],
          [sg.T()],
          [sg.Text('Version: GPIO 0.99')],
          [sg.Text('By Céderic van Rossum for LVC')],
          [sg.Button(button_text='Quit Booty-Python', key='-QUIT-')]]

if mode == 'TKT':  # if using PySimpleGUI(Qt) then don't use web_ip etc. params
    window = sg.Window('Booty-Pi', layout)
else:
    window = sg.Window('Booty-Pi', layout, web_ip=IP, web_port=PORT, web_start_browser=False, disable_close=True,
                       httpusername=username, httppassword=password)

while True:
    event, values = window.read()
    if event == '-QUIT-' or event == sg.WIN_CLOSED or event == 'None':
        GPIO.cleanup()
        break
    if event is 'Turn on PC':
        if values['-PC01P-']:
            turnon(r1)
        if values['-PC02P-']:
            turnon(r2)
        if values['-PC03P-']:
            turnon(r3)
        if values['-PC04P-']:
            turnon(r4)
        if values['-PC05P-']:
            turnon(r5)
        if values['-PC06P-']:
            turnon(r6)
        if values['-PC07P-']:
            turnon(r7)
        if values['-PC08P-']:
            turnon(r8)
    if event is '-FORCESD-':
        if values['-PCDROP-'] != '':
            # if sg.popup_ok_cancel('Are you sure you want to FORCE SHUT-DOWN ' + values['-PCDROP-'] + '?') == 'OK':
            if confirmation_window(values['-PCDROP-']) == 'OK':
                if values['-PCDROP-'] == 'Henk':
                    forceshutdown(r1)
                if values['-PCDROP-'] == 'NDI Pro 1':
                    forceshutdown(r2)
                if values['-PCDROP-'] == 'NDI Pro 2':
                    forceshutdown(r3)
                if values['-PCDROP-'] == 'NDI Rec':
                    forceshutdown(r4)
                if values['-PCDROP-'] == 'Regie':
                    forceshutdown(r5)
                if values['-PCDROP-'] == 'Storage':
                    forceshutdown(r6)
                if values['-PCDROP-'] == 'Videoserver':
                    forceshutdown(r7)
                if values['-PCDROP-'] == 'PC-08':
                    forceshutdown(r8)

window.close()

# TODO turn into module for function use
# TODO remove quit button (I moved it)
# TODO add status indicators (maybe with pinging?)
