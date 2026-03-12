import os
import asyncio
from datetime import datetime
from tempfile import TemporaryDirectory

import slicer
from slicer import vtkMRMLVolumeNode
from trame_server import Server
from undo_stack import Signal

from trame_slicer.core import SlicerApp
from trame_slicer.utils import write_client_files_to_dir
from trame_slicer.utils.dicom_phase_detector import detect_dicom_phases

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

    async def _on_load_volume(self, files: list[dict], is_loading_state_name: str) -> None:
        try:
            self.server.state.loading_active = True
            self.server.state.loading_fade_out = False
            self.server.state.loading_progress = 0
            self.server.state.loading_status = "Iniciando importação..."
            self.server.state.flush()
            await asyncio.sleep(0.1)
            
            await self._load_volume_files(files)
            
            self.server.state.loading_progress = 100
            self.server.state.loading_status = "Ambiente pronto"
            self.server.state.loading_fade_out = True
            self.server.state.flush()
            
            await asyncio.sleep(0.6)
            self.server.state.loading_active = False
            
        finally:
            self.state[is_loading_state_name] = False
            self.server.state.flush()

    async def _load_volume_files(self, files: list[dict]) -> None:
        if not files:
            return

        self._slicer_app.scene.Clear()
        
        self.server.state.loading_status = "Lendo arquivos DICOM..."
        self.server.state.loading_progress = 20
        self.server.state.flush()
        await asyncio.sleep(0.1)

        with TemporaryDirectory() as tmp_dir:
            loaded_files = write_client_files_to_dir(files, tmp_dir)
            
            self.server.state.loading_status = "Indexando volume médico..."
            self.server.state.loading_progress = 50
            self.server.state.flush()
            await asyncio.sleep(0.1)
            
            if len(loaded_files) == 1 and loaded_files[0].endswith(".mrb"):
                await self._on_load_scene(loaded_files[0])
            else:
                await self._on_load_volume_files(loaded_files)

    async def _on_load_scene(self, scene_file):
        self._slicer_app.io_manager.load_scene(scene_file)
        self._show_largest_volume(list(self._slicer_app.scene.GetNodesByClass("vtkMRMLVolumeNode")))

    async def _on_load_volume_files(self, loaded_files):
        self.server.state.loading_status = "Reconstruindo volume 3D..."
        self.server.state.loading_progress = 75
        self.server.state.flush()
        await asyncio.sleep(0.1)
        
        try:
            if len(loaded_files) == 1:
                success, node = slicer.util.loadVolume(loaded_files[0], returnNode=True)
                volumes = [node] if success else []
            else:
                volumes = self._slicer_app.io_manager.load_volumes(loaded_files)
                
            if not volumes or volumes[0] is None:
                self.server.state.loading_status = "Nenhum volume médico encontrado."
                return
        except Exception as e:
            print(f"Erro do Slicer ao ler volume: {e}")
            self.server.state.loading_status = "Erro: Formato não suportado ou corrompido."
            self.server.state.loading_progress = 100
            self.server.state.loading_fade_out = True
            self.server.state.flush()
            return
            
        try:
            fases_detectadas = detect_dicom_phases(loaded_files)
            self.server.state.dicom_series_phases = fases_detectadas
        except Exception as e:
            print(f"Erro ao detectar fases DICOM: {e}")
            
        self.server.state.loading_status = "Preparando renderização..."
        self.server.state.loading_progress = 90
        self.server.state.flush()
        await asyncio.sleep(0.1)
        
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