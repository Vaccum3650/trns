
import open3d as o3d
import numpy as np
from pathlib import Path
import time

# ==========================================
# CONFIGURAÇÕES
# ==========================================

PASTA = Path(__file__).resolve().parent

FICHEIRO = PASTA / "20260923100429_Convert to PLY.ply"

TAMANHO_PONTO = 5.0
LARGURA_JANELA = 1600
ALTURA_JANELA = 900

# ==========================================
# CARREGAR O MAPA ORIGINAL
# ==========================================

print("=" * 50)
print("HOSPITAL - MAPA COMPLETO")
print("=" * 50)

if not FICHEIRO.exists():
    raise FileNotFoundError(
        f"Ficheiro não encontrado: {FICHEIRO}"
    )

inicio = time.time()

print("\nA carregar TODOS os pontos...")
print("Aguarda. Pode demorar vários minutos.")

nuvem = o3d.io.read_point_cloud(str(FICHEIRO))

total_pontos = len(nuvem.points)

if total_pontos == 0:
    raise RuntimeError("A nuvem de pontos está vazia.")

print("\nMapa carregado!")
print(f"Total de pontos: {total_pontos:,}")
print(f"Cores RGB: {nuvem.has_colors()}")
print(f"Tempo: {time.time() - inicio:.2f} segundos")

# ==========================================
# VERIFICAR DIMENSÕES
# ==========================================

minimos = nuvem.get_min_bound()
maximos = nuvem.get_max_bound()

print("\nDimensões do mapa:")
print("X:", maximos[0] - minimos[0])
print("Y:", maximos[1] - minimos[1])
print("Z:", maximos[2] - minimos[2])

# ==========================================
# VISUALIZADOR
# ==========================================

print("\nA iniciar visualização completa...")

vis = o3d.visualization.Visualizer()

sucesso = vis.create_window(
    window_name="HOSPITAL - FULL RESOLUTION",
    width=LARGURA_JANELA,
    height=ALTURA_JANELA,
    visible=True
)

if not sucesso:
    raise RuntimeError(
        "Não foi possível criar a janela Open3D."
    )

# Adicionar TODOS os pontos
vis.add_geometry(nuvem)

# ==========================================
# CONFIGURAÇÕES VISUAIS
# ==========================================

opcoes = vis.get_render_option()

opcoes.point_size = TAMANHO_PONTO
opcoes.background_color = np.array([0.05, 0.05, 0.05])
opcoes.show_coordinate_frame = True

# Desativar iluminação artificial dos pontos
opcoes.light_on = False

print("\nVISUALIZADOR PRONTO")
print("Nenhum ponto foi removido.")
print("Nenhum voxel filtering foi aplicado.")
print(f"Pontos carregados: {total_pontos:,}")

# ==========================================
# EXECUTAR
# ==========================================

vis.run()

# Fechar corretamente
vis.destroy_window()

print("\nVisualizador terminado.")
