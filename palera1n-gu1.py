import urwid
import os

choices = u'Semi-Tethered Tweaks Start Quit'.split()

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

semistatus = False
tweakstatus = False


def exit_program(button):
    raise urwid.ExitMainLoop()

def invoke_pale(button):
    global semistatus, tweakstatus
    try:
        os.remove(".torun")
    except:
        pass
    with open(".torun", "x") as file:
        file.writelines("/bin/sh " + os.getcwd() + "/palera1n/palera1n.sh" + (" --semi-tethered" if semistatus else "") + (" --tweaks" if tweakstatus else ""))
    exit_program(button)

original_wid = None

def go_back(button):
    main.original_widget = original_wid

def item_chosen(button, choice):
    global original_wid, semistatus, tweakstatus
    if choice == "Quit":
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

    if choice == "Start":
        invoke_pale(button)
        




main = urwid.Padding(menu(u'Palera1n', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()