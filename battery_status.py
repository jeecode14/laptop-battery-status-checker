import base64


import psutil
import time

# to create a GUI
# GUI Library
import PySimpleGUI as sg #! pip install pysimplegui
from plyer import notification

#for  multi-threading task
import threading


# define a lock to protect the global variable
lock = threading.Lock()


# GLOBAL VAR
thread_check_if_done = False
batt_full_in_percent = 0
batt_low_in_percent = 0

def call_pop(stat, message):
    
    try:
        if stat == "fullbat": 
            title = "BATTERY FULL" 
            icon = "image/batt_full.ico"
        else: 
            title = "BATTERY LOW" 
            icon = "image/batt_low.ico"

        notification.notify(
            title=title,
            message=message,
            app_name="Battery Auto-warning Apps",
            timeout=5, # Timeout in seconds,
            app_icon=icon
        )
    except Exception as e:
        sg.PopupNonBlocking("Error: {}".format(e))

def move_center(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

def get_battery():
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    if plugged==False:
        plugged="Not Plugged In"
    else:
        plugged="Plugged In"
    return percent, plugged


def battery_auto_warning():
    while True:
        percent, plugged = get_battery()
        percent = int(percent)
        #print("Full:", batt_full_in_percent, "Low:", batt_low_in_percent)
        #print("Battery Percentage:", percent)
        #print("Plugged In:", plugged)

        if percent >= batt_full_in_percent:
            if plugged == "Plugged In":
                #sg.popup_notify("Please unplug power adapter.")
                #sg.PopupNonBlocking("Please unplug power adapter.")
                call_pop("fullbat","Battery is {}%. Please unplug power adapter.".format(percent))
                

        if percent <= batt_low_in_percent:
            if plugged == "Not Plugged In":
                #sg.popup_notify("Please plug power adapter.")
                #sg.PopupNonBlocking("Please plug power adapter.")
                call_pop("lowbat","Battery is {}%. Please plug power adapter.".format(percent))
                
                

        time.sleep(30)

def main():
    global thread_check_if_done, batt_full_in_percent, batt_low_in_percent
    batt_full_list = ['100','95','90','85','80']
    batt_low_list = ['30','25','20','15','10']
    body = [
        [
            sg.Text("When Battery is full (%):\t"),
            sg.Combo(batt_full_list, default_value=batt_full_list[0], key='-BATTERY_FULL-',size = (10,8), readonly=True, enable_events=True),
            
        ],
        [
            sg.Text("When Battery is low (%):\t"),
            sg.Combo(batt_low_list, default_value=batt_low_list[2],key='-BATTERY_LOW-',size = (10,8), readonly=True, enable_events=True),
            
        ],
        [sg.Text("")],
        [sg.Button('Save settings',key='-SETTINGS-', size=(20, 2), disabled=True)],   
    ]
    layout = [
        [sg.T('Battery Auto-Warning Apps v.4.2023', font='_ 14', justification='c', expand_x=True)],
        [sg.Push(),sg.Image('./image/battery-auto-warning-logo.png'), sg.Push()],
        [sg.Frame(title='',layout=body, element_justification='left')],
        [sg.Text('\\nIf you liked this software, please support my youtube channel so that we can continue \
            \\nto make more FREE apps just like this one. Thank you so much!\
            \\n\\nYoutube: youtube.com/@jeecodetv \
            \\nFacebook: facebook.com/@jeecodeTV \
            \\nFor Business Inquiries: jeecode.itsolution@gmail.com \
            ')]
    ]


    window = sg.Window('Battery Auto-Warning Apps - Jeecode IT Solution', layout, element_justification='center', size = (700, 400), finalize=True )

    # move the window form at the center of the screen upon loaded
    move_center(window)

    
    while True:
        if thread_check_if_done is False:
            event, value = window.read(timeout=10)
            #window['-STATUS-'].update("")
        else:
            if thread_check_if_done:
                #window['-STATUS-'].update('Scan Complete!')
                

                # set to default "False"
                thread_check_if_done=False

            event, value = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if value['-BATTERY_FULL-'] and value['-BATTERY_LOW-']:
            window['-SETTINGS-'].update(disabled=False)
        
        if event == '-SETTINGS-':
            result = sg.popup_ok("Process begin. Running on the background. \
                                This window will hide automatically.\
                                If you want to disable this program later, just restart your computer.",title="Info")
            if result == "OK":
                batt_full_in_percent = int(value['-BATTERY_FULL-'])
                batt_low_in_percent = int(value['-BATTERY_LOW-'])
                long_operation_function1()
                window.hide()
            

            

    window.close()

def long_operation_function1():
    with lock:
        threading.Thread(target=battery_auto_warning, daemon=True).start()


if __name__ == "__main__" :
    main()
        


