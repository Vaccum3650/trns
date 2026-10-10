
import open3d as o3d
from pathlib import Path

pasta = Path(__file__).resolve().parent
regioes = sorted((pasta / "regioes").glob("*.ply"))

if not regioes:
    raise ValueError("Não foram encontradas regiões.")

print("Regiões disponíveis:")
for i, ficheiro in enumerate(regioes):
    print(i, ficheiro.name)

numero = int(input("Número da região a visualizar: "))

if not 0 <= numero < len(regioes):
    raise ValueError("Número inválido.")

nuvem = o3d.io.read_point_cloud(str(regioes[numero]))

print("Pontos:", len(nuvem.points))

visualizador = o3d.visualization.Visualizer()
visualizador.create_window(
    window_name=regioes[numero].name,
    width=1280,
    height=800
)

visualizador.add_geometry(nuvem)

opcoes = visualizador.get_render_option()
opcoes.point_size = 2.0

visualizador.run()
visualizador.destroy_window()
