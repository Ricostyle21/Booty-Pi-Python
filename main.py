#!/usr/bin/python3
import PySimpleGUIWebAuth as sg
import threading

mode = 'WEB'  # WEB or TKT
IP = '192.168.178.10'
PORT = 8069
username = 'test'  # if you leave either one blank no authentication will be required
password = 'test'


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
          [sg.Text('Version: Print/Non-GPIO 1.00')],
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
                if values['-PCDROP-'] == 'Henk':
                    forceshutdown('Henk')
                if values['-PCDROP-'] == 'NDI Pro 1':
                    forceshutdown('NDI Pro 1')
                if values['-PCDROP-'] == 'NDI Pro 2':
                    forceshutdown('NDI Pro 1')
                if values['-PCDROP-'] == 'NDI Rec':
                    forceshutdown('NDI Rec')
                if values['-PCDROP-'] == 'Regie':
                    forceshutdown('Regie')
                if values['-PCDROP-'] == 'Storage':
                    forceshutdown('Storage')
                if values['-PCDROP-'] == 'Videoserver':
                    forceshutdown('Videoserver')
                if values['-PCDROP-'] == 'PC-08':
                    forceshutdown('PC-08')

window.close()

# TODO turn into module for function use
# TODO remove quit button (I moved it)
# TODO add status indicators (maybe with pinging?)
