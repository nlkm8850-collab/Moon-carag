#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <pthread.h>
#include <time.h>

#define DEVICE_NAME "/dev/moon_kernel_device"
#define MAX_BUFFER 256
#define MAX_MESSAGES 100

// هيكل لتخزين الرسائل
typedef struct {
    char content[MAX_BUFFER];
    char timestamp[64];
    int message_id;
} Message;

// متغيرات عامة
Message messages[MAX_MESSAGES];
int message_count = 0;
int device_file = -1;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

// دالة للحصول على الوقت الحالي
void get_current_time(char *buffer, size_t size) {
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    strftime(buffer, size, "%Y-%m-%d %H:%M:%S", tm_info);
}

// دالة لطباعة رأس الواجهة
void print_header() {
    printf("\033[2J\033[H");  // مسح الشاشة
    printf("\n");
    printf("╔════════════════════════════════════════════════════════════╗\n");
    printf("║           واجهة استقبال نواة Moon Kernel                  ║\n");
    printf("║         Moon Kernel Reception Interface v1.0               ║\n");
    printf("╚════════════════════════════════════════════════════════════╝\n\n");
}

// دالة لطباعة القائمة الرئيسية
void print_menu() {
    printf("\n┌─ القائمة الرئيسية ─────────────────────────────────────────┐\n");
    printf("│ 1. إرسال رسالة إلى الجهاز (Send Message to Device)         │\n");
    printf("│ 2. قراءة البيانات من الجهاز (Read from Device)            │\n");
    printf("│ 3. عرض سجل الرسائل (View Message History)                │\n");
    printf("│ 4. مسح السجل (Clear History)                              │\n");
    printf("│ 5. معلومات الاتصال (Connection Info)                     │\n");
    printf("│ 6. خروج (Exit)                                            │\n");
    printf("└────────────────────────────────────────────────────────────┘\n");
    printf("\nاختر خياراً (1-6): ");
}

// دالة للاتصال بالجهاز
int connect_to_device() {
    if (device_file < 0) {
        device_file = open(DEVICE_NAME, O_RDWR);
        if (device_file < 0) {
            printf("\n❌ خطأ: فشل الاتصال بالجهاز %s\n", DEVICE_NAME);
            printf("تأكد من تحميل الـ kernel module:\n");
            printf("  sudo insmod kernel.ko\n");
            return -1;
        }
        printf("\n✓ تم الاتصال بنجاح بالجهاز\n");
    }
    return 0;
}

// دالة لإرسال رسالة
void send_message() {
    char buffer[MAX_BUFFER];
    char timestamp[64];
    
    if (connect_to_device() < 0) return;
    
    printf("\n┌─ إرسال رسالة ──────────────────────────────────────────────┐\n");
    printf("│ أدخل الرسالة (اضغط Enter لإرسالها):                       │\n");
    printf("└────────────────────────────────────────────────────────────┘\n");
    printf(">> ");
    
    fgets(buffer, sizeof(buffer), stdin);
    
    // إزالة حرف السطر الجديد
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len-1] == '\n') {
        buffer[len-1] = '\0';
    }
    
    if (strlen(buffer) == 0) {
        printf("❌ لا يمكن إرسال رسالة فارغة\n");
        return;
    }
    
    // الكتابة إلى الجهاز
    ssize_t bytes_written = write(device_file, buffer, strlen(buffer));
    
    if (bytes_written > 0) {
        get_current_time(timestamp, sizeof(timestamp));
        
        pthread_mutex_lock(&lock);
        
        if (message_count < MAX_MESSAGES) {
            messages[message_count].message_id = message_count + 1;
            strncpy(messages[message_count].content, buffer, MAX_BUFFER - 1);
            strncpy(messages[message_count].timestamp, timestamp, 63);
            message_count++;
        }
        
        pthread_mutex_unlock(&lock);
        
        printf("\n✓ تم إرسال الرسالة بنجاح!\n");
        printf("  📤 عدد البايتات المرسلة: %ld\n", bytes_written);
        printf("  ⏰ الوقت: %s\n", timestamp);
    } else {
        printf("\n❌ خطأ في إرسال الرسالة\n");
    }
}

