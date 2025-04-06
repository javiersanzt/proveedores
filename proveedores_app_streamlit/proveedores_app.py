import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

# Configurar página
st.set_page_config(page_title="Gestor de Proveedores", layout="wide")

# Nombre del archivo Excel
excel_file = "proveedores_productos.xlsx"

# Definir columnas
columnas = [
    "Proveedor", "Plataforma", "Producto", "Categoría", "Precio Coste (€)", "Precio Venta (€)",
    "Margen (%)", "MOQ", "Dropshipping", "Ubicación", "Notas"
]

# Cargar o crear DataFrame
if Path(excel_file).exists():
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=columnas)

# TÍTULO PRINCIPAL
st.title("🧵 Gestor de Proveedores y Productos")
st.markdown("Una herramienta interna para registrar, comparar y exportar productos de proveedores mayoristas.")

st.divider()

# FORMULARIO
st.subheader("➕ Añadir nuevo producto al listado")

with st.form("nuevo_producto"):
    col1, col2, col3 = st.columns(3)
    with col1:
        proveedor = st.text_input("Proveedor")
        plataforma = st.text_input("Plataforma (Ankorstore, Faire...)")
        categoria = st.text_input("Categoría")
    with col2:
        producto = st.text_input("Nombre del producto")
        coste = st.number_input("Precio de coste (€)", min_value=0.0, format="%.2f")
        venta = st.number_input("Precio de venta (€)", min_value=0.0, format="%.2f")
    with col3:
        moq = st.text_input("MOQ (mínimo pedido)")
        dropshipping = st.selectbox("Dropshipping disponible", ["Sí", "No"])
        ubicacion = st.text_input("Ubicación del proveedor")

    notas = st.text_area("Notas adicionales")

    submitted = st.form_submit_button("📦 Añadir producto")

    if submitted:
        margen = round(((venta - coste) / coste) * 100, 2) if coste > 0 else 0
        nuevo = pd.DataFrame([[
            proveedor, plataforma, producto, categoria,
            coste, venta, margen, moq, dropshipping, ubicacion, notas
        ]], columns=columnas)
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_excel(excel_file, index=False)
        st.success(f"✅ Producto '{producto}' añadido correctamente.")

st.divider()

# MOSTRAR TABLA
st.subheader("📊 Tabla de productos registrada")
st.dataframe(df, use_container_width=True)

# DESCARGAR EXCEL
st.divider()
st.subheader("📥 Exportar tabla")
output = BytesIO()
df.to_excel(output, index=False, engine='openpyxl')
output.seek(0)

st.download_button(
    label="⬇️ Descargar Excel",
    data=output,
    file_name="proveedores_productos_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
