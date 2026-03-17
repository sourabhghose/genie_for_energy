#!/usr/bin/env python3
"""Generate professional documentation images from real workspace data."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

DB_DARK = '#1B3139'
DB_RED = '#FF3621'
DB_ORANGE = '#FF6F61'
DB_GRAY = '#F5F5F5'
DB_LIGHT_GRAY = '#E8E8E8'
DB_TEXT = '#1B3139'
DB_MUTED = '#6B7280'
DB_WHITE = '#FFFFFF'
DB_GREEN = '#10B981'
DB_BLUE = '#3B82F6'


def generate_catalog_tables_image():
    """Image 1: Catalog Explorer showing 7 energy tables with real row counts."""
    tables = [
        ('raw_meter_readings', '10,685,000', 'MANAGED', 'DELTA'),
        ('raw_billing', '603,047', 'MANAGED', 'DELTA'),
        ('raw_customers', '50,000', 'MANAGED', 'DELTA'),
        ('raw_demand_response', '20,000', 'MANAGED', 'DELTA'),
        ('raw_outages', '5,000', 'MANAGED', 'DELTA'),
        ('raw_equipment', '2,000', 'MANAGED', 'DELTA'),
        ('raw_weather', '1,825', 'MANAGED', 'DELTA'),
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.3, 7.8), 11.4, 0.9, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.7, 8.25, 'Catalog Explorer', fontsize=14, fontweight='bold',
            color=DB_WHITE, fontfamily='sans-serif')
    ax.text(6, 8.25, 'main  >  sourabh_energy_workshop',
            fontsize=11, color='#94A3B8', fontfamily='sans-serif')

    headers = ['Table Name', 'Rows', 'Type', 'Format']
    header_x = [0.7, 6.5, 8.5, 10.2]
    for i, h in enumerate(headers):
        ax.text(header_x[i], 7.3, h, fontsize=10, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.5, 11.5], [7.1, 7.1], color=DB_LIGHT_GRAY, linewidth=1)

    for idx, (name, rows, ttype, fmt) in enumerate(tables):
        y = 6.5 - idx * 0.85
        bg_color = '#F8FAFC' if idx % 2 == 0 else DB_WHITE
        ax.add_patch(FancyBboxPatch((0.4, y - 0.25), 11.2, 0.7,
                                    boxstyle="round,pad=0.05",
                                    facecolor=bg_color, edgecolor='none'))
        ax.text(0.7, y + 0.05, name, fontsize=11, color=DB_TEXT,
                fontfamily='monospace', fontweight='bold')
        ax.text(6.5, y + 0.05, rows, fontsize=11, color=DB_TEXT,
                fontfamily='sans-serif', ha='left')
        ax.text(8.5, y + 0.05, ttype, fontsize=9, color=DB_GREEN,
                fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ECFDF5', edgecolor='none'))
        ax.text(10.2, y + 0.05, fmt, fontsize=9, color=DB_BLUE,
                fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='none'))

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '03-catalog-tables.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 03-catalog-tables.png')


def generate_customers_schema_image():
    """Image 2: raw_customers table schema with real column data."""
    columns = [
        ('account_id', 'STRING', 'Primary customer account identifier'),
        ('customer_name', 'STRING', 'Full name of the customer'),
        ('street_address', 'STRING', 'Street address'),
        ('city', 'STRING', 'City name'),
        ('state', 'STRING', 'US state code'),
        ('zipcode', 'STRING', 'ZIP code'),
        ('region', 'STRING', 'Service region (Northeast, Southeast, etc.)'),
        ('customer_type', 'STRING', 'residential / commercial / industrial'),
        ('rate_plan', 'STRING', 'Pricing plan (fixed, variable, TOU, EV)'),
        ('signup_date', 'DATE', 'Account creation date'),
        ('contract_end_date', 'DATE', 'Contract expiration date'),
        ('has_solar', 'BOOLEAN', 'Has solar panel installation'),
        ('has_ev', 'BOOLEAN', 'Has electric vehicle'),
        ('demand_response_enrolled', 'BOOLEAN', 'Enrolled in DR program'),
    ]

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.3, 9.8), 11.4, 0.9, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.7, 10.25, 'raw_customers', fontsize=14, fontweight='bold',
            color=DB_WHITE, fontfamily='monospace')
    ax.text(6, 10.25, 'main.sourabh_energy_workshop | 50,000 rows',
            fontsize=11, color='#94A3B8', fontfamily='sans-serif')

    tab_y = 9.4
    ax.add_patch(FancyBboxPatch((0.5, tab_y - 0.15), 1.8, 0.45,
                                boxstyle="round,pad=0.05",
                                facecolor=DB_WHITE, edgecolor=DB_BLUE, linewidth=1.5))
    ax.text(1.4, tab_y + 0.05, 'Schema', fontsize=10, fontweight='bold',
            color=DB_BLUE, ha='center', fontfamily='sans-serif')
    ax.text(3.2, tab_y + 0.05, 'Sample Data', fontsize=10,
            color=DB_MUTED, fontfamily='sans-serif')

    headers = ['Column', 'Type', 'Description']
    header_x = [0.7, 4.5, 6.5]
    for i, h in enumerate(headers):
        ax.text(header_x[i], 8.8, h, fontsize=10, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.5, 11.5], [8.6, 8.6], color=DB_LIGHT_GRAY, linewidth=1)

    for idx, (name, dtype, desc) in enumerate(columns):
        y = 8.2 - idx * 0.55
        bg = '#F8FAFC' if idx % 2 == 0 else DB_WHITE
        ax.add_patch(plt.Rectangle((0.4, y - 0.2), 11.2, 0.5,
                                   facecolor=bg, edgecolor='none'))
        ax.text(0.7, y, name, fontsize=10, color=DB_TEXT,
                fontfamily='monospace', fontweight='bold')
        type_colors = {
            'STRING': ('#7C3AED', '#F5F3FF'),
            'DATE': ('#D97706', '#FFFBEB'),
            'BOOLEAN': ('#059669', '#ECFDF5'),
        }
        tc, bg_c = type_colors.get(dtype, ('#6B7280', '#F3F4F6'))
        ax.text(4.5, y, dtype, fontsize=9, color=tc, fontfamily='sans-serif',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=bg_c, edgecolor='none'))
        ax.text(6.5, y, desc, fontsize=9, color=DB_MUTED, fontfamily='sans-serif')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '04-customers-schema.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 04-customers-schema.png')


def generate_customers_sample_image():
    """Image 3: Sample data from raw_customers."""
    cols = ['account_id', 'customer_name', 'city', 'state', 'customer_type', 'rate_plan', 'has_solar']
    rows = [
        ['ACCT-012501', 'Jesus Simpson', 'North Brandon', 'CO', 'residential', 'variable', 'false'],
        ['ACCT-012502', 'Gabriella Richardson', 'Kristinaton', 'AS', 'residential', 'EV', 'false'],
        ['ACCT-012503', 'Victoria Wiley', 'Vanessatown', 'RI', 'residential', 'TOU', 'false'],
        ['ACCT-012504', 'Miss Sarah Garcia', 'South Coleburgh', 'TX', 'residential', 'EV', 'false'],
        ['ACCT-012505', 'Danielle Bowman', 'West Michael', 'TX', 'residential', 'fixed', 'false'],
    ]

    fig, ax = plt.subplots(figsize=(14, 4.5))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.1, 4.5), 13.8, 0.8, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.5, 4.85, 'raw_customers', fontsize=13, fontweight='bold',
            color=DB_WHITE, fontfamily='monospace')
    ax.text(4, 4.85, 'Sample Data (5 of 50,000 rows)',
            fontsize=10, color='#94A3B8', fontfamily='sans-serif')

    col_x = [0.3, 2.2, 4.5, 6.8, 8.0, 9.5, 11.0]
    for i, c in enumerate(cols):
        ax.text(col_x[i], 4.1, c, fontsize=8.5, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.2, 13.8], [3.9, 3.9], color=DB_LIGHT_GRAY, linewidth=1)

    for ridx, row in enumerate(rows):
        y = 3.5 - ridx * 0.7
        bg = '#F8FAFC' if ridx % 2 == 0 else DB_WHITE
        ax.add_patch(plt.Rectangle((0.15, y - 0.25), 13.7, 0.6,
                                   facecolor=bg, edgecolor='none'))
        for cidx, val in enumerate(row):
            ax.text(col_x[cidx], y, val, fontsize=8.5, color=DB_TEXT,
                    fontfamily='monospace' if cidx == 0 else 'sans-serif')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '04-customers-sample.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 04-customers-sample.png')


def generate_workshop_folder_image():
    """Image 4: Workspace browser showing workshop notebooks."""
    notebooks = [
        ('00_generate_energy_data', 'Python', 'Mar 14, 2026'),
        ('01_energy_data_explorer', 'Python', 'Mar 14, 2026'),
        ('02_data_engineering_prompt_guide', 'Python', 'Mar 14, 2026'),
        ('03_data_science_prompt_guide', 'Python', 'Mar 14, 2026'),
        ('04_dashboard_prompt_guide', 'Python', 'Mar 14, 2026'),
        ('04b_debugging_prompt_guide', 'Python', 'Mar 14, 2026'),
        ('04b_broken_notebook', 'Python', 'Mar 14, 2026'),
        ('06_genai_observability_prompt_guide', 'Python', 'Mar 14, 2026'),
        ('07_system_table_queries', 'Python', 'Mar 14, 2026'),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.3, 8.8), 11.4, 0.9, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.7, 9.25, 'Workspace', fontsize=14, fontweight='bold',
            color=DB_WHITE, fontfamily='sans-serif')
    ax.text(3.2, 9.25,
            'Users / sourabh.ghose@databricks.com / genie-code-energy-workshop',
            fontsize=10, color='#94A3B8', fontfamily='sans-serif')

    headers = ['Name', 'Language', 'Modified']
    header_x = [1.0, 8.0, 10.0]
    for i, h in enumerate(headers):
        ax.text(header_x[i], 8.3, h, fontsize=10, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.5, 11.5], [8.1, 8.1], color=DB_LIGHT_GRAY, linewidth=1)

    for idx, (name, lang, modified) in enumerate(notebooks):
        y = 7.5 - idx * 0.8
        bg = '#F8FAFC' if idx % 2 == 0 else DB_WHITE
        ax.add_patch(plt.Rectangle((0.4, y - 0.25), 11.2, 0.7,
                                   facecolor=bg, edgecolor='none'))
        ax.text(0.7, y + 0.05, '\u2630', fontsize=12, color=DB_BLUE)
        ax.text(1.0, y + 0.05, name, fontsize=10, color=DB_TEXT,
                fontfamily='monospace', fontweight='bold')
        ax.text(8.0, y + 0.05, lang, fontsize=9, color='#7C3AED',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#F5F3FF', edgecolor='none'))
        ax.text(10.0, y + 0.05, modified, fontsize=9, color=DB_MUTED)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '01-workshop-folder.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 01-workshop-folder.png')


def generate_skills_folder_image():
    """Image 5: Agent Skills folder showing 10 skills."""
    skills = [
        ('energy-analytics', 'Energy KPIs, grid reliability, load factor'),
        ('regulatory-compliance', 'NERC/FERC standards, compliance checks'),
        ('carbon-reporting', 'Carbon footprint, emissions tracking'),
        ('customer-communications', 'Bill explanations, outage notifications'),
        ('ai-functions-energy', 'ai_forecast, ai_classify for energy data'),
        ('genie-space-creator', 'Programmatic Genie Space creation via API'),
        ('dashboard-deployer', 'Deploy AI/BI dashboards via REST API'),
        ('job-deployer', 'Create and schedule Databricks Jobs'),
        ('pipeline-scaffolder', 'Scaffold Lakeflow SDP pipelines'),
        ('knowledge-assistant-creator', 'Create RAG-based knowledge assistants'),
    ]

    fig, ax = plt.subplots(figsize=(12, 7.5))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.3, 9.8), 11.4, 0.9, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.7, 10.25, 'Workspace', fontsize=14, fontweight='bold',
            color=DB_WHITE, fontfamily='sans-serif')
    ax.text(3.2, 10.25,
            'Users / sourabh.ghose / .assistant / skills',
            fontsize=10, color='#94A3B8', fontfamily='sans-serif')

    headers = ['Skill Name', 'Description']
    header_x = [1.0, 5.5]
    for i, h in enumerate(headers):
        ax.text(header_x[i], 9.3, h, fontsize=10, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.5, 11.5], [9.1, 9.1], color=DB_LIGHT_GRAY, linewidth=1)

    tier_colors = {
        0: ('#10B981', '#ECFDF5', 'Knowledge'),
        1: ('#10B981', '#ECFDF5', 'Knowledge'),
        2: ('#10B981', '#ECFDF5', 'Knowledge'),
        3: ('#10B981', '#ECFDF5', 'Knowledge'),
        4: ('#D97706', '#FFFBEB', 'AI Functions'),
        5: ('#EF4444', '#FEF2F2', 'Creator'),
        6: ('#EF4444', '#FEF2F2', 'Creator'),
        7: ('#EF4444', '#FEF2F2', 'Creator'),
        8: ('#EF4444', '#FEF2F2', 'Creator'),
        9: ('#EF4444', '#FEF2F2', 'Creator'),
    }

    for idx, (name, desc) in enumerate(skills):
        y = 8.5 - idx * 0.8
        bg = '#F8FAFC' if idx % 2 == 0 else DB_WHITE
        ax.add_patch(plt.Rectangle((0.4, y - 0.25), 11.2, 0.7,
                                   facecolor=bg, edgecolor='none'))
        ax.text(0.7, y + 0.05, '\u25B6', fontsize=9, color=DB_BLUE)
        ax.text(1.0, y + 0.05, name, fontsize=10, color=DB_TEXT,
                fontfamily='monospace', fontweight='bold')
        tc, tbg, tlabel = tier_colors[idx]
        ax.text(4.0, y + 0.05, tlabel, fontsize=8, color=tc,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=tbg, edgecolor='none'))
        ax.text(5.5, y + 0.05, desc, fontsize=9, color=DB_MUTED)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '05-skills-folder.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 05-skills-folder.png')


def generate_genie_code_pane_image():
    """Image 6: Simulated Genie Code pane in a notebook."""
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Notebook area (left side)
    ax.add_patch(FancyBboxPatch((0.2, 0.2), 8.6, 8.5, boxstyle="round,pad=0.1",
                                facecolor='#252526', edgecolor='#3C3C3C', linewidth=1))

    ax.text(0.5, 8.2, 'energy_data_explorer.py', fontsize=11, fontweight='bold',
            color='#CCCCCC', fontfamily='sans-serif')
    ax.text(4.5, 8.2, 'Python', fontsize=9, color='#569CD6',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#1E3A5F', edgecolor='none'))

    code_lines = [
        ('1', '# Databricks notebook source', '#6A9955'),
        ('2', '', '#CCCCCC'),
        ('3', '# Load the raw customer data', '#6A9955'),
        ('4', 'customers_df = spark.table(', '#CCCCCC'),
        ('5', '    "main.sourabh_energy_workshop.raw_customers"', '#CE9178'),
        ('6', ')', '#CCCCCC'),
        ('7', '', '#CCCCCC'),
        ('8', '# BUG: Wrong column reference', '#6A9955'),
        ('9', 'billing_df = spark.table(', '#CCCCCC'),
        ('10', '    "main.sourabh_energy_workshop.raw_billing"', '#CE9178'),
        ('11', ')', '#CCCCCC'),
        ('12', '', '#CCCCCC'),
        ('13', '# Join on wrong key (bug)', '#6A9955'),
        ('14', 'joined = customers_df.join(', '#CCCCCC'),
        ('15', '    billing_df,', '#CCCCCC'),
        ('16', '    customers_df.customer_name ==', '#CCCCCC'),
        ('17', '      billing_df.customer_name,', '#CCCCCC'),
        ('18', '    "inner"', '#CE9178'),
        ('19', ')', '#CCCCCC'),
    ]

    for i, (num, line, color) in enumerate(code_lines):
        y = 7.6 - i * 0.38
        ax.text(0.5, y, num, fontsize=8, color='#858585', fontfamily='monospace', ha='right')
        ax.text(0.7, y, line, fontsize=8, color=color, fontfamily='monospace')

    # Error highlight on line 16-17
    ax.add_patch(plt.Rectangle((0.65, 7.6 - 15 * 0.38 - 0.12), 7.8, 0.76,
                               facecolor='#5C2020', alpha=0.4, edgecolor='none'))

    # Genie Code pane (right side)
    ax.add_patch(FancyBboxPatch((9.0, 0.2), 4.8, 8.5, boxstyle="round,pad=0.1",
                                facecolor='#1A1A2E', edgecolor='#3C3C3C', linewidth=1))

    ax.add_patch(FancyBboxPatch((9.2, 8.0), 4.4, 0.5, boxstyle="round,pad=0.05",
                                facecolor=DB_RED, edgecolor='none'))
    ax.text(10.5, 8.2, 'Genie Code', fontsize=12, fontweight='bold',
            color=DB_WHITE, fontfamily='sans-serif')

    # User message
    ax.add_patch(FancyBboxPatch((9.4, 6.8), 4.0, 0.8, boxstyle="round,pad=0.1",
                                facecolor='#2D2D5E', edgecolor='none'))
    ax.text(9.6, 7.3, 'You', fontsize=8, fontweight='bold', color='#94A3B8')
    ax.text(9.6, 7.0, '/fix this join - the columns don\'t match', fontsize=9,
            color='#E2E8F0', fontfamily='sans-serif')

    # Genie response
    ax.add_patch(FancyBboxPatch((9.4, 3.8), 4.0, 2.7, boxstyle="round,pad=0.1",
                                facecolor='#162032', edgecolor='none'))
    ax.text(9.6, 6.2, 'Genie Code', fontsize=8, fontweight='bold', color=DB_RED)
    response_lines = [
        "The join uses `customer_name` but",
        "`raw_billing` doesn't have that column.",
        "",
        "Fix: Join on `account_id` = `customer_id`:",
        "",
        "  customers_df.join(",
        "    billing_df,",
        "    customers_df.account_id ==",
        "      billing_df.customer_id,",
        '    "inner"',
        "  )",
    ]
    for i, line in enumerate(response_lines):
        y = 5.9 - i * 0.2
        color = '#A5D6FF' if line.startswith('  ') else '#E2E8F0'
        if '`' in line:
            color = '#FFA657'
        ax.text(9.6, y, line, fontsize=7.5, color=color, fontfamily='monospace')

    # Input box
    ax.add_patch(FancyBboxPatch((9.4, 0.5), 4.0, 0.6, boxstyle="round,pad=0.1",
                                facecolor='#2D2D3E', edgecolor='#4C4C6C'))
    ax.text(9.6, 0.75, 'Ask Genie Code...', fontsize=9, color='#6B7280',
            fontstyle='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '02-genie-code-pane.png'), dpi=150,
                bbox_inches='tight', facecolor='#1E1E1E')
    plt.close()
    print('Created: 02-genie-code-pane.png')


def generate_data_generation_results_image():
    """Image 7: Data generation verification output."""
    tables = [
        ('raw_meter_readings', '10,685,000', '7 columns', 'timestamp, kwh_consumed, voltage...'),
        ('raw_billing', '603,047', '11 columns', 'bill_id, customer_id, total_kwh...'),
        ('raw_customers', '50,000', '14 columns', 'account_id, customer_name, region...'),
        ('raw_demand_response', '20,000', '8 columns', 'event_id, target_reduction_kwh...'),
        ('raw_outages', '5,000', '8 columns', 'outage_id, region, cause...'),
        ('raw_equipment', '2,000', '9 columns', 'equipment_id, equipment_type...'),
        ('raw_weather', '1,825', '9 columns', 'date, region, temp_high, humidity...'),
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(0.3, 8.5, 'Cell 8 Output  \u2714  Data Generation Complete', fontsize=13,
            fontweight='bold', color='#4EC9B0', fontfamily='sans-serif')

    ax.text(0.3, 7.8, '\u2500' * 60, fontsize=9, color='#555555', fontfamily='monospace')

    headers = ['Table', 'Rows', 'Columns', 'Key Fields']
    hx = [0.5, 4.5, 6.5, 8.5]
    for i, h in enumerate(headers):
        ax.text(hx[i], 7.4, h, fontsize=10, fontweight='bold',
                color='#569CD6', fontfamily='monospace')

    ax.text(0.3, 7.0, '\u2500' * 60, fontsize=9, color='#555555', fontfamily='monospace')

    for idx, (name, rows, ncols, fields) in enumerate(tables):
        y = 6.5 - idx * 0.75
        ax.text(0.5, y, name, fontsize=9.5, color='#4EC9B0', fontfamily='monospace')
        ax.text(4.5, y, rows, fontsize=9.5, color='#B5CEA8', fontfamily='monospace', ha='left')
        ax.text(6.5, y, ncols, fontsize=9.5, color='#DCDCAA', fontfamily='monospace')
        ax.text(8.5, y, fields, fontsize=8.5, color='#808080', fontfamily='monospace')

    ax.text(0.3, 0.8, '\u2500' * 60, fontsize=9, color='#555555', fontfamily='monospace')
    ax.text(0.5, 0.3, 'Total: 11,366,872 rows across 7 tables in main.sourabh_energy_workshop',
            fontsize=10, color='#CCCCCC', fontfamily='monospace')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '06-data-generation-results.png'), dpi=150,
                bbox_inches='tight', facecolor='#1E1E1E')
    plt.close()
    print('Created: 06-data-generation-results.png')


def generate_meter_readings_image():
    """Image 8: Sample meter readings data."""
    cols = ['meter_id', 'customer_id', 'timestamp', 'kwh_consumed', 'voltage', 'power_factor', 'is_peak_hour']
    rows = [
        ['MTR-000001', 'ACCT-004288', '2025-01-01T00:00:00', '9.077', '245.6', '0.937', 'false'],
        ['MTR-000002', 'ACCT-015521', '2025-01-01T01:00:00', '0.225', '240.9', '0.970', 'false'],
        ['MTR-000003', 'ACCT-003129', '2025-01-01T02:00:00', '0.255', '233.1', '0.865', 'false'],
        ['MTR-000004', 'ACCT-015324', '2025-01-01T03:00:00', '0.193', '242.8', '0.896', 'false'],
        ['MTR-000005', 'ACCT-000003', '2025-01-01T04:00:00', '1.604', '245.3', '0.957', 'false'],
    ]

    fig, ax = plt.subplots(figsize=(14, 4.5))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((0.1, 4.5), 13.8, 0.8, boxstyle="round,pad=0.1",
                                facecolor=DB_DARK, edgecolor='none'))
    ax.text(0.5, 4.85, 'raw_meter_readings', fontsize=13, fontweight='bold',
            color=DB_WHITE, fontfamily='monospace')
    ax.text(5, 4.85, 'Sample Data (5 of 10,685,000 rows)',
            fontsize=10, color='#94A3B8', fontfamily='sans-serif')

    col_x = [0.3, 2.0, 3.7, 6.5, 8.3, 9.8, 11.5]
    for i, c in enumerate(cols):
        ax.text(col_x[i], 4.1, c, fontsize=8, fontweight='bold',
                color=DB_MUTED, fontfamily='sans-serif')
    ax.plot([0.2, 13.8], [3.9, 3.9], color=DB_LIGHT_GRAY, linewidth=1)

    for ridx, row in enumerate(rows):
        y = 3.5 - ridx * 0.7
        bg = '#F8FAFC' if ridx % 2 == 0 else DB_WHITE
        ax.add_patch(plt.Rectangle((0.15, y - 0.25), 13.7, 0.6,
                                   facecolor=bg, edgecolor='none'))
        for cidx, val in enumerate(row):
            ax.text(col_x[cidx], y, val, fontsize=8, color=DB_TEXT,
                    fontfamily='monospace' if cidx < 3 else 'sans-serif')

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '07-meter-readings-sample.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 07-meter-readings-sample.png')


def generate_dataset_overview_image():
    """Image 9: Visual overview of all 7 tables and their relationships."""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(DB_WHITE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(7, 9.5, 'SmartGrid Analytics Platform - Data Model',
            fontsize=16, fontweight='bold', color=DB_TEXT, ha='center')
    ax.text(7, 9.05, 'main.sourabh_energy_workshop  |  7 tables  |  11.4M rows',
            fontsize=11, color=DB_MUTED, ha='center')

    def draw_table_box(x, y, name, rows, cols, color):
        w, h = 3.2, 1.8
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                    facecolor=DB_WHITE, edgecolor=color, linewidth=2))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.5), w, 0.5, boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor='none'))
        ax.text(x + w/2, y + h - 0.25, name, fontsize=9, fontweight='bold',
                color=DB_WHITE, ha='center', fontfamily='monospace')
        ax.text(x + 0.15, y + h - 0.8, f'{rows} rows', fontsize=8,
                color=DB_TEXT, fontfamily='sans-serif')
        for i, col in enumerate(cols[:3]):
            ax.text(x + 0.15, y + h - 1.1 - i * 0.22, col, fontsize=7.5,
                    color=DB_MUTED, fontfamily='monospace')

    # Central table
    draw_table_box(5.4, 4.5, 'raw_customers', '50K',
                   ['account_id (PK)', 'customer_name', 'region, customer_type'], DB_BLUE)

    # Connected tables
    draw_table_box(0.3, 6.5, 'raw_meter_readings', '10.7M',
                   ['meter_id, customer_id', 'timestamp, kwh_consumed', 'voltage, power_factor'], DB_RED)

    draw_table_box(10.5, 6.5, 'raw_billing', '603K',
                   ['bill_id, customer_id', 'total_kwh, amount_charged', 'payment_date, balance'], '#7C3AED')

    draw_table_box(0.3, 2.5, 'raw_demand_response', '20K',
                   ['event_id, customer_id', 'target_reduction_kwh', 'actual_reduction_kwh'], DB_ORANGE)

    draw_table_box(10.5, 2.5, 'raw_equipment', '2K',
                   ['equipment_id', 'equipment_type, region', 'failure_count, capacity'], '#059669')

    draw_table_box(3.8, 0.5, 'raw_outages', '5K',
                   ['outage_id, region', 'start_time, end_time', 'cause, affected_meters'], '#D97706')

    draw_table_box(8, 0.5, 'raw_weather', '1.8K',
                   ['date, region', 'temp_high, humidity', 'wind_speed, precipitation'], '#6366F1')

    # Relationship arrows
    arrow_style = dict(arrowstyle='->', color='#9CA3AF', lw=1.5,
                       connectionstyle='arc3,rad=0.1')
    ax.annotate('', xy=(5.4, 5.4), xytext=(3.5, 7.0), arrowprops=arrow_style)
    ax.annotate('', xy=(8.6, 5.4), xytext=(10.5, 7.0), arrowprops=arrow_style)
    ax.annotate('', xy=(5.4, 4.9), xytext=(3.5, 3.8), arrowprops=arrow_style)
    ax.annotate('', xy=(8.6, 4.9), xytext=(10.5, 3.8), arrowprops=arrow_style)

    # Labels on arrows
    ax.text(4.2, 6.5, 'customer_id', fontsize=7, color='#9CA3AF', fontstyle='italic',
            rotation=20)
    ax.text(9.2, 6.5, 'customer_id', fontsize=7, color='#9CA3AF', fontstyle='italic',
            rotation=-20)
    ax.text(4.0, 4.0, 'customer_id', fontsize=7, color='#9CA3AF', fontstyle='italic',
            rotation=-20)
    ax.text(9.8, 4.0, 'region', fontsize=7, color='#9CA3AF', fontstyle='italic',
            rotation=20)

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, '00-data-model.png'), dpi=150,
                bbox_inches='tight', facecolor=DB_WHITE)
    plt.close()
    print('Created: 00-data-model.png')


if __name__ == '__main__':
    generate_catalog_tables_image()
    generate_customers_schema_image()
    generate_customers_sample_image()
    generate_workshop_folder_image()
    generate_skills_folder_image()
    generate_genie_code_pane_image()
    generate_data_generation_results_image()
    generate_meter_readings_image()
    generate_dataset_overview_image()
    print('\nAll images generated successfully!')