// دالة لقراءة البيانات من الجهاز
void read_from_device() {
    char buffer[MAX_BUFFER] = {0};
    char timestamp[64];
    
    if (connect_to_device() < 0) return;
    
    printf("\n┌─ قراءة البيانات ───────────────────────────────────────────┐\n");
    printf("│ جاري القراءة من الجهاز...                                  │\n");
    printf("└────────────────────────────────────────────────────────────┘\n");
    
    lseek(device_file, 0, SEEK_SET);
    ssize_t bytes_read = read(device_file, buffer, MAX_BUFFER - 1);
    
    if (bytes_read > 0) {
        buffer[bytes_read] = '\0';
        get_current_time(timestamp, sizeof(timestamp));
        
        printf("\n✓ تم القراءة بنجاح!\n");
        printf("  📥 عدد البايتات المقروءة: %ld\n", bytes_read);
        printf("  ⏰ الوقت: %s\n", timestamp);
        printf("  📝 المحتوى:\n");
        printf("  ┌────────────────────────────────────────────────────┐\n");
        printf("  │ %s\n", buffer);
        printf("  └────────────────────────────────────────────────────┘\n");
        
        pthread_mutex_lock(&lock);
        
        if (message_count < MAX_MESSAGES) {
            messages[message_count].message_id = message_count + 1;
            strncpy(messages[message_count].content, buffer, MAX_BUFFER - 1);
            strncpy(messages[message_count].timestamp, timestamp, 63);
            message_count++;
        }
        
        pthread_mutex_unlock(&lock);
        
    } else if (bytes_read == 0) {
        printf("\n⚠ لا توجد بيانات للقراءة\n");
    } else {
        printf("\n❌ خطأ في القراءة من الجهاز\n");
    }
}

// دالة لعرض سجل الرسائل
void view_history() {
    printf("\n┌─ سجل الرسائل ──────────────────────────────────────────────┐\n");
    
    pthread_mutex_lock(&lock);
    
    if (message_count == 0) {
        printf("│ لا توجد رسائل في السجل                                    │\n");
    } else {
        printf("│ إجمالي الرسائل: %d                                          │\n", message_count);
        printf("└────────────────────────────────────────────────────────────┘\n\n");
        
        for (int i = 0; i < message_count; i++) {
            printf("[%d] ⏰ %s\n", messages[i].message_id, messages[i].timestamp);
            printf("    📝 %s\n\n", messages[i].content);
        }
    }
    
    pthread_mutex_unlock(&lock);
}

// دال�� لمسح السجل
void clear_history() {
    printf("\n┌─ مسح السجل ─────────────────────────────────────────────────┐\n");
    printf("│ هل تريد فعلاً مسح جميع الرسائل؟ (y/n): ");
    
    char choice;
    scanf("%c", &choice);
    getchar();  // استهلاك حرف السطر الجديد
    
    if (choice == 'y' || choice == 'Y') {
        pthread_mutex_lock(&lock);
        message_count = 0;
        pthread_mutex_unlock(&lock);
        
        printf("│ ✓ تم مسح السجل بنجاح                                      │\n");
    } else {
        printf("│ تم الإلغاء                                                  │\n");
    }
    printf("└────────────────────────────────────────────────────────────┘\n");
}

// دالة لعرض معلومات الاتصال
void show_connection_info() {
    printf("\n┌─ معلومات الاتصال ──────────────────────────────────────────┐\n");
    
    if (device_file >= 0) {
        printf("│ ✓ الحالة: متصل (Connected)                              │\n");
        printf("│ 📱 اسم الجهاز: %s                                   │\n", DEVICE_NAME);
        printf("│ 📊 عدد الرسائل المسجلة: %d                                 │\n", message_count);
    } else {
        printf("│ ❌ الحالة: غير متصل (Disconnected)                        │\n");
        printf("│ 📱 اسم الجهاز: %s                                   │\n", DEVICE_NAME);
    }
    
    printf("└────────────────────────────────────────────────────────────┘\n");
}

// البرنامج الرئيسي
int main() {
    char choice[10];
    
    printf("🚀 جاري تحميل واجهة الاستقبال...\n");
    sleep(1);
    
    while (1) {
        print_header();
        print_menu();
        
        fgets(choice, sizeof(choice), stdin);
        
        switch (choice[0]) {
            case '1':
                send_message();
                break;
            case '2':
                read_from_device();
                break;
            case '3':
                view_history();
                break;
            case '4':
                clear_history();
                break;
            case '5':
                show_connection_info();
                break;
            case '6':
                printf("\n🛑 إغلاق الواجهة...\n");
                if (device_file >= 0) {
                    close(device_file);
                    printf("✓ تم إغلاق الاتصال بالجهاز\n");
                }
                printf("👋 شكراً لاستخدام واجهة Moon Kernel!\n\n");
                return 0;
            default:
                printf("❌ اختيار غير صحيح. حاول مرة أخرى.\n");
        }
        
        printf("\nاضغط Enter للمتابعة...");
        getchar();
    }
    
    return 0;
}
