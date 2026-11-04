"""Copy the lesson images (as JPG, for WhatsApp) and the Word lessons to the Desktop."""
import os
import shutil
import sys
from PIL import Image

src = sys.argv[1]  # folder holding Bridzs_2-1_Lecke_N.docx and Lapok_Lecke_N/
dst = os.path.join(os.path.expanduser("~"), "Desktop", "Bridzs lectii")
lessons = [int(n) for n in sys.argv[2:]] or [1, 2]

for n in lessons:
    friend = os.path.join(dst, f"Lectia {n}", "Pentru prieten")
    me = os.path.join(dst, f"Lectia {n}", "Pentru mine")
    os.makedirs(friend, exist_ok=True)
    os.makedirs(me, exist_ok=True)
    folder = os.path.join(src, f"Lapok_Lecke_{n}")
    for f in sorted(os.listdir(folder)):
        num = f.split("_")[1]
        target = friend if f.endswith("_barat.png") else me
        Image.open(os.path.join(folder, f)).convert("RGB").save(
            os.path.join(target, f"L{n} dona {num}.jpg"), quality=92)
    shutil.copy2(os.path.join(src, f"Bridzs_2-1_Lecke_{n}.docx"),
                 os.path.join(me, f"Lectia {n} - explicatii.docx"))
    print(f"Lectia {n}: copiata in {dst}")
