# 📮 Postman Collection Guide

## 🚀 **Quick Start**

1. **Import Collection**: Import `PortOptimizer_API.postman_collection.json`
2. **Import Environment**: Import `PortOptimizer_API.postman_environment.json`
3. **Select Environment**: Choose "PortOptimizer Excel API Environment"
4. **Start API**: Run `python app.py` on port 5004
5. **Test Endpoints**: Use the organized folder structure

---

## 📁 **Collection Structure**

### **📋 Information**
- **API Info** - Get API information and endpoints
- **System Status** - Get system status, settings, and file counts

### **📥 Excel Operations**
- **Download Excel Now** - Download Excel + convert to PDF immediately
- **Get Excel by Date** - Get Excel report by date with public download URL

### **📄 PDF Operations**
- **Get PDF by Date** - Get PDF report by date with public download URL

### **📁 File Downloads**
- **Download Excel File** - Download specific Excel file
- **Download PDF File** - Download specific PDF file

### **⚙️ Admin Functions**
- **Change Frequency** - Change download frequency (hours)
- **Set Preferred Hour** - Set preferred hour for scheduled captures
- **Update Credentials** - Update portal login credentials
- **Cleanup Files** - Delete all files (USE WITH CAUTION)

### **❌ Error Testing**
- **Invalid Admin Password** - Test error handling
- **Invalid Date Format** - Test validation

---

## 🔧 **Environment Variables**

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | API base URL | `http://localhost:5004` |
| `admin_password` | Admin password | `YB02Ss3JJdk` |
| `current_date` | Current date (auto-generated) | `2025-10-26` |
| `excel_filename` | Last Excel filename | `2025-10-26_14-30-45.xlsx` |
| `pdf_filename` | Last PDF filename | `2025-10-26_14-30-45.pdf` |
| `excel_download_url` | Excel download URL | `http://localhost:5004/download/...` |
| `pdf_download_url` | PDF download URL | `http://localhost:5004/download/...` |
| `frequency_hours` | Download frequency | `24` |
| `preferred_hour` | Preferred hour (0-23) | `10` |
| `username` | Portal username | `sara@fouroneone.io` |
| `password` | Portal password | `Ss925201!` |

---

## 🧪 **Testing Workflow**

### **1. Basic Setup**
1. Run **API Info** to verify connection
2. Run **System Status** to check current settings

### **2. Download Excel Report**
1. Run **Download Excel Now** (takes ~2-3 minutes)
2. Check response for both Excel and PDF download URLs
3. Variables are automatically set for next requests

### **3. Test File Retrieval**
1. Run **Get Excel by Date** to get Excel report
2. Run **Get PDF by Date** to get PDF report
3. Both return JSON with public download URLs

### **4. Test File Downloads**
1. Run **Download Excel File** using `{{excel_filename}}`
2. Run **Download PDF File** using `{{pdf_filename}}`
3. Files are downloaded directly

### **5. Admin Functions**
1. Run **Change Frequency** to modify schedule
2. Run **Set Preferred Hour** to set capture time
3. Run **Update Credentials** to change login info
4. Run **Cleanup Files** to delete all files (careful!)

---

## ✅ **Test Validation**

### **JSON Response Validation**
- All GET endpoints return proper JSON structure
- Required fields: `success`, `date`, `filename`, `download_url`, `message`
- Download URLs are public and accessible

### **File Download Validation**
- Excel files have correct MIME type
- PDF files have correct MIME type
- Files are downloaded successfully

### **Error Handling Validation**
- Invalid admin password returns 403
- Invalid date format returns 400
- Missing files return 404

---

## 🌍 **UTC Timestamp Support**

### **File Naming**
- All files use UTC timestamps: `YYYY-MM-DD_HH-MM-SS`
- Timezone independent - works globally
- Easy chronological sorting

### **Date Search**
- Search by date: `2025-10-26`
- Finds all files from that UTC date
- Works regardless of server timezone

---

## 📊 **Example Responses**

### **Excel Report Response**
```json
{
  "success": true,
  "date": "2025-10-26",
  "filename": "2025-10-26_14-30-45.xlsx",
  "download_url": "http://localhost:5004/download/2025-10-26_14-30-45.xlsx",
  "message": "Excel report found for 2025-10-26"
}
```

### **PDF Report Response**
```json
{
  "success": true,
  "date": "2025-10-26",
  "filename": "2025-10-26_14-30-45.pdf",
  "download_url": "http://localhost:5004/download/2025-10-26_14-30-45.pdf",
  "message": "PDF report found for 2025-10-26"
}
```

### **System Status Response**
```json
{
  "success": true,
  "frequency_hours": 24,
  "preferred_hour": 10,
  "username": "sara@fouroneone.io",
  "total_screenshots": 0,
  "total_excel_files": 5,
  "total_pdf_files": 5,
  "last_screenshot": null,
  "scheduler_running": true
}
```

---

## 🚨 **Important Notes**

1. **Port**: Make sure API is running on port 5004
2. **Timing**: Excel download takes 2-3 minutes
3. **UTC**: All timestamps are in UTC for timezone independence
4. **Cleanup**: Use cleanup function carefully - it deletes all files
5. **Variables**: Test scripts automatically set variables for chaining requests

---

## 🔄 **Automated Testing**

The collection includes comprehensive test scripts that:
- Validate response status codes
- Check JSON structure
- Verify required fields
- Test file downloads
- Set variables for chaining
- Handle error conditions

Run the entire collection or individual requests to test the complete API functionality! 🎯