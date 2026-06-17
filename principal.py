import streamlit as st
from streamlit_option_menu import option_menu  # <-- IMPORTAÇÃO NOVA AQUI
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (Deixa em tela cheia e com título na aba)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="O Ambiente que Expulsa - A3", layout="wide")

# -----------------------------------------------------------------------------
# ESTILOS GLOBAIS (CSS injetado uma única vez)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Cartão genérico reutilizável */
        .v0-card {
            background: linear-gradient(160deg, #1E293B 0%, #16202E 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #2B3A4F;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
            height: 100%;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .v0-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.45);
            border-color: #3B5070;
        }
        .v0-card-accent {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 46px;
            height: 46px;
            border-radius: 12px;
            font-size: 22px;
            margin-bottom: 14px;
        }
        .v0-card h3 {
            margin: 0 0 8px 0;
            font-size: 19px;
            font-weight: 700;
        }
        .v0-card p {
            margin: 0;
            color: #CBD5E1;
            font-size: 15px;
            line-height: 1.6;
        }
        .v0-card .v0-tag {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 3px 10px;
            border-radius: 999px;
            margin-bottom: 12px;
        }
        /* Banner de destaque (callouts) */
        .v0-callout {
            border-radius: 14px;
            padding: 18px 20px;
            display: flex;
            gap: 14px;
            align-items: flex-start;
            border: 1px solid transparent;
            margin-bottom: 4px;
        }
        .v0-callout .v0-ico { font-size: 24px; line-height: 1.2; }
        .v0-callout p { margin: 4px 0 0 0; font-size: 15px; line-height: 1.6; }
        .v0-callout strong { color: #F8FAFC; }

        /* ---------- Cabeçalho / Hero das páginas ---------- */
        .v0-hero {
            text-align: center;
            padding: 8px 0 4px 0;
        }
    button[data-baseweb="tab"] {
        font-size: 18px !important; 
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }

    /* Opcional: Ajustar a cor do texto ao selecionar a aba */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #60A5FA !important; 
    }
        .v0-hero .v0-eyebrow {
            display: inline-block;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #60A5FA;
            background: rgba(59,130,246,0.12);
            border: 1px solid rgba(59,130,246,0.30);
            padding: 5px 14px;
            border-radius: 999px;
            margin-bottom: 14px;
        }
        .v0-hero h1 {
            margin: 0;
            font-size: 42px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        .v0-hero p {
            margin: 12px auto 0 auto;
            max-width: 640px;
            font-size: 17px;
            line-height: 1.6;
            color: #94A3B8;
        }
        /* Régua/divisória sutil com gradiente */
        .v0-rule {
            height: 1px;
            border: none;
            margin: 22px 0;
            background: linear-gradient(90deg, transparent, #334155 20%, #334155 80%, transparent);
        }
        /* Cabeçalho de seção menor (com barrinha de acento) */
        .v0-section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 20px;
            font-weight: 700;
            color: #F1F5F9;
            margin: 4px 0 6px 0;
        }
        .v0-section-title::before {
            content: "";
            width: 4px;
            height: 22px;
            border-radius: 4px;
            background: #60A5FA;
        }
        .v0-section-sub {
            color: #94A3B8;
            font-size: 15px;
            line-height: 1.6;
            margin: 0 0 8px 0;
        }
        /* ---------- Fluxo de processo (página 2) ---------- */
        .v0-flow {
            display: flex;
            align-items: stretch;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin: 6px 0 8px 0;
        }
        .v0-flow-step {
            flex: 1;
            min-width: 180px;
            background: linear-gradient(160deg, #1E293B 0%, #16202E 100%);
            border: 1px solid #2B3A4F;
            border-radius: 14px;
            padding: 18px;
            text-align: center;
        }
        .v0-flow-step .ico { font-size: 26px; }
        .v0-flow-step .lbl { display:block; margin-top:8px; font-weight:700; color:#E2E8F0; font-size:15px; }
        .v0-flow-step .desc { display:block; margin-top:4px; color:#94A3B8; font-size:13px; }
        .v0-flow-arrow {
            display: flex;
            align-items: center;
            color: #475569;
            font-size: 24px;
            font-weight: 700;
        }
        @media (max-width: 720px) { .v0-flow-arrow { transform: rotate(90deg); } }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_hero(eyebrow, title, subtitle=""):
    """Cabeçalho padronizado para o topo de cada página."""
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="v0-hero">
            <span class="v0-eyebrow">{eyebrow}</span>
            <h1>{title}</h1>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=""):
    """Cabeçalho de seção com barrinha de acento."""
    sub_html = f"<p class='v0-section-sub'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"<div class='v0-section-title'>{title}</div>{sub_html}",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# MENU LATERAL (Navegação da Apresentação)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Um título mais robusto (Ajustado para Azul Claro no Modo Escuro)
    st.markdown(
        "<h2 style='text-align: center; color: #60A5FA;'>Evasão Escolar</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # O novo menu super profissional (Sem fonte pixelada)
    pagina = option_menu(
        menu_title="Tópicos",
        options=[
            "1. O Despertar",
            "2. A Bússola",
            "3. A Virada",
            "4. O Veredito",
        ],
        icons=[
            "lightning-charge-fill",
            "shield-lock-fill",
            "bar-chart-line-fill",
            "bullseye",
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#60A5FA", "font-size": "18px"},  # Ícones mais claros
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#334155",  # Hover mais suave pro escuro
                "font-weight": "normal",  # Garante que o texto normal não seja negrito
            },
            "nav-link-selected": {
                "background-color": "#1E3A8A",  # Fundo azul do botão selecionado
                "color": "white",
                "font-weight": "normal",  # Impede que ele fique negrito ao ser selecionado
            },
        },
    )

    st.markdown("---")

    # Uma assinatura da equipe para dar aquele toque final
    st.markdown(
        """
        <div style="background: linear-gradient(160deg, #1E293B 0%, #16202E 100%);
            border: 1px solid #2B3A4F; border-radius: 14px; padding: 16px;">
            <div style="display:flex; align-items:center; gap:8px; font-size:12px; font-weight:700;
                letter-spacing:0.08em; text-transform:uppercase; color:#60A5FA; margin-bottom:10px;">
                <span>👨‍💻</span> Desenvolvido por
            </div>
            <div style="color:#E2E8F0; font-size:14px; line-height:1.9;">
                Rodson Junior<br>
                Marcílio Filho<br>
                Maria Clara
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# RENDERIZAÇÃO DAS PÁGINAS
# -----------------------------------------------------------------------------

# --- PÁGINA 1: INTRODUÇÃO ---
if pagina == "1. O Despertar":
    # 1. Cabeçalho padronizado (hero)
    page_hero(
        "Capítulo 1 · O Despertar",
        "O Ambiente que Expulsa",
        "A Infraestrutura Escolar como Fator Determinante para a Evasão Escolar no Brasil",
    )

    st.markdown("<hr class='v0-rule'>", unsafe_allow_html=True)

    # 2. Criando 3 colunas para a imagem não ficar gigante na tela
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            "images/SalaDeAulaVazia.png",
            use_container_width=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. As provocações em formato de card de alerta (CSS inline)
        st.markdown(
            """
            <div class="v0-callout" style="background: rgba(59,130,246,0.10); border-color: rgba(59,130,246,0.35);">
                <span class="v0-ico">💡</span>
                <div>
                    <strong>O que é o "mínimo" para uma escola funcionar?</strong>
                    <p>Computador? Internet? Ar-condicionado?</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # 4. A frase de efeito final em card vermelho
        st.markdown(
            """
            <div class="v0-callout" style="background: rgba(205,62,92,0.12); border-color: rgba(205,62,92,0.40);">
                <span class="v0-ico">🚪</span>
                <div>
                    <p style="font-size:16px; color:#FCA5A5;">A evasão não é uma escolha do aluno.
                    <strong style="color:#FECACA;"> O ambiente o expulsa.</strong></p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- PÁGINA 2: GOVERNANÇA ---
elif pagina == "2. A Bússola":
    page_hero(
        "Capítulo 2 · A Bússola",
        "Governança e Dados",
        "Como transformamos milhões de registros em decisões seguras",
    )
    st.markdown("<hr class='v0-rule'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="v0-flow">
            <div class="v0-flow-step">
                <span class="ico">📊</span>
                <span class="lbl">Bases Brutas do INEP</span>
                <span class="desc">Microdados abertos</span>
            </div>
            <div class="v0-flow-arrow">➜</div>
            <div class="v0-flow-step">
                <span class="ico">⚙️</span>
                <span class="lbl">Processamento Python</span>
                <span class="desc">Limpeza e unificação</span>
            </div>
            <div class="v0-flow-arrow">➜</div>
            <div class="v0-flow-step">
                <span class="ico">🎯</span>
                <span class="lbl">Decisão Estratégica</span>
                <span class="desc">Padrões acionáveis</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="v0-card">
                <div class="v0-card-accent" style="background: rgba(16,185,129,0.15); color:#6EE7B7;">🛡️</div>
                <span class="v0-tag" style="background: rgba(16,185,129,0.15); color:#6EE7B7;">Segurança & Ética</span>
                <h3 style="color:#6EE7B7;">Conformidade com a LGPD</h3>
                <p>Trabalhamos exclusivamente com microdados abertos. <b style="color:#E2E8F0;">Anonimização total:</b>
                nenhuma escola ou aluno foi exposto. O algoritmo foca em padrões, não em indivíduos.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="v0-card">
                <div class="v0-card-accent" style="background: rgba(59,130,246,0.15); color:#60A5FA;">⚙️</div>
                <span class="v0-tag" style="background: rgba(59,130,246,0.15); color:#60A5FA;">Engenharia de Dados</span>
                <h3 style="color:#60A5FA;">Pipeline ETL</h3>
                <p>Limpamos ruídos e unificamos bases distintas. Consolidamos <b style="color:#E2E8F0;">16 variáveis de
                infraestrutura</b> em uma métrica única e criamos a métrica global NOTA_GERAL do ENEM.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='v0-rule'>", unsafe_allow_html=True)
    section_title(
        "🔍 Amostra da Base Consolidada",
        "Pronta para análise, com as variáveis já unificadas.",
    )

    df_exemplo = pd.DataFrame(
        {
            "COD_ESCOLA": [102938, 102939, 102940, 102941, 102942],
            "REDE": ["Pública", "Pública", "Privada", "Pública", "Privada"],
            "MEDIA_INFRA (%)": [45.5, 80.0, 100.0, 20.0, 95.5],
            "EVASAO_MEDIO (%)": [35.2, 12.5, 2.1, 60.8, 5.0],
            "NOTA_GERAL_ENEM": [480.2, 540.5, 620.0, 410.1, 590.3],
        }
    )

    st.dataframe(df_exemplo, use_container_width=True)

# --- PÁGINA 3: RESULTADOS E OUTLIERS (O Clímax) ---
elif pagina == "3. A Virada":
    page_hero(
        "Capítulo 3 · A Virada",
        "Descobrindo os Padrões",
        "Os dados revelam onde o sistema falha — e o que realmente segura o aluno na escola.",
    )
    st.markdown("<hr class='v0-rule'>", unsafe_allow_html=True)
    # 1. DEFINIÇÃO DAS ABAS (Garante que todas existam)
    tabs = st.tabs(
        [
            "📊 1. A Crise Sistêmica",
            "🚨 2. Ranking de Urgências",
            "🏢 3. Diferença das Infraestruturas",
            "📉 4. O Efeito U",
            "🧠 5. Permanência x Desempenho",
            "📌 6. Análise de Outliers",
        ]
    )

    aba1, aba2, aba3, aba4, aba5, aba6 = tabs

    with aba1:
        section_title(
            "A Crise é Geral: Ensino Médio e Fundamental",
            "A distribuição dos dados mostra como o modelo atual falha de forma generalizada em reter os alunos.",
        )

        # ==============================================================================
        # 1. IMPORTAÇÃO E TRATAMENTO DOS DADOS (Direto do GitHub)
        # ==============================================================================
        url = "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Maiores_Taxas_Evasao_e_Reprovacao_2024.csv"

        @st.cache_data
        def carregar_dados():
            df = pd.read_csv(url)
            cols_evasao = ["evasao_fundamental_total", "evasao_medio_total"]
            for col in cols_evasao:
                df[col] = pd.to_numeric(
                    df[col].replace("Não informado", np.nan), errors="coerce"
                )
            return df, cols_evasao

        df_evasao, cols = carregar_dados()

        # ==============================================================================
        # 2. PREPARAÇÃO DOS DADOS (MELTING)
        # ==============================================================================
        df_melt = df_evasao.melt(
            id_vars=["dependencia_adm"],
            value_vars=cols,
            var_name="Nivel_Ensino",
            value_name="Taxa_Evasao",
        )
        df_melt["Nivel_Ensino"] = df_melt["Nivel_Ensino"].replace(
            {cols[1]: "Ensino Médio", cols[0]: "Ensino Fundamental"}
        )

        # ==============================================================================
        # 3. GERAÇÃO E ESTILIZAÇÃO DO GRÁFICO
        # ==============================================================================
        fig = px.box(
            df_melt,
            x="dependencia_adm",
            y="Taxa_Evasao",
            color="dependencia_adm",
            facet_col="Nivel_Ensino",
            color_discrete_sequence=[
                "#217CE2",
                "#1D9B85",
                "#FA9B28",
                "#CD3E5C",
                "#5B5696",
            ],
            title="<b>Distribuição da Evasão por Tipo de Escola</b>",
            labels={
                "dependencia_adm": "Tipo de Escola",
                "Taxa_Evasao": "Taxa de Evasão (%)",
            },
        )

        fig.update_traces(
            boxmean=True,
            hovertemplate="<b>Tipo:</b> %{x}<br><b>Média:</b> %{mean:.2f}%<br><b>Mediana:</b> %{median:.2f}%<extra></extra>",
        )

        fig.update_layout(
            height=600,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="closest",
            showlegend=False,
            font=dict(family="Arial, sans-serif", color="#E2E8F0"),
            title_font=dict(size=18, color="#F8FAFC"),
            margin=dict(l=40, r=40, t=100, b=40),
        ).update_yaxes(showgrid=True, gridcolor="#334155", zeroline=False).update_xaxes(
            showgrid=False
        )

        fig.for_each_annotation(
            lambda a: a.update(
                text=a.text.split("=")[-1].upper(), font=dict(size=18, color="white")
            )
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)
        pass

    with aba4:
        section_title(
            "O Paradoxo da Reprovação: O Efeito U",
            "Aprovação automática gera quebra de vínculo. Rigor extremo gera frustração. O segredo da retenção está no equilíbrio do desafio.",
        )

        # ==========================================
        # 1. IMPORTAÇÃO E TRATAMENTO (Com Cache)
        # ==========================================
        @st.cache_data
        def preparar_dados_efeito_u():
            df_evasao = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Maiores_Taxas_Evasao_e_Reprovacao_2024.csv"
            )

            df_evasao["evasao_medio_total"] = pd.to_numeric(
                df_evasao["evasao_medio_total"].replace("Não informado", np.nan),
                errors="coerce",
            )
            df_evasao["reprovacao_medio_total"] = pd.to_numeric(
                df_evasao["reprovacao_medio_total"].replace("Não informado", np.nan),
                errors="coerce",
            )

            df_clean = df_evasao.dropna(
                subset=["evasao_medio_total", "reprovacao_medio_total"]
            ).copy()

            bins = [-1, 2, 5, 10, 20, 100]
            labels = ["0 a 2%", "2% a 5%", "5% a 10%", "10% a 20%", "Mais de 20%"]
            df_clean["Faixa_Reprovacao"] = pd.cut(
                df_clean["reprovacao_medio_total"], bins=bins, labels=labels
            )

            return (
                df_clean.groupby("Faixa_Reprovacao", observed=False)[
                    "evasao_medio_total"
                ]
                .mean()
                .reset_index()
            )

        grouped = preparar_dados_efeito_u()

        # ==========================================
        # 2. GERAÇÃO DO GRÁFICO INTERATIVO
        # ==========================================
        cores_barras = [
            "#6C296B",
            "#EFB08C",
            "#DE6A6A",
            "#A6406C",
            "#2A1A4A",
        ]

        fig_u = px.bar(
            grouped,
            x="Faixa_Reprovacao",
            y="evasao_medio_total",
            text="evasao_medio_total",
            color="Faixa_Reprovacao",
            color_discrete_sequence=cores_barras,
            title="<b>O Efeito U: Relação entre o Nível de Reprovação e a Evasão Escolar</b>",
            labels={
                "Faixa_Reprovacao": "Taxa de Reprovação da Escola",
                "evasao_medio_total": "Taxa Média de Evasão (%)",
            },
        )

        fig_u.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            textfont=dict(size=14, color="#F8FAFC", family="Arial", weight="bold"),
        )

        fig_u.update_layout(
            height=600,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial, sans-serif", color="#E2E8F0"),
            title_font=dict(size=18, color="#F8FAFC"),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(
                showgrid=True, gridcolor="#334155", zeroline=False, range=[0, 60]
            ),
            margin=dict(l=40, r=40, t=70, b=40),
            hovermode="x",
        )

        st.plotly_chart(fig_u, use_container_width=True, theme=None)
        pass

    with aba2:
        section_title(
            "Ranking de Urgências: O Fator Socialização",
            "O esporte e o pertencimento seguram o aluno na escola muito mais do que um computador.",
        )

        # ==========================================
        # 1. IMPORTAÇÃO E TRATAMENTO DOS DADOS
        # ==========================================
        @st.cache_data
        def preparar_dados_infra():
            df_censo = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/01_Cleaned/Tabela_Censo_Escolar_2024.csv",
                sep=";",
            )
            df_evasao = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Maiores_Taxas_Evasao_e_Reprovacao_2024.csv"
            )

            df_evasao["evasao_medio_total"] = pd.to_numeric(
                df_evasao["evasao_medio_total"].replace("Não informado", np.nan),
                errors="coerce",
            )
            df_evasao["evasao_fundamental_total"] = pd.to_numeric(
                df_evasao["evasao_fundamental_total"].replace("Não informado", np.nan),
                errors="coerce",
            )

            df_merged = pd.merge(
                df_censo,
                df_evasao,
                left_on="CO_ENTIDADE",
                right_on="codigo_escola",
                how="inner",
            )

            infra_map = {
                "IN_ENERGIA_REDE_PUBLICA": "Energia Elétrica",
                "IN_AGUA_POTAVEL": "Água Potável",
                "IN_INTERNET": "Internet (Geral)",
                "IN_QUADRA_ESPORTES": "Quadra de Esportes",
                "IN_LABORATORIO_CIENCIAS": "Lab. de Ciências",
                "IN_REFEITORIO": "Refeitório/Cantina",
                "IN_LABORATORIO_INFORMATICA": "Lab. de Informática",
                "IN_INTERNET_ALUNOS": "Internet para Alunos",
                "IN_ESGOTO_REDE_PUBLICA": "Rede de Esgoto",
                "IN_SALA_LEITURA": "Sala de Leitura/Biblioteca",
                "IN_ALIMENTACAO": "Fornece Alimentação",
            }

            data_list = []

            for col, name in infra_map.items():
                if col in df_merged.columns:
                    grouped = (
                        df_merged.groupby(col)[
                            ["evasao_medio_total", "evasao_fundamental_total"]
                        ]
                        .mean()
                        .round(1)
                    )

                    if 0.0 in grouped.index and 1.0 in grouped.index:
                        medio_sem = (
                            grouped.loc[0.0, "evasao_medio_total"]
                            if not pd.isna(grouped.loc[0.0, "evasao_medio_total"])
                            else 0
                        )
                        medio_com = (
                            grouped.loc[1.0, "evasao_medio_total"]
                            if not pd.isna(grouped.loc[1.0, "evasao_medio_total"])
                            else 0
                        )
                        fund_sem = (
                            grouped.loc[0.0, "evasao_fundamental_total"]
                            if not pd.isna(grouped.loc[0.0, "evasao_fundamental_total"])
                            else 0
                        )
                        fund_com = (
                            grouped.loc[1.0, "evasao_fundamental_total"]
                            if not pd.isna(grouped.loc[1.0, "evasao_fundamental_total"])
                            else 0
                        )

                        data_list.append(
                            {
                                "item": name,
                                "medio_sem": float(medio_sem),
                                "medio_com": float(medio_com),
                                "fund_sem": float(fund_sem),
                                "fund_com": float(fund_com),
                                "impacto_medio": float(medio_sem - medio_com),
                            }
                        )

            return pd.DataFrame(data_list).sort_values(
                by="impacto_medio", ascending=True
            )

        df_plot = preparar_dados_infra()

        # ==========================================
        # 2. FILTRO NATIVO DO STREAMLIT
        # ==========================================
        st.markdown("<br>", unsafe_allow_html=True)
        nivel_selecionado = st.radio(
            "Filtrar por:",
            ["Ensino Médio", "Ensino Fundamental"],
            horizontal=True,
        )

        # ==========================================
        # 3. GERAÇÃO DO GRÁFICO
        # ==========================================
        fig_urg = go.Figure()
        cor_sem = "#00664b"
        cor_com = "#004030"

        if nivel_selecionado == "Ensino Médio":
            fig_urg.add_trace(
                go.Bar(
                    y=df_plot["item"],
                    x=df_plot["medio_sem"],
                    name="Escolas SEM o item",
                    orientation="h",
                    marker_color=cor_sem,
                    text=df_plot["medio_sem"],
                    textposition="auto",
                    textfont=dict(color="white"),
                )
            )
            fig_urg.add_trace(
                go.Bar(
                    y=df_plot["item"],
                    x=df_plot["medio_com"],
                    name="Escolas COM o item",
                    orientation="h",
                    marker_color=cor_com,
                    text=df_plot["medio_com"],
                    textposition="auto",
                    textfont=dict(color="white"),
                )
            )
            titulo_grafico = (
                "<b>Impacto da Infraestrutura na Evasão Escolar - Ensino Médio</b>"
            )
        else:
            fig_urg.add_trace(
                go.Bar(
                    y=df_plot["item"],
                    x=df_plot["fund_sem"],
                    name="Escolas SEM o item ",
                    orientation="h",
                    marker_color=cor_sem,
                    text=df_plot["fund_sem"],
                    textposition="auto",
                    textfont=dict(color="white"),
                )
            )
            fig_urg.add_trace(
                go.Bar(
                    y=df_plot["item"],
                    x=df_plot["fund_com"],
                    name="Escolas COM o item ",
                    orientation="h",
                    marker_color=cor_com,
                    text=df_plot["fund_com"],
                    textposition="auto",
                    textfont=dict(color="white"),
                )
            )
            titulo_grafico = "<b>Impacto da Infraestrutura na Evasão Escolar - Ensino Fundamental</b>"

        fig_urg.update_layout(
            title=dict(
                text=titulo_grafico, font=dict(size=18, color="#F8FAFC"), x=0.5, y=0.98
            ),
            barmode="group",
            xaxis_title="Taxa Média de Evasão (%)",
            height=650,
            margin=dict(l=180, t=100, r=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial, sans-serif", color="#E2E8F0"),
            xaxis=dict(showgrid=True, gridcolor="#334155", zeroline=False),
            yaxis=dict(showgrid=False),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=1,
            ),
        )

        st.plotly_chart(fig_urg, use_container_width=True, theme=None)
        pass
    with aba5:
        section_title(
            "Correlação: Permanência vs. Desempenho no ENEM",
            "A análise por estados brasileiros demonstra a relação direta entre retenção e sucesso acadêmico.",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================
        # 1. CARREGAR E PREPARAR DADOS (Otimizado)
        # ==========================================
        @st.cache_data
        def preparar_dados_correlacao():
            df_evasao = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/Data_Cleaning/src/Datas/Maiores_Taxas_Evasao_e_Reprovacao_2024.csv"
            )
            df_censo = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/Data_Table_Relationships/src/Datas/censo_filtrado.csv",
                sep=";",
            )
            df_enem = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/Data_Cleaning/src/Datas/Tabela_ENEM_2024.csv"
            )

            df_evasao["evasao_medio_total"] = pd.to_numeric(
                df_evasao["evasao_medio_total"].replace("Não informado", np.nan),
                errors="coerce",
            )
            df_escolas_censo = pd.merge(
                df_censo,
                df_evasao,
                left_on="CO_ENTIDADE",
                right_on="codigo_escola",
                how="inner",
            )
            df_escolas_censo["taxa_permanencia"] = (
                100 - df_escolas_censo["evasao_medio_total"]
            )

            permanencia_uf = (
                df_escolas_censo.groupby("SG_UF")["taxa_permanencia"]
                .mean()
                .reset_index()
            )
            enem_uf = (
                df_enem.groupby("SG_UF_PROVA")[["NOTA_GERAL"]].mean().reset_index()
            )

            df_final = pd.merge(
                permanencia_uf,
                enem_uf,
                left_on="SG_UF",
                right_on="SG_UF_PROVA",
                how="inner",
            )
            media_nac = df_enem["NOTA_GERAL"].mean()
            return df_final, media_nac

        df_final, media_nacional = preparar_dados_correlacao()

        # ==========================================
        # 2. GERAÇÃO DO GRÁFICO (Trendline/Regressão)
        # ==========================================
        fig_uf = px.scatter(
            df_final,
            x="taxa_permanencia",
            y="NOTA_GERAL",
            text="SG_UF",
            trendline="ols",  # Linha de regressão
            labels={
                "taxa_permanencia": "Taxa de Permanência (%)",
                "NOTA_GERAL": "Nota Média ENEM",
            },
        )

        # Estilo dos pontos
        fig_uf.update_traces(
            marker=dict(size=14, color="#60A5FA", line=dict(width=1.5, color="white")),
            textposition="top center",
            textfont=dict(color="#E2E8F0", size=11),
        )

        # Estilo da linha de tendência
        fig_uf.update_traces(
            line=dict(color="#F59E0B", width=3), selector=dict(mode="lines")
        )

        # Linha Média Nacional
        fig_uf.add_hline(
            y=media_nacional,
            line_dash="dash",
            line_color="#10B981",
            line_width=2,
            annotation_text=f"Média Nacional: {media_nacional:.1f}",
            annotation_font=dict(color="#10B981", size=12),
        )

        # Layout Dark Mode
        fig_uf.update_layout(
            title=dict(
                text="<b>Correlação Nacional: Permanência vs. Desempenho</b>",
                font=dict(size=18, color="#F8FAFC"),
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            xaxis=dict(showgrid=True, gridcolor="#334155"),
            yaxis=dict(showgrid=True, gridcolor="#334155"),
            margin=dict(l=40, r=40, t=60, b=40),
        )

        st.plotly_chart(fig_uf, use_container_width=True, theme=None)

        # ==========================================
        # 3. CONCLUSÃO DA TELA
        # ==========================================
        st.markdown(
            """
        <div class="v0-card" style="border-top: 4px solid #10B981;">
            <h3>Insight Estratégico</h3>
            <p>Os dados confirmam: estados com maior taxa de permanência apresentam resultados superiores no ENEM. 
            Isso valida que <b>o tempo de vínculo do aluno com a escola</b> é um preditor direto do sucesso acadêmico final.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        pass
    with aba3:
        section_title(
            "Impacto da Infraestrutura: Comparativo de Quartis",
            "Análise comparativa da infraestrutura entre escolas de alta e baixa evasão.",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================
        # 1. CARREGAR E PREPARAR DADOS (Otimizado)
        # ==========================================
        @st.cache_data
        def preparar_dados_infra_quartis():
            url_menor = "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Tabela_Censo_Escolar_Menor_Evasao_2024.csv"
            url_maior = "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Tabela_Censo_Escolar_Maior_Evasao_2024.csv"

            df_menor = pd.read_csv(url_menor, sep=";")
            df_maior = pd.read_csv(url_maior, sep=";")

            colunas_infra = [
                "IN_AGUA_POTAVEL",
                "IN_ENERGIA_REDE_PUBLICA",
                "IN_ESGOTO_REDE_PUBLICA",
                "IN_BANHEIRO",
                "IN_COZINHA",
                "IN_REFEITORIO",
                "IN_QUADRA_ESPORTES",
                "IN_LABORATORIO_CIENCIAS",
                "IN_LABORATORIO_INFORMATICA",
                "IN_SALA_DIRETORIA",
                "IN_SECRETARIA",
                "IN_SALA_MULTIUSO",
                "IN_SALA_LEITURA",
                "IN_ALIMENTACAO",
                "IN_INTERNET",
                "IN_INTERNET_ALUNOS",
            ]

            # Média de infraestrutura por escola
            df_menor["MEDIA_INFRAESTRUTURA"] = (
                df_menor[colunas_infra].mean(axis=1) * 100
            )
            df_maior["MEDIA_INFRAESTRUTURA"] = (
                df_maior[colunas_infra].mean(axis=1) * 100
            )

            # Cálculos de Quartis
            df_maior["QUARTIL_INFRA"] = pd.qcut(
                df_maior["MEDIA_INFRAESTRUTURA"],
                q=4,
                labels=["Q1 (Crítico)", "Q2 (Básico)", "Q3 (Interm.)", "Q4 (Melhor)"],
                duplicates="drop",
            )
            resumo_maior = (
                df_maior.groupby("QUARTIL_INFRA", observed=False)[
                    "MEDIA_INFRAESTRUTURA"
                ]
                .mean()
                .round(1)
                .reset_index()
            )

            df_menor["QUARTIL_INFRA"] = pd.qcut(
                df_menor["MEDIA_INFRAESTRUTURA"],
                q=4,
                labels=[
                    "Q1 (Básico)",
                    "Q2 (Interm.)",
                    "Q3 (Avançado)",
                    "Q4 (Excelência)",
                ],
                duplicates="drop",
            )
            resumo_menor = (
                df_menor.groupby("QUARTIL_INFRA", observed=False)[
                    "MEDIA_INFRAESTRUTURA"
                ]
                .mean()
                .round(1)
                .reset_index()
            )

            return resumo_maior, resumo_menor

        resumo_maior, resumo_menor = preparar_dados_infra_quartis()

        # ==========================================
        # 2. GERAÇÃO DO GRÁFICO (DARK MODE)
        # ==========================================
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                "<b>MAIOR Evasão Escolar</b>",
                "<b>MENOR Evasão Escolar</b>",
            ),
            horizontal_spacing=0.15,
        )

        # Gráfico Maior Evasão (Vermelhos)
        fig.add_trace(
            go.Bar(
                y=resumo_maior["QUARTIL_INFRA"],
                x=resumo_maior["MEDIA_INFRAESTRUTURA"],
                orientation="h",
                marker=dict(color=["#fb6a4a", "#ef3b2c", "#cb181d", "#99000d"]),
                text=[f"{val}%" for val in resumo_maior["MEDIA_INFRAESTRUTURA"]],
                textposition="auto",
            ),
            row=1,
            col=1,
        )

        # Gráfico Menor Evasão (Azuis)
        fig.add_trace(
            go.Bar(
                y=resumo_menor["QUARTIL_INFRA"],
                x=resumo_menor["MEDIA_INFRAESTRUTURA"],
                orientation="h",
                marker=dict(color=["#9ecae1", "#6baed6", "#3182bd", "#08519c"]),
                text=[f"{val}%" for val in resumo_menor["MEDIA_INFRAESTRUTURA"]],
                textposition="auto",
            ),
            row=1,
            col=2,
        )

        # Layout Dark Mode
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            title_font=dict(size=18, color="#F8FAFC"),
            showlegend=False,
            height=500,
            margin=dict(t=80, b=50),
        )

        # Ajuste das grades e eixos
        fig.update_xaxes(
            title_text="<b>Infra (%)</b>",
            range=[0, 100],
            showgrid=True,
            gridcolor="#334155",
        )
        fig.update_yaxes(autorange="reversed")

        st.plotly_chart(fig, use_container_width=True, theme=None)
        pass
    with aba6:
        section_title(
            "Análise de Quadrantes: Onde o Sistema Falha",
            "Cruzando Infraestrutura e Evasão para identificar anomalias.",
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================
        # 1. CARREGAR E PREPARAR DADOS
        # ==========================================
        @st.cache_data
        def preparar_dados_anomalias():
            censo = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/01_Cleaned/Tabela_Censo_Escolar_2024.csv",
                sep=";",
            )
            evasao = pd.read_csv(
                "https://raw.githubusercontent.com/MarcilioFilh0/Data_Analysis_Education/refs/heads/main/Data/02_filtered/Maiores_Taxas_Evasao_e_Reprovacao_2024.csv"
            )

            evasao_temp = evasao.copy()
            evasao_temp["evasao_medio_total"] = pd.to_numeric(
                evasao_temp["evasao_medio_total"].replace("Não informado", np.nan),
                errors="coerce",
            )

            df = pd.merge(
                censo,
                evasao_temp,
                left_on="CO_ENTIDADE",
                right_on="codigo_escola",
                how="inner",
            )
            df = df.dropna(subset=["evasao_medio_total", "MEDIA_INFRAESTRUTURA"])
            return df

        df_anomalias = preparar_dados_anomalias()
        mediana_infra = df_anomalias["MEDIA_INFRAESTRUTURA"].median()
        mediana_evasao = df_anomalias["evasao_medio_total"].median()

        # ==========================================
        # 2. GRÁFICO DE DISPERSÃO (ESTILO LIGHT)
        # ==========================================
        # 2. GRÁFICO DE DISPERSÃO (ADAPTADO PARA DARK MODE)
        fig = px.scatter(
            df_anomalias,
            x="MEDIA_INFRAESTRUTURA",
            y="evasao_medio_total",
            color_discrete_sequence=["#F37C20"],
            opacity=0.7,
            hover_name="nome_escola",
        )

        # Linhas das Medianas
        fig.add_shape(
            type="line",
            x0=mediana_infra,
            y0=0,
            x1=mediana_infra,
            y1=100,
            line=dict(color="#62C4DA", width=2),
        )
        fig.add_shape(
            type="line",
            x0=0,
            y0=mediana_evasao,
            x1=100,
            y1=mediana_evasao,
            line=dict(color="#7E0406", width=2),
        )

        # Anotações (Fundo escuro semitransparente, letra branca)
        fig.add_annotation(
            x=90,
            y=90,
            text="<b>EXCEÇÃO 1:</b><br>Ótima Estrutura, mas<br>Alta Evasão",
            showarrow=False,
            font=dict(size=12, color="white"),
            bgcolor="rgba(30, 41, 59, 0.9)",
            bordercolor="#FCA5A5",
            borderwidth=1,
            borderpad=6,
        )
        fig.add_annotation(
            x=10,
            y=10,
            text="<b>EXCEÇÃO 2:</b><br>Péssima Estrutura, mas<br>Retém Alunos",
            showarrow=False,
            font=dict(size=12, color="white"),
            bgcolor="rgba(30, 41, 59, 0.9)",
            bordercolor="#60A5FA",
            borderwidth=1,
            borderpad=6,
        )

        # Layout Dark Mode (Transparente e Cores Claras)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0", family="Arial"),
            title=dict(
                text="<b>ANOMALIAS NA EVASÃO ESCOLAR</b>", font=dict(color="#F8FAFC")
            ),
            xaxis=dict(
                title="Índice de Infraestrutura Escolar (%)",
                gridcolor="#334155",
                range=[0, 100],
            ),
            yaxis=dict(
                title="Taxa de Evasão Escolar (%)", gridcolor="#334155", range=[0, 100]
            ),
            margin=dict(l=40, r=40, t=80, b=40),
        )

        # Grade tracejada suave (Dark Mode)
        fig.update_xaxes(
            showgrid=True, gridwidth=0.5, gridcolor="#334155", griddash="dash"
        )
        fig.update_yaxes(
            showgrid=True, gridwidth=0.2, gridcolor="#334155", griddash="dash"
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)

# --- PÁGINA 4: CONCLUSÃO ---
elif pagina == "4. O Veredito":
    page_hero(
        "Capítulo 4 · O Veredito",
        "O Veredito Final",
        "Recomendações acionáveis para gestores",
    )
    st.markdown("<hr class='v0-rule'>", unsafe_allow_html=True)

    # Banner de destaque (resumo) com CSS inline
    st.markdown(
        """
        <div class="v0-callout" style="background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(59,130,246,0.12));
            border-color: rgba(16,185,129,0.35); justify-content:center; text-align:center;">
            <div>
                <p style="font-size:17px; color:#ECFDF5;">🎯 <strong>A excelência nas notas do ENEM é a linha de chegada.
                O motor é a retenção do aluno.</strong></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-size: 16px; color: #CBD5E1;'>Não podemos buscar o atalho da tecnologia como maquiagem para problemas estruturais.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. "Cards" de UI modernos usando CSS inline
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="v0-card" style="border-top: 4px solid #3B82F6;">
                <div class="v0-card-accent" style="background: rgba(59,130,246,0.15); color:#60A5FA;">🚰</div>
                <span class="v0-tag" style="background: rgba(59,130,246,0.15); color:#60A5FA;">Prioridade 1</span>
                <h3 style="color:#60A5FA;">Sobrevivência</h3>
                <p>Garantir a <b style="color:#E2E8F0;">dignidade humana</b> básica. Erradicar escolas sem acesso à
                água potável, saneamento e energia elétrica.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="v0-card" style="border-top: 4px solid #F59E0B;">
                <div class="v0-card-accent" style="background: rgba(245,158,11,0.15); color:#FCD34D;">🤝</div>
                <span class="v0-tag" style="background: rgba(245,158,11,0.15); color:#FCD34D;">Prioridade 2</span>
                <h3 style="color:#FCD34D;">Pertencimento</h3>
                <p>Investir em <b style="color:#E2E8F0;">espaços de convivência e esporte</b> (quadras).
                A socialização cria disciplina, saúde mental e vínculo com a instituição.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="v0-card" style="border-top: 4px solid #10B981;">
                <div class="v0-card-accent" style="background: rgba(16,185,129,0.15); color:#6EE7B7;">🚀</div>
                <span class="v0-tag" style="background: rgba(16,185,129,0.15); color:#6EE7B7;">Prioridade 3</span>
                <h3 style="color:#6EE7B7;">Excelência</h3>
                <p>Implementar <b style="color:#E2E8F0;">tecnologia e inovação</b> (laboratórios, IA) de forma
                eficiente, <i>somente</i> após garantir a base estrutural.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 3. Frase final com estilo de citação reflexiva
    st.markdown(
        """
    <div style='text-align: center; padding: 32px; border: 1px solid #334155; border-radius: 16px;
        background: linear-gradient(160deg, #0F172A 0%, #131C2E 100%); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);'>
        <div style="font-size:40px; line-height:1; color:#3B5070; margin-bottom:8px;">&ldquo;</div>
        <h2 style='color: #F8FAFC; margin: 0; font-style: italic; font-weight: 400; max-width: 760px; margin: 0 auto;'>
            A escola precisa ser um ambiente onde o jovem queira estar, não um lugar do qual ele precise sobreviver.
        </h2>
    </div>
    """,
        unsafe_allow_html=True,
    )
