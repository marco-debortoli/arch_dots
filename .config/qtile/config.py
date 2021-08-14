

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import os
import subprocess

mod = "mod4"
FONT = 'Caskaydia Cove Nerd Font'


from key_config import keys


# Dracula Color Theme
colors = [
    ["#282a36", "#282a36"], # Background                [0]
    ["#44475a", "#44475a"], # Current Line / Selection  [1]
    ["#f8f8f2", "#f8f8f2"], # Foreground                [2]
    ["#6272a4", "#6272a4"], # Comment                   [3]
    ["#8be9fd", "#8be9fd"], # Cyan                      [4]
    ["#50fa7b", "#50fa7b"], # Green                     [5]
    ["#ffb86c", "#ffb86c"], # Orange                    [6]
    ["#ff79c6", "#ff79c6"], # Pink                      [7]
    ["#bd93f9", "#bd93f9"], # Purple                    [8]
    ["#ff5555", "#ff5555"], # Red                       [9]
    ["#f1fa8c", "#f1fa8c"], # Yellow                    [10]
]



group_names = [
    ( 
        "   ", # SYS
        {
            "layout": "columns"
        }
    ),

    (
        "   ", # DEV
        {
            "layout": "max"
        }
    ),

    (
        "   ", # WEB
        {
            "layout": "columns"
        }
    ),

    (
        "   ", # CHAT
        {
            "layout": "columns"
        }
    ),

    (
        "   ", # HOME
        {
            "layout": "columns"
        }
    ),

    (
        "   ", # GAME
        {
            "layout": "columns"
        }
    ),

    (
        "   ", # EXTRA
        {
            "layout": "columns"
        }
    )
]

groups = [ Group( config[ 0 ], **config[ 1 ] ) for config in group_names ]

for i, group in enumerate( groups, 1 ):
    keys.extend([
        # Key to switch to group
        Key(
            [ mod ], 
            str( i ), 
            lazy.group[ group.name ].toscreen(), 
            desc = f"Switch to group {group.name}" 
        ),

        # Key to move a focused window to a group (but no follow)
        Key( 
            [ mod, "shift" ], 
            str( i ), 
            lazy.window.togroup( group.name ), 
            desc = f"move focused window to group {group.name}"
        ) 
   ])


layout_theme = {
    "border_width": 2,
    "margin": 6,
    "border_focus": colors[ 8 ][ 0 ],
    "border_normal": colors[ 0 ][ 0 ]
}

layouts = [
    layout.Columns( **layout_theme ),
    layout.MonadTall( **layout_theme ),
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

widget_defaults = dict(
    font = FONT,
    fontsize = 12,
    padding = 5,
    background = colors[ 0 ]
)

extension_defaults = widget_defaults.copy()

# - Mouse Callbacks - #

def power_options():
    """
    Lock the computer using betterlockscreen
    """

    qtile.cmd_spawn( "bash /home/marco/.config/scripts/power_options.sh" )


def sleep_action():
    """
    Suspend the computer
    """

    qtile.cmd_spawn( "systemctl suspend" )


def shutdown_action():
    """
    Shutdown the computer
    """

    qtile.cmd_spawn( "shutdown now" )


screens = [
    Screen(
        top = bar.Bar(
            [
                widget.GroupBox(
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[ 8 ],
                    inactive = colors[ 2 ],
                    rounded = False,
                    highlight_color = colors[ 1 ],
                    highlight_method = "line",
                    this_current_screen_border = colors[ 8 ],
                    this_screen_border = colors[ 8 ],
                    foreground = colors[ 0 ],
                    background = colors[ 0 ],
                    fontsize = 14,
                    disable_drag = True
                ),

                widget.Sep(
                    linewidth = 0, padding = 24, background = colors[ 0 ]
                ),

                widget.WindowName(
                    background = colors[ 0 ], foreground = colors[ 8 ] 
                ),


                widget.Systray(
                    background = colors[ 0 ]
                ),

                widget.Sep(
                    linewidth = 0, padding = 12, background = colors[ 0 ]
                ),

                widget.Net(
                    update_interval = 5,
                    background = colors[ 1 ],
                    foreground = colors[ 2 ]
                ),

                widget.Sep(
                    linewidth = 0, padding = 6, background = colors[ 0 ]
                ),

                widget.Clock(
                    foreground = colors[ 2 ],
                    format = "%A %B %d %H:%M:%S",
                    padding = 8
                ),

                widget.Sep(
                    linewidth = 0, padding = 6, background = colors[ 0 ]
                ),

                widget.Sep(
                    linewidth = 0, padding = 6, background = colors[ 1 ]
                ),

                widget.TextBox(
                    text = " \uf011 ",
                    background = colors[ 1 ],
                    foreground = colors[ 2 ],
                    font = FONT,
                    fontsize = 14,
                    padding = 0,
                    mouse_callbacks = {
                        "Button1": power_options
                    }
                ),

                widget.Sep(
                    linewidth = 0, padding = 10, background = colors[ 1 ]
                ),


            ],
            26,
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
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
