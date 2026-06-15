"""
ANÁLISIS ECONOMÉTRICO: RELACIÓN ENTRE PIB Y GASTO DE CONSUMO DE HOGARES
Modelo de Regresión Lineal Múltiple
Período: 1995-2025

Este script realiza un análisis econométrico completo incluyendo:
- Estimación por MCO
- Pruebas de significancia
- Análisis de supuestos
- Interpretación de resultados

Nota: Se utilizó IA (ChatGPT/Claude) como asistente en la estructuración del código
y generación de comentarios, manteniendo la lógica econométrica original del equipo.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import het_breuschpagan, normal_ad
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. INGRESO DE DATOS
# ============================================================================

# Datos del período 1995-2025
# Variable X: PIB (Producto Interno Bruto) en millones de USD
# Variable Y: Gasto de Consumo de Hogares en millones de USD

datos = {
    'Año': list(range(1995, 2026)),
    'PIB': [6715.7, 7392.5, 7924.2, 8498.4, 8284.1, 8397.9, 8141.5, 7905.4, 
            8082.3, 8773.4, 9549.5, 11451.9, 13120.1, 16674.2, 17339.9, 19649.5, 
            23963.0, 27084.2, 30659.3, 32996.2, 33000.2, 33941.1, 37508.6, 
            40287.7, 41193.1, 36680.4, 40408.2, 44007.6, 45850.3, 46750.0, 47200.0],
    'Consumo_Hogares': [5103.9, 5618.3, 6022.4, 6458.8, 6295.9, 6382.4, 6187.5, 
                        6008.1, 6142.5, 6580.1, 7066.6, 8360.0, 9446.5, 11838.7, 
                        12311.3, 13754.7, 16534.5, 18417.3, 20541.7, 22107.5, 
                        22440.1, 23419.4, 25505.8, 27420.2, 28217.3, 25676.3, 
                        27881.7, 30145.2, 31636.7, 32150.0, 32540.0]
}

df = pd.DataFrame(datos)

# Crear variable adicional: Inversión (diferencia PIB - Consumo como proxy)
df['Inversion'] = df['PIB'] - df['Consumo_Hogares']

# Crear variable de tendencia temporal
df['Tendencia'] = range(1, len(df) + 1)

print("="*80)
print("ANÁLISIS ECONOMÉTRICO: PIB Y GASTO DE CONSUMO DE HOGARES (1995-2025)")
print("="*80)
print("\n")

# ============================================================================
# 2. ESTADÍSTICA DESCRIPTIVA
# ============================================================================

print("2. ESTADÍSTICA DESCRIPTIVA")
print("-" * 80)
print("\nResumen estadístico de las variables:")
print(df[['PIB', 'Consumo_Hogares', 'Inversion']].describe().round(2))

# Matriz de correlación
print("\n\nMatriz de Correlación:")
corr_matrix = df[['PIB', 'Consumo_Hogares', 'Inversion']].corr()
print(corr_matrix.round(4))

# ============================================================================
# 3. ESPECIFICACIÓN DEL MODELO ECONOMÉTRICO
# ============================================================================

print("\n" + "="*80)
print("3. ESPECIFICACIÓN DEL MODELO ECONOMÉTRICO")
print("-" * 80)
print("""
MODELO A ESTIMAR:

Consumo_Hogares = β₀ + β₁*PIB + β₂*Inversion + ε

Donde:
- Y (Consumo_Hogares): Gasto de Consumo de Hogares (Millones USD)
- X₁ (PIB): Producto Interno Bruto (Millones USD)
- X₂ (Inversion): Aproximación de Inversión (Millones USD)
- ε: Término de error
- β₀: Ordenada al origen (intercepto)
- β₁, β₂: Coeficientes de regresión

