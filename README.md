# Weekly Project Visibility Card & Automated Tracker System 📊

**Executive-Level Weekly Project Status Tracking, Web Visibility Portal & Google Sheets Sync**

இந்த திட்டம் உங்கள் திட்டங்களின் (Projects) வாராந்திர அறிக்கைகளை (Weekly Visibility Cards) எளிதாக உருவாக்கவும், சேகரிக்கவும், மேலாண்மைக்கு (CEO / Management) உயர் மட்ட காட்சிப் பார்வையையும் (Executive Web Visibility Card Dashboard) வழங்கும் வகையில் வடிவமைக்கப்பட்டுள்ளது.

---

## 📸 Reference Card Layout (வாராந்திர பார்வை அட்டை)

உங்கள் புகைப்படத்தில் உள்ள **WEEKLY PROJECT VISIBILITY CARD**-ன் அனைத்து 6 முக்கிய கூறுகளும் இந்த சிஸ்டத்தில் டிஜிட்டல் வடிவில் கொண்டு வரப்பட்டுள்ளன:

1. **Header & Metadata Bar**: Company, Project ID, Client, Project Name, Current Release, Week No., Week Ending Date, Overall Status Badge (`GREEN`, `AMBER`, `RED`).
2. **Resource Allocation Box**: Resources Table (Name, Role, Allocated Days, Responsibilities) + Total Allocation (150 Man-Days) & Release Start Date.
3. **1. Scope & Release Journey**: Delivered Release 1, Current Release 2 (Core Modules, Integrations, Specific Objectives), Future Release 3.
4. **2. Current Release Plan**: Original Plan vs Forecast Dates, Delay (+21 Days), Schedule Status (`OFF TRACK`), Milestone Breakdown with Variance & Status dots.
5. **3. Resource Effort Summary**: Original Allocation, Consumed to Date, Forecast Remaining, Forecast Total, Overrun (+30 Days / +20%), Budget Status (`OVER BUDGET`), Effort Consumed % Progress Bar.
6. **4. What Changed This Week?**: Schedule Change, Scope Change (CR tags), Effort Change & Material Notes.
7. **5. Risks / Issues & CEO Attention**: Top Risks & Issues (High/Medium/Low priority badges), Decisions / Approvals Required (Due Dates), Escalation Status.
8. **6. At A Glance (Donut Charts)**: Overall Progress %, Time Elapsed %, Effort Consumed % SVG Donut Gauges & Insight Note.

---

## 📁 Project Structure (கோப்பு கட்டமைப்பு)

```
📁 project tracker/
 ├── 📊 tracker.py                             # Python Parser, HTML Generator & Google Sheets Engine
 ├── 🌐 dashboard/
 │    └── 📄 index.html                        # Executive Web Visibility Portal (Interactive Dashboard)
 ├── 📝 templates/
 │    ├── 📄 weekly_visibility_card_template.md  # PM Markdown Filling Template
 │    └── 📄 weekly_visibility_card_template.json# Standard JSON Schema Template
 ├── 📂 reports/
 │    ├── 📄 sample_week36_card.json            # Reference Week 36 Data (NBC Digital Platform)
 │    └── 📄 week36_visibility_card.html       # Standalone Executive HTML Card Report
 └── 📄 README.md                              # Complete User Guide
```

---

## 🚀 பயன்படுத்துவது எப்படி? (Usage Guide)

### 1. Interactive Web Dashboard-ஐ இயக்க (Launch Web Visibility Portal)

எந்தவொரு உலாவி மூலமாகவும் (Browser) வாராந்திர Visibility Card-களைக் காணவும், புதிய Updates-ஐ உள்ளிடவும் கீழே உள்ள கட்டளையை இயக்கவும்:

```bash
python tracker.py --serve
```

- இது உங்கள் உலாவியில் `http://localhost:8000`-ஐத் திறக்கும்.
- **Submit Weekly Update** பொத்தானைக் கிளிக் செய்து வெப் பார்ம் மூலமாகவோ அல்லது `.json` / `.md` ஃபைலை Drag & Drop செய்தோ வாராந்திர அறிக்கையைப் புதுப்பிக்கலாம்.
- **Export / Print Card** பொத்தானை அழுத்தி கார்டை அப்படியே Executive PDF-ஆக பெறலாம்.

---

### 2. Standalone HTML Executive Card உருவாக்க (Generate Executive Card HTML)

JSON அல்லது Markdown அறிக்கையிலிருந்து தனியான HTML கார்டை உருவாக்க:

```bash
python tracker.py --file reports/sample_week36_card.json --output-html reports/week36_card.html
```

---

### 3. Dry Run (சோதனை முறை - Google Sheet-க்கு அனுப்பாமல் பார்க்க)

```bash
python tracker.py --file reports/sample_week36_card.json --dry-run
```

---

### 4. Google Sheets-ல் Auto-Sync செய்ய (Push to Google Sheets)

`service_account.json` ஃபைலை திட்டத்தின் கோப்புறையில் வைத்து:

```bash
python tracker.py --file reports/sample_week36_card.json --spreadsheet "Company Project Weekly Tracker"
```

---

## 📝 PMs வாராந்திர அறிக்கை அனுப்பும் முறை (Submitting Weekly Updates)

Project Manager அல்லது Team Lead இரு முறைகளில் அறிக்கையை அளிக்கலாம்:

1. **Option A (Web Portal Form)**:
   - `python tracker.py --serve` மூலம் Web UI திறந்து, **Submit Weekly Update** பொத்தானைக் கிளிக் செய்து விவரங்களை நிரப்பி சமர்ப்பிக்கலாம்.

2. **Option B (JSON Report File)**:
   - `templates/weekly_visibility_card_template.json`-ஐக் காப்பி செய்து, `reports/week37_card.json` எனப் பெயர் மாற்றி வாராந்திர விவரங்களை நிரப்பி சேமிக்கவும்.

3. **Option C (Markdown Report File)**:
   - `templates/weekly_visibility_card_template.md`-ஐப் பயன்படுத்தி Markdown கோப்பாகவும் பூர்த்தி செய்து சமர்ப்பிக்கலாம்.
