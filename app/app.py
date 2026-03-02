from flask import Flask, jsonify, render_template_string
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date, SmallInteger, BigInteger
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)
DATABASE_URL = "postgresql://adventure:adventure123@localhost:5432/adventureworks_oltp"
engine = create_engine(DATABASE_URL)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AdventureWorks Analytics</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  :root {
    --bg:          #ffffff;
    --sidebar:     #f7f7f5;
    --border:      #e8e8e4;
    --text:        #1a1a1a;
    --muted:       #8a8a8a;
    --light:       #b0b0b0;
    --accent:      #2563eb;
    --accent-bg:   #eff4ff;
    --accent-bdr:  #c7d9fa;
    --hover:       #f0f0ee;
    --shadow:      0 1px 3px rgba(0,0,0,.07), 0 1px 2px rgba(0,0,0,.04);
    --radius:      8px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    height: 100vh;
    display: flex;
    overflow: hidden;
    font-size: 14px;
    -webkit-font-smoothing: antialiased;
  }

  /* ── SIDEBAR ───────────────────────────────── */
  #sidebar {
    width: 248px;
    min-width: 248px;
    background: var(--sidebar);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    padding-bottom: 24px;
  }

  .sb-top {
    padding: 20px 16px 16px;
    border-bottom: 1px solid var(--border);
  }

  .sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .sb-logo {
    width: 30px; height: 30px;
    background: #1a1a1a;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: -.02em;
    flex-shrink: 0;
  }

  .sb-brand-name  { font-size: 13px; font-weight: 600; color: var(--text); }
  .sb-brand-sub   { font-size: 11px; color: var(--muted); margin-top: 1px; }

  .sb-nav { padding: 12px 8px 0; flex: 1; }

  .sb-label {
    font-size: 10.5px;
    font-weight: 500;
    color: var(--light);
    text-transform: uppercase;
    letter-spacing: .07em;
    padding: 8px 8px 4px;
  }

  .sb-item {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 8px;
    border-radius: 6px;
    cursor: pointer;
    color: var(--muted);
    font-size: 13px;
    font-weight: 400;
    transition: background .12s, color .12s;
    user-select: none;
    margin-bottom: 1px;
  }

  .sb-item:hover { background: var(--hover); color: var(--text); }
  .sb-item.active { background: var(--accent-bg); color: var(--accent); font-weight: 500; }

  .sb-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    flex-shrink: 0;
    opacity: .5;
  }
  .sb-item.active .sb-dot { opacity: 1; }

  .sb-divider { height: 1px; background: var(--border); margin: 10px 12px; }

  .sb-footer {
    padding: 12px 16px 0;
    font-size: 11px;
    color: var(--light);
    line-height: 1.6;
  }

  /* ── MAIN ──────────────────────────────────── */
  #main {
    flex: 1;
    overflow-y: auto;
    background: var(--bg);
  }

  .section { display: none; }
  .section.active { display: block; }

  /* ── PAGE SHELL ────────────────────────────── */
  .page-header {
    padding: 56px 64px 28px;
    border-bottom: 1px solid var(--border);
  }

  .page-eyebrow {
    font-size: 11px;
    font-weight: 500;
    color: var(--light);
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 10px;
  }

  .page-title {
    font-size: 30px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -.03em;
    line-height: 1.15;
    margin-bottom: 10px;
  }

  .page-desc {
    font-size: 15px;
    color: var(--muted);
    font-weight: 400;
    line-height: 1.6;
    max-width: 640px;
  }

  .page-content { padding: 36px 64px 72px; }

  /* ── HOME PAGE ─────────────────────────────── */
  .home-meta {
    display: flex;
    gap: 32px;
    margin-top: 24px;
  }

  .home-meta-item { }
  .home-meta-label { font-size: 11px; color: var(--light); text-transform: uppercase; letter-spacing: .07em; margin-bottom: 4px; }
  .home-meta-value { font-size: 13px; color: var(--text); font-weight: 500; }

  .home-divider { height: 1px; background: var(--border); margin: 36px 0; }

  .home-section-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -.01em;
    margin-bottom: 16px;
  }

  .home-body {
    font-size: 14px;
    color: #3a3a3a;
    line-height: 1.75;
    max-width: 680px;
  }

  .home-body p { margin-bottom: 14px; }
  .home-body p:last-child { margin-bottom: 0; }

  .home-cards {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 28px;
  }

  .home-card {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    background: var(--bg);
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: border-color .15s, box-shadow .15s;
  }

  .home-card:hover {
    border-color: #c0c0c0;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
  }

  .home-card-num {
    font-size: 11px;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: .07em;
    margin-bottom: 8px;
  }

  .home-card-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
    letter-spacing: -.01em;
  }

  .home-card-desc {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.55;
  }

  .home-stack {
    margin-top: 28px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .stack-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    background: var(--hover);
    color: var(--text);
    border: 1px solid var(--border);
  }

  /* ── CALLOUT ───────────────────────────────── */
  .callout {
    background: var(--accent-bg);
    border: 1px solid var(--accent-bdr);
    border-radius: var(--radius);
    padding: 12px 16px;
    font-size: 13px;
    color: #1e40af;
    margin-bottom: 28px;
    line-height: 1.6;
  }

  /* ── STAT CARDS ────────────────────────────── */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
  }

  .stat-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    box-shadow: var(--shadow);
  }

  .stat-label  { font-size: 11px; font-weight: 500; color: var(--light); text-transform: uppercase; letter-spacing: .06em; margin-bottom: 8px; }
  .stat-value  { font-size: 24px; font-weight: 700; color: var(--text); letter-spacing: -.02em; line-height: 1.1; }
  .stat-sub    { font-size: 12px; color: var(--muted); margin-top: 5px; }

  .stat-badge {
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 8px;
  }
  .b-blue   { background: var(--accent-bg);  color: var(--accent); }
  .b-green  { background: #f0fdf4; color: #16a34a; }
  .b-amber  { background: #fffbeb; color: #d97706; }
  .b-gray   { background: var(--hover); color: var(--muted); }

  /* ── CHART BLOCK ───────────────────────────── */
  .chart-block {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow);
    margin-bottom: 20px;
  }

  .chart-title { font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 4px; }
  .chart-sub   { font-size: 12px; color: var(--muted); margin-bottom: 20px; }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }

  /* ── TABLE ─────────────────────────────────── */
  .table-block {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    margin-bottom: 20px;
  }

  .table-head {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .table-count { font-size: 12px; font-weight: 400; color: var(--muted); }

  table { width: 100%; border-collapse: collapse; }
  th {
    padding: 9px 16px;
    font-size: 11px; font-weight: 500;
    color: var(--muted);
    text-align: left;
    text-transform: uppercase;
    letter-spacing: .05em;
    border-bottom: 1px solid var(--border);
    background: var(--sidebar);
  }
  td {
    padding: 10px 16px;
    font-size: 13px;
    color: var(--text);
    border-bottom: 1px solid var(--border);
  }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--hover); }

  .td-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    background: var(--hover);
    color: var(--text);
    border: 1px solid var(--border);
  }

  .td-rank {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: var(--accent-bg);
    color: var(--accent);
    font-size: 11px; font-weight: 600;
    display: flex; align-items: center; justify-content: center;
  }

  /* ── LOADING ───────────────────────────────── */
  .loading {
    display: flex; align-items: center; justify-content: center;
    padding: 56px; color: var(--muted); font-size: 13px; gap: 10px;
  }
  .spinner {
    width: 15px; height: 15px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin .6s linear infinite;
    flex-shrink: 0;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ── SCROLLBAR ─────────────────────────────── */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
</head>
<body>

<!-- SIDEBAR -->
<div id="sidebar">
  <div class="sb-top">
    <div class="sb-brand">
      <div class="sb-logo">AW</div>
      <div>
        <div class="sb-brand-name">AdventureWorks</div>
        <div class="sb-brand-sub">Taller 02 — Analytics</div>
      </div>
    </div>
  </div>

  <div class="sb-nav">
    <div class="sb-label">General</div>
    <div class="sb-item active" onclick="showPage('home', this)">
      <div class="sb-dot"></div>
      Inicio
    </div>

    <div class="sb-divider"></div>
    <div class="sb-label">Análisis</div>

    <div class="sb-item" onclick="showPage('p1', this)">
      <div class="sb-dot"></div>
      Clientes Recurrentes
    </div>
    <div class="sb-item" onclick="showPage('p2', this)">
      <div class="sb-dot"></div>
      Varianza de Margen
    </div>
    <div class="sb-item" onclick="showPage('p3', this)">
      <div class="sb-dot"></div>
      Análisis de Canasta
    </div>
    <div class="sb-item" onclick="showPage('p4', this)">
      <div class="sb-dot"></div>
      Cohortes
    </div>
  </div>

  <div class="sb-divider"></div>
  <div class="sb-footer">
    Análisis de Datos<br>
    P. Universidad Javeriana — 2026
  </div>
</div>

<!-- MAIN -->
<div id="main">

  <!-- HOME -->
  <div id="home" class="section active">
    <div class="page-header">
      <div class="page-eyebrow">Taller 02</div>
      <div class="page-title">Pipeline ETL y Modelo OLAP<br>sobre AdventureWorks</div>
      <div class="page-desc">
        Diseño e implementación de un proceso ETL desde SQL Server hacia PostgreSQL,
        construcción de un modelo dimensional en estrella y análisis de cuatro preguntas de negocio.
      </div>
      <div class="home-meta">
        <div class="home-meta-item">
          <div class="home-meta-label">Autor</div>
          <div class="home-meta-value">Juan Sebastián Cruz Rojas</div>
        </div>
        <div class="home-meta-item">
          <div class="home-meta-label">Materia</div>
          <div class="home-meta-value">Análisis de Datos</div>
        </div>
        <div class="home-meta-item">
          <div class="home-meta-label">Universidad</div>
          <div class="home-meta-value">Pontificia Universidad Javeriana</div>
        </div>
        <div class="home-meta-item">
          <div class="home-meta-label">Año</div>
          <div class="home-meta-value">2026</div>
        </div>
      </div>
    </div>

    <div class="page-content">

      <div class="home-section-title">Descripción del proyecto</div>
      <div class="home-body">
        <p>
          Este taller implementa un pipeline ETL completo sobre la base de datos
          <strong>AdventureWorks 2025</strong>, restaurada desde un backup de SQL Server 2025.
          Los datos son extraídos, transformados y cargados hacia un modelo OLAP
          en PostgreSQL 18, siguiendo un esquema en estrella con dimensiones
          de fecha, cliente, producto y territorio.
        </p>
        <p>
          A partir del modelo dimensional se responden cuatro preguntas de negocio
          concretas que permiten tomar decisiones sobre clientes, márgenes,
          combinaciones de productos y cohortes de adquisición.
        </p>
        <p>
          La capa de presentación es esta aplicación web construida con Flask y
          SQLAlchemy, que consulta directamente el esquema OLAP y visualiza
          los resultados con Chart.js.
        </p>
      </div>

      <div class="home-divider"></div>

      <div class="home-section-title">Preguntas de negocio</div>
      <div class="home-cards">
        <div class="home-card" onclick="navTo('p1')">
          <div class="home-card-num">Pregunta 1</div>
          <div class="home-card-title">Clientes Recurrentes vs Únicos</div>
          <div class="home-card-desc">
            Qué porción de los ingresos totales es generada por clientes que han realizado
            más de una compra frente a quienes solo compraron una vez.
          </div>
        </div>
        <div class="home-card" onclick="navTo('p2')">
          <div class="home-card-num">Pregunta 2</div>
          <div class="home-card-title">Varianza de Margen por Producto</div>
          <div class="home-card-desc">
            Qué productos presentan mayor varianza en su margen de ganancia,
            relevante para decisiones de compra de temporada navideña.
          </div>
        </div>
        <div class="home-card" onclick="navTo('p3')">
          <div class="home-card-num">Pregunta 3</div>
          <div class="home-card-title">Análisis de Canasta</div>
          <div class="home-card-desc">
            Qué parejas de productos son compradas juntas con mayor frecuencia
            en una misma transacción, para estrategias de venta cruzada.
          </div>
        </div>
        <div class="home-card" onclick="navTo('p4')">
          <div class="home-card-num">Pregunta 4</div>
          <div class="home-card-title">Análisis de Cohortes</div>
          <div class="home-card-desc">
            Cuáles son las tres cohortes de clientes con mayor margen total,
            agrupadas por el mes en que realizaron su primera compra.
          </div>
        </div>
      </div>

      <div class="home-divider"></div>

      <div class="home-section-title">Stack tecnológico</div>
      <div class="home-stack">
        <span class="stack-tag">Python 3.13</span>
        <span class="stack-tag">Flask 3.1</span>
        <span class="stack-tag">SQLAlchemy 2.0</span>
        <span class="stack-tag">PostgreSQL 18</span>
        <span class="stack-tag">SQL Server 2025</span>
        <span class="stack-tag">Chart.js</span>
        <span class="stack-tag">Podman</span>
        <span class="stack-tag">AdventureWorks 2025</span>
      </div>

      <div class="home-divider"></div>

      <div class="home-section-title">Modelo dimensional</div>
      <div class="home-body">
        <p>
          El esquema OLAP sigue una arquitectura en estrella con una tabla de hechos central
          <strong>fact_sales</strong> (121,317 registros) y cuatro dimensiones:
          <strong>dim_date</strong> (1,139 fechas),
          <strong>dim_customer</strong> (19,820 clientes),
          <strong>dim_product</strong> (504 productos) y
          <strong>dim_territory</strong> (10 territorios).
        </p>
        <p>
          La tabla de hechos almacena métricas calculadas como
          <code>line_cost</code>, <code>line_margin</code> y <code>margin_pct</code>,
          además de la fecha de primera compra y la cohorte de cada cliente
          en las dimensiones correspondientes.
        </p>
      </div>

    </div>
  </div>

  <!-- P1 -->
  <div id="p1" class="section">
    <div class="page-header">
      <div class="page-eyebrow">Pregunta 1</div>
      <div class="page-title">Clientes Recurrentes vs Únicos</div>
      <div class="page-desc">
        Porción de ingresos generados por clientes con más de una compra
        frente a clientes de una sola transacción.
      </div>
    </div>
    <div class="page-content">
      <div class="callout">
        Un cliente recurrente ha realizado más de una orden distinta dentro del periodo analizado.
        Esta métrica refleja directamente la fidelización y el valor a largo plazo del cliente.
      </div>
      <div id="p1-cards" class="stat-grid">
        <div class="loading"><div class="spinner"></div> Cargando datos...</div>
      </div>
      <div class="two-col">
        <div class="chart-block">
          <div class="chart-title">Distribución de Ingresos</div>
          <div class="chart-sub">Recurrentes vs Únicos</div>
          <canvas id="p1-pie" height="200"></canvas>
        </div>
        <div class="chart-block">
          <div class="chart-title">Comparativa de Ingresos</div>
          <div class="chart-sub">Total por tipo de cliente</div>
          <canvas id="p1-bar" height="200"></canvas>
        </div>
      </div>
    </div>
  </div>

  <!-- P2 -->
  <div id="p2" class="section">
    <div class="page-header">
      <div class="page-eyebrow">Pregunta 2</div>
      <div class="page-title">Varianza de Margen por Producto</div>
      <div class="page-desc">
        Productos con mayor varianza en su margen de ganancia, relevantes para
        decisiones de compra de temporada navideña antes del 10 de abril.
      </div>
    </div>
    <div class="page-content">
      <div class="callout">
        Alta varianza indica precios o costos inestables en el tiempo.
        Los productos con mayor varianza requieren análisis adicional antes
        de incluirlos en pedidos de gran volumen.
      </div>
      <div class="chart-block">
        <div class="chart-title">Top 20 — Varianza de Margen</div>
        <div class="chart-sub">Mayor varianza implica mayor riesgo e incertidumbre en el margen</div>
        <canvas id="p2-chart" height="100"></canvas>
      </div>
      <div class="table-block">
        <div class="table-head">
          <span>Detalle de Productos</span>
          <span class="table-count" id="p2-count"></span>
        </div>
        <div id="p2-table"><div class="loading"><div class="spinner"></div> Cargando datos...</div></div>
      </div>
    </div>
  </div>

  <!-- P3 -->
  <div id="p3" class="section">
    <div class="page-header">
      <div class="page-eyebrow">Pregunta 3</div>
      <div class="page-title">Análisis de Canasta</div>
      <div class="page-desc">
        Identificación de los pares de productos comprados juntos con mayor frecuencia
        dentro de una misma transacción.
      </div>
    </div>
    <div class="page-content">
      <div class="callout">
        El análisis de canasta (market basket analysis) permite identificar
        combinaciones de productos para venta cruzada, bundles o ubicación
        estratégica en tienda y plataformas digitales.
      </div>
      <div class="chart-block">
        <div class="chart-title">Top 10 — Parejas de Productos</div>
        <div class="chart-sub">Número de transacciones donde ambos productos aparecen juntos</div>
        <canvas id="p3-chart" height="80"></canvas>
      </div>
      <div class="table-block">
        <div class="table-head">
          <span>Parejas más frecuentes</span>
          <span class="table-count" id="p3-count"></span>
        </div>
        <div id="p3-table"><div class="loading"><div class="spinner"></div> Cargando datos...</div></div>
      </div>
    </div>
  </div>

  <!-- P4 -->
  <div id="p4" class="section">
    <div class="page-header">
      <div class="page-eyebrow">Pregunta 4</div>
      <div class="page-title">Análisis de Cohortes</div>
      <div class="page-desc">
        Clientes agrupados por el mes de su primera compra. Se identifican las tres
        cohortes con mayor margen total acumulado.
      </div>
    </div>
    <div class="page-content">
      <div class="callout">
        Una cohorte agrupa clientes cuya primera compra ocurrió en el mismo mes.
        Analizar el margen por cohorte permite evaluar la calidad de cada
        campaña de adquisición de clientes.
      </div>
      <div id="p4-cards" class="stat-grid">
        <div class="loading"><div class="spinner"></div> Cargando datos...</div>
      </div>
      <div class="chart-block">
        <div class="chart-title">Margen Total por Cohorte</div>
        <div class="chart-sub">Todas las cohortes ordenadas por margen descendente — top 3 destacados</div>
        <canvas id="p4-chart" height="80"></canvas>
      </div>
      <div class="table-block">
        <div class="table-head">
          <span>Detalle por Cohorte</span>
          <span class="table-count" id="p4-count"></span>
        </div>
        <div id="p4-table"><div class="loading"><div class="spinner"></div> Cargando datos...</div></div>
      </div>
    </div>
  </div>

</div><!-- /main -->

<script>
  const fmt  = n => parseFloat(n).toLocaleString('es-CO', {minimumFractionDigits:0, maximumFractionDigits:0});
  const fmtM = n => '$' + fmt(n);
  const fmtD = n => parseFloat(n).toFixed(2);

  Chart.defaults.font  = { family: "Inter, -apple-system, sans-serif", size: 12 };
  Chart.defaults.color = '#8a8a8a';

  let charts = {}, loaded = {};

  function showPage(id, el) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.sb-item').forEach(b => b.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    el.classList.add('active');
    if (!loaded[id]) { loadPage(id); loaded[id] = true; }
  }

  function navTo(id) {
    const el = document.querySelector(`.sb-item[onclick="showPage('${id}', this)"]`);
    showPage(id, el);
  }

  function loadPage(id) {
    if (id === 'p1') loadP1();
    if (id === 'p2') loadP2();
    if (id === 'p3') loadP3();
    if (id === 'p4') loadP4();
  }

  // ── P1 ──────────────────────────────────────────────────────
  async function loadP1() {
    const d = await fetch('/api/p1').then(r => r.json());
    const total = d.recurrentes.ingresos + d.unicos.ingresos;
    const pR = (d.recurrentes.ingresos / total * 100).toFixed(1);
    const pU = (100 - pR).toFixed(1);

    document.getElementById('p1-cards').innerHTML = `
      <div class="stat-card">
        <div class="stat-label">Clientes Recurrentes</div>
        <div class="stat-value">${fmt(d.recurrentes.clientes)}</div>
        <div class="stat-sub">Más de una compra</div>
        <span class="stat-badge b-blue">${pR}% de los ingresos</span>
      </div>
      <div class="stat-card">
        <div class="stat-label">Clientes Únicos</div>
        <div class="stat-value">${fmt(d.unicos.clientes)}</div>
        <div class="stat-sub">Solo una compra</div>
        <span class="stat-badge b-amber">${pU}% de los ingresos</span>
      </div>
      <div class="stat-card">
        <div class="stat-label">Ingresos Recurrentes</div>
        <div class="stat-value">${fmtM(d.recurrentes.ingresos)}</div>
        <div class="stat-sub">Generados por clientes fieles</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Ingresos Totales</div>
        <div class="stat-value">${fmtM(total)}</div>
        <div class="stat-sub">Periodo completo</div>
        <span class="stat-badge b-gray">100%</span>
      </div>`;

    charts.p1pie = new Chart(document.getElementById('p1-pie'), {
      type: 'doughnut',
      data: {
        labels: ['Recurrentes', 'Únicos'],
        datasets: [{ data: [d.recurrentes.ingresos, d.unicos.ingresos],
          backgroundColor: ['#2563eb', '#e5e7eb'],
          borderWidth: 0, hoverOffset: 4 }]
      },
      options: {
        cutout: '70%',
        plugins: { legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } } }
      }
    });

    charts.p1bar = new Chart(document.getElementById('p1-bar'), {
      type: 'bar',
      data: {
        labels: ['Recurrentes', 'Únicos'],
        datasets: [{ data: [d.recurrentes.ingresos, d.unicos.ingresos],
          backgroundColor: ['#2563eb', '#e5e7eb'], borderRadius: 6, borderSkipped: false }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: { grid: { color: '#f0f0ee' }, border: { display: false } }
        }
      }
    });
  }

  // ── P2 ──────────────────────────────────────────────────────
  async function loadP2() {
    const d = await fetch('/api/p2').then(r => r.json());
    document.getElementById('p2-count').textContent = d.length + ' productos';

    charts.p2 = new Chart(document.getElementById('p2-chart'), {
      type: 'bar',
      data: {
        labels: d.map(r => r.product_name.substring(0, 26)),
        datasets: [{ label: 'Varianza Margen %', data: d.map(r => r.variance),
          backgroundColor: '#2563eb', borderRadius: 4, borderSkipped: false }]
      },
      options: {
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: '#f0f0ee' }, border: { display: false } },
          y: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 11 } } }
        }
      }
    });

    document.getElementById('p2-table').innerHTML = `
      <table>
        <thead><tr><th>#</th><th>Producto</th><th>Categoría</th><th>Varianza</th><th>Margen Prom.</th><th>Ventas</th></tr></thead>
        <tbody>${d.map((r, i) => `
          <tr>
            <td><div class="td-rank">${i+1}</div></td>
            <td style="font-weight:500">${r.product_name}</td>
            <td><span class="td-badge">${r.category || 'Sin categoría'}</span></td>
            <td>${fmtD(r.variance)}</td>
            <td>${fmtD(r.avg_margin)}%</td>
            <td>${fmt(r.total_sales)}</td>
          </tr>`).join('')}
        </tbody>
      </table>`;
  }

  // ── P3 ──────────────────────────────────────────────────────
  async function loadP3() {
    const d = await fetch('/api/p3').then(r => r.json());
    document.getElementById('p3-count').textContent = d.length + ' parejas';

    charts.p3 = new Chart(document.getElementById('p3-chart'), {
      type: 'bar',
      data: {
        labels: d.map(r => r.product1.substring(0,18) + ' + ' + r.product2.substring(0,18)),
        datasets: [{ label: 'Ocurrencias', data: d.map(r => r.ocurrencias),
          backgroundColor: '#2563eb', borderRadius: 4, borderSkipped: false }]
      },
      options: {
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: '#f0f0ee' }, border: { display: false } },
          y: { grid: { display: false }, border: { display: false }, ticks: { font: { size: 10 } } }
        }
      }
    });

    document.getElementById('p3-table').innerHTML = `
      <table>
        <thead><tr><th>#</th><th>Producto 1</th><th>Producto 2</th><th>Ocurrencias</th></tr></thead>
        <tbody>${d.map((r, i) => `
          <tr>
            <td><div class="td-rank">${i+1}</div></td>
            <td style="font-weight:500">${r.product1}</td>
            <td>${r.product2}</td>
            <td><span class="stat-badge b-blue" style="margin:0">${fmt(r.ocurrencias)}</span></td>
          </tr>`).join('')}
        </tbody>
      </table>`;
  }

  // ── P4 ──────────────────────────────────────────────────────
  async function loadP4() {
    const d = await fetch('/api/p4').then(r => r.json());
    document.getElementById('p4-count').textContent = d.all.length + ' cohortes';

    document.getElementById('p4-cards').innerHTML = d.top3.map((r, i) => `
      <div class="stat-card">
        <div class="stat-label">${['1er', '2do', '3er'][i]} Lugar</div>
        <div class="stat-value" style="font-size:20px">${r.cohort}</div>
        <div class="stat-sub">${fmt(r.customers)} clientes &middot; ${fmt(r.orders)} órdenes</div>
        <span class="stat-badge b-blue">Margen ${fmtM(r.total_margin)}</span>
      </div>`).join('');

    charts.p4 = new Chart(document.getElementById('p4-chart'), {
      type: 'bar',
      data: {
        labels: d.all.map(r => r.cohort),
        datasets: [{ label: 'Margen Total', data: d.all.map(r => r.total_margin),
          backgroundColor: d.all.map((_, i) => i < 3 ? '#2563eb' : '#bfdbfe'),
          borderRadius: 4, borderSkipped: false }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, border: { display: false }, ticks: { maxRotation: 45, font: { size: 10 } } },
          y: { grid: { color: '#f0f0ee' }, border: { display: false } }
        }
      }
    });

    document.getElementById('p4-table').innerHTML = `
      <table>
        <thead><tr><th>#</th><th>Cohorte</th><th>Clientes</th><th>Margen Total</th><th>Margen Prom.</th><th>Órdenes</th></tr></thead>
        <tbody>${d.all.map((r, i) => `
          <tr>
            <td><div class="td-rank" style="${i<3 ? 'background:#eff4ff;color:#2563eb' : ''}">${i+1}</div></td>
            <td><span class="td-badge">${r.cohort}</span></td>
            <td>${fmt(r.customers)}</td>
            <td style="font-weight:${i<3?'600':'400'}">${fmtM(r.total_margin)}</td>
            <td>${fmtM(r.avg_margin)}</td>
            <td>${fmt(r.orders)}</td>
          </tr>`).join('')}
        </tbody>
      </table>`;
  }
