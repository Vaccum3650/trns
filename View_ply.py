
import open3d as o3d
import numpy as np
from pathlib import Path

pasta = Path(__file__).resolve().parent
ficheiro = pasta / "20260923100429_Convert to PLY.ply"
saida = pasta / "regioes"
saida.mkdir(exist_ok=True)

print("A carregar o mapa...")
nuvem = o3d.io.read_point_cloud(str(ficheiro))
pontos = np.asarray(nuvem.points)

if len(pontos) == 0:
    raise ValueError("O ficheiro PLY está vazio.")

# Tamanho de cada região (em metros)
tamanho = 10.0

# Usar coordenadas XY para dividir o piso
origem = pontos.min(axis=0)[:2]
indices = np.floor(
    (pontos[:, :2] - origem) / tamanho
).astype(np.int32)

# Identificar regiões existentes
regioes, inverso = np.unique(
    indices,
    axis=0,
    return_inverse=True
)

print("Total de regiões:", len(regioes))

# Guardar os pontos originais de cada região
for i, regiao in enumerate(regioes):
    ids = np.where(inverso == i)[0]

    if len(ids) < 100:
        continue

    parte = nuvem.select_by_index(ids.tolist())

    nome = f"regiao_{regiao[0]}_{regiao[1]}.ply"
    caminho = saida / nome

    o3d.io.write_point_cloud(
        str(caminho),
        parte,
        write_ascii=False,
        compressed=False
    )

    print(nome, "-", len(ids), "pontos")

print("Terminado! As regiões estão na pasta 'regioes'.")
