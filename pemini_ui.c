#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/ioctl.h>
#include <linux/mutex.h>
#include <asm/io.h>

#define DEVICE_NAME "pemini"
#define CLASS_NAME "pemini_ui"
#define PEMINI_MAGIC 'P'

/* IOCTL Commands */
#define PEMINI_DISPLAY_TEXT _IOW(PEMINI_MAGIC, 1, char *)
#define PEMINI_CLEAR_SCREEN _IO(PEMINI_MAGIC, 2)
#define PEMINI_SET_COLOR _IOW(PEMINI_MAGIC, 3, int)
#define PEMINI_GET_STATUS _IOR(PEMINI_MAGIC, 4, int)
#define PEMINI_INIT_DISPLAY _IO(PEMINI_MAGIC, 5)

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Moon Carag ARM Development Team");
MODULE_DESCRIPTION("Pemini UI - ARM Kernel Interface Module for Moon Carag");
MODULE_VERSION("1.0");

/* Device structure */
typedef struct {
    uint32_t width;
    uint32_t height;
    uint32_t color;
    uint32_t background_color;
    char buffer[512];
    int is_initialized;
} pemini_device_t;

static int majorNumber = 0;
static struct class* peminiClass = NULL;
static struct device* peminiDevice = NULL;
static pemini_device_t pemini_dev;
static DEFINE_MUTEX(pemini_mutex);

/* ARM-specific register definitions for display control */
#define ARM_DISPLAY_BASE 0xF0000000
#define DISPLAY_CTRL_REG 0x00
#define DISPLAY_DATA_REG 0x04
#define DISPLAY_STATUS_REG 0x08
#define DISPLAY_COLOR_REG 0x0C

/* Function prototypes */
static int pemini_open(struct inode *inode, struct file *file);
static int pemini_release(struct inode *inode, struct file *file);
static ssize_t pemini_read(struct file *filp, char *buffer, size_t len, loff_t *offset);
static ssize_t pemini_write(struct file *filp, const char *buffer, size_t len, loff_t *offset);
static long pemini_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

static struct file_operations fops = {
    .open = pemini_open,
    .read = pemini_read,
    .write = pemini_write,
    .release = pemini_release,
    .unlocked_ioctl = pemini_ioctl,
};

/* ARM-specific initialization function */
static void pemini_init_arm_display(void)
{
    void __iomem *display_base;
    uint32_t ctrl_value;
    
    printk(KERN_INFO "Pemini: Initializing ARM display controller\n");
    
    /* Request memory mapping for display base address */
    display_base = ioremap(ARM_DISPLAY_BASE, 4096);
    if (!display_base) {
        printk(KERN_ERR "Pemini: Failed to map display base address\n");
        return;
    }
    
    /* Initialize display control register */
    ctrl_value = readl(display_base + DISPLAY_CTRL_REG);
    ctrl_value |= 0x01; /* Enable display */
    writel(ctrl_value, display_base + DISPLAY_CTRL_REG);
    
    /* Set default resolution for ARM device */
    pemini_dev.width = 1024;
    pemini_dev.height = 768;
    pemini_dev.color = 0xFFFFFF; /* White */
    pemini_dev.background_color = 0x000000; /* Black */
    pemini_dev.is_initialized = 1;
    
    /* Unmap the display base address */
    iounmap(display_base);
    
    printk(KERN_INFO "Pemini: ARM display initialized (Resolution: %ux%u)\n", 
           pemini_dev.width, pemini_dev.height);
}

/* Clear the display buffer */
static void pemini_clear_display(void)
{
    void __iomem *display_base;
    
    display_base = ioremap(ARM_DISPLAY_BASE, 4096);
    if (!display_base) {
        printk(KERN_ERR "Pemini: Failed to map display base for clearing\n");
        return;
    }
    
    /* Write clear command to display control register */
    writel(0x00, display_base + DISPLAY_DATA_REG);
    
    memset(pemini_dev.buffer, 0, sizeof(pemini_dev.buffer));
    
    iounmap(display_base);
    printk(KERN_INFO "Pemini: Display cleared\n");
}

