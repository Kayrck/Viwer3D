import pydicom

def detect_dicom_phases(file_paths):
    """
    Recebe uma lista de caminhos de arquivos, analisa as tags SeriesDescription e ProtocolName 
    usando pydicom e retorna um dicionário mapeando SeriesInstanceUID para a fase detectada.
    """
    series_phase_map = {}
    
    # Palavras-chave comuns para identificar cada fase
    phase_keywords = {
        "arterial": ["arterial", "art", "aorta"],
        "venous": ["venous", "ven", "portal", "v.p"],
        "delayed": ["delayed", "del", "tardia", "tardio"],
        "pre contrast": ["pre", "non con", "unenhanced", "sem contraste", "nc"]
    }

    for file_path in file_paths:
        try:
            # Lê apenas os metadados
            dcm = pydicom.dcmread(file_path, stop_before_pixels=True)
            
            series_uid = getattr(dcm, 'SeriesInstanceUID', None)
            if not series_uid or series_uid in series_phase_map:
                continue  # Ignora se não tiver UID ou se a série já foi classificada
                
            description = getattr(dcm, 'SeriesDescription', '').lower()
            protocol = getattr(dcm, 'ProtocolName', '').lower()
            
            # Tenta detectar a fase baseada nas palavras-chave
            detected_phase = "unknown"
            for phase, keywords in phase_keywords.items():
                if any(kw in description or kw in protocol for kw in keywords):
                    detected_phase = phase
                    break
                    
            series_phase_map[series_uid] = {
                "phase": detected_phase,
                "description": getattr(dcm, 'SeriesDescription', 'Unknown')
            }
            
        except Exception:
            # Arquivo não é DICOM ou não pôde ser lido, ignora silenciosamente
            continue
            
    return series_phase_map