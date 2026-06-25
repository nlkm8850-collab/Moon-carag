#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>

#define DEVICE_NAME "/dev/moon_kernel_device"

int main()
{
    int device_file;
    char buffer[256] = {0};
    char write_buffer[256] = "مرحباً من User Space\n";
    ssize_t bytes_read;
    
    printf("=== Moon Kernel Module Test Program ===\n\n");
    
    // فتح جهاز
    printf("فتح جهاز %s...\n", DEVICE_NAME);
    device_file = open(DEVICE_NAME, O_RDWR);
    if (device_file < 0) {
        perror("فشل فتح الجهاز");
        printf("تأكد من تحميل الـ kernel module أولاً:\n");
        printf("  sudo insmod kernel.ko\n");
        printf("  ls -la /dev/moon_kernel_device\n");
        return -1;
    }
    
    printf("✓ تم فتح الجهاز بنجاح\n\n");
    
    // قراءة من الجهاز
    printf("--- اختبار القراءة ---\n");
    bytes_read = read(device_file, buffer, sizeof(buffer) - 1);
    if (bytes_read > 0) {
        buffer[bytes_read] = '\0';
        printf("تم قراءة %ld بايت:\n", bytes_read);
        printf("المحتوى: %s", buffer);
    } else if (bytes_read == 0) {
        printf("لا توجد بيانات للقراءة\n");
    } else {
        perror("خطأ في القراءة");
    }
    
    printf("\n--- اختبار الكتابة ---\n");
    ssize_t bytes_written = write(device_file, write_buffer, strlen(write_buffer));
    if (bytes_written > 0) {
        printf("تم كتابة %ld بايت بنجاح\n", bytes_written);
    } else {
        perror("خطأ في الكتابة");
    }
    
    // قراءة البيانات المكتوبة
    printf("\n--- قراءة البيانات بعد الكتابة ---\n");
    lseek(device_file, 0, SEEK_SET);  // العودة لبداية البافر
    memset(buffer, 0, sizeof(buffer));
    bytes_read = read(device_file, buffer, sizeof(buffer) - 1);
    if (bytes_read > 0) {
        buffer[bytes_read] = '\0';
        printf("المحتوى الجديد: %s", buffer);
    }
    
    // إغلاق الجهاز
    printf("\nإغلاق الجهاز...\n");
    close(device_file);
    printf("✓ تم إغلاق الجهاز بنجاح\n\n");
    
    printf("=== انتهى الاختبار ===\n");
    
    return 0;
}
