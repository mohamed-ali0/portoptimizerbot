# PortOptimizer API Endpoints

## 📋 **Available Endpoints**

### **1. Information**
- **GET** `/` - API information and endpoint list

### **2. File Downloads**
- **GET** `/download/<filename>` - Download specific file (Excel or PDF)
  - Searches: `downloads/pdfs/` → `downloads/` → `screenshots/`

### **3. Excel Reports**
- **GET** `/excel/<date>` - Get Excel report by date (format: YYYY-MM-DD)
  - Returns JSON with download link
  - Searches Excel files only

- **POST** `/excel/now` - Download Excel report immediately
  - Body: `{"admin_password": "password"}`
  - Automatically converts to PDF with borders
  - Returns both Excel and PDF download links

### **4. PDF Reports**
- **GET** `/pdf/<date>` - Get PDF report by date (format: YYYY-MM-DD)
  - Returns JSON with download link
  - Searches PDF files in `downloads/pdfs/` directory

### **4. Screenshots (Legacy)**
- **GET** `/screenshots/range` - Get screenshots for date range
  - Parameters: `start_date`, `end_date`, or `last_n`
  - Returns ZIP file with screenshots

### **5. Admin Functions**
- **POST** `/admin/frequency` - Change download frequency
  - Body: `{"admin_password": "password", "frequency_hours": 24}`

- **POST** `/admin/preferred_hour` - Set preferred hour for scheduled captures
  - Body: `{"admin_password": "password", "preferred_hour": 10}`
  - Hour format: 0-23 (24-hour format)

- **POST** `/admin/credentials` - Update login credentials
  - Body: `{"admin_password": "password", "username": "user", "password": "pass"}`

- **POST** `/admin/cleanup` - Delete all files
  - Body: `{"admin_password": "password"}`

### **6. System Status**
- **GET** `/status` - Get current system status
  - Returns frequency, preferred hour, username, file counts, scheduler status

---

## 📁 **File Structure**
```
downloads/
├── 2025-10-26_14-30-45.xlsx    # Excel files (UTC timestamp)
└── pdfs/
    └── 2025-10-26_14-30-45.pdf  # PDF files with borders (UTC timestamp)
```

## 🌍 **Timezone Independence**
- All timestamps use **UTC** for timezone independence
- Files can be accessed from any timezone
- Date search works regardless of server location
- Format: `YYYY-MM-DD_HH-MM-SS` (24-hour UTC time)

## 🔄 **Workflow**
1. **Download**: Excel file → `downloads/`
2. **Convert**: PDF with gray borders → `downloads/pdfs/`
3. **Access**: Both files available via API endpoints

## 📝 **Example Usage**

### Download Excel Report Now:
```bash
curl -X POST http://localhost:5004/excel/now \
  -H "Content-Type: application/json" \
  -d '{"admin_password": "password"}'
```

### Get Report by Date:
```bash
curl http://localhost:5004/excel/2025-10-26
```

### Download File:
```bash
curl http://localhost:5004/download/2025-10-26_14-30-45.pdf
```

### Check Status:
```bash
curl http://localhost:5004/status
```
