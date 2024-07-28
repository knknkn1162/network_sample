from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    r0 = lab.create_iosv(ini.iosv_0.__name__, 700, 700, slots=2)
    c0 = lab.create_server(ini.server_0.__name__, 300, 700, slots=1)
    c1 = lab.create_server(ini.server_1.__name__, 1000, 700, slots=1)

    r0.create_links([c0[0], c1[0]])
    c0.create_links([r0[0]])
    c1.create_links([r0[1]])
    
    lab.start()

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()