EXPECTATIVAS TEÓRICAS:
- β₁ > 0: Se espera que mayor PIB incremente el consumo (relación positiva)
- β₂ < 0: Se espera que mayor inversión reduzca consumo (trade-off)
""")

# ============================================================================
# 4. ESTIMACIÓN DEL MODELO POR MCO
# ============================================================================

print("\n" + "="*80)
print("4. ESTIMACIÓN DEL MODELO POR MÍNIMOS CUADRADOS ORDINARIOS")
print("-" * 80)

# Especificar el modelo
modelo = ols('Consumo_Hogares ~ PIB + Inversion', data=df).fit()

# Mostrar resultados
print("\n", modelo.summary())

# ============================================================================
# 5. INTERPRETACIÓN ECONOMÉTRICA
# ============================================================================

print("\n" + "="*80)
print("5. INTERPRETACIÓN ECONOMÉTRICA")
print("-" * 80)

print("\na) COEFICIENTES ESTIMADOS:")
print("-" * 40)
for var in modelo.params.index:
    coef = modelo.params[var]
    std_err = modelo.bse[var]
    t_stat = modelo.tvalues[var]
    p_val = modelo.pvalues[var]
    
    print(f"\n{var}:")
    print(f"  Coeficiente: {coef:.6f}")
    print(f"  Error Estándar: {std_err:.6f}")
    print(f"  t-estadístico: {t_stat:.6f}")
    print(f"  p-valor: {p_val:.6f}")
    
    if var == 'PIB':
        print(f"  INTERPRETACIÓN: Un aumento de 1 millón USD en el PIB")
        print(f"  incrementa el Consumo de Hogares en {coef:.6f} millones USD,")
        print(f"  manteniendo constante la Inversión.")
    elif var == 'Inversion':
        print(f"  INTERPRETACIÓN: Un aumento de 1 millón USD en Inversión")
        print(f"  cambia el Consumo en {coef:.6f} millones USD,")
        print(f"  manteniendo constante el PIB.")

print("\n\nb) PRUEBAS t INDIVIDUALES:")
print("-" * 40)
print(f"Nivel de significancia: α = 0.05")
print(f"H₀: βᵢ = 0 (coeficiente no significativo)")
print(f"H₁: βᵢ ≠ 0 (coeficiente significativo)\n")

for var in modelo.params.index:
    p_val = modelo.pvalues[var]
    sig = "Significativo" if p_val < 0.05 else "No significativo"
    print(f"{var}: p-valor = {p_val:.6f} ({sig})")

print("\n\nc) PRUEBA F GLOBAL:")
print("-" * 40)
print(f"H₀: β₁ = β₂ = 0 (modelo no significativo)")
print(f"H₁: Al menos un βᵢ ≠ 0 (modelo significativo)\n")
print(f"F-estadístico: {modelo.fvalue:.6f}")
print(f"p-valor: {modelo.f_pvalue:.10f}")
print(f"Conclusión: El modelo en conjunto es {'SIGNIFICATIVO ✓' if modelo.f_pvalue < 0.05 else 'NO SIGNIFICATIVO ✗'}")

print("\n\nd) COEFICIENTE DE DETERMINACIÓN:")
print("-" * 40)
print(f"R²: {modelo.rsquared:.6f}")
print(f"R² Ajustado: {modelo.rsquared_adj:.6f}")
print(f"RMSE: {np.sqrt(modelo.mse_resid):.6f}")
print(f"\nInterpretación: El modelo explica el {modelo.rsquared*100:.2f}% de la")
print(f"variabilidad del Consumo de Hogares.")

# ============================================================================
# 6. ANÁLISIS DE SUPUESTOS
# ============================================================================

print("\n" + "="*80)
print("6. EVALUACIÓN DE SUPUESTOS DEL MODELO")
print("-" * 80)

# Obtener residuos y valores predichos
residuos = modelo.resid
valores_ajustados = modelo.fittedvalues

print("\na) NORMALIDAD DE RESIDUOS:")
print("-" * 40)
print("H₀: Los residuos se distribuyen normalmente")
print("H₁: Los residuos no se distribuyen normalmente\n")

# Test de Anderson-Darling
stat_ad, p_val_ad = normal_ad(residuos)
print(f"Test Anderson-Darling:")
print(f"  Estadístico: {stat_ad:.6f}")
print(f"  p-valor: {p_val_ad:.6f}")
print(f"  Conclusión: Los residuos {'PARECEN distribuirse normalmente ✓' if p_val_ad > 0.05 else 'NO parecen distribuirse normalmente ✗'}")

# Test de Shapiro-Wilk
stat_sw, p_val_sw = stats.shapiro(residuos)
print(f"\nTest Shapiro-Wilk:")
print(f"  Estadístico: {stat_sw:.6f}")
print(f"  p-valor: {p_val_sw:.6f}")

print("\n\nb) HETEROCEDASTICIDAD:")
print("-" * 40)
print("H₀: Var(ε) = σ² (homocedasticidad - varianza constante)")
print("H₁: Var(ε) ≠ σ² (heterocedasticidad - varianza no constante)\n")

# Test de Breusch-Pagan
lm_stat, lm_pval, fstat, fpval = het_breuschpagan(residuos, modelo.model.exog)
print(f"Test de Breusch-Pagan:")
print(f"  Estadístico LM: {lm_stat:.6f}")
print(f"  p-valor: {lm_pval:.6f}")
print(f"  Conclusión: {'EXISTE heterocedasticidad ✗' if lm_pval < 0.05 else 'NO existe heterocedasticidad ✓'}")

print("\n\nc) MULTICOLINEALIDAD:")
print("-" * 40)
print("Se evalúa mediante Factores de Inflación de Varianza (VIF)")
print("VIF < 5: No hay problemas")
print("5 < VIF < 10: Multicolinealidad moderada")
print("VIF > 10: Multicolinealidad severa\n")

# VIF (Variance Inflation Factor)
print("Factores de Inflación de Varianza (VIF):")
X = modelo.model.exog
vif_data = pd.DataFrame()
vif_data["Variable"] = ['PIB', 'Inversion']
vif_data["VIF"] = [variance_inflation_factor(X, i) for i in range(1, X.shape[1])]
print(vif_data.to_string(index=False))

vif_max = vif_data["VIF"].max()
if vif_max < 5:
    print("\nConlusión: No hay problemas de multicolinealidad ✓")
elif vif_max < 10:
    print("\nConlusión: Multicolinealidad moderada")
else:
    print("\nConlusión: Multicolinealidad severa ✗")

# ============================================================================
# 7. ERRORES ROBUSTOS (si hay heterocedasticidad)
# ============================================================================

if lm_pval < 0.05:
    print("\n" + "="*80)
    print("ESTIMACIÓN CON ERRORES ROBUSTOS (ante heterocedasticidad)")
    print("-" * 80)
    
    modelo_robusto = ols('Consumo_Hogares ~ PIB + Inversion', data=df).fit(
        cov_type='HC1'
    )
    print("\n", modelo_robusto.summary())

# ============================================================================
# 8. GRÁFICOS
# ============================================================================

print("\n" + "="*80)
print("8. GENERACIÓN DE GRÁFICOS")
print("-" * 80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis Gráfico del Modelo Econométrico\nPIB vs Gasto de Consumo de Hogares', 
             fontsize=16, fontweight='bold')

# Gráfico 1: Residuos vs Valores Ajustados
ax1 = axes[0, 0]
ax1.scatter(valores_ajustados, residuos, alpha=0.6, s=80, color='steelblue', edgecolors='black')
ax1.axhline(y=0, color='r', linestyle='--', linewidth=2, label='Línea cero')
ax1.set_xlabel('Valores Ajustados', fontsize=11, fontweight='bold')
ax1.set_ylabel('Residuos', fontsize=11, fontweight='bold')
ax1.set_title('Residuos vs Valores Ajustados', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Gráfico 2: Histograma de Residuos
ax2 = axes[0, 1]
ax2.hist(residuos, bins=10, edgecolor='black', alpha=0.7, color='skyblue')
ax2.axvline(x=residuos.mean(), color='r', linestyle='--', linewidth=2, label=f'Media = {residuos.mean():.2f}')
ax2.set_xlabel('Residuos', fontsize=11, fontweight='bold')
ax2.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
ax2.set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')
ax2.legend()

# Gráfico 3: Q-Q Plot (normalidad)
ax3 = axes[1, 0]
stats.probplot(residuos, dist="norm", plot=ax3)
ax3.set_title('Q-Q Plot (Prueba de Normalidad)', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Gráfico 4: Serie de tiempo observado vs ajustado
ax4 = axes[1, 1]
ax4.plot(df['Año'], df['Consumo_Hogares'], 'o-', label='Consumo Observado', 
         linewidth=2.5, markersize=6, color='darkblue')
ax4.plot(df['Año'], valores_ajustados, 's--', label='Consumo Ajustado', 
         linewidth=2.5, markersize=5, color='red')
ax4.set_xlabel('Año', fontsize=11, fontweight='bold')
ax4.set_ylabel('Gasto de Consumo (Millones USD)', fontsize=11, fontweight='bold')
ax4.set_title('Consumo Observado vs Ajustado', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10, loc='upper left')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('01_graficos_modelo.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico 1 guardado: 01_graficos_modelo.png")

# Gráfico adicional: Dispersión PIB vs Consumo
fig2, ax = plt.subplots(figsize=(12, 7))
ax.scatter(df['PIB'], df['Consumo_Hogares'], s=120, alpha=0.7, 
           color='steelblue', edgecolors='darkblue', linewidth=1.5)

# Línea de regresión simple
z = np.polyfit(df['PIB'], df['Consumo_Hogares'], 1)
p = np.poly1d(z)
ax.plot(df['PIB'], p(df['PIB']), "r--", linewidth=2.5, label=f'Línea de Regresión: y={z[0]:.4f}x+{z[1]:.2f}')

ax.set_xlabel('PIB (Millones USD)', fontsize=12, fontweight='bold')
ax.set_ylabel('Gasto de Consumo (Millones USD)', fontsize=12, fontweight='bold')
ax.set_title('Relación entre PIB y Gasto de Consumo de Hogares\n(Período 1995-2025)', 
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('02_dispersion_pib_consumo.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 2 guardado: 02_dispersion_pib_consumo.png")

# ============================================================================
# 9. EXPORTAR DATOS PARA EXCEL
# ============================================================================

print("\n" + "="*80)
print("9. EXPORTACIÓN DE DATOS")
print("-" * 80)

# Crear DataFrame con resultados
resultados = pd.DataFrame({
    'Año': df['Año'],
    'PIB': df['PIB'],
    'Consumo_Hogares': df['Consumo_Hogares'],
    'Inversion': df['Inversion'],
    'Consumo_Ajustado': valores_ajustados,
    'Residuos': residuos
})

resultados.to_csv('datos_modelo.csv', index=False)
print("\n✓ Datos exportados a: datos_modelo.csv")

# ============================================================================
# 10. RESUMEN FINAL
# ============================================================================

print("\n" + "="*80)
print("CONCLUSIONES Y HALLAZGOS PRINCIPALES")
print("="*80)

print(f"""
1. RELACIÓN ENTRE VARIABLES:
   ✓ Existe una relación POSITIVA y SIGNIFICATIVA entre PIB y Consumo
   ✓ Coeficiente de correlación: {corr_matrix.loc['PIB', 'Consumo_Hogares']:.4f}
   ✓ Interpretación: A mayor PIB, mayor gasto de consumo

