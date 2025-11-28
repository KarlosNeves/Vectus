import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
import os

print(f"🎯 TESTANDO NO PROJETO TRIBUTEC-AI")
print(f"📁 Pasta atual: {os.getcwd()}")

# 1. Testar pandas e numpy
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100)
})
print(f"✅ DataFrame criado: {df.shape}")

# 2. Testar scikit-learn
X, y = make_classification(n_samples=100, n_features=4, random_state=42)
print(f"✅ Dados ML criados: {X.shape}, {y.shape}")

# 3. Testar matplotlib e seaborn
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.scatter(df['x'], df['y'])
plt.title('Matplotlib - Projeto Tributec-AI')

plt.subplot(1, 2, 2)
sns.histplot(df['x'], kde=True)
plt.title('Seaborn - Projeto Tributec-AI')

plt.tight_layout()
plt.savefig('teste_tributec_ai.png')
print("✅ Gráficos salvos como 'teste_tributec_ai.png'")

print("🎉 AMBIENTE TRIBUTEC-AI PRONTO PARA DATA SCIENCE!")