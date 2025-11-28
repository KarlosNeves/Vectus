# empresas_simuladas.py
import numpy as np
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Evita erro do tkinter no Windows/Python 3.13
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

def gerar_dados_empresas(n=100, seed=42):
    np.random.seed(seed)
    faturamento = np.random.uniform(100_000, 10_000_000, n)
    icms = faturamento * 0.18 + np.random.normal(0, 100_000, n)
    ir = faturamento * 0.15 + np.random.normal(0, 50_000, n)
    icms = np.clip(icms, 0, None)
    ir = np.clip(ir, 0, None)
    return faturamento, icms, ir

def salvar_dados_csv(faturamento, icms, ir, filepath='data/empresas_simuladas.csv'):
    df = pd.DataFrame({'faturamento': faturamento, 'icms': icms, 'ir': ir})
    df.to_csv(filepath, index=False)
    print(f"✅ Dados salvos em: {filepath}")

def plotar_grafico_3d_com_regressao(faturamento, icms, ir, save_path='plots/empresas_3d_regressao.png'):
    # Criar gráfico 3D
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plotar pontos
    scatter = ax.scatter(
        faturamento, icms, ir,
        c=ir, cmap='plasma', s=60, alpha=0.8, edgecolors='w', linewidth=0.3
    )
    
    # ⬇️ REGRESSÃO LINEAR 3D ⬇️
    X = np.column_stack([faturamento, icms])  # features
    y = ir                                     # target
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Gerar plano para visualização
    x_range = np.linspace(faturamento.min(), faturamento.max(), 20)
    y_range = np.linspace(icms.min(), icms.max(), 20)
    xx, yy = np.meshgrid(x_range, y_range)
    zz = model.predict(np.column_stack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    
    # Plotar plano de regressão (translúcido)
    ax.plot_surface(xx, yy, zz, alpha=0.25, color='red', edgecolor='none')
    
    # Labels e estilo
    ax.set_xlabel('Faturamento (R$)', fontsize=12)
    ax.set_ylabel('ICMS (R$)', fontsize=12)
    ax.set_zlabel('IR (R$)', fontsize=12)
    ax.set_title('100 Empresas Simuladas — 3D + Plano de Regressão', fontsize=14, fontweight='bold')
    
    plt.colorbar(scatter, ax=ax, shrink=0.6, pad=0.1, label='IR (R$)')
    ax.view_init(elev=15, azim=50)
    plt.tight_layout()
    
    # Salvar
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    print(f"✅ Gráfico com regressão salvo em: {save_path}")
    
    # Salvar previsões
    df_pred = pd.DataFrame({
        'faturamento': faturamento,
        'icms': icms,
        'ir_real': ir,
        'ir_previsto': model.predict(X),
        'residuo': ir - model.predict(X)
    })
    df_pred.to_csv('data/empresas_previsao.csv', index=False)
    print("✅ Previsões e resíduos salvos em: data/empresas_previsao.csv")
    
    # Mostrar coeficientes
    print("\n📊 Coeficientes da regressão:")
    print(f"   Faturamento: {model.coef_[0]:.6e}")
    print(f"   Intercepto:  {model.intercept_:.6e}")
    print(f"   R²:          {model.score(X, y):.4f}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print("🚀 Gerando dados de 100 empresas...")
    faturamento, icms, ir = gerar_dados_empresas(100)
    
    salvar_dados_csv(faturamento, icms, ir)
    plotar_grafico_3d_com_regressao(faturamento, icms, ir)