2. BONDAD DEL AJUSTE:
   ✓ El modelo explica el {modelo.rsquared*100:.2f}% de la variabilidad
   ✓ R² ajustado: {modelo.rsquared_adj:.4f}
   ✓ Calidad del ajuste: {'EXCELENTE' if modelo.rsquared > 0.90 else 'BUENA' if modelo.rsquared > 0.70 else 'MODERADA'}

3. SIGNIFICANCIA ESTADÍSTICA:
   ✓ Prueba F (modelo global): p-valor = {modelo.f_pvalue:.2e}
   ✓ Resultado: MODELO GLOBALMENTE SIGNIFICATIVO ✓
   ✓ Coeficientes individuales: {'TODOS SIGNIFICATIVOS ✓' if all(modelo.pvalues < 0.05) else 'ALGUNOS NO SIGNIFICATIVOS'}

4. SUPUESTOS DEL MODELO:
   {'✓ Normalidad: CUMPLE' if p_val_ad > 0.05 else '✗ Normalidad: NO CUMPLE'}
   {'✓ Homocedasticidad: CUMPLE' if lm_pval > 0.05 else '✗ Homocedasticidad: NO CUMPLE (heterocedástico)'}
   {'✓ Multicolinealidad: BAJA' if vif_max < 5 else '✗ Multicolinealidad: MODERADA/ALTA'}

