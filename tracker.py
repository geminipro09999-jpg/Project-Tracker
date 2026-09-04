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
    Parses a Weekly Project Visibility Card markdown document into structured JSON.
    """
    data = {}

    # Metadata extraction
    def get_field(pattern, default="N/A"):
        m = re.search(pattern, md_text, re.IGNORECASE)
        return m.group(1).strip() if m else default

    data['company'] = get_field(r'\*\*(?:Company):\*\*\s*(.*?)\n', "GOVTECH SOLUTIONS")
    data['project_id'] = get_field(r'\*\*(?:Project ID):\*\*\s*(.*?)\n', "PROJ-001")
    data['client'] = get_field(r'\*\*(?:Client):\*\*\s*(.*?)\n', "CLIENT NAME")
    data['project_name'] = get_field(r'\*\*(?:Project Name):\*\*\s*(.*?)\n', "PROJECT NAME")
    data['current_release'] = get_field(r'\*\*(?:Current Release):\*\*\s*(.*?)\n', "RELEASE 1")
    data['week_no'] = get_field(r'\*\*(?:Week No):\*\*\s*(.*?)\n', "1")
    data['week_ending_date'] = get_field(r'\*\*(?:Week Ending Date):\*\*\s*(.*?)\n', "N/A")
    
    # Overall Status (strip HTML comments if any)
    raw_status = get_field(r'\*\*(?:Overall Status):\*\*\s*(.*?)\n', "GREEN")
    raw_status = re.sub(r'<!--.*?-->', '', raw_status).strip().upper()
    data['overall_status'] = raw_status if raw_status in ['GREEN', 'AMBER', 'RED'] else "AMBER"

    # Resource Allocation
    data['total_allocation_man_days'] = int(get_field(r'\*\*(?:Total Allocated Man-Days):\*\*\s*(\d+)', "100"))
    data['release_start_date'] = get_field(r'\*\*(?:Release Start Date):\*\*\s*(.*?)\n', "N/A")

    # Resource Table
    resources = []
    res_table_match = re.search(r'\|\s*Resource Name\s*\|.*?\n\|[:\s|-]+\n(.*?)(?=\n---|###|\n\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if res_table_match:
        lines = res_table_match.group(1).strip().split('\n')
        for line in lines:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                try:
                    alloc_val = int(re.sub(r'\D', '', cols[2]))
                except ValueError:
                    alloc_val = 0
                resources.append({
                    "name": cols[0],
                    "role": cols[1],
                    "allocation_days": alloc_val,
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

    deliv_match = re.search(r'###\s*Delivered Releases.*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if deliv_match:
        items = re.findall(r'[-*]\s*(.*?)\n', deliv_match.group(1))
        scope_journey["delivered_releases"] = [{"name": "DELIVERED", "go_live": "", "items": items}]

    curr_scope_match = re.search(r'###\s*Current Release.*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if curr_scope_match:
        text = curr_scope_match.group(1)
        core_m = re.search(r'\*\*Core Modules:\*\*\s*(.*?)\n', text)
        if core_m:
            scope_journey["current_release"]["core_modules"] = [x.strip() for x in core_m.group(1).split(',')]
        
        integ_m = re.search(r'\*\*Integrations:\*\*\s*(.*?)\n', text)
        if integ_m:
            scope_journey["current_release"]["integrations"] = [x.strip() for x in integ_m.group(1).split(',')]
            
        obj_m = re.search(r'\*\*Specific Objectives:\*\*\s*(.*?)\n', text)
        if obj_m:
            scope_journey["current_release"]["specific_objectives"] = [x.strip() for x in obj_m.group(1).split(',')]

    fut_match = re.search(r'###\s*Future Releases.*?\n(.*?)(?=###|\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
    if fut_match:
        items = re.findall(r'[-*]\s*(.*?)\n', fut_match.group(1))
        scope_journey["future_releases"] = [{"name": "FUTURE", "planned_start": "Tentative", "items": items}]

    data['scope_journey'] = scope_journey

    # Section 2: Release Plan
    rel_plan = {
        "original_plan_start": get_field(r'\*\*(?:Original Plan Start):\*\*\s*(.*?)\n', "N/A"),
        "original_plan_end": get_field(r'\*\*(?:Original Plan End):\*\*\s*(.*?)\n', "N/A"),
        "current_forecast_start": get_field(r'\*\*(?:Current Forecast Start):\*\*\s*(.*?)\n', "N/A"),
        "current_forecast_end": get_field(r'\*\*(?:Current Forecast End):\*\*\s*(.*?)\n', "N/A"),
        "delay_days": get_field(r'\*\*(?:Schedule Delay):\*\*\s*(.*?)\n', "0 DAYS"),
        "schedule_status": re.sub(r'<!--.*?-->', '', get_field(r'\*\*(?:Schedule Status):\*\*\s*(.*?)\n', "ON TRACK")).strip().upper(),
        "milestones": []
    }

    m_table_match = re.search(r'\|\s*Milestone\s*\|.*?\n\|[:\s|-]+\n(.*?)(?=\n---|###|\n\n##|\Z)', md_text, re.DOTALL | re.IGNORECASE)
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
    data['release_plan'] = rel_plan

    # Section 3: Effort Summary
    orig_alloc = get_field(r'\*\*(?:Original Allocation):\*\*\s*(.*?)\n', "100 MAN-DAYS")
    cons_td = get_field(r'\*\*(?:Consumed To Date):\*\*\s*(.*?)\n', "0 MAN-DAYS")
    fore_rem = get_field(r'\*\*(?:Forecast Remaining):\*\*\s*(.*?)\n', "0 MAN-DAYS")
    fore_tot = get_field(r'\*\*(?:Forecast Total):\*\*\s*(.*?)\n', "100 MAN-DAYS")
    
    data['effort_summary'] = {
        "original_allocation": orig_alloc,
        "consumed_to_date": cons_td,
        "forecast_remaining": fore_rem,
        "forecast_total": fore_tot,
        "overrun": get_field(r'\*\*(?:Forecast Overrun):\*\*\s*(.*?)\n', "0 MAN-DAYS"),
        "budget_status": re.sub(r'<!--.*?-->', '', get_field(r'\*\*(?:Budget Status):\*\*\s*(.*?)\n', "WITHIN BUDGET")).strip().upper(),
        "consumed_percentage": int(re.sub(r'\D', '', get_field(r'\*\*(?:Consumed Percentage):\*\*\s*(\d+)%', "50")) or 50),
        "consumed_text": get_field(r'\*\*(?:Consumed Subtext):\*\*\s*(.*?)\n', f"{cons_td} consumed")
    }

    # Section 4: What Changed This Week
    data['what_changed_this_week'] = {
        "schedule_change": get_field(r'\*\*(?:Schedule Change):\*\*\s*(.*?)\n', "No change"),
        "scope_change": get_field(r'\*\*(?:Scope Change):\*\*\s*(.*?)\n', "No change"),
        "scope_change_tag": get_field(r'\*\*(?:Scope Change Tag):\*\*\s*(.*?)\n', "Approved"),
        "effort_change": get_field(r'\*\*(?:Effort Change):\*\*\s*(.*?)\n', "No change"),
        "note": get_field(r'\*\*(?:Material Notes):\*\*\s*(.*?)\n', "No material changes this week.")
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
        for item in re.findall(r'[-*]\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\n', dec_match.group(1)):
            decisions.append({"description": item[0], "due_date": item[1]})

    data['risks_and_attention'] = {
        "top_risks": top_risks,
        "decisions_required": decisions,
        "escalation": get_field(r'\*\*(?:Escalation Status):\*\*\s*(.*?)\n', "No escalations.")
    }

    # Section 6: At A Glance
    data['at_a_glance'] = {
        "overall_progress_percent": int(re.sub(r'\D', '', get_field(r'\*\*(?:Overall Progress \(Scope Complete\)):\*\*\s*(\d+)%', "50")) or 50),
        "time_elapsed_percent": int(re.sub(r'\D', '', get_field(r'\*\*(?:Time Elapsed):\*\*\s*(\d+)%', "50")) or 50),
        "effort_consumed_percent": int(re.sub(r'\D', '', get_field(r'\*\*(?:Effort Consumed):\*\*\s*(\d+)%', "50")) or 50),
        "insight_note": get_field(r'\*\*(?:Key Insight Note):\*\*\s*(.*?)\n', "Development on track.")
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

    print(f"💾 Updated central multi-project store: [{card_data.get('project_name')}] - Week {week_no}")
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
