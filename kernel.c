#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "moon_kernel_device"
#define CLASS_NAME "moon_kernel_class"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Moon Carag Development Team");
MODULE_DESCRIPTION("A simple Linux kernel module for Moon Carag project");
MODULE_VERSION("1.0");

static int majorNumber;
static struct class* moonClass = NULL;
static struct device* moonDevice = NULL;

static int device_open(struct inode *inode, struct file *file);
static int device_release(struct inode *inode, struct file *file);
static ssize_t device_read(struct file *filp, char *buffer, size_t len, loff_t *offset);
static ssize_t device_write(struct file *filp, const char *buffer, size_t len, loff_t *offset);

static struct file_operations fops = {
    .open = device_open,
    .read = device_read,
    .write = device_write,
    .release = device_release,
};

static char device_buffer[256] = "مرحباً بك في نواة Moon Carag\n";
static size_t device_buffer_size = 30;

static int device_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Moon Kernel: Device opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Moon Kernel: Device closed\n");
    return 0;
}

static ssize_t device_read(struct file *filp, char *buffer, size_t len, loff_t *offset)
{
    size_t bytes_to_read = device_buffer_size - *offset;
    
    if (*offset >= device_buffer_size)
        return 0;
    
    if (bytes_to_read > len)
        bytes_to_read = len;
    
    if (copy_to_user(buffer, device_buffer + *offset, bytes_to_read)) {
        return -EFAULT;
    }
    
    *offset += bytes_to_read;
    printk(KERN_INFO "Moon Kernel: Read %zu bytes\n", bytes_to_read);
    
    return bytes_to_read;
}

static ssize_t device_write(struct file *filp, const char *buffer, size_t len, loff_t *offset)
{
    size_t bytes_to_write = len;
    
    if (bytes_to_write > sizeof(device_buffer) - 1)
        bytes_to_write = sizeof(device_buffer) - 1;
    
    if (copy_from_user(device_buffer, buffer, bytes_to_write)) {
        return -EFAULT;
    }
    
    device_buffer[bytes_to_write] = '\0';
    device_buffer_size = bytes_to_write;
    
    printk(KERN_INFO "Moon Kernel: Written %zu bytes\n", bytes_to_write);
    
    return bytes_to_write;
}

static int __init moon_kernel_init(void)
{
    printk(KERN_INFO "Moon Kernel: Initializing the device\n");
    
    majorNumber = register_chrdev(0, DEVICE_NAME, &fops);
    if (majorNumber < 0) {
        printk(KERN_ALERT "Moon Kernel: Failed to register a major number\n");
        return majorNumber;
    }
    
    printk(KERN_INFO "Moon Kernel: Registered successfully with major number %d\n", majorNumber);
    
    moonClass = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(moonClass)) {
        unregister_chrdev(majorNumber, DEVICE_NAME);
        printk(KERN_ALERT "Moon Kernel: Failed to register device class\n");
        return PTR_ERR(moonClass);
    }
    
    moonDevice = device_create(moonClass, NULL, MKDEV(majorNumber, 0), NULL, DEVICE_NAME);
    if (IS_ERR(moonDevice)) {
        class_destroy(moonClass);
        unregister_chrdev(majorNumber, DEVICE_NAME);
        printk(KERN_ALERT "Moon Kernel: Failed to create the device\n");
        return PTR_ERR(moonDevice);
    }
    
    printk(KERN_INFO "Moon Kernel: Device created successfully\n");
    return 0;
}

static void __exit moon_kernel_exit(void)
{
    device_destroy(moonClass, MKDEV(majorNumber, 0));
    class_unregister(moonClass);
    class_destroy(moonClass);
    unregister_chrdev(majorNumber, DEVICE_NAME);
    printk(KERN_INFO "Moon Kernel: Device removed successfully\n");
}

module_init(moon_kernel_init);
module_exit(moon_kernel_exit);
