import os
import subprocess

def wipe_disk_nist_compliant(disk_device):
    """Erase disk as per NIST SP 800-88 clear method (multi-pattern overwrite)"""
    patterns = [
        "/dev/urandom",               # random data
        "/dev/zero",                  # zero fill
        "/dev/urandom"                # random data again
    ]
    for idx, pattern in enumerate(patterns):
        subprocess.run(
            ["sudo", "dd", f"if={pattern}", f"of={disk_device}", "bs=1M", "status=progress"],
            check=True
        )
        print(f"NIST erase pass {idx+1} complete.")
    print(f"Disk wipe NIST SP 800-88 compliant complete for {disk_device}.")
    return True

def secure_erase_ssd_nist(disk_device):
    # Same as secure_erase_ssd but ensure you check SSD specs and use correct passwords on all drives
    import subprocess
    try:
        # Setup user password for security erase
        subprocess.run(
            ["sudo", "hdparm", "--user-master", "u", "--security-set-pass", "ByteShift", disk_device],
            check=True
        )
        # Issue security erase command
        subprocess.run(
            ["sudo", "hdparm", "--security-erase", "ByteShift", disk_device],
            check=True
        )
        print(f"SSD Secure erase (NIST compliant) done for {disk_device}")
        return True
    except Exception as e:
        print(f"Error during SSD secure erase: {e}")
        return False
    
def wipe_file(file_path, passes=3):
    # Same as your previous logic for multi-pass wipe
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False
    file_size = os.path.getsize(file_path)
    try:
        with open(file_path, "r+b") as f:
            for p in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        with open(file_path, "r+b") as f:
            f.seek(0)
            f.write(b"\x00" * file_size)
            f.flush()
            os.fsync(f.fileno())
        os.remove(file_path)
        print(f"File securely wiped and deleted: {file_path}")
        return True
    except Exception as e:
        print(f"Error wiping file: {e}")
        return False

def wipe_partition(partition_path):
    try:
        print(f"[wipe_utils] Simulating wiping partition: {partition_path}")
        for root, dirs, files in os.walk(partition_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        return True
    except Exception as e:
        print(f"[wipe_utils] Partition wipe failed: {e}")
        return False


def wipe_os(disk_device="/dev/sda"):
    """
    Perform a NIST SP 800-88 compliant full wipe (Clear) on the OS disk.

    WARNING: This destroys ALL data on the specified disk irreversibly.
    Make sure this is run ONLY from a live boot environment outside the target disk OS.
    """
    try:
        print(f"[wipe_os] Starting full disk wipe on {disk_device} ...")

        # NIST SP 800-88 Clear method with 3 passes: random, zeros, random.
        passes = [
            "/dev/urandom",
            "/dev/zero",
            "/dev/urandom"
        ]

        for idx, pattern in enumerate(passes):
            print(f"[wipe_os] Starting pass {idx+1} with pattern {pattern} ...")
            # Use dd to overwrite disk
            subprocess.run(
                [
                    "dd",
                    f"if={pattern}",
                    f"of={disk_device}",
                    "bs=1M",
                    "status=progress",
                    "conv=fsync"
                ],
                check=True
            )
            print(f"[wipe_os] Pass {idx+1} complete.")

        print(f"[wipe_os] Full disk wipe complete for {disk_device}.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[wipe_os] Error during disk wipe: {e}")
        return False

    except Exception as e:
        print(f"[wipe_os] Unexpected error: {e}")
        return False

