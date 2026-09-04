import os
import re
import sys
import argparse
import json
import http.server
import socketserver
import webbrowser

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


def parse_markdown(md_text):
    """
    Parses any Weekly Project Visibility Card markdown document into structured JSON.
    Handles N/A, TBD, custom milestone tables, and various field name formats.
    """
    data = {}

    def get_field(pattern, default="N/A"):
        m = re.search(pattern, md_text, re.IGNORECASE)
        return m.group(1).strip() if m else default

    # Metadata extraction
    data['company'] = get_field(r'\*\*(?:Company):\*\*\s*(.*?)\n', "TIC INCUBATOR")
    
    proj_id = get_field(r'\*\*(?:Project ID):\*\*\s*(.*?)\n', "N/A")
    data['project_id'] = proj_id if proj_id not in ["N/A / Not Provided", "N/A", "TBD", ""] else ""

    data['client'] = get_field(r'\*\*(?:Client):\*\*\s*(.*?)\n', "CLIENT")
    
    proj_name = get_field(r'\*\*(?:Project Name):\*\*\s*(.*?)\n', "PROJECT NAME")
    data['project_name'] = proj_name

    # If project_id is empty, create a clean slug from project_name
    if not data['project_id']:
        slug = re.sub(r'[^a-zA-Z0-9]', '_', proj_name).upper()
        data['project_id'] = slug[:16]

    data['current_release'] = get_field(r'\*\*(?:Current Release / Phase|Current Release):\*\*\s*(.*?)\n', "RELEASE 1")
    raw_week = get_field(r'\*\*(?:Week No):\*\*\s*(.*?)\n', "1")
    week_num = re.sub(r'(?i)week\s*', '', raw_week).strip()
    data['week_no'] = week_num if week_num else "1"
    data['week_ending_date'] = get_field(r'\*\*(?:Week Ending Date):\*\*\s*(.*?)\n', "N/A")
    
    # Overall Status (strip HTML comments if any)
    raw_status = get_field(r'\*\*(?:Overall Status|Overall RAG Status|Project Status):\*\*\s*(.*?)\n', "GREEN")
    raw_status = re.sub(r'<!--.*?-->', '', raw_status).strip().upper()
    if "GREEN" in raw_status:
        data['overall_status'] = "GREEN"
    elif "RED" in raw_status:
        data['overall_status'] = "RED"
    else:
        data['overall_status'] = "AMBER"

    # Resource Allocation
    data['total_allocation_man_days'] = get_field(r'\*\*(?:Total Allocated Man-Days):\*\*\s*(.*?)\n', "TBD")
    data['release_start_date'] = get_field(r'\*\*(?:Release Start Date|Original Start Date):\*\*\s*(.*?)\n', "N/A")

    # Resource Table
    resources = []
    res_table_match = re.search(r'\|\s*Resource Name\s*\|.*?\n\|[:\s|-]+\n(.*?)(?=\n---|###|\n\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if res_table_match:
        lines = res_table_match.group(1).strip().split('\n')
        for line in lines:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                resources.append({
                    "name": cols[0],
                    "role": cols[1],
                    "allocation_days": cols[2],
                    "responsibility": cols[3]
                })
    data['resources'] = resources

    # Section 1: Scope & Release Journey
    scope_journey = {
        "delivered_releases": [],
        "current_release": {
            "name": data['current_release'],
            "core_modules": [],
            "integrations": [],
            "specific_objectives": []
        },
        "future_releases": []
    }

    # Delivered Releases
    deliv_match = re.search(r'###\s*(?:Delivered Releases|Delivered / Completed|Previous / Available|Completed This Period).*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if deliv_match:
        items = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', deliv_match.group(1)) if x.strip()]
        if items:
            scope_journey["delivered_releases"] = [{"name": "DELIVERED", "go_live": "", "items": items}]

    # Current Release Section
    curr_scope_match = re.search(r'###\s*(?:Current Release|Current Phase|Current Work|This Week).*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if curr_scope_match:
        text = curr_scope_match.group(1)

        # 1. Parse Core Modules Table if present
        core_table = re.search(r'####\s*Core Modules.*?\n\|.*?\n\|[:\s|-]+\n(.*?)(?=####|###|\n---\n|\Z)', md_text, re.DOTALL | re.IGNORECASE)
        if core_table:
            modules = []
            for line in core_table.group(1).strip().split('\n'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) >= 2:
                    mod_name = cols[0].replace('**', '')
                    status = cols[2] if len(cols) >= 3 else cols[1]
                    modules.append(f"**{mod_name}:** {status}")
            if modules:
                scope_journey["current_release"]["core_modules"] = modules

        # 2. Parse Integrations Table if present
        integ_table = re.search(r'####\s*Integrations.*?\n\|.*?\n\|[:\s|-]+\n(.*?)(?=####|###|\n---\n|\Z)', md_text, re.DOTALL | re.IGNORECASE)
        if integ_table:
            integrations = []
            for line in integ_table.group(1).strip().split('\n'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) >= 2:
                    integ_name = cols[0].replace('**', '')
                    purpose = cols[1]
                    status = cols[2] if len(cols) >= 3 else ""
                    status_text = f" — {status}" if status else ""
                    integrations.append(f"**{integ_name}:** {purpose}{status_text}")
            if integrations:
                scope_journey["current_release"]["integrations"] = integrations

        # 3. Parse Specific Objectives
        obj_sec = re.search(r'####\s*Specific Objectives.*?\n(.*?)(?=###|\n---\n|\Z)', md_text, re.DOTALL | re.IGNORECASE)
        if obj_sec:
            objs = [x.strip() for x in re.findall(r'(?:\*\*Objective\s*\d+[^*]*\*\*|[-*])\s*(.*?)\n', obj_sec.group(1)) if x.strip()]
            if not objs:
                objs = [line.strip() for line in obj_sec.group(1).split('\n') if line.strip() and not line.startswith('#')]
            if objs:
                scope_journey["current_release"]["specific_objectives"] = objs

        # Fallbacks for standard key-value or bullet lists
        if not scope_journey["current_release"]["core_modules"]:
            core_m = re.search(r'\*\*(?:Core Modules|Completed This Period|Current Work):\*\*\s*(.*?)\n', text)
            if core_m:
                scope_journey["current_release"]["core_modules"] = [x.strip() for x in core_m.group(1).split(',')]
            
        if not scope_journey["current_release"]["integrations"]:
            integ_m = re.search(r'\*\*(?:Integrations|Integration Status):\*\*\s*(.*?)\n', text)
            if integ_m:
                scope_journey["current_release"]["integrations"] = [x.strip() for x in integ_m.group(1).split(',')]

        if not scope_journey["current_release"]["core_modules"]:
            list_items = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', text) if x.strip()]
            if list_items:
                scope_journey["current_release"]["core_modules"] = list_items

    # Future Releases
    fut_match = re.search(r'###\s*(?:Future Releases|Post-Release / Next|Next Phase|Next Week|Upcoming / Pending).*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if fut_match:
        items = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', fut_match.group(1)) if x.strip()]
        if items:
            scope_journey["future_releases"] = [{"name": "FUTURE / UPCOMING", "planned_start": "Planned", "items": items}]

    data['scope_journey'] = scope_journey

    # Section 2: Release Plan
    rel_plan = {
        "original_plan_start": get_field(r'\*\*(?:Original Plan Start|Original Start Date):\*\*\s*(.*?)\n', "N/A"),
        "original_plan_end": get_field(r'\*\*(?:Original Plan End|Original End Date):\*\*\s*(.*?)\n', "N/A"),
        "current_forecast_start": get_field(r'\*\*(?:Current Forecast Start):\*\*\s*(.*?)\n', "N/A"),
        "current_forecast_end": get_field(r'\*\*(?:Current Forecast End):\*\*\s*(.*?)\n', "N/A"),
        "delay_days": get_field(r'\*\*(?:Schedule Delay):\*\*\s*(.*?)\n', "0 DAYS"),
        "schedule_status": re.sub(r'<!--.*?-->', '', get_field(r'\*\*(?:Schedule Status|Current Release Status):\*\*\s*(.*?)\n', "ON TRACK")).strip().upper(),
        "milestones": []
    }

    m_table_match = re.search(r'\|\s*(?:Milestone|Work Item)\s*\|.*?\n\|[:\s|-]+\n(.*?)(?=\n---|###|\n\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if m_table_match:
        lines = m_table_match.group(1).strip().split('\n')
        for line in lines:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 5:
                rel_plan["milestones"].append({
                    "milestone": cols[0],
                    "original_plan": cols[1],
                    "current_forecast": cols[2],
                    "variance": cols[3],
                    "status": cols[4].upper()
                })
            elif len(cols) == 4:
                # 4-column format: Work Item | Category | Status | Remarks
                m_status = cols[2].upper()
                status_color = "GREEN" if "COMPLET" in m_status else ("AMBER" if "PROGRESS" in m_status or "START" in m_status else "RED")
                rel_plan["milestones"].append({
                    "milestone": cols[0],
                    "original_plan": cols[1],
                    "current_forecast": cols[3] if cols[3] else cols[2],
                    "variance": "0 days",
                    "status": status_color
                })
            elif len(cols) >= 2:
                # 2-column table format (Milestone | Status)
                m_status = cols[1].upper()
                status_color = "GREEN" if "COMPLET" in m_status else ("AMBER" if "PROGRESS" in m_status or "START" in m_status else "RED")
                rel_plan["milestones"].append({
                    "milestone": cols[0],
                    "original_plan": "N/A",
                    "current_forecast": cols[1],
                    "variance": "0 days",
                    "status": status_color
                })
    data['release_plan'] = rel_plan

    # Section 3: Effort Summary
    orig_alloc = get_field(r'\*\*(?:Original Allocation):\*\*\s*(.*?)\n', "N/A")
    cons_td = get_field(r'\*\*(?:Consumed To Date):\*\*\s*(.*?)\n', "N/A")
    fore_rem = get_field(r'\*\*(?:Forecast Remaining):\*\*\s*(.*?)\n', "N/A")
    fore_tot = get_field(r'\*\*(?:Forecast Total):\*\*\s*(.*?)\n', "N/A")
    
    # Extract consumed percentage
    consumed_pct_raw = get_field(r'\*\*(?:Consumed Percentage|Overall Progress \(Scope Complete\)|Overall Progress|Scope Completion):\*\*\s*(.*?)\n', "0%")
    try:
        pct_val = int(re.sub(r'\D', '', consumed_pct_raw))
    except ValueError:
        pct_val = 0

    data['effort_summary'] = {
        "original_allocation": orig_alloc,
        "consumed_to_date": cons_td,
        "forecast_remaining": fore_rem,
        "forecast_total": fore_tot,
        "overrun": get_field(r'\*\*(?:Forecast Overrun|Forecast Overrun / Underrun):\*\*\s*(.*?)\n', "0 DAYS"),
        "budget_status": re.sub(r'<!--.*?-->', '', get_field(r'\*\*(?:Budget Status):\*\*\s*(.*?)\n', "WITHIN BUDGET")).strip().upper(),
        "consumed_percentage": pct_val,
        "consumed_text": get_field(r'\*\*(?:Consumed Subtext):\*\*\s*(.*?)\n', f"{cons_td} consumed")
    }

    # Section 4: What Changed This Week
    sched_change = get_field(r'\*\*(?:Schedule Change|Main Objective):\*\*\s*(.*?)\n', "")
    scope_change = get_field(r'\*\*(?:Scope Change|Patch Work|Completed Work):\*\*\s*(.*?)\n', "")
    effort_change = get_field(r'\*\*(?:Effort Change|Enhancements):\*\*\s*(.*?)\n', "")
    material_notes = get_field(r'\*\*(?:Material Notes|Note):\*\*\s*(.*?)\n', "")

    # Subheading bullet fallbacks if key-values are empty
    sec4_match = re.search(r'##\s*4\.\s*WHAT CHANGED.*?\n(.*?)(?=##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if sec4_match:
        s4_text = sec4_match.group(1)
        if not scope_change:
            comp_bullets = re.search(r'###\s*(?:Completed Work|Delivered|Work In Progress).*?\n(.*?)(?=###|\n##|\Z)', s4_text, re.DOTALL | re.IGNORECASE)
            if comp_bullets:
                bullets = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', comp_bullets.group(1)) if x.strip()]
                if bullets:
                    scope_change = "; ".join(bullets)
        if not effort_change:
            enh_bullets = re.search(r'###\s*(?:Enhancements|Newly Added Tasks|Support / Development Setup).*?\n(.*?)(?=###|\n##|\Z)', s4_text, re.DOTALL | re.IGNORECASE)
            if enh_bullets:
                bullets = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', enh_bullets.group(1)) if x.strip()]
                if bullets:
                    effort_change = "; ".join(bullets)

    data['what_changed_this_week'] = {
        "schedule_change": sched_change if sched_change else "No schedule change reported.",
        "scope_change": scope_change if scope_change else "No scope change reported.",
        "scope_change_tag": get_field(r'\*\*(?:Scope Change Tag):\*\*\s*(.*?)\n', "Approved"),
        "effort_change": effort_change if effort_change else "No effort change reported.",
        "note": material_notes if material_notes else "No material changes reported."
    }

    # Section 5: Risks & CEO Attention
    top_risks = []
    risks_match = re.search(r'###\s*Top Risks / Issues.*?\n\|.*?\n\|[:\s|-]+\n(.*?)(?=\n---|###|\n\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if risks_match:
        for line in risks_match.group(1).strip().split('\n'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 3:
                top_risks.append({"description": cols[1], "severity": cols[2].upper()})

    decisions = []
    dec_match = re.search(r'###\s*Decisions / Approvals Required.*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if dec_match:
        for item in re.findall(r'[-*]\s*\*\*(.*?)\*\*\s*\|?\s*(.*?)\n', dec_match.group(1)):
            decisions.append({"description": item[0], "due_date": item[1] if item[1] else "N/A"})
        if not decisions:
            items = [x.strip() for x in re.findall(r'[-*]\s*(.*?)\n', dec_match.group(1)) if x.strip()]
            for it in items:
                decisions.append({"description": it, "due_date": "N/A"})

    escalation_val = get_field(r'\*\*(?:Escalation Status):\*\*\s*(.*?)\n', "")
    if not escalation_val:
        esc_match = re.search(r'###\s*Escalation Status.*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
        if esc_match:
            escalation_val = esc_match.group(1).strip()

    data['risks_and_attention'] = {
        "top_risks": top_risks,
        "decisions_required": decisions,
        "escalation": escalation_val if escalation_val else "No escalations reported."
    }

    # Section 6: At A Glance
    time_elapsed_raw = get_field(r'\*\*(?:Time Elapsed):\*\*\s*(.*?)\n', "0%")
    try:
        time_pct = int(re.sub(r'\D', '', time_elapsed_raw))
    except ValueError:
        time_pct = 0

    effort_cons_raw = get_field(r'\*\*(?:Effort Consumed):\*\*\s*(.*?)\n', "0%")
    try:
        effort_pct = int(re.sub(r'\D', '', effort_cons_raw))
    except ValueError:
        effort_pct = pct_val

    data['at_a_glance'] = {
        "overall_progress_percent": pct_val,
        "time_elapsed_percent": time_pct,
        "effort_consumed_percent": effort_pct,
        "insight_note": get_field(r'\*\*(?:Key Insight Note):\*\*\s*(.*?)\n', "Project update received.")
    }

    return data


def update_projects_store(card_data, store_filepath="dashboard/projects_data.json"):
    """
    Updates the central multi-project store (projects_data.json) with new weekly card data.
    """
    os.makedirs(os.path.dirname(store_filepath), exist_ok=True)
    
    store = {}
    if os.path.exists(store_filepath):
        try:
            with open(store_filepath, 'r', encoding='utf-8') as f:
                store = json.load(f)
        except Exception:
            store = {}

    proj_id = card_data.get('project_id', 'PROJ-DEFAULT')
    week_no = str(card_data.get('week_no', '1'))

    if proj_id not in store:
        store[proj_id] = {
            "project_id": proj_id,
            "project_name": card_data.get('project_name', 'Unknown Project'),
            "company": card_data.get('company', 'Company'),
            "client": card_data.get('client', 'Client'),
            "weeks": {}
        }

    store[proj_id]["project_name"] = card_data.get('project_name', store[proj_id]["project_name"])
    store[proj_id]["weeks"][week_no] = card_data

    with open(store_filepath, 'w', encoding='utf-8') as f:
        json.dump(store, f, indent=2, ensure_ascii=False)

    print(f"💾 Updated central multi-project store: [{card_data.get('project_name')}] ({proj_id}) - Week {week_no}")
    return store


def generate_html_card(card_data, output_filepath="reports/weekly_visibility_card.html"):
    """
    Renders a standalone HTML visibility card from data.
    """
    template_path = os.path.join(os.path.dirname(__file__), "dashboard", "index.html")
    if not os.path.exists(template_path):
        template_path = "dashboard/index.html"
    
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    json_str = json.dumps(card_data, ensure_ascii=False)
    injection = f"const weekDataStore = {{ 'current': {json_str} }};\n"
    
    html_content = re.sub(
        r'const weekDataStore = \{.*?\};',
        injection + "    renderCardData(weekDataStore['current']);",
        html_content,
        flags=re.DOTALL
    )

    dir_name = os.path.dirname(output_filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✨ Successfully generated Executive Visibility Card HTML: '{output_filepath}'")


def run_web_server(port=8000):
    """
    Launches a local HTTP server for the dashboard.
    """
    web_dir = os.path.join(os.path.dirname(__file__), "dashboard")
    if not os.path.exists(web_dir):
        web_dir = "."

    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    
    print(f"\n🚀 Launching Weekly Project Visibility Portal at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server.")
    
    try:
        webbrowser.open(f"http://localhost:{port}")
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped.")


def main():
    parser = argparse.ArgumentParser(description="Weekly Project Visibility Card System")
    parser.add_argument("--file", help="Path to markdown (.md) or JSON (.json) report file")
    parser.add_argument("--dir", help="Path to directory containing report files")
    parser.add_argument("--spreadsheet", default="Company Project Weekly Tracker", help="Google Spreadsheet Name")
    parser.add_argument("--creds", default="service_account.json", help="Path to service_account.json")
    parser.add_argument("--output-html", help="Path to generate standalone Executive HTML Visibility Card")
    parser.add_argument("--dry-run", action="store_true", help="Parse files and print output without saving")
    parser.add_argument("--serve", nargs='?', const=8000, type=int, help="Launch local web server for Executive Dashboard (default port: 8000)")

    args = parser.parse_args()

    if args.serve:
        run_web_server(args.serve)
        return

    files_to_process = []
    if args.file:
        files_to_process.append(args.file)
    elif args.dir:
        for f in sorted(os.listdir(args.dir)):
            if f.endswith(".md") or f.endswith(".json"):
                files_to_process.append(os.path.join(args.dir, f))
    else:
        print("Please specify --file, --dir, or --serve. Use --help for instructions.")
        sys.exit(1)

    for filepath in files_to_process:
        print(f"\n📄 Processing: {filepath}")
        
        if filepath.endswith(".json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                parsed_data = json.load(f)
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                md_text = f.read()
            parsed_data = parse_markdown(md_text)

        if not args.dry_run:
            update_projects_store(parsed_data)

        if args.output_html:
            generate_html_card(parsed_data, args.output_html)

        if args.dry_run:
            print("--- Extracted Data (Dry Run) ---")
            print(json.dumps(parsed_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
