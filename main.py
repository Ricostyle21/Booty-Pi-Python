#!/usr/bin/python3
import os
import threading
from datetime import datetime

import PySimpleGUIWebAuth as sg

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.10'
PORT = 8069
username = 'test'  # if you leave either one blank no authentication will be required
password = 'test'

servers = {"Henk": "172.16.0.102",
           "NDI Pro 1": "192.168.178.120",
           "NDI Pro 2": "192.168.178.118",
           "NDI Rec": "192.168.178.11",
           "Regie": "172.16.0.10",
           "Storage": "172.16.0.4",
           "Videoserver": "172.16.0.100",
           "PC-08": ""
           }

buttons = {"Henk": "Henk",
           "NDI Pro 1": "NDI Pro 1",
           "NDI Pro 2": "NDI Pro 2",
           "NDI Rec": "NDI Rec",
           "Regie": "Regie",
           "Storage": "Storage",
           "Videoserver": "Videoserver",
           "PC-08": "PC-08"}


def turnon(selector):
    print(str(selector) + "'s power button pressed!")
    threading.Timer(0.2, print, [str(selector) + "'s power button released!"]).start()


def forceshutdown(selector):
    print(str(selector) + "'s power button pressed! FORCED")
    threading.Timer(5, print, [str(selector) + "'s power button released! FORCED"]).start()


def confirmation_window(pc_name):
    conflayout = [[sg.T('Are you sure you want to FORCE SHUT-DOWN'),
                   sg.T(pc_name, text_color='red', pad=(0, 3)), sg.T('?', pad=(0, 3))],
                  [sg.OK(button_color=('white', 'red')), sg.Cancel(button_color=('white', 'green'))]]

    confevent, confvalues = sg.Window('Are you sure?', conflayout).read(close=True)
    return confevent


def confirmation_quit():
    conflayout = [[sg.T('Are you sure you want to '),
                   sg.T('QUIT BOOTY-PYTHON', text_color='red', pad=(0, 3)), sg.T('?', pad=(0, 3))],
                  [sg.InputText(focus=True, default_text='Type LVC_YES to continue', key='-TEXT-')],
                  [sg.OK(button_color=('white', 'red')), sg.Cancel(button_color=('white', 'green'))]]

    confevent, confvalues = sg.Window('Are you sure?', conflayout).read(close=True)
    if confevent == 'OK' and confvalues['-TEXT-'] == 'LVC_YES':
        return confevent
    elif confevent == 'OK' and confvalues['-TEXT-'] != 'LVC_YES':
        sg.PopupError('Wrong terminate phrase, not quitting.')


sg.theme('Default1')

layout = [[sg.Text('Welcome to Booty-Python!')],
          [sg.Text('Running on port ' + str(PORT) + '@' + IP)],
          [sg.Text('Select the servers you want to turn on below:')],
          [sg.Checkbox(key='Henk', text='', size=(0, 0)), sg.Text('Henk', key='HenkStatus', text_color='red')],
          [sg.Checkbox(key='NDI Pro 1', text='', size=(0, 0)),
           sg.Text('NDI Pro 1', key='NDI Pro 1Status', text_color='red')],
          [sg.Checkbox(key='NDI Pro 2', text='', size=(0, 0)),
           sg.Text('NDI Pro 2', key='NDI Pro 2Status', text_color='red')],
          [sg.Checkbox(key='NDI Rec', text='', size=(0, 0)), sg.Text('NDI Rec', key='NDI RecStatus', text_color='red')],
          [sg.Checkbox(key='Regie', text='', size=(0, 0)), sg.Text('Regie', key='RegieStatus', text_color='red')],
          [sg.Checkbox(key='Storage', text='', size=(0, 0)), sg.Text('Storage', key='StorageStatus', text_color='red')],
          [sg.Checkbox(key='Videoserver', text='', size=(0, 0)),
           sg.Text('Videoserver', key='VideoserverStatus', text_color='red')],
          [sg.Checkbox(key='PC-08', text='', size=(0, 0)), sg.Text('PC-08', key='PC-08Status', text_color='red')],
          [sg.Button(button_text='Turn on Server'), sg.Button(button_text='Ping Servers'),
           sg.Text(key='-STATUSLINE-', text='', size=(33, 1), text_color='darkgreen')],
          [sg.T('(If the checkbox turned off the server has (probably) been turned on.)')],
          [sg.T()],
          [sg.Text('Select a server to force shut-down below:')],
          [sg.Text(' BE CAREFUL!', text_color='red')],
          [sg.Combo(['', 'Henk', 'NDI Pro 1', 'NDI Pro 2', 'NDI Rec', 'Regie', 'Storage', 'Videoserver', 'PC-08'],
                    default_value='', readonly=True, key='-PCDROP-'),
           sg.Button(button_text='Force Shut-down PC', button_color=('white', 'red'), key='-FORCESD-')],
          [sg.T()],
          [sg.Text('Version: Print/Non-GPIO 1.50')],
          [sg.Text('By Céderic van Rossum for LVC')],
          [sg.Button(button_text='Quit Booty-Python', key='-QUIT-')],
          [sg.Image(r'.\LVC.png', size=(150, 150))]]

if mode == 'TKT':  # if using PySimpleGUI(Qt) then don't use web_ip etc. params
    window = sg.Window('Booty-Pi', layout)
else:
    window = sg.Window('Booty-Pi', layout, web_ip=IP, web_port=PORT, web_start_browser=False, disable_close=True,
                       httpusername=username, httppassword=password)

while True:
    event, values = window.read()
    if event == '-QUIT-':
        if confirmation_quit() == 'OK':
            # GPIO.cleanup()
            break
    if event == sg.WIN_CLOSED or event == 'None':
        # GPIO.cleanup()
        break
    if event is 'Ping Servers':
        window['-STATUSLINE-'].update('Hold on tight, pinging servers...')
        for server in servers:
            if os.system('ping -n 1 "' + str(servers[server]) + '" > NUL') == 0:
                window[server + 'Status'].update(text_color='green')
                # print(server + " is on")
            else:
                window[server + 'Status'].update(text_color='red')
                # print(server + " is off")
        window['-STATUSLINE-'].update('Last pinged servers at ' + str(datetime.now().strftime('%H:%M:%S on %d-%m-%Y.')))
    if event is 'Turn on Server':
        for button in buttons:
            if values[button]:
                turnon(buttons[button])
            window[button].update(False)
    if event is '-FORCESD-':
        if values['-PCDROP-'] != '':
            # if sg.popup_ok_cancel('Are you sure you want to FORCE SHUT-DOWN ' + values['-PCDROP-'] + '?') == 'OK':
            if confirmation_window(values['-PCDROP-']) == 'OK':
                forceshutdown(values['-PCDROP-'])

window.close()

# TODO turn into module for function use
