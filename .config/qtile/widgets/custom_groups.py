from libqtile.widget.groupbox import _GroupBase, base
from libqtile.log_utils import logger


class SolarGroups(_GroupBase):
    """
    This is my own custom GroupBox widget that I am using to render the solar
    system workspace selector. Unfortunately the GroupBox standard widget
    did not offer the capability to change the label when active

    This is not meant to be generic - but to be used for my exact use case
    at the moment.
    """
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        (
            "visible_groups",
            None,
            "Groups that will be visible. "
            "If set to None or [], all groups will be visible."
            "Visible groups are identified by name not by their displayed label."
        ),
        (
            "spacing",
            None,
            "Spacing between groups"
            "(if set to None, will be equal to margin_x)"
        )
    ]

    COLORS = {
        "mercury": "#d8dee9",
        "venus": "#eed053",
        "earth": "#a3be8c",
        "mars": "#ad6242",
        "jupiter": "#b07f35",
        "saturn": "#fae5bf",
        "uranus": "#ace5ee",
        "neptune": "#366896"
    }

    DEFAULT_COLOR = "#eceff4"

    BOX_WIDTH = 30

    def __init__(self, **config):
        _GroupBase.__init__(self, **config)
        self.add_defaults(SolarGroups.defaults)

        if self.spacing is None:
            self.spacing = self.margin_x
        
        self.clicked = None
        self.click = None
        self.disable_drag = True
        self.hide_unused = False
        self.visible_groups = None
        self.fontsize = 14
       
        self.add_callbacks({'Button1': self.select_group})

    @property
    def groups(self):
        """
        returns list of visible groups.
        The existing groups are filtered by the visible_groups attribute and
        their label. Groups with an empty string as label are never contained.
        Groups that are not named in visible_groups are not returned.
        """
        if self.hide_unused:
            if self.visible_groups:
                return [
                    g for g in self.qtile.groups
                    if g.label and (g.windows or g.screen) and
                    g.name in self.visible_groups
                ]
            else:
                return [
                    g for g in self.qtile.groups if g.label and
                    (g.windows or g.screen)
                ]
        else:
            if self.visible_groups:
                return [
                    g for g in self.qtile.groups
                    if g.label and g.name in self.visible_groups
                ]
            else:
                return [g for g in self.qtile.groups if g.label]

    def get_clicked_group(self):
        return self.groups[self.click // self.BOX_WIDTH]

    def button_press(self, x, y, button):
        self.click = x
        _GroupBase.button_press(self, x, y, button)

    def select_group(self):
        self.clicked = None
        group = self.get_clicked_group()

        if not self.disable_drag:
            self.clicked = group

        self.go_to_group(group)

    def go_to_group(self, group):
        if group:
            self.bar.screen.set_group(group, warp=False)

    def button_release(self, x, y, button):
        self.click = x
        if button not in (5, 4):
            group = self.get_clicked_group()
            if group and self.clicked:
                group.cmd_switch_groups(self.clicked.name)
                self.clicked = None

    def calculate_length(self):
        return self.BOX_WIDTH * len(self.groups) + 5

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)
        offset = 0

        for i, g in enumerate(self.groups):
            if g.windows:
                text_color = self.COLORS[g.name.lower()]
                label = "\uf111"
            else:
                label = "\uf10c"
                text_color = self.DEFAULT_COLOR

            if self.bar.screen.group.name == g.name and self.qtile.current_screen == g.screen:
                label = "\uf135"

            self.drawbox(
                offset,
                label,
                None,
                text_color,
                highlight_color=None,
                width=self.BOX_WIDTH,
                rounded=False,
                block=False,
                line=False,
                highlighted=False
            )
            offset += self.BOX_WIDTH
        
        self.drawer.draw(offsetx=self.offset, width=self.width)