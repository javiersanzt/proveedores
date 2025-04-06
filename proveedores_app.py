
import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

# Configurar página
st.set_page_config(page_title="Gestor de Proveedores", layout="wide")

# Archivo Excel donde se guardan los datos
excel_file = "proveedores_productos.xlsx"

# Definir columnas
columnas = [
    "Proveedor", "Plataforma", "Producto", "Categoría",
    "Precio Coste (€)", "Precio Venta (€)", "Margen (%)",
    "MOQ", "Dropshipping", "Ubicación", "Notas"
]

# Cargar o crear DataFrame
df = pd.read_excel(excel_file) if Path(excel_file).exists() else pd.DataFrame(columns=columnas)

# Título principal
st.title("🧵 Gestor de Proveedores y Productos")
st.markdown("Herramienta interna para registrar, analizar y exportar productos de proveedores mayoristas.")
st.divider()

# Función para calcular margen
def calcular_margen(coste, venta):
    return round(((venta - coste) / coste) * 100, 2) if coste > 0 else 0

# Formulario
st.subheader("➕ Añadir nuevo producto")
with st.form("formulario_producto"):
    col1, col2, col3 = st.columns(3)

    with col1:
        proveedor = st.text_input("Proveedor")
        plataforma = st.text_input("Plataforma")
        categoria = st.text_input("Categoría")

    with col2:
        producto = st.text_input("Nombre del producto")
        coste = st.number_input("Precio de coste (€)", min_value=0.0, step=0.01)
        venta = st.number_input("Precio de venta (€)", min_value=0.0, step=0.01)

    with col3:
        moq = st.text_input("MOQ (mínimo pedido)")
        dropshipping = st.selectbox("Dropshipping disponible", ["Sí", "No"])
        ubicacion = st.text_input("Ubicación del proveedor")

    notas = st.text_area("Notas adicionales")

    submitted = st.form_submit_button("📦 Añadir producto")

    if submitted:
        margen = calcular_margen(coste, venta)
        nuevo = pd.DataFrame([[
            proveedor, plataforma, producto, categoria,
            coste, venta, margen, moq, dropshipping, ubicacion, notas
        ]], columns=columnas)
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_excel(excel_file, index=False)
        st.success(f"✅ Producto '{producto}' añadido correctamente.")

st.divider()

# Mostrar tabla
st.subheader("📊 Productos registrados")
st.dataframe(df, use_container_width=True)

# Exportar Excel
st.divider()
st.subheader("📥 Exportar datos")
output = BytesIO()
df.to_excel(output, index=False, engine="openpyxl")
output.seek(0)

st.download_button(
    label="⬇️ Descargar Excel",
    data=output,
    file_name="proveedores_productos_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
