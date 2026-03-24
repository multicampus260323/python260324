import os
import shutil
from pathlib import Path

def move_download_files():
    download_dir = Path(r"C:\Users\student\Downloads")

    targets = {
        "images": [".jpg", ".jpeg"],
        "data": [".csv", ".xlsx"],
        "docs": [".txt", ".doc", ".pdf"],
        "archive": [".zip"],
    }

    # 이동 디렉터리 미리 만듦
    for subdir in targets.keys():
        target_dir = download_dir / subdir
        target_dir.mkdir(parents=True, exist_ok=True)

    # 다운로드 폴더 파일 순회
    for item in download_dir.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            moved = False
            for subdir, ext_list in targets.items():
                if ext in ext_list:
                    dest = download_dir / subdir / item.name
                    # 이름 중복 시 덮어쓰기 또는 새 이름 지정
                    if dest.exists():
                        # 원하는 동작에 따라 수정 가능(덮어쓰기, 건너뛰기 등)
                        dest.unlink()
                    shutil.move(str(item), str(dest))
                    moved = True
                    break
            # 확장자 매칭 안 되면 그냥 놔둠
            if not moved:
                continue

if __name__ == "__main__":
    move_download_files()
    print("이동 완료")
