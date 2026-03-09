import os
from datetime import datetime
from tempfile import TemporaryDirectory

import slicer
from slicer import vtkMRMLVolumeNode
from trame_server import Server
from undo_stack import Signal

from trame_slicer.core import SlicerApp
from trame_slicer.utils import write_client_files_to_dir

from ..ui import (
    LoadVolumeState,
    LoadVolumeUI,
)
from .base_logic import BaseLogic


class LoadVolumeLogic(BaseLogic[LoadVolumeState]):
    volume_loaded = Signal(vtkMRMLVolumeNode)

    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, LoadVolumeState)
        self.state.show_save_alert = False

    def set_ui(self, ui: LoadVolumeUI):
        ui.on_load_volume.connect(self._on_load_volume)
        ui.on_save_files.connect(self.save_files)

    def save_files(self):
        slicer.mrmlScene = self._slicer_app.scene
        
        folder_name = datetime.now().strftime("Arquivos_Salvos_%Y%m%d_%H%M%S")
        save_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(save_path, exist_ok=True)
        
        volumes = self._slicer_app.scene.GetNodesByClass("vtkMRMLScalarVolumeNode")
        for i in range(volumes.GetNumberOfItems()):
            node = volumes.GetItemAsObject(i)
            base_name = node.GetName().replace(".nrrd", "")
            file_path = os.path.join(save_path, f"{base_name}.nrrd")
            self._slicer_app.io_manager.write_node(
                node, file_path, slicer.vtkMRMLVolumeArchetypeStorageNode, False
            )
            
        segmentations = self._slicer_app.scene.GetNodesByClass("vtkMRMLSegmentationNode")
        for i in range(segmentations.GetNumberOfItems()):
            node = segmentations.GetItemAsObject(i)
            base_name = node.GetName().replace(".seg.nrrd", "").replace(".nrrd", "").replace(".seg", "")
            file_path = os.path.join(save_path, f"{base_name}.seg.nrrd")
            self._slicer_app.io_manager.write_node(
                node, file_path, slicer.vtkMRMLSegmentationStorageNode, False
            )
            
        self.state.show_save_alert = True

    def _on_load_volume(self, files: list[dict], is_loading_state_name: str) -> None:
        try:
            self._load_volume_files(files)
        finally:
            self.state[is_loading_state_name] = False

    def _load_volume_files(self, files: list[dict]) -> None:
        if not files:
            return

        self._slicer_app.scene.Clear()

        with TemporaryDirectory() as tmp_dir:
            loaded_files = write_client_files_to_dir(files, tmp_dir)
            if len(loaded_files) == 1 and loaded_files[0].endswith(".mrb"):
                self._on_load_scene(loaded_files[0])
            else:
                self._on_load_volume_files(loaded_files)

    def _on_load_scene(self, scene_file):
        self._slicer_app.io_manager.load_scene(scene_file)
        self._show_largest_volume(list(self._slicer_app.scene.GetNodesByClass("vtkMRMLVolumeNode")))

    def _on_load_volume_files(self, loaded_files):
        volumes = self._slicer_app.io_manager.load_volumes(loaded_files)
        if not volumes:
            return
        self._show_largest_volume(volumes)

    def _show_largest_volume(self, volumes):
        if not volumes:
            return

        def bounds_volume(v):
            b = [0] * 6
            v.GetImageData().GetBounds(b)
            return (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4])

        volumes = sorted(volumes, key=bounds_volume)
        volume_node = volumes[-1]

        self._slicer_app.display_manager.show_volume(
            volume_node,
            do_reset_views=True,
        )

        self.volume_loaded(volume_node)