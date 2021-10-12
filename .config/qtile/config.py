

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from widgets import custom_groups, covid

import os
import subprocess

mod = "mod4"
FONT = "Caskaydia Cove Nerd Font"


from key_config import keys


# Dracula Color Theme
# colors = [
#     ["#282a36", "#282a36"], # Background                [0]
#     ["#44475a", "#44475a"], # Current Line / Selection  [1]
#     ["#f8f8f2", "#f8f8f2"], # Foreground                [2]
#     ["#6272a4", "#6272a4"], # Comment                   [3]
#     ["#8be9fd", "#8be9fd"], # Cyan                      [4]
#     ["#50fa7b", "#50fa7b"], # Green                     [5]
#     ["#ffb86c", "#ffb86c"], # Orange                    [6]
#     ["#ff79c6", "#ff79c6"], # Pink                      [7]
#     ["#bd93f9", "#bd93f9"], # Purple                    [8]
#     ["#ff5555", "#ff5555"], # Red                       [9]
#     ["#f1fa8c", "#f1fa8c"], # Yellow                    [10]
# ]

colors = [
    ["#2e3440", "#2e3440"], # nord0
    ["#3b4252", "#3b4252"], # nord1
    ["#434c5e", "#434c5e"], # nord2
    ["#4c566a", "#4c566a"], # nord3
    ["#d8dee9", "#d8dee9"], # nord4
    ["#e5e9f0", "#e5e9f0"], # nord5
    ["#eceff4", "#eceff4"], # nord6
    ["#8fbcbb", "#8fbcbb"], # nord7
    ["#88c0d0", "#88c0d0"], # nord8
    ["#81a1c1", "#81a1c1"], # nord9
    ["#5e81ac", "#5e81ac"], # nord10
    ["#bf616a", "#bf616a"], # nord11
    ["#d08770", "#d08770"], # nord12
    ["#ebcb8b", "#ebcb8b"], # nord13
    ["#a3be8c", "#a3be8c"], # nord14
    ["#b48ead", "#b48ead"], # nord15
]


# group_names = [
#     # SYS
#     (" \uf120  ", {"layout": "columns"}),

#     # DEV
#     (" \uf121  ", {"layout": "columns"}),

#     # WEB
#     (" \uf268  ", {"layout": "columns"}),

#     # CHAT
#     (" \uf086  ", {"layout": "columns"}),

#     # HOME
#     (" \uf015  ", {"layout": "columns"}),

#     # GAME
#     (" \uf11b  ", {"layout": "columns"}),

#     # EXTRA
#     (" \uf249  ", {"layout": "columns"})
# ]

solar_system_groups = [
    ("Mercury", {"layout": "columns"}),
    ("Venus", {"layout": "columns"}),
    ("Earth", {"layout": "columns"}),
    ("Mars", {"layout": "columns"}),
    ("Jupiter", {"layout": "columns"}),
    ("Saturn", {"layout": "columns"}),
    ("Uranus", {"layout": "columns"}),
    ("Neptune", {"layout": "columns"}),
]


groups = [
    Group(config[0], **config[1]) for config in solar_system_groups
]


for i, group in enumerate(groups, 1):
    keys.extend([
        # Key to switch to group
        Key(
            [mod], 
            str(i), 
            lazy.group[group.name].toscreen(), 
            desc=f"Switch to group {group.name}" 
        ),

        # Key to move a focused window to a group (but no follow)
        Key( 
            [mod, "shift"], 
            str(i), 
            lazy.window.togroup(group.name), 
            desc=f"move focused window to group {group.name}"
        ) 
   ])


layout_theme = {
    "border_width": 4,
    "margin": [10, 4, 10, 4],
    "margin_on_single": [10, 8, 10, 8],
    "border_focus": colors[8][0],
    "border_normal": colors[0][0]
}


