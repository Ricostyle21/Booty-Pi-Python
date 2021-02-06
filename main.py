#!/usr/bin/python3
import PySimpleGUIWeb as sg
import threading

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.10'
PORT = 8069


def turnon(selector):
    print(str(selector) + "'s power button pressed!")
    threading.Timer(0.2, print, [str(selector) + "'s power button released!"]).start()


def forceshutdown(selector):
    print(str(selector) + "'s power button pressed! FORCED")
    threading.Timer(5, print, [str(selector) + "'s power button released! FORCED"]).start()


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
          [sg.Text('Version: Print/Non-GPIO 0.95')],
          [sg.Text('By Céderic van Rossum for LVC')]]

if mode == 'TKT':
    window = sg.Window('Booty-Pi', layout)
else:
    window = sg.Window('Booty-Pi', layout, web_ip=IP, web_port=PORT, web_start_browser=False, disable_close=True)

while True:
    event, values = window.read()
    if event == '-QUIT-' or event == sg.WIN_CLOSED or event == 'None':
        # GPIO.cleanup()
        break
    if event is 'Turn on PC':
        if values['-PC01P-']:
            turnon('PC-01')
        if values['-PC02P-']:
            turnon('PC-02')
        if values['-PC03P-']:
            turnon('PC-03')
        if values['-PC04P-']:
            turnon('PC-04')
        if values['-PC05P-']:
            turnon('PC-05')
        if values['-PC06P-']:
            turnon('PC-06')
        if values['-PC07P-']:
            turnon('PC-07')
        if values['-PC08P-']:
            turnon('PC-08')
    if event is '-FORCESD-':
        if values['-PCDROP-'] != '':
            # if sg.popup_ok_cancel('Are you sure you want to FORCE SHUT-DOWN ' + values['-PCDROP-'] + '?') == 'OK':
            if confirmation_window(values['-PCDROP-']) == 'OK':
                if values['-PCDROP-'] == 'PC-01':
                    forceshutdown('PC-01')
                if values['-PCDROP-'] == 'PC-02':
                    forceshutdown('PC-02')
                if values['-PCDROP-'] == 'PC-03':
                    forceshutdown('PC-03')
                if values['-PCDROP-'] == 'PC-04':
                    forceshutdown('PC-04')
                if values['-PCDROP-'] == 'PC-05':
                    forceshutdown('PC-05')
                if values['-PCDROP-'] == 'PC-06':
                    forceshutdown('PC-06')
                if values['-PCDROP-'] == 'PC-07':
                    forceshutdown('PC-07')
                if values['-PCDROP-'] == 'PC-08':
                    forceshutdown('PC-08')

window.close()

# TODO turn into module for function use
# TODO remove quit button
# TODO add status indicators (maybe with pinging?)
