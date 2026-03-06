from dataclasses import dataclass

from trame.ui.vuetify3 import VAppLayout
from trame.widgets.vuetify3 import (
    VAppBar,
    VBtn,
    VDivider,
    VFooter,
    VIcon,
    VMain,
    VNavigationDrawer,
    VProgressCircular,
    VSpacer,
    VToolbarTitle,
)
from trame_server import Server
from trame_server.utils.typed_state import TypedState

from .flex_container import FlexContainer


@dataclass
class ViewerLayoutState:
    is_drawer_visible: bool = False
    active_tool: str | None = None
    is_volume_loaded: bool = False


class ViewerLayout(VAppLayout):
    def __init__(
        self,
        server: Server,
        template_name="main",
        title: str = "Cirurgic3D", 
        theme: str = "dark",
        is_drawer_visible: bool = False,
    ):
        super().__init__(server, template_name=template_name)
        self.typed_state = TypedState(self.state, ViewerLayoutState)

        self.root.theme = theme

        with self:
            with VAppBar(color="#192E41", elevation=2) as self.appbar:
                self.title = VToolbarTitle(title, classes="font-weight-bold")

            with VFooter(app=True, classes="my-0 py-0", border=True, color="#000000") as self.footer:
                VProgressCircular(
                    indeterminate=("!!trame__busy",),
                    color="#7FF9C6", 
                    size=16,
                    width=3,
                    classes="ml-n3 mr-1",
                )
                self.footer.add_child(
                    '<span class="text-grey-lighten-1 text-caption">Desenvolvido por Cirurgic3D</span>'
                )
                VSpacer()
                
                reload = self.server.controller.on_server_reload
                if reload.exists():
                    with VBtn(
                        size="x-small",
                        density="compact",
                        icon=True,
                        elevation=0,
                        click=self.on_server_reload,
                        classes="mx-2",
                        color="#126D83", 
                    ):
                        VIcon("mdi-autorenew", size="small", color="#7FF9C6")

                self.footer.add_child(
                    f'<span class="text-grey-lighten-1 text-caption">© 2026 Cirurgic3D</span>'
                )

            with VMain():
                self.content = FlexContainer(row=True, fill_height=True)

            self.drawer = VNavigationDrawer(
                disable_resize_watcher=True,
                disable_route_watcher=True,
                permanent=True,
                location="left",
                v_model=(self.typed_state.name.is_drawer_visible, is_drawer_visible),
                width=350,
                color="#000000", 
            )

            with (
                VNavigationDrawer(
                    disable_resize_watcher=True,
                    disable_route_watcher=True,
                    permanent=True,
                    width=40,
                    location="left",
                    color="#192E41",
                ),
                FlexContainer(fill_height=True),
            ):
                self.toolbar = FlexContainer(classes="py-2", align="center")
                VDivider(color="#1EB3B2") 
                VSpacer()
                VDivider(color="#1EB3B2")
                self.undo_redo = FlexContainer(classes="py-2", align="center")