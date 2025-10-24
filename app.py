from flask import Flask, jsonify, request, send_file, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
import json
import zipfile
from pathlib import Path
from automation import take_screenshot
from system_settings import SystemSettings
import threading

app = Flask(__name__)

# Initialize system settings
settings = SystemSettings()

# Initialize screenshots directory
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Scheduler for automated screenshots
scheduler = BackgroundScheduler()
screenshot_lock = threading.Lock()


def scheduled_screenshot_task():
    """Task to take screenshot - runs according to frequency"""
    with screenshot_lock:
        try:
            print(f"[{datetime.now()}] Taking scheduled screenshot...")
            credentials = settings.get_login_credentials()
            success, message = take_screenshot(
                credentials['username'], 
                credentials['password']
            )
            if success:
                print(f"[{datetime.now()}] Screenshot taken successfully: {message}")
            else:
                print(f"[{datetime.now()}] Screenshot failed: {message}")
                # Schedule retry in 5 minutes
                print(f"[{datetime.now()}] Scheduling retry in 5 minutes...")
                scheduler.add_job(
                    func=scheduled_screenshot_task,
                    trigger="date",
                    run_date=datetime.now() + timedelta(minutes=5),
                    id='screenshot_retry',
                    replace_existing=True
                )
        except Exception as e:
            print(f"[{datetime.now()}] Error in scheduled screenshot: {str(e)}")
            # Schedule retry in 5 minutes on exception
            print(f"[{datetime.now()}] Scheduling retry in 5 minutes after exception...")
            try:
                scheduler.add_job(
                    func=scheduled_screenshot_task,
                    trigger="date",
                    run_date=datetime.now() + timedelta(minutes=5),
                    id='screenshot_retry',
                    replace_existing=True
                )
            except:
                pass


def restart_scheduler():
    """Restart the scheduler with updated frequency"""
    scheduler.remove_all_jobs()
    frequency_hours = settings.get_frequency()
    scheduler.add_job(
        func=scheduled_screenshot_task,
        trigger="interval",
        hours=frequency_hours,
        id='screenshot_job',
        replace_existing=True
    )
    print(f"Scheduler restarted with frequency: {frequency_hours} hours")