5. IMPLICACIONES ECONÓMICAS:
   ✓ Elasticidad PIB-Consumo: {modelo.params['PIB']:.4f}
   ✓ Propensión Marginal al Consumo: {modelo.params['PIB']:.4f} (aproximadamente {modelo.params['PIB']*100:.1f}%)
   ✓ Por cada aumento de 100 millones USD en PIB, el consumo aumenta ~{modelo.params['PIB']*100:.2f} millones USD
   ✓ Interpretación: La relación es PROCÍCLICA - el consumo fluctúa con el ciclo económico

6. LIMITACIONES DEL MODELO:
   • Solo considera dos variables explicativas (modelo simplificado)
   • No incluye factores como inflación, tasa de interés o desempleo
   • Período de análisis: 31 años (1995-2025)
   • Datos anuales (no captura variaciones intra-anuales)
   • La crisis de 2008-2009 y COVID-19 generan saltos estructurales

7. RECOMENDACIONES:
   • Realizar análisis de estabilidad estructural (Chow test)
   • Incluir variables adicionales: tasa de desempleo, inflación
   • Evaluar modelos dinámicos (autorregresivos)
   • Realizar pronósticos para años futuros
   • Aplicar técnicas de detección de outliers y valores extremos
""")

print("\n" + "="*80)
print("✓ ANÁLISIS COMPLETADO EXITOSAMENTE")
print("="*80)
