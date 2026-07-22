from pathlib import Path
def save_upload(file):
    if not file or not file.filename: return {'error':'No file provided'}
    folder=Path('uploads/temp'); folder.mkdir(parents=True,exist_ok=True)
    path=folder / Path(file.filename).name; file.save(path)
    return {'filename':path.name,'path':str(path)}
