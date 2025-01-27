import streamlit as st
import pandas as pd

def realizar_merge(df1, df_cuestionario):
    # Realizar el merge entre los dos DataFrames
    df_merged_cuestionario = pd.merge(df1, df_cuestionario, on='Codigo', how='inner')
    return df_merged_cuestionario

# Título de la aplicación
st.title("Generador de Propuesta de cuestionario")

# Subida de archivos
st.subheader("Sube los archivos necesarios")
archivo_checkname = st.file_uploader("Sube el archivo generado por el sistema", type=["xlsx"])
archivo_cuestionario = st.file_uploader("Preguntas Globales", type=["xlsx"])

if archivo_checkname and archivo_cuestionario:
    try:
        # Leer los archivos subidos
        df_checkname = pd.read_excel(archivo_checkname)
        df_cuestionario = pd.read_excel(archivo_cuestionario)

        st.write("Vista previa del archivo de Check Names:")
        st.dataframe(df_checkname.head())

        st.write("Vista previa del archivo de Cuestionario:")
        st.dataframe(df_cuestionario.head())

        # Verificar que ambos DataFrames contengan la columna 'Codigo'
        if 'Codigo' in df_checkname.columns and 'Codigo' in df_cuestionario.columns:
            # Realizar el merge
            df_merged = realizar_merge(df_checkname, df_cuestionario)

            st.subheader("Resultado del Merge")
            st.dataframe(df_merged.head())

            # Botón para descargar el resultado
            @st.cache_data
            def convertir_excel(df):
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Resultado')
                processed_data = output.getvalue()
                return processed_data

            excel_data = convertir_excel(df_merged)
            st.download_button(
                label="Descargar el resultado en Excel",
                data=excel_data,
                file_name="resultado_merge.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Ambos archivos deben contener una columna llamada 'Codigo'.")
    except Exception as e:
        st.error(f"Hubo un error al procesar los archivos: {e}")
else:
    st.info("Por favor, sube ambos archivos para continuar.")