layouts = [
    layout.Columns(**layout_theme, insert_position=1),
    layout.MonadTall(**layout_theme),
    layout.Max(),
    
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


BACKGROUND = colors[1]

widget_defaults = dict(
    font=FONT,
    fontsize=12,
    padding=5,
    background=BACKGROUND
)


extension_defaults = widget_defaults.copy()

# - Mouse Callbacks - #

def power_options():
    """
    Lock the computer using betterlockscreen
    """
    qtile.cmd_spawn("bash /home/marco/.config/scripts/power_options.sh")


PROGRAMS = {
    "visual studio code": "\ue70c  Visual Studio Code",
    "google chrome": "\uf268  Google Chrome",
    "alacritty": "\uf120  Terminal",
    "slack": "\uf198  Slack",
    "obsidian": "\uf249  Obsidian"
}

def window_name(text):
    for k in PROGRAMS.keys():
        if k in text.lower():
            return PROGRAMS[k]

    return f"\uf824  {text}"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle_flipped.png",
                    length=15,
                ),
                
                widget.TextBox(
                    text="\uf185 ",
                    foreground=colors[13],
                    background=BACKGROUND,
                    padding=1,
                    fontsize=22
                ),

                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=BACKGROUND
                ),

                custom_groups.SolarGroups(
                    margin_x=0,
                    spacing=0,
                    margin_y=4,
                    padding_y=0
                ),

                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle.png",
                    margin_x=-1,
                    length=15
                ),

                widget.Spacer(
                    background=None
                ),

                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle_flipped.png",
                    length=15,
                ),

                widget.WindowName(
                    background=BACKGROUND,
                    foreground=colors[4],
                    width=bar.CALCULATED,
                    parse_text=window_name,
                    empty_group_string="No Window"
                ),

                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle.png",
                    margin_x=-1,
                    length=15
                ),

                widget.Spacer(
                    background=None
                ),

                # System Tray

                widget.Systray(
                    background=None
                ),

                widget.Sep(
                    linewidth=0,
                    padding=12,
                    background=None
                ),

                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle_flipped.png",
                    length=15
                ),

                # COVID WIDGET

                covid.CovidCaseCount(
                    state="Massachusetts",
                    ignore_weekend=True,
                    update_interval=21600,
                    fontsize=14,
                    increasing_case_colour=colors[11],
                    decreasing_case_colour=colors[14]
                ),

                widget.TextBox(
                    text="|",
                    foreground=colors[4],
                    background=BACKGROUND,
                    padding=8,
                    fontsize=10
                ),

                # CPU WIDGET

                widget.TextBox(
                    text="\uf109",
                    font=FONT,
                    fontsize=14,
                    foreground=colors[12],
                    padding=6
                ),

                widget.Sep(
                    linewidth=0, 
                    padding=4, 
                    background=BACKGROUND
                ),

                widget.CPU(
                    background=BACKGROUND,
                    foreground=colors[12],
                    font=FONT,
                    fontsize=14,
                    format='{load_percent}%',
                    update_interval=10.0
                ),

                widget.TextBox(
                    text="|",
                    foreground=colors[4],
                    background=BACKGROUND,
                    padding=8,
                    fontsize=10
                ),

                # Volume Widget                

                widget.TextBox(
                    text="\ufa7d",
                    font=FONT,
                    fontsize=14,
                    foreground=colors[13],
                    padding=4
                ),

                widget.Sep(
                    linewidth=0, 
                    padding=4, 
                    background=BACKGROUND
                ),

                widget.PulseVolume(
                    font=FONT,
                    fontsize=14,
                    foreground=colors[13],
                    update_interval=0.2
                ),

                widget.TextBox(
                    text="|",
                    foreground=colors[4],
                    background=BACKGROUND,
                    padding=8,
                    fontsize=10
                ),

                # Clock Widget

                widget.Clock(
                    foreground=colors[4],
                    background=BACKGROUND,
                    format="%A %B %d %H:%M",
                    padding=0
                ),

                widget.Sep(
                    linewidth=0,
                    padding=6,
                    background=BACKGROUND
                ),

                # Exit Widget

                widget.TextBox(
                    text="\uf438",
                    background=BACKGROUND,
                    foreground=colors[11],
                    padding=-5,
                    fontsize=44
                ),

                widget.TextBox(
                    text=" \uf705 ",
                    background=colors[11],
                    foreground=colors[4],
                    font=FONT,
                    fontsize=18,
                    padding=-4,
                    mouse_callbacks={
                        "Button1": power_options
                    }
                ),

                widget.Image(
                    background=None,
                    filename="~/.config/qtile/images/semicircle_red.png",
                    margin_x=-1,
                    length=15
                ),
            ],
            32,
            opacity=1,
            margin=[8,5,0,5],
            background="#00000000"
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag(
        [mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# -- HOOKS -- #

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# Now sure what this is below

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
