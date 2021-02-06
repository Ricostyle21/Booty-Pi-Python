#!/usr/bin/python3
import RPi.GPIO as GPIO
import PySimpleGUIWeb as sg
import threading

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.106'
PORT = 8069

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
    conflayout = [[sg.Text('Are you sure you want to FORCE SHUT-DOWN ' + pc_name + '?')],
                  [sg.OK(button_color=('white', 'red')), sg.Cancel(button_color=('white', 'green'))]]

    confevent, confvalues = sg.Window('Are you sure?', conflayout).read(close=True)
    return confevent


sg.theme('Default1')

layout = [[sg.Text('Welcome to Booty-Python!')],
          [sg.Text('Running on port ' + str(PORT) + '@' + IP)],
          [sg.Text('Select the PC\'s you want to turn on below:')],
          [sg.Checkbox(key='-PC01P-', text='PC-01')],
          [sg.Checkbox(key='-PC02P-', text='PC-02')],
          [sg.Checkbox(key='-PC03P-', text='PC-03')],
          [sg.Checkbox(key='-PC04P-', text='PC-04')],
          [sg.Checkbox(key='-PC05P-', text='PC-05')],
          [sg.Checkbox(key='-PC06P-', text='PC-06')],
          [sg.Checkbox(key='-PC07P-', text='PC-07')],
          [sg.Checkbox(key='-PC08P-', text='PC-08')],
          [sg.Button(button_text='Turn on PC'), sg.Button(button_text='Quit Booty-Python', key='-QUIT-')],
          [sg.T()],
          [sg.Text('Select a PC to force shut-down below:')],
          [sg.Text(' BE CAREFUL!', text_color='red')],
          [sg.Combo(['', 'PC-01', 'PC-02', 'PC-03', 'PC-04', 'PC-05', 'PC-06', 'PC-07', 'PC-08'],
                    default_value='', readonly=True, key='-PCDROP-'),
           sg.Button(button_text='Force Shut-down PC', button_color=('white', 'red'), key='-FORCESD-')],
          [sg.T()],
          [sg.Text('Version: GPIO 0.95')],
          [sg.Text('By Céderic van Rossum for LVC')]]

if mode == 'TKT':  # if using PySimpleGUI(Qt) then don't use web_ip etc. params
    window = sg.Window('Booty-Pi', layout)
else:
    window = sg.Window('Booty-Pi', layout, web_ip=IP, web_port=PORT, web_start_browser=False, disable_close=True)

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
                if values['-PCDROP-'] == 'PC-01':
                    forceshutdown(r1)
                if values['-PCDROP-'] == 'PC-02':
                    forceshutdown(r2)
                if values['-PCDROP-'] == 'PC-03':
                    forceshutdown(r3)
                if values['-PCDROP-'] == 'PC-04':
                    forceshutdown(r4)
                if values['-PCDROP-'] == 'PC-05':
                    forceshutdown(r5)
                if values['-PCDROP-'] == 'PC-06':
                    forceshutdown(r6)
                if values['-PCDROP-'] == 'PC-07':
                    forceshutdown(r7)
                if values['-PCDROP-'] == 'PC-08':
                    forceshutdown(r8)

window.close()

# TODO turn into module for function use
# TODO remove quit button
# TODO add status indicators (maybe with pinging?)
