# app.py

import streamlit as st
from gethubs import get_hubs
from getprojects import get_projects
from navelements import get_top_folders, get_folder_contents

def main():
    st.title("Visualizador de Dados Autodesk")

    # Inicializar o estado da aplicação
    if 'project_id' not in st.session_state:
        st.session_state.project_id = None
    if 'folder_stack' not in st.session_state:
        st.session_state.folder_stack = []

    # Obter a lista de hubs
    hubs_df = get_hubs()
    if hubs_df is not None and not hubs_df.empty:
        # Filtrar o hub com nome 'Blossom Consult' ou usar o primeiro hub
        hub_name = 'Blossom Consult'
        if 'name' in hubs_df.columns and hub_name in hubs_df['name'].values:
            hub_id = hubs_df[hubs_df['name'] == hub_name]['id'].iloc[0]
            st.header(f"Hub: {hub_name}")
        else:
            hub_id = hubs_df['id'].iloc[0]
            hub_name = hubs_df['name'].iloc[0] if 'name' in hubs_df.columns else 'Unknown'
            st.header(f"Hub: {hub_name}")

        # Obter e exibir a lista de projetos
        st.text("Abrindo o get projects")
        projects_df = get_projects(hub_id)
        st.text("Abriu o get projects")
        if projects_df is not None and not projects_df.empty:
            st.write("Colunas em projects_df:", projects_df.columns.tolist())
            st.write("Conteúdo de projects_df:")
            st.write(projects_df[['id', 'name']])  # Exibe apenas as colunas 'id' e 'name'

            # Selecionar um projeto
            project_name = st.selectbox("Selecione um Projeto", projects_df['name'])
            project_id = projects_df[projects_df['name'] == project_name]['id'].iloc[0]
            st.session_state.project_id = project_id
            st.subheader(f"Projeto: {project_name}")

            # Se não houver pastas na pilha, adicionar as pastas de nível superior
            if not st.session_state.folder_stack:
                top_folders_df = get_top_folders(project_id)
                if top_folders_df is not None and not top_folders_df.empty:
                    st.session_state.folder_stack.append({
                        'name': 'Pastas de Nível Superior',
                        'folders_df': top_folders_df
                    })
                    display_current_folder()
                else:
                    st.write("Nenhuma pasta encontrada ou erro ao obter as pastas.")
                    st.write("Verifique se você tem permissões para acessar este projeto e se o projeto contém pastas.")
            else:
                display_current_folder()
        else:
            st.write("Nenhum projeto encontrado ou erro ao obter os projetos.")
    else:
        st.write("Nenhum hub encontrado ou erro ao obter os hubs.")

def display_current_folder():
    current_folder = st.session_state.folder_stack[-1]
    st.write(f"## {current_folder['name']}")

    folders_df = current_folder['folders_df']
    for idx, row in folders_df.iterrows():
        if st.button(f"Abrir Pasta: {row['name']}", key=f"open_{row['id']}"):
            open_folder(row['name'], row['id'])
    if len(st.session_state.folder_stack) > 1:
        if st.button("Voltar", key="back_button"):
            st.session_state.folder_stack.pop()
            st.experimental_rerun()

def open_folder(folder_name, folder_id):
    project_id = st.session_state.project_id
    contents_df = get_folder_contents(project_id, folder_id)
    if contents_df is not None and not contents_df.empty:
        # Filtrar apenas pastas
        subfolders_df = contents_df[contents_df['type'] == 'folders'].reset_index(drop=True)
        st.session_state.folder_stack.append({
            'name': folder_name,
            'folders_df': subfolders_df
        })
        st.experimental_rerun()
    else:
        st.write("Pasta vazia ou erro ao obter o conteúdo.")

if __name__ == "__main__":
    main()
