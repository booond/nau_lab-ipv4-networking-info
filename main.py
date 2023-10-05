import re
import sys


def calculate_network_info(ip_address):
    special_addresses = {
        '0.0.0.0': {"Призначення": "обмежена адреса відправника"},
        '255.255.255.255': {"Призначення": "обмежена широкомовна адреса (limited broadcast)"},
        '127.0.0.0': {"Призначення": "зарезервовано для програмного інтерфейсу (loopback)"}
    }

    if ip_address in special_addresses:
        return special_addresses[ip_address]

    octets = ip_address.split('.')
    first_octet = int(octets[0])

    if first_octet > 255 or int(octets[1]) > 255 or int(octets[2]) > 255 or int(octets[3]) > 255:
        return {"Помилка": "октет не може містити число більше 255"}
    elif 1 <= first_octet <= 126:
        ip_class = 'A'
        subnet_mask = '255.0.0.0'
        network_address = f'{octets[0]}.0.0.0'
        host_address = f'0.0.0.{octets[3]}'
        broadcast_address = f'{octets[0]}.255.255.255'
    elif 128 <= first_octet <= 191:
        ip_class = 'B'
        subnet_mask = '255.255.0.0'
        network_address = f'{octets[0]}.{octets[1]}.0.0'
        host_address = f'0.0.{octets[2]}.{octets[3]}'
        broadcast_address = f'{octets[0]}.{octets[1]}.255.255'
    elif 192 <= first_octet <= 223:
        ip_class = 'C'
        subnet_mask = '255.255.255.0'
        network_address = f'{octets[0]}.{octets[1]}.{octets[2]}.0'
        host_address = f'0.0.0.{octets[3]}'
        broadcast_address = f'{octets[0]}.{octets[1]}.{octets[2]}.255'
    elif 224 <= first_octet <= 239:
        ip_class = 'D'
        subnet_mask = 'N/A'
        network_address = 'N/A'
        host_address = 'N/A'
        broadcast_address = 'N/A'
    elif 240 <= first_octet <= 255:
        ip_class = 'E'
        subnet_mask = 'N/A'
        network_address = 'N/A'
        host_address = 'N/A'
        broadcast_address = 'N/A'
    else:
        return {'Помилка': 'адреса є недійсною'}

    binary_ip = '.'.join([bin(int(octet))[2:].zfill(8) for octet in octets])

    result = {
        'Клас': ip_class,
        'Адреса мережі': network_address,
        'Адреса хоста': host_address,
        'Мережева маска': subnet_mask,
        'Двійкове значення IP': binary_ip,
        'Широкомовна адреса': broadcast_address
    }
    if broadcast_address == ip_address:
        result['Призначення'] = 'Мережна (підмережна) широкомовна адреса'
    elif ip_address == host_address:
        result['Призначення'] = 'Адреса хоста'
    return result


def main(ip_list):
    ip_pattern = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'
    for ip in ip_list:
        print(f'IP-адреса: {ip}')
        if re.match(ip_pattern, ip):
            result = calculate_network_info(ip)
            for key, value in result.items():
                print(f'{key}: {value}')
        else:
            print('Цей варіант не є IP-адресою, адже не введений у форматі "x.x.x.x".')
        print('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
