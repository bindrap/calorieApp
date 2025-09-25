#!/usr/bin/env python3
"""
Image Storage Cleanup and Archival System
Keeps recent images accessible, archives older ones to save space
"""

import os
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

class ImageCleanupManager:
    """Manages image storage, cleanup, and archival"""

    def __init__(self, app_root="/mnt/c/Users/bindrap/Documents/calorieApp"):
        self.app_root = app_root
        self.upload_folder = os.path.join(app_root, "static/uploads")
        self.archive_folder = os.path.join(app_root, "archives")
        self.db_path = os.path.join(app_root, "calorie_tracker.db")

        # Create archive folder if it doesn't exist
        os.makedirs(self.archive_folder, exist_ok=True)

    def cleanup_old_images(self, keep_days=7):
        """
        Keep images from last 7 days accessible, archive older ones

        Args:
            keep_days: Number of days to keep images easily accessible
        """
        print(f"🧹 Starting image cleanup (keeping {keep_days} days)")

        cutoff_date = datetime.now() - timedelta(days=keep_days)
        images_to_archive = []
        total_size_before = 0
        total_size_after = 0

        # Scan upload folder
        for filename in os.listdir(self.upload_folder):
            filepath = os.path.join(self.upload_folder, filename)

            if not os.path.isfile(filepath):
                continue

            # Get file modification time
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_size = os.path.getsize(filepath)
            total_size_before += file_size

            if file_time < cutoff_date:
                images_to_archive.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size': file_size,
                    'date': file_time
                })
            else:
                total_size_after += file_size

        if not images_to_archive:
            print(f"✅ No old images to archive")
            return

        # Create archive
        archive_filename = f"images_archive_{datetime.now().strftime('%Y%m%d')}.zip"
        archive_path = os.path.join(self.archive_folder, archive_filename)

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for image_info in images_to_archive:
                # Add file to zip
                zipf.write(image_info['filepath'], image_info['filename'])

                # Update database to mark as archived
                self._update_database_archived_status(image_info['filename'], archive_filename)

                # Remove original file
                os.remove(image_info['filepath'])

                print(f"  📁 Archived: {image_info['filename']} ({image_info['size']/1024:.1f} KB)")

        archive_size = os.path.getsize(archive_path)
        space_saved = sum(img['size'] for img in images_to_archive) - archive_size

        print(f"✅ Cleanup complete:")
        print(f"  📁 Archived {len(images_to_archive)} images")
        print(f"  💾 Space saved: {space_saved/1024:.1f} KB")
        print(f"  📦 Archive: {archive_filename} ({archive_size/1024:.1f} KB)")
        print(f"  📊 Active storage: {total_size_after/1024:.1f} KB")

    def _update_database_archived_status(self, filename, archive_name):
        """Update database to track archived images"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Add archived status to food entries
            cursor.execute("""
                UPDATE food_entries
                SET image_path = ?
                WHERE image_filename = ?
            """, (f"archived:{archive_name}", filename))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Database update failed for {filename}: {e}")

    def get_storage_stats(self):
        """Get current storage statistics"""
        upload_size = 0
        upload_count = 0

        if os.path.exists(self.upload_folder):
            for filename in os.listdir(self.upload_folder):
                filepath = os.path.join(self.upload_folder, filename)
                if os.path.isfile(filepath):
                    upload_size += os.path.getsize(filepath)
                    upload_count += 1

        archive_size = 0
        archive_count = 0

        if os.path.exists(self.archive_folder):
            for filename in os.listdir(self.archive_folder):
                filepath = os.path.join(self.archive_folder, filename)
                if os.path.isfile(filepath) and filename.endswith('.zip'):
                    archive_size += os.path.getsize(filepath)
                    archive_count += 1

        return {
            'active_images': upload_count,
            'active_size_kb': upload_size / 1024,
            'archived_files': archive_count,
            'archived_size_kb': archive_size / 1024,
            'total_size_kb': (upload_size + archive_size) / 1024
        }

    def restore_archived_image(self, filename, archive_name=None):
        """Restore an archived image back to active storage"""
        if not archive_name:
            # Find which archive contains the file
            for archive_file in os.listdir(self.archive_folder):
                if archive_file.endswith('.zip'):
                    with zipfile.ZipFile(os.path.join(self.archive_folder, archive_file), 'r') as zipf:
                        if filename in zipf.namelist():
                            archive_name = archive_file
                            break

        if not archive_name:
            raise FileNotFoundError(f"Image {filename} not found in any archive")

        archive_path = os.path.join(self.archive_folder, archive_name)
        restore_path = os.path.join(self.upload_folder, filename)

        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extract(filename, self.upload_folder)

        # Update database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE food_entries
                SET image_path = ?
                WHERE image_filename = ?
            """, (restore_path, filename))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Database restore update failed: {e}")

        print(f"✅ Restored {filename} from {archive_name}")

def main():
    """Run image cleanup"""
    cleanup_manager = ImageCleanupManager()

    print("📊 Current Storage Stats:")
    stats = cleanup_manager.get_storage_stats()
    print(f"  Active Images: {stats['active_images']} files ({stats['active_size_kb']:.1f} KB)")
    print(f"  Archived Files: {stats['archived_files']} files ({stats['archived_size_kb']:.1f} KB)")
    print(f"  Total Storage: {stats['total_size_kb']:.1f} KB")

    # Run cleanup (keep 7 days of images)
    cleanup_manager.cleanup_old_images(keep_days=7)

    print("\n📊 Storage Stats After Cleanup:")
    stats = cleanup_manager.get_storage_stats()
    print(f"  Active Images: {stats['active_images']} files ({stats['active_size_kb']:.1f} KB)")
    print(f"  Archived Files: {stats['archived_files']} files ({stats['archived_size_kb']:.1f} KB)")
    print(f"  Total Storage: {stats['total_size_kb']:.1f} KB")

if __name__ == "__main__":
    main()