/* Write text to display */
static void pemini_write_text(const char *text, size_t len)
{
    void __iomem *display_base;
    size_t i;
    
    if (len > sizeof(pemini_dev.buffer) - 1)
        len = sizeof(pemini_dev.buffer) - 1;
    
    display_base = ioremap(ARM_DISPLAY_BASE, 4096);
    if (!display_base) {
        printk(KERN_ERR "Pemini: Failed to map display base for writing\n");
        return;
    }
    
    /* Write each character to display */
    for (i = 0; i < len; i++) {
        writel((uint32_t)text[i], display_base + DISPLAY_DATA_REG);
    }
    
    memcpy(pemini_dev.buffer, text, len);
    pemini_dev.buffer[len] = '\0';
    
    iounmap(display_base);
    printk(KERN_INFO "Pemini: Text written to display\n");
}

/* Set display color */
static void pemini_set_color(uint32_t color)
{
    void __iomem *display_base;
    
    display_base = ioremap(ARM_DISPLAY_BASE, 4096);
    if (!display_base) {
        printk(KERN_ERR "Pemini: Failed to map display base for color setting\n");
        return;
    }
    
    writel(color, display_base + DISPLAY_COLOR_REG);
    pemini_dev.color = color;
    
    iounmap(display_base);
    printk(KERN_INFO "Pemini: Display color set to 0x%06X\n", color);
}

/* Device open function */
static int pemini_open(struct inode *inode, struct file *file)
{
    mutex_lock(&pemini_mutex);
    
    if (!pemini_dev.is_initialized) {
        pemini_init_arm_display();
    }
    
    mutex_unlock(&pemini_mutex);
    printk(KERN_INFO "Pemini: Device opened\n");
    return 0;
}

/* Device release function */
static int pemini_release(struct inode *inode, struct file *file)
{
    mutex_lock(&pemini_mutex);
    printk(KERN_INFO "Pemini: Device closed\n");
    mutex_unlock(&pemini_mutex);
    return 0;
}

/* Device read function */
static ssize_t pemini_read(struct file *filp, char *buffer, size_t len, loff_t *offset)
{
    size_t bytes_to_read;
    size_t buffer_len = strlen(pemini_dev.buffer);
    
    mutex_lock(&pemini_mutex);
    
    if (*offset >= buffer_len) {
        mutex_unlock(&pemini_mutex);
        return 0;
    }
    
    bytes_to_read = buffer_len - *offset;
    if (bytes_to_read > len)
        bytes_to_read = len;
    
    if (copy_to_user(buffer, pemini_dev.buffer + *offset, bytes_to_read)) {
        mutex_unlock(&pemini_mutex);
        return -EFAULT;
    }
    
    *offset += bytes_to_read;
    mutex_unlock(&pemini_mutex);
    
    printk(KERN_INFO "Pemini: Read %zu bytes\n", bytes_to_read);
    return bytes_to_read;
}

/* Device write function */
static ssize_t pemini_write(struct file *filp, const char *buffer, size_t len, loff_t *offset)
{
    char kernel_buffer[256];
    size_t bytes_to_write;
    
    mutex_lock(&pemini_mutex);
    
    bytes_to_write = len > (sizeof(kernel_buffer) - 1) ? (sizeof(kernel_buffer) - 1) : len;
    
    if (copy_from_user(kernel_buffer, buffer, bytes_to_write)) {
        mutex_unlock(&pemini_mutex);
        return -EFAULT;
    }
    
    kernel_buffer[bytes_to_write] = '\0';
    pemini_write_text(kernel_buffer, bytes_to_write);
    
    mutex_unlock(&pemini_mutex);
    printk(KERN_INFO "Pemini: Written %zu bytes\n", bytes_to_write);
    
    return bytes_to_write;
}