@app.route('/')
def index():
    """API information endpoint"""
    return jsonify({
        "name": "PortOptimizer Screenshot API",
        "version": "1.0.0",
        "endpoints": {
            "GET /screenshot/<date>": "Get screenshot by date (format: YYYY-MM-DD)",
            "GET /screenshots/range": "Get screenshots range (params: start_date, end_date or last_n)",
            "POST /admin/frequency": "Change screenshot frequency (requires admin_password, frequency_hours)",
            "POST /admin/credentials": "Update login credentials (requires admin_password, username, password)",
            "POST /admin/cleanup": "Delete all screenshots (requires admin_password)",
            "POST /screenshot/now": "Take screenshot immediately (requires admin_password)"
        }
    })


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Download a specific screenshot file
    """
    try:
        file_path = os.path.join(SCREENSHOTS_DIR, filename)
        if os.path.exists(file_path):
            return send_from_directory(
                SCREENSHOTS_DIR, 
                filename,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({
                "success": False,
                "error": "File not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/screenshot/<date_str>', methods=['GET'])
def get_screenshot(date_str):
    """
    Get screenshot for a specific date
    Date format: YYYY-MM-DD
    Returns JSON with download link
    """
    try:
        # Validate date format
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Find screenshot files for that date
        date_pattern = target_date.strftime("%Y-%m-%d")
        matching_files = []
        
        for filename in os.listdir(SCREENSHOTS_DIR):
            if filename.startswith(date_pattern) and filename.endswith('.png'):
                matching_files.append(filename)
        
        if not matching_files:
            return jsonify({
                "success": False,
                "error": f"No screenshot found for date {date_str}"
            }), 404
        
        # Return the most recent screenshot for that date
        matching_files.sort(reverse=True)
        screenshot_file = matching_files[0]
        
        # Return JSON with download link
        download_url = f"{request.host_url}download/{screenshot_file}"
        
        return jsonify({
            "success": True,
            "date": date_str,
            "filename": screenshot_file,
            "download_url": download_url,
            "message": f"Screenshot found for {date_str}"
        })
    
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/screenshots/range', methods=['GET'])
def get_screenshots_range():
    """
    Get screenshots for a date range or last N screenshots
    Parameters:
    - start_date: YYYY-MM-DD (required if not using last_n)
    - end_date: YYYY-MM-DD (required if not using last_n)
    - last_n: number of most recent screenshots (optional)
    Returns JSON with download link for ZIP file
    """
    try:
        last_n = request.args.get('last_n', type=int)
        
        if last_n:
            # Get last N screenshots
            all_files = sorted(
                [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')],
                reverse=True
            )
            selected_files = all_files[:last_n]
        else:
            # Get screenshots in date range
            start_date_str = request.args.get('start_date')
            end_date_str = request.args.get('end_date')
            
            if not start_date_str or not end_date_str:
                return jsonify({
                    "success": False,
                    "error": "Provide either 'last_n' or both 'start_date' and 'end_date'"
                }), 400
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            if start_date > end_date:
                return jsonify({
                    "success": False,
                    "error": "start_date must be before or equal to end_date"
                }), 400
            
            # Find all screenshots in range
            selected_files = []
            for filename in os.listdir(SCREENSHOTS_DIR):
                if filename.endswith('.png'):
                    try:
                        # Extract date from filename (format: YYYY-MM-DD_HH-MM-SS.png)
                        file_date_str = filename.split('_')[0]
                        file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
                        
                        if start_date <= file_date <= end_date:
                            selected_files.append(filename)
                    except:
                        continue
            
            selected_files.sort()
        
        if not selected_files:
            return jsonify({
                "success": False,
                "error": "No screenshots found for the specified criteria"
            }), 404
        
        # Create zip file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"screenshots_{timestamp}.zip"
        zip_path = os.path.join(SCREENSHOTS_DIR, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in selected_files:
                file_path = os.path.join(SCREENSHOTS_DIR, filename)
                zipf.write(file_path, filename)
        
        # Return JSON with download link
        download_url = f"{request.host_url}download/{zip_filename}"
        
        return jsonify({
            "success": True,
            "zip_filename": zip_filename,
            "download_url": download_url,
            "screenshot_count": len(selected_files),
            "screenshots": selected_files,
            "message": f"ZIP file created with {len(selected_files)} screenshot(s)"
        })
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/admin/frequency', methods=['POST'])
def change_frequency():
    """
    Change screenshot frequency
    Body: {
        "admin_password": "password",
        "frequency_hours": 24
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be JSON"
            }), 400
        
        admin_password = data.get('admin_password')
        frequency_hours = data.get('frequency_hours')
        
        if not admin_password or frequency_hours is None:
            return jsonify({
                "success": False,
                "error": "admin_password and frequency_hours are required"
            }), 400
        
        # Verify admin password
        if not settings.verify_admin_password(admin_password):
            return jsonify({
                "success": False,
                "error": "Invalid admin password"
            }), 403
        
        # Validate frequency
        if not isinstance(frequency_hours, (int, float)) or frequency_hours <= 0:
            return jsonify({
                "success": False,
                "error": "frequency_hours must be a positive number"
            }), 400
        
        # Update frequency
        settings.set_frequency(frequency_hours)
        restart_scheduler()
        
        return jsonify({
            "success": True,
            "message": f"Frequency updated to {frequency_hours} hours",
            "frequency_hours": frequency_hours
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/admin/credentials', methods=['POST'])
def update_credentials():
    """
    Update login credentials for the portal
    Body: {
        "admin_password": "password",
        "username": "new_username",
        "password": "new_password"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be JSON"
            }), 400
        
        admin_password = data.get('admin_password')
        username = data.get('username')
        password = data.get('password')
        
        if not admin_password or not username or not password:
            return jsonify({
                "success": False,
                "error": "admin_password, username, and password are required"
            }), 400
        
        # Verify admin password
        if not settings.verify_admin_password(admin_password):
            return jsonify({
                "success": False,
                "error": "Invalid admin password"
            }), 403
        
        # Update credentials
        settings.set_login_credentials(username, password)
        
        return jsonify({
            "success": True,
            "message": "Login credentials updated successfully"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/admin/cleanup', methods=['POST'])
def cleanup():
    """
    Delete all screenshots
    Body: {
        "admin_password": "password"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be JSON"
            }), 400
        
        admin_password = data.get('admin_password')
        
        if not admin_password:
            return jsonify({
                "success": False,
                "error": "admin_password is required"
            }), 400
        
        # Verify admin password
        if not settings.verify_admin_password(admin_password):
            return jsonify({
                "success": False,
                "error": "Invalid admin password"
            }), 403
        
        # Delete all screenshots
        deleted_count = 0
        for filename in os.listdir(SCREENSHOTS_DIR):
            if filename.endswith('.png') or filename.endswith('.zip'):
                file_path = os.path.join(SCREENSHOTS_DIR, filename)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {filename}: {str(e)}")
        
        return jsonify({
            "success": True,
            "message": f"Cleanup completed. {deleted_count} files deleted."
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/screenshot/now', methods=['POST'])
def take_screenshot_now():
    """
    Take a screenshot immediately
    Body: {
        "admin_password": "password"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be JSON"
            }), 400
        
        admin_password = data.get('admin_password')
        
        if not admin_password:
            return jsonify({
                "success": False,
                "error": "admin_password is required"
            }), 400
        
        # Verify admin password
        if not settings.verify_admin_password(admin_password):
            return jsonify({
                "success": False,
                "error": "Invalid admin password"
            }), 403
        
        # Take screenshot
        with screenshot_lock:
            credentials = settings.get_login_credentials()
            success, message = take_screenshot(
                credentials['username'], 
                credentials['password']
            )
        
        if success:
            return jsonify({
                "success": True,
                "message": "Screenshot taken successfully",
                "filename": message
            })
        else:
            return jsonify({
                "success": False,
                "error": message
            }), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/status', methods=['GET'])
def status():
    """Get current system status"""
    try:
        frequency = settings.get_frequency()
        credentials = settings.get_login_credentials()
        
        # Count screenshots
        screenshot_count = len([f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')])
        
        # Get last screenshot time
        screenshots = sorted(
            [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith('.png')],
            reverse=True
        )
        last_screenshot = screenshots[0] if screenshots else None
        
        return jsonify({
            "success": True,
            "frequency_hours": frequency,
            "username": credentials['username'],
            "total_screenshots": screenshot_count,
            "last_screenshot": last_screenshot,
            "scheduler_running": scheduler.running
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Start the scheduler
    scheduler.start()
    restart_scheduler()
    
    print("=" * 50)
    print("PortOptimizer Screenshot API")
    print("=" * 50)
    print(f"Screenshot frequency: {settings.get_frequency()} hours")
    print(f"Screenshots directory: {SCREENSHOTS_DIR}")
    print("Scheduler started")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5004, debug=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\nShutdown complete")