</script>
</body>
</html>
"""

class Base(DeclarativeBase):
    pass

class DimCustomer(Base):
    __tablename__ = 'dim_customer'
    __table_args__ = {'schema': 'olap'}
    customer_key = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    full_name = Column(String)
    customer_type = Column(String)
    cohort_year_month = Column(String)
    first_purchase_date = Column(Date)

class DimProduct(Base):
    __tablename__ = 'dim_product'
    __table_args__ = {'schema': 'olap'}
    product_key = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    product_name = Column(String)
    category = Column(String)
    subcategory = Column(String)

class DimTerritory(Base):
    __tablename__ = 'dim_territory'
    __table_args__ = {'schema': 'olap'}
    territory_key = Column(Integer, primary_key=True)
    territory_name = Column(String)

class FactSales(Base):
    __tablename__ = 'fact_sales'
    __table_args__ = {'schema': 'olap'}
    sale_key = Column(BigInteger, primary_key=True)
    order_id = Column(Integer)
    customer_key = Column(Integer)
    product_key = Column(Integer)
    territory_key = Column(Integer)
    order_quantity = Column(SmallInteger)
    unit_price = Column(Numeric)
    line_total = Column(Numeric)
    line_margin = Column(Numeric)
    margin_pct = Column(Numeric)
    order_date = Column(Date)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/p1')
def p1():
    with Session(engine) as session:
        result = session.execute(text("""
            WITH cpc AS (
                SELECT customer_key, COUNT(DISTINCT order_id) as n, SUM(line_total) as ing
                FROM olap.fact_sales GROUP BY customer_key
            ),
            cls AS (
                SELECT CASE WHEN n > 1 THEN 'recurrente' ELSE 'unico' END as tipo,
                COUNT(*) as clientes, SUM(ing) as ingresos
                FROM cpc GROUP BY CASE WHEN n > 1 THEN 'recurrente' ELSE 'unico' END
            )
            SELECT tipo, clientes, ingresos FROM cls
        """)).fetchall()
        data = {'recurrentes': {'clientes': 0, 'ingresos': 0}, 'unicos': {'clientes': 0, 'ingresos': 0}}
        for r in result:
            k = 'recurrentes' if r[0] == 'recurrente' else 'unicos'
            data[k] = {'clientes': int(r[1]), 'ingresos': float(r[2])}
        return jsonify(data)

@app.route('/api/p2')
def p2():
    with Session(engine) as session:
        result = session.execute(text("""
            SELECT p.product_name, p.category,
                VARIANCE(f.margin_pct) as variance,
                AVG(f.margin_pct) as avg_margin,
                COUNT(*) as total_sales
            FROM olap.fact_sales f
            JOIN olap.dim_product p ON f.product_key = p.product_key
            WHERE f.margin_pct IS NOT NULL
            GROUP BY p.product_key, p.product_name, p.category
            HAVING COUNT(*) > 5
            ORDER BY variance DESC NULLS LAST LIMIT 20
        """)).fetchall()
        return jsonify([{'product_name': r[0], 'category': r[1],
            'variance': float(r[2]) if r[2] else 0,
            'avg_margin': float(r[3]) if r[3] else 0,
            'total_sales': int(r[4])} for r in result])

@app.route('/api/p3')
def p3():
    with Session(engine) as session:
        result = session.execute(text("""
            SELECT p1.product_name, p2.product_name, COUNT(*) as occ
            FROM olap.fact_sales f1
            JOIN olap.fact_sales f2 ON f1.order_id = f2.order_id AND f1.product_key < f2.product_key
            JOIN olap.dim_product p1 ON f1.product_key = p1.product_key
            JOIN olap.dim_product p2 ON f2.product_key = p2.product_key
            GROUP BY p1.product_name, p2.product_name
            ORDER BY occ DESC LIMIT 10
        """)).fetchall()
        return jsonify([{'product1': r[0], 'product2': r[1], 'ocurrencias': int(r[2])} for r in result])

@app.route('/api/p4')
def p4():
    with Session(engine) as session:
        result = session.execute(text("""
            SELECT dc.cohort_year_month,
                COUNT(DISTINCT f.customer_key) as customers,
                SUM(f.line_margin) as total_margin,
                AVG(f.line_margin) as avg_margin,
                COUNT(DISTINCT f.order_id) as orders
            FROM olap.fact_sales f
            JOIN olap.dim_customer dc ON f.customer_key = dc.customer_key
            WHERE dc.cohort_year_month IS NOT NULL
            GROUP BY dc.cohort_year_month
            ORDER BY total_margin DESC
        """)).fetchall()
        all_data = [{'cohort': r[0], 'customers': int(r[1]),
            'total_margin': float(r[2]) if r[2] else 0,
            'avg_margin': float(r[3]) if r[3] else 0,
            'orders': int(r[4])} for r in result]
        return jsonify({'top3': all_data[:3], 'all': all_data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)