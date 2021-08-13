

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import os
import subprocess

mod = "mod4"
terminal = "alacritty"

keys = [
	# Switch between windows
	Key(
		[ mod ], "h", 
		lazy.layout.left(), 
		desc = "Move focus to left"
	),

	Key(
		[ mod ], "l", 
		lazy.layout.right(), 
		desc = "Move focus to right" 
	),
	
	Key(
		[ mod ], "j", 
		lazy.layout.down(), 
		desc = "Move focus down" 
	),

	Key(
		[ mod ], "k", 
		lazy.layout.up(), 
		desc = "Move focus up"
	),

	Key(
		[ mod ], "space", 
		lazy.layout.next(),
		desc = "Move window focus to other window"
	),

	# Move windows between left/right columns or move up/down in current stack.
	# Moving out of range in Columns layout will create new column.
	Key( 
		[ mod, "shift" ], "h", 
		lazy.layout.shuffle_left(),
		desc = "Move window to the left" 
	),

	Key( 
		[ mod, "shift" ], "l", 
		lazy.layout.shuffle_right(),
		desc = "Move window to the right"
	),

	Key(
		[ mod, "shift" ], "j", 
		lazy.layout.shuffle_down(),
		desc = "Move window down"
	),

	Key(
		[ mod, "shift" ], "k", 
		lazy.layout.shuffle_up(), 
		desc = "Move window up"
	),

	# Grow windows. If current window is on the edge of screen and direction
	# will be to screen edge - window would shrink.
	Key(
		[ mod, "control" ], "h", 
		lazy.layout.grow_left(),
		desc = "Grow window to the left"
	),

	Key(
		[ mod, "control" ], "l", 
		lazy.layout.grow_right(),
		desc = "Grow window to the right"
	),
	
	Key(
		[ mod, "control" ], "j", 
		lazy.layout.grow_down(),
		desc = "Grow window down"
	),
	
	Key(
		[ mod, "control" ], "k", 
		lazy.layout.grow_up(), 
		desc = "Grow window up"
	),

	Key(
		[ mod ], "n", 
		lazy.layout.normalize(), 
		desc = "Reset all window sizes"
	),

	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	Key(
		[ mod, "shift" ], "Return", 
		lazy.layout.toggle_split(),
		desc = "Toggle between split and unsplit sides of stack"
	),

	Key(
		[ mod ], "Return", 
		lazy.spawn( terminal ), 
		desc = "Launch terminal"
	),

	# Toggle between different layouts as defined below
	Key(
		[ mod ], "Tab", 
		lazy.next_layout(), 
		desc = "Toggle between layouts"
	),

	Key(
		[ mod ], "w", 
		lazy.window.kill(), 
		desc = "Kill focused window"
	),

	Key(
		[ mod, "control" ], "r", 
		lazy.restart(), 
		desc = "Restart Qtile"
	),

	Key(
		[ mod, "control" ], "q", 
		lazy.shutdown(), 
		desc = "Shutdown Qtile"
	),

	# Controls for launching applications

	Key(
		[ mod ], "r", 
		lazy.spawncmd(),
		desc = "Spawn a command using a prompt widget"
	),

	Key(
		[ mod ], "space", 
		lazy.spawn( "rofi -show drun" ),
		desc = "Rofi spawn window"
	),

	Key(
		[ mod, "shift" ], "space",
		lazy.spawn( "rofi -show run" ),
		desc = "Rofi show running windows"
	)



]


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
	font = 'Caskaydia Cove Nerd Font',
	fontsize = 12,
	padding = 5,
	background = colors[ 0 ]
)

extension_defaults = widget_defaults.copy()

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

				widget.Prompt(
					background = colors[ 1 ],
					foreground = colors[ 6 ]
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
					linewidth = 0, padding = 12, background = colors[ 0 ]
				),

				widget.LaunchBar(
					progs = [
						( "lock-solid", "betterlockscreen -l dim", "Lock" )
					],
					padding = 3
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
