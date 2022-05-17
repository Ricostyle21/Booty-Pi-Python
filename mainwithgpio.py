#!/usr/bin/python3
import os
import threading
from datetime import datetime

import RPi.GPIO as GPIO

import PySimpleGUIWebAuth as sg

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.10'
PORT = 8069
username = 'test'  # if you leave either one blank no authentication will be required
password = 'test'

ipmi_host = 'xxIPxx'
ipmi_username = 'username'
ipmi_password = 'password'

r1 = 3  # these are all of the pins the relays are connected to
r2 = 5
r3 = 7
r4 = 8
r5 = 10
r6 = 11
r7 = 12
r8 = 13

servers = {"Henk": ["192.168.216.52", r6],
           "NDI Pro 1": ["192.168.216.54", r4],
           "NDI Pro 2": ["192.168.216.55", r3],
           "NDI Rec": ["192.168.216.53", r5],
           "Regie": ["192.168.216.51", r7],
           "Storage": ["192.168.216.57", r1],
           "Videoserver": ["192.168.216.56", r2],
           "Helyx": ["192.168.216.58", r8]
           }

GPIO.setmode(GPIO.BOARD)
for server in servers:
    GPIO.setup(servers[server][1], GPIO.OUT)
    GPIO.output(servers[server][1], GPIO.HIGH)  # this is vital, otherwise all of the pc's get booted when the script first starts running


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
          [sg.Checkbox(key='Helyx', text='', size=(0, 0)), sg.Text('Helyx', key='HelyxStatus', text_color='red')],
          [sg.Button(button_text='Turn on Server'), sg.Button(button_text='Ping Servers'),
           sg.Text(key='-STATUSLINE-', text='', size=(33, 1), text_color='darkgreen')],
          [sg.T('(If the checkbox turned off the server was (probably) turned on.)')],
          [sg.T()],
          [sg.Text('Select a server to force shut-down below:')],
          [sg.Text(' BE CAREFUL!', text_color='red')],
          [sg.Combo(['', 'Henk', 'NDI Pro 1', 'NDI Pro 2', 'NDI Rec', 'Regie', 'Storage', 'Videoserver', 'Helyx'],
                    default_value='', readonly=True, key='-PCDROP-'),
           sg.Button(button_text='Force Shut-down PC', button_color=('white', 'red'), key='-FORCESD-')],
          [sg.T()],
          [sg.Text('Version: GPIO 1.6')],
          [sg.Text('By Céderic van Rossum for LVC')],
          [sg.Button(button_text='Quit Booty-Python', key='-QUIT-')],
          [sg.Image(r'./LVC.png', size=(150, 150))]]

if mode == 'TKT':  # if using PySimpleGUI(Qt) then don't use web_ip etc. params
    window = sg.Window('Booty-Pi', layout)
else:
    window = sg.Window('Booty-Pi', layout, web_ip=IP, web_port=PORT, web_start_browser=False, disable_close=True,
                       httpusername=username, httppassword=password)

while True:
    event, values = window.read()

    if event == '-QUIT-':
        if confirmation_quit() == 'OK':
            GPIO.cleanup()
            break
    if event == sg.WIN_CLOSED or event == 'None':
        GPIO.cleanup()
        break

    if event is 'Ping Servers':
        window['-STATUSLINE-'].update('Hold on tight, pinging servers...')
        for server in servers:
            if os.system('ping -c 1 "' + str(servers[server][0]) + '" > /dev/null') == 0:
                window[server + 'Status'].update(text_color='green')
                # print(server + " is on")
            else:
                window[server + 'Status'].update(text_color='red')
                # print(server + " is off")
        window['-STATUSLINE-'].update('Last pinged servers at ' + str(datetime.now().strftime('%H:%M:%S on %d-%m-%Y.')))

    if event is 'Turn on Server':
        if values[server] == 'Helyx':
            os.system('ipmitool -I lanplus -H {} -U {} -P {} power on'.format(ipmi_host, ipmi_username, ipmi_password))
        else:
            for server in servers:
                if values[server]:
                    turnon(servers[server][1])
                window[server].update(False)
    if event is '-FORCESD-':
        if values['-PCDROP-'] != '':
            if confirmation_window(values['-PCDROP-']) == 'OK':
                if values['-PCDROP-'] == 'Helyx':
                    os.system('ipmitool -I lanplus -H {} -U {} -P {} power off'.format(ipmi_host, ipmi_username, ipmi_password))
                else:
                    forceshutdown(servers[values['-PCDROP-']][1])

window.close()

# TODO turn into module for function use
