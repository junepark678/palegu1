import urwid
import os

choices = u'Restore-RootFS Semi-Tethered Tweaks Start Quit Checkra1n'.split()


edit = urwid.Edit("", edit_text="", multiline=False, align="left", wrap="space", allow_tab=False)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    body.append(urwid.Divider())
    body.append(urwid.Text("Version: (None if starting in normal mode)"))
    body.append(edit)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

semistatus = False
tweakstatus = False
checkra1n = False

def exit_program(button):
    raise urwid.ExitMainLoop()

def invoke_pale(button):
    global semistatus, tweakstatus



    try:
        os.remove(".torun")
    except:
        pass
    if checkra1n:
        with open(".torun", "x") as file:
            file.writelines("/bin/sh " + os.getcwd() + "/checkra1n/palera1n.sh" + " " + edit.get_edit_text())
        exit_program(button)
    with open(".torun", "x") as file:
        file.writelines("/bin/sh " + os.getcwd() + "/palera1n/palera1n.sh" + (" --semi-tethered" if semistatus else "") + (" --tweaks" if tweakstatus else "") + " " + edit.get_edit_text())
    exit_program(button)

def restore_pale(button):
    try:
        os.remove(".torun")
    except:
        pass
    with open(".torun", "x") as file:
        file.writelines("/bin/sh " + os.getcwd() + "/palera1n/palera1n.sh" + " --restorerootfs " + edit.get_edit_text())
    exit_program(button)


original_wid = None

def go_back(button):
    main.original_widget = original_wid

def item_chosen(button, choice):
    global original_wid, semistatus, tweakstatus, checkra1n
    if choice == "Quit":
        try:
            os.remove(".torun")
        except:
            pass
        exit_program(button)
    if choice == "Semi-Tethered":
        semistatus = not semistatus
        response = urwid.Text(["You selected Semi-Tethered and it is now set to ", str(semistatus)])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', go_back)
        original_wid = main.original_widget
        main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    if choice == "Tweaks":
        tweakstatus = not tweakstatus
        response = urwid.Text(["You selected Tweaks and it is now set to ", str(tweakstatus)])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', go_back)
        original_wid = main.original_widget
        main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))

    if choice == "Restore-RootFS":
        restore_pale(button)

    if choice == "Start":
        invoke_pale(button)
    
    if choice == "Checkra1n":
        checkra1n = not checkra1n
        response = urwid.Text(["You selected Checkra1n and it is now set to ", str(checkra1n)])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', go_back)
        original_wid = main.original_widget
        main.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(done, None, focus_map='reversed')]))
        




main = urwid.Padding(menu(u'Palera1n', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()