/* IOCTL handler */
static long pemini_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    char __user *user_buffer;
    char kernel_buffer[256];
    uint32_t color_value;
    int status;
    
    mutex_lock(&pemini_mutex);
    
    switch (cmd) {
        case PEMINI_DISPLAY_TEXT:
            user_buffer = (char __user *)arg;
            if (copy_from_user(kernel_buffer, user_buffer, sizeof(kernel_buffer) - 1)) {
                mutex_unlock(&pemini_mutex);
                return -EFAULT;
            }
            kernel_buffer[255] = '\0';
            pemini_write_text(kernel_buffer, strlen(kernel_buffer));
            printk(KERN_INFO "Pemini: IOCTL - Display text executed\n");
            break;
            
        case PEMINI_CLEAR_SCREEN:
            pemini_clear_display();
            printk(KERN_INFO "Pemini: IOCTL - Clear screen executed\n");
            break;
            
        case PEMINI_SET_COLOR:
            color_value = (uint32_t)arg;
            pemini_set_color(color_value);
            printk(KERN_INFO "Pemini: IOCTL - Set color executed\n");
            break;
            
        case PEMINI_GET_STATUS:
            status = pemini_dev.is_initialized ? 1 : 0;
            if (copy_to_user((int __user *)arg, &status, sizeof(int))) {
                mutex_unlock(&pemini_mutex);
                return -EFAULT;
            }
            printk(KERN_INFO "Pemini: IOCTL - Get status executed\n");
            break;
            
        case PEMINI_INIT_DISPLAY:
            pemini_init_arm_display();
            printk(KERN_INFO "Pemini: IOCTL - Init display executed\n");
            break;
            
        default:
            printk(KERN_WARNING "Pemini: Unknown IOCTL command: 0x%X\n", cmd);
            mutex_unlock(&pemini_mutex);
            return -EINVAL;
    }
    
    mutex_unlock(&pemini_mutex);
    return 0;
}

/* Module initialization */
static int __init pemini_init(void)
{
    printk(KERN_INFO "========================================\n");
    printk(KERN_INFO "Pemini UI - ARM Kernel Module Initializing\n");
    printk(KERN_INFO "========================================\n");
    
    /* Register character device */
    majorNumber = register_chrdev(0, DEVICE_NAME, &fops);
    if (majorNumber < 0) {
        printk(KERN_ALERT "Pemini: Failed to register a major number\n");
        return majorNumber;
    }
    
    printk(KERN_INFO "Pemini: Registered successfully with major number %d\n", majorNumber);
    
    /* Create device class */
    peminiClass = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(peminiClass)) {
        unregister_chrdev(majorNumber, DEVICE_NAME);
        printk(KERN_ALERT "Pemini: Failed to register device class\n");
        return PTR_ERR(peminiClass);
    }
    
    /* Create device */
    peminiDevice = device_create(peminiClass, NULL, MKDEV(majorNumber, 0), NULL, DEVICE_NAME);
    if (IS_ERR(peminiDevice)) {
        class_destroy(peminiClass);
        unregister_chrdev(majorNumber, DEVICE_NAME);
        printk(KERN_ALERT "Pemini: Failed to create the device\n");
        return PTR_ERR(peminiDevice);
    }
    
    /* Initialize Pemini device */
    pemini_dev.is_initialized = 0;
    mutex_init(&pemini_mutex);
    
    printk(KERN_INFO "========================================\n");
    printk(KERN_INFO "Pemini UI Module loaded successfully!\n");
    printk(KERN_INFO "Device: /dev/pemini\n");
    printk(KERN_INFO "Architecture: ARM\n");
    printk(KERN_INFO "========================================\n");
    
    return 0;
}

/* Module exit */
static void __exit pemini_exit(void)
{
    printk(KERN_INFO "========================================\n");
    printk(KERN_INFO "Pemini UI - Removing Module\n");
    printk(KERN_INFO "========================================\n");
    
    device_destroy(peminiClass, MKDEV(majorNumber, 0));
    class_unregister(peminiClass);
    class_destroy(peminiClass);
    unregister_chrdev(majorNumber, DEVICE_NAME);
    
    printk(KERN_INFO "Pemini: Module removed successfully\n");
    printk(KERN_INFO "========================================\n");
}

module_init(pemini_init);
module_exit(pemini_